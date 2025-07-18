#!/usr/bin/env python3

import viser
import numpy as np
import open3d as o3d
import argparse
import os

def load_point_cloud(file_path):
    """Load point cloud from PLY file using Open3D"""
    print(f"Loading point cloud from: {file_path}")
    
    # Load the point cloud
    pcd = o3d.io.read_point_cloud(file_path)
    
    # Get points and colors
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    
    print(f"Loaded {len(points)} points")
    print(f"Point cloud bounds: {pcd.get_min_bound()} to {pcd.get_max_bound()}")
    
    return points, colors

def main():
    parser = argparse.ArgumentParser(description='Visualize point cloud with viser')
    parser.add_argument('--ply_path', type=str, 
                       default='/root/output/tum/no_calib/rgbd_dataset_freiburg1_room/rgbd_dataset_freiburg1_room/rgbd_dataset_freiburg1_room.ply',
                       help='Path to the PLY file')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind to')
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.ply_path):
        print(f"Error: File {args.ply_path} does not exist!")
        return
    
    # Load point cloud
    try:
        points, colors = load_point_cloud(args.ply_path)
    except Exception as e:
        print(f"Error loading point cloud: {e}")
        return
    
    # Create viser server
    server = viser.ViserServer(host=args.host, port=args.port)
    
    # Add point cloud to the scene
    server.scene.add_point_cloud(
        "/point_cloud",
        points=points,
        colors=colors,
        point_size=0.01,  # Adjust point size as needed
    )
    
    # Add some helpful UI elements
    server.gui.add_markdown("## Point Cloud Viewer")
    server.gui.add_markdown(f"**File:** {os.path.basename(args.ply_path)}")
    server.gui.add_markdown(f"**Points:** {len(points):,}")
    
    # Add controls for point size
    point_size = server.gui.add_slider(
        "Point Size", 
        min=0.001, 
        max=0.1, 
        step=0.001, 
        initial_value=0.01
    )
    
    @point_size.on_update
    def _(_):
        server.scene.update_point_cloud(
            "/point_cloud",
            point_size=point_size.value
        )
    
    print(f"Viser server started at http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop the server")
    
    # Keep the server running
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")

if __name__ == "__main__":
    main()