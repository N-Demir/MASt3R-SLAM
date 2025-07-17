import dataclasses
import weakref
from pathlib import Path

import viser

import lietorch
import torch
import numpy as np

from mast3r_slam.frame import Frame, Mode
from mast3r_slam.geometry import get_pixel_coords
from mast3r_slam.lietorch_utils import as_SE3
from mast3r_slam.visualization_utils import (
    Frustums,
    Lines,
    depth2rgb,
    image_with_text,
)
from mast3r_slam.config import load_config, config, set_global_config

@dataclasses.dataclass
class WindowMsg:
    is_terminated: bool = False
    is_paused: bool = False
    next: bool = False
    C_conf_threshold: float = 1.5

class Viewer:
    def __init__(self, states, keyframes, main2viz, viz2main):
        self.keyframes = keyframes
        self.states = states
        self.main2viz = main2viz
        self.viz2main = viz2main

        self.server = viser.ViserServer()
        self.scene = self.server.scene

    def add_keyframe(self, keyframe: Frame):
        t, q = as_SE3(keyframe.T_WC.cpu()).data.split([3, 4], -1)
        self.scene.add_camera_frustum(f"/keyframes/{keyframe.frame_id}", 
                                      fov=55, 
                                      aspect=1.0,
                                      scale=0.1,
                                      position=t.flatten().numpy(),
                                      wxyz=q.flatten().numpy())

        if keyframe.X_canon is not None and keyframe.C is not None:
            self.scene.add_point_cloud(f"/points/{keyframe.frame_id}", 
                                    points=keyframe.X_canon.cpu().numpy().astype(np.float32) ,
                                    colors=(0, 1, 0),
                                    # colors=keyframe.C.cpu().numpy().astype(np.float32), # TODO: I think this is something else like confidence
                                    point_size=0.01
                                    )


    # def render(self):
    #     curr_frame = self.states.get_frame()
    #     h, w = curr_frame.img_shape.flatten()
    #     # self.frustums.make_frustum(h, w)

    #     self.curr_img_np = curr_frame.uimg.numpy()
    #     # self.curr_img.write(self.curr_img_np)

    #     cam_T_WC = as_SE3(curr_frame.T_WC).cpu()

    #     #! This may define how the viewer's camera is repositioned every time (i assume mast3r-slam) detects the camera has moved somewhere
    #     #! Interesting that mast3r detects new camera positions without necessarily taking keyframes (and I assume getting dense geometry)
    #     # if self.follow_cam:
    #     #     T_WC = cam_T_WC.matrix().numpy().astype(
    #     #         dtype=np.float32
    #     #     ) @ translation_matrix(np.array([0, 0, -2], dtype=np.float32))
    #     #     self.camera.follow_cam(np.linalg.inv(T_WC))
    #     # else:
    #     #     self.camera.unfollow_cam()

    #     #! Generate a new frustum TODO: Where does the actual drawing of frustum's happen in the old code?
    #     # self.frustums.add(
    #     #     cam_T_WC,
    #     #     scale=self.frustum_scale,
    #     #     color=[0, 1, 0, 1],
    #     #     thickness=self.line_thickness * self.scale,
    #     # )

    #     #! This gets the total number of keyframes and the "dirty" keyframes (ones that need to be re-rendered)
    #     with self.keyframes.lock:
    #         N_keyframes = len(self.keyframes)
    #         dirty_idx = self.keyframes.get_dirty_idx()

    #     for kf_idx in dirty_idx:
    #         keyframe = self.keyframes[kf_idx]
    #         h, w = keyframe.img_shape.flatten()
    #         X = self.frame_X(keyframe)
    #         C = keyframe.get_average_conf().cpu().numpy().astype(np.float32)

    #         #! Frame got "written" here
    #         # TODO: Update the frame

    #     for kf_idx in range(N_keyframes):
    #         keyframe = self.keyframes[kf_idx]
    #         h, w = keyframe.img_shape.flatten()
    #         # self.kf_img_np = keyframe.uimg.numpy()

    #         color = [1, 0, 0, 1]
    #         self.frustums.add(
    #             as_SE3(keyframe.T_WC.cpu()),
    #             scale=self.frustum_scale,
    #             color=color,
    #             thickness=self.line_thickness * self.scale,
    #         )

    #         #! Render the frustum
    #         # self.render_pointmap(keyframe.T_WC.cpu(), w, h, ptex, ctex, itex)

    #     if self.states.get_mode() != Mode.INIT:
    #         if config["use_calib"]:
    #             curr_frame.K = self.keyframes.get_intrinsics()

    #         h, w = curr_frame.img_shape.flatten()
    #         X = self.frame_X(curr_frame)
    #         C = curr_frame.C.cpu().numpy().astype(np.float32)
    #         if "curr" not in self.textures:
    #             ptex = self.ctx.texture((w, h), 3, dtype="f4", alignment=4)
    #             ctex = self.ctx.texture((w, h), 1, dtype="f4", alignment=4)
    #             itex = self.ctx.texture((w, h), 3, dtype="f4", alignment=4)
    #             self.textures["curr"] = ptex, ctex, itex
    #         ptex, ctex, itex = self.textures["curr"]
    #         ptex.write(X.tobytes())
    #         ctex.write(C.tobytes())
    #         itex.write(depth2rgb(X[..., -1], colormap="turbo"))
    #         self.render_pointmap(
    #             curr_frame.T_WC.cpu(),
    #             w,
    #             h,
    #             ptex,
    #             ctex,
    #             itex,
    #             use_img=True,
    #             depth_bias=self.depth_bias,
    #         )
        
    #     # TODO: Rendering frames here

    # def frame_X(self, frame):
    #     if config["use_calib"]:
    #         Xs = frame.X_canon[None]
    #         if self.dP_dz is None:
    #             device = Xs.device
    #             dtype = Xs.dtype
    #             img_size = frame.img_shape.flatten()[:2]
    #             K = frame.K
    #             p = get_pixel_coords(
    #                 Xs.shape[0], img_size, device=device, dtype=dtype
    #             ).view(*Xs.shape[:-1], 2)
    #             tmp1 = (p[..., 0] - K[0, 2]) / K[0, 0]
    #             tmp2 = (p[..., 1] - K[1, 2]) / K[1, 1]
    #             self.dP_dz = torch.empty(
    #                 p.shape[:-1] + (3, 1), device=device, dtype=dtype
    #             )
    #             self.dP_dz[..., 0, 0] = tmp1
    #             self.dP_dz[..., 1, 0] = tmp2
    #             self.dP_dz[..., 2, 0] = 1.0
    #             self.dP_dz = self.dP_dz[..., 0].cpu().numpy().astype(np.float32)
    #         return (Xs[..., 2:3].cpu().numpy().astype(np.float32) * self.dP_dz)[0]

    #     return frame.X_canon.cpu().numpy().astype(np.float32)
