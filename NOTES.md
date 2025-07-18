Eval -- `python main.py --dataset datasets/tum/rgbd_dataset_freiburg1_room --no-viz --save-as /root/output/tum/no_calib/rgbd_dataset_freiburg1_room/rgbd_dataset_freiburg1_room --config config/eval_no_calib.yaml`

`python main.py --dataset datasets/tum/rgbd_dataset_freiburg1_room --no-viz --save-as /root/output/tum/calib/rgbd_dataset_freiburg1_room/rgbd_dataset_freiburg1_room --config config/eval_calib.yaml`

---

`evo_ape tum --ref datasets/tum/rgbd_dataset_freiburg1_room/groundtruth.txt /root/output/tum/calib/rgbd_dataset_freiburg1_room/rgbd_dataset_freiburg1_room/rgbd_dataset_freiburg1_room.txt -as`

`evo_traj tum --ref datasets/tum/rgbd_dataset_freiburg1_room/groundtruth.txt /root/output/tum/no_calib/rgbd_dataset_freiburg1_room/rgbd_dataset_freiburg1_room/rgbd_dataset_freiburg1_room.txt --save_plot traj -as`


run with `python main.py --dataset datasets/tum/rgbd_dataset_freiburg1_room/ --config config/calib.yaml`

---

While running with calibration did half the APE (from 0.1 mean to 0.05).

Make sure to align the trajectories with `-as` if using `evo_traj` 

