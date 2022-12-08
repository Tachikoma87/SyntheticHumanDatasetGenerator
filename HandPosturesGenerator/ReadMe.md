# Hand Posture Generator Framework
These files were used to create our extensive hand gesture data set. We provide ten different human models and their respective Blender files are set up to create the respective images and meta data.

## Quickstart
1. Change the paths to the background images in the *config.json* so they match your file structure. Absolute paths are required.
    * Tag *Background* (lines 320 - 330)
2. Open one of the *Mesh0X.blend* files
3. Go to the Scripting tab and execute the *GenPoses* script.
    * The console window will print the current state of the process.
4. Switch to the *Export* script and specify the *file_path* where the metadata should be exported to. Execute the script.
    * The specified folder has to exist!
5. Go to the *Compositing* tab and specify in the *File Output* node the location where the annotations should be stored.
6. Specify the output path of the rendered samples under *Output Properties => Output*
7. Start *Render => Render Animation* (Ctrl + F12)

### Copyright Note
HDR Textures credits to: https://polyhaven.com

Human models created with MakeHuman software: http://www.makehumancommunity.org/