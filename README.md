# Copy Vertices Location by UV Map

## Description

This Blender addon allows you to copy the vertices' locations from one mesh object to another based on their UV maps. This is useful for transferring vertex positions between similar meshes that share the same UV layout.

## Features

- Copies vertex locations from one object to another by comparing their UV coordinates.
- Supports customizable UV maps for both source and target objects.
- Includes a user interface for easy interaction in the 3D View panel.
- Adjustable UV distance threshold for finer control over vertex matching.

## Requirements

- Blender version 2.79. (haven't tested with 2.8+)

## Installation

1. Download the Python script or copy the code into a `.py` file.
2. Open Blender and go to `Edit` > `Preferences`.
3. Navigate to the `Add-ons` tab and click on `Install...`.
4. Select the `.py` file of this addon and click `Install Add-on`.
5. Enable the addon by checking the box next to it.

## Usage

1. In the 3D View, navigate to the **Tool** tab in the side panel.
2. Select the **Source Mesh** and the **Target Mesh** in the addon panel.
3. Specify the **Source UV Name** and the **Target UV Name** to define the UV maps for both objects (default is `"UVMap"`).
4. Set the **UV Distance Threshold** to control the vertex matching sensitivity.
5. Click the **Do the Magic!** button to start the vertex transfer process.
6. Wait for the process to complete. Blender might appear unresponsive during the operation, but it will complete as long as you don’t interrupt it.

## Notes

- The source and target objects must have similar UV layouts for the transfer to work correctly.
- The script may take time to process large meshes; Blender may look unresponsive during this time.

## Support

For any issues or questions, feel free to contact the author via email: [alirezafarzaneh138@gmail.com](mailto:alirezafarzaneh138@gmail.com).
