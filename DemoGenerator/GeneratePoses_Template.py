# Script to generate poses based on Config
# To be used in Blender only
# Felix Weigand 2022

import bpy
import math
import mathutils
import pathlib
import json
import random
import numpy

#Adjust Paths before running
config_path = "C:\\Temp\\conf2.json"
bvh_path = "C:\\Temp\\poses.bvh"

#Setup node tree to set backgrounds (HDRI)
#Usage of returned struct see "SelectAndSetBackground"
def MakeBackground(json):
    backgrounds = []
    bg_weight_sum = 0
	
	#parse the "Background" node of the config json 
    for bg in json:
        img = bpy.data.images.load(bg["Path"])
		#sum up weigths
        bg_weight_sum += bg["Weigth"]
        backgrounds.append({'node': 0, 'img': img, 'sum': bg_weight_sum})
    
	#access scene node tree for background & delete it
    tree = bpy.context.scene.world.node_tree
    tree.nodes.clear()
    
    # Add Output node
    node_output = tree.nodes.new(type='ShaderNodeOutputWorld')   
    node_output.location = 200,0
    
    last_add = tree.nodes.new(type='ShaderNodeAddShader')
    link = tree.links.new(last_add.outputs["Shader"], node_output.inputs["Surface"])
    
	# add and connect shaders for each background image
    for bg in backgrounds:
        add        = tree.nodes.new(type='ShaderNodeAddShader')
        texture    = tree.nodes.new(type='ShaderNodeTexEnvironment')
        texture.image = bg["img"]
        bg["node"] = tree.nodes.new(type='ShaderNodeBackground')
		#set strength to 0
        bg["node"].inputs[1].default_value = 0

        tree.links.new(texture.outputs["Color"], bg["node"].inputs["Color"])
        tree.links.new(bg["node"].outputs["Background"], add.inputs[0])
        tree.links.new(add.outputs["Shader"], last_add.inputs[1])
        
        last_add = add
    
    return backgrounds

#Select a random background for the given frame
def SelectAndSetBackground(backgrounds, frame_num):
	# get reandom int between 0 and sum of all weigths
    i = numpy.random.randint(0,backgrounds[-1]["sum"])

    found = 0
    for el in backgrounds:
		# iterate until the sum of the background weigths reaches the random value
        if i < el["sum"] and found == 0:
            found = el
			#Set strength for match to 1.0
            el["node"].inputs[1].default_value = 1
            el["node"].inputs[1].keyframe_insert("default_value", frame=frame_num)
        else:
			#Set strength for others to 0.0
            el["node"].inputs[1].default_value = 0
            el["node"].inputs[1].keyframe_insert("default_value", frame=frame_num)
    
    return found

#Parse an distribution node to get an accourding random value
def GetRandomFloat(json):
    
    if json["Type"] == "uniform":
        f = numpy.random.uniform(json["Min"],json["Max"])
        return f
    
	#splited normal distribution. See document for details
    if json["Type"] == "normal":
        u1 = numpy.random.uniform(0.0,1.0)
        u2 = numpy.random.uniform(0.0,1.0)
        c = math.cos(2*math.pi*u2)
        if c > 0.0:
            f = json["Dev+"] * 0.5 * math.sqrt(-2.0 * math.log(u1)) * c + json["Mean"]
        else:
            f = json["Dev-"] * 0.5 * math.sqrt(-2.0 * math.log(u1)) * c + json["Mean"]
        return f
    
	#invalid input
    return 0
    
#parse camera node to set camera to random location
def SetCamera(json, armature, frame_num):
	#randomize parameters
    pitch = math.radians(GetRandomFloat(json["Pitch"]))
    yaw = math.radians(GetRandomFloat(json["Yaw"]))
    zoom = GetRandomFloat(json["Zoom"])
    
	#get position of scene center (set via "Track To" constraint)
    o = bpy.data.objects[armature]
    p = o.pose.bones[bpy.data.objects["Camera"].constraints["Track To"].subtarget]
    offs = (o.matrix_world @ p.matrix) @ p.location

    #Calc Camera Positon using sphere coordinates
    pos = offs + mathutils.Vector((zoom * math.cos(yaw) * math.sin(pitch) , zoom * math.sin(yaw) * math.sin(pitch), zoom * math.cos(pitch)))
    bpy.data.objects["Camera"].location.x = pos.x
    bpy.data.objects["Camera"].location.y = pos.y
    bpy.data.objects["Camera"].location.z = pos.z
    
	#set keyframe to save camera options
    bpy.data.objects["Camera"].keyframe_insert("rotation_euler", frame=frame_num)
    bpy.data.objects["Camera"].keyframe_insert("location", frame=frame_num)
  
#Make dict for anatomic limits and set default rotation mode
def MakeLimits(rig, armature):
    limits = dict()

    for bone in rig["Bones"]:
        limits[bone["BoneName"]] = bone
        bpy.data.objects[armature].pose.bones[bone["BoneName"]].rotation_mode = 'YXZ'
        
    return limits

#Prepare BasePoses by sum up the weigths
def MakeRegionsAndBasePoses(json):

    for r in json:
        bp_weight_sum = 0
        
        for bp in r["BasePoses"]:
            bp_weight_sum += bp["Weigth"]
            bp["sum"] = bp_weight_sum
    
    return json

#Clamp function for json based limits	
def ClampAngle(f, lim):  
    return max(min(f, lim["Max"]), lim["Min"])
    
#MAIN
with open(config_path) as data_file:  
    data = json.load(data_file)
    
    sample_count = data["SampleCount"];
    numpy.random.seed(data["Seed"]);
    
    rig = data["Rig"];
    armature = rig["Armature"]; 

    #Prepare Background List 
    backgrounds = MakeBackground(data["Background"])
   
	#Prepare Skeleton informations
    limits = MakeLimits(rig, armature)
    regions = MakeRegionsAndBasePoses(data["BodyRegions"])
   

    bpy.context.scene.frame_end = sample_count+1

	#generate each scene (saved in keyframes for an frame)
    for frame_num in range(1,sample_count+1):   
        
        if frame_num % 10 == 0:
            print(frame_num)
        
        bpy.context.scene.frame_current = frame_num
        
        SelectAndSetBackground(backgrounds, frame_num)
        
		SetCamera(data["Camera"],armature,frame_num)
        
		#for each region
        for r in regions:
		
			#select base pose using summed weigths
            i = numpy.random.randint(0,r["BasePoses"][-1]["sum"]) 
            for bp in r["BasePoses"]:
                if i < bp["sum"]:  
				
					#foreach bone in selected base pose
                    for j in bp["Joints"]:
						#get bone by name
                        pose_bone = bpy.data.objects[armature].pose.bones[j["BoneName"]]
                        lim = limits[j["BoneName"]]
						#randomize, clamp and convert every angle
                        pose_bone.rotation_euler[0] = math.radians(ClampAngle(GetRandomFloat(j["X"]), lim["X"]))
                        pose_bone.rotation_euler[1] = math.radians(ClampAngle(GetRandomFloat(j["Y"]), lim["Y"]))
                        pose_bone.rotation_euler[2] = math.radians(ClampAngle(GetRandomFloat(j["Z"]), lim["Z"]))
                        
						#save as keyframe
                        pose_bone.keyframe_insert("rotation_euler", frame=frame_num)
                           
                    break   