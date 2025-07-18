Eval -- `python main.py --dataset datasets/tum/rgbd_dataset_freiburg1_room --no-viz --save-as /root/output/tum/no_calib/rgbd_dataset_freiburg1_room/rgbd_dataset_freiburg1_room --config config/eval_no_calib.yaml`

`python main.py --dataset datasets/tum/rgbd_dataset_freiburg1_room --no-viz --save-as /root/output/tum/calib/rgbd_dataset_freiburg1_room/rgbd_dataset_freiburg1_room --config config/eval_calib.yaml`

`evo_ape tum datasets/tum/rgbd_dataset_freiburg1_room/groundtruth.txt /root/output/tum/no_calib/rgbd_dataset_freiburg1_room/rgbd_dataset_freiburg1_room/rgbd_dataset_freiburg1_room.txt -as`

`evo_traj tum datasets/tum/rgbd_dataset_freiburg1_room/groundtruth.txt /root/output/tum/no_calib/rgbd_dataset_freiburg1_room/rgbd_dataset_freiburg1_room/rgbd_dataset_freiburg1_room.txt --save_plot traj`


run with `python main.py --dataset datasets/tum/rgbd_dataset_freiburg1_room/ --config config/calib.yaml`