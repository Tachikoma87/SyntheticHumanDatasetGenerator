# DemoDataset

This dataset acts as a demonstration of the Framework abilities. 

On Example of only one human model, a configuration is applied, yielding in the shown (randomized) poses. 

To handle Complexity the Model is splitted into Regions with inidpendent Pose Generation: Head, Body, Legs, Left Arm, Rigth Arm, Left Wrist, Rigth Wrist, Left Fingers and Rigth Fingers.

Each Region features some BasePoses, which one is selected per Sample and evaluated to get the sub Pose for this Region and Sample. The Number of Base Poses are limited, to match a reasonable effort for this demo (around 8h of time for configuration from scratch). Particularly for Fingers much more gestures may needed than currently provided, to get best possible AI training results.

All Regions have a small chance to be completely random within the anatomic limits intentionally. This should show possible a way to maximize variance and cover poses the framworks user may didn't come up with.

Finally the Rendered Images are analysed by OpenPose to mark the skeleton and detailed bones for hands. This acts as an evaluation of the interpretability by AI.

##### Reminders

(A1) Beside the Export and Configuration, ALL Data is contained in the Blender Project. Any additional data required can be extracted from this project using Blender.

(A2) Each animation frame in Blender represents one Sample in the dataset.

(B) The Framwork is highly configuratable, unpleasant Properties, like Camera angles, bad poses, missing poses or lack of varianz can be easily be adjusted in further steps of improvment.

(C) Current Version does NOT contain any checks for physical correctness or certain part visibility for the poses.

(D) Generation is deterministic, change the Seed in Configuration to get other Samples.

(E) In Compositor (File Output Nodes) and the main Script (TextEditor->GenPoses), as well as the configuration file absolute paths are used, which may need to be adjusted to run the framework.

##### List of Content
| File | Description |
|------|------|
| Image/						| Rendered Images |
| Annotation/					| Annotation Data (Bodyparts marked by Color) |
| config.json					| Configuration File for Controlling the Dataset generation |
| Poses.bvh						| Export of generated Poses | 
| Mesh01.mhx2					| Make Human Export of the used Human Modell |
| Blender/Template3.blend		| Main Project file containing Scripts, Data, etc. (to be used with Blender 2.93.0) |
| Blender/\*.hdr				| Images for Background and Image based Ligthning |
| Blender/textures/				| Addidtional textures required by Blender project |
| OpenPose/						| Rendered Images annotated by OpenPose |
| GeneratePoses_Template.py		| Blender script for pose generation (cleaned and commented code) |

##### Technical Info

Sample Count: 1000

Resolution: 800x600

Number of animated Bones: 49

Number of Backgrounds: 8

Generation Time: \~14s

Render Time: \~43min

Number of Human Models: 1

Images per Pose: 1 (+ Annotation Image)

Render Engine: Cycles (GPU), Sampling: 16-64, Denoising: AI-based (OptiX)

HDR Textures credits to: https://polyhaven.com