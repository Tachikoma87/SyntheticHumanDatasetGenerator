# Demo Dataset
This dataset acts as a demonstration for the capabilities of the framework. On the example of a single human model, a configuration is applied, yielding in randomized poses.  To handle complexity, the Model is split into regions with independent pose generation: Head, Body, Legs, Left Arm, Right Arm, Left Wrist, Right Wrist, Left Fingers and Right Fingers. Each region features some base poses, which one is selected per sample and evaluated to get the sub pose for this region and sample. The number of base poses are limited, to match a reasonable effort for this demo (around 8h of time for configuration from scratch). Particularly for fingers much more gestures may needed than currently provided, to get best possible AI training results. All Regions have a small chance to be completely random within the anatomic limits intentionally. This shows a possible way to maximize variance and cover poses the framework's user may didn't come up with.

## Notes
* Each animation frame in Blender represents one sample in the dataset.
* The framework is highly configurable. Unpleasant properties, such as camera angles, bad poses, missing poses, or lack of variety can be easily adjusted in further steps of improvement.
* Current version does NOT contain any checks for physical correctness or certain part visibility for the poses.
* Generation is deterministic. Change the seed in configuration to get other samples.
* In compositor (File Output Nodes) and the main script (*TextEditor->GenPoses*), as well as the configuration file, absolute paths are used, which may need to be adjusted to run the framework.

## Quickstart
1. Change the paths to the background images in the *config.json* so they match your file structure. Absolute paths are required.
    * Tag *Background* (lines 320 - 330)
2. Open *Template.blend*
3. Go to the Scripting tab and execute the GenPoses script.
4. Specify the output path under *Output Properties => Output*
5. Start *Render => Render Animation* (Ctrl + F12)

### Copyright Note
HDR Textures credits to: https://polyhaven.com