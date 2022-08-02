import json
from os import path
from polygon_to_mask import gen_mask
import overlap_bool


#Opening Export File
filePath = '/Users/markcox-smith/Documents/Remedy Temp/c8c6d3016fa82f1f49645c650583b150f789fade561907f1c3abc2ead14bf805_0000000_0000001.json'

with open(filePath) as f:    
    data = json.load(f)  
f.close()


#Setting initial parameters
new_path = 'new_complex_json.json'

new_list = []
task_list = []

previous_keyframe: int
height = data['image']['height']
width = data['image']['width']


#Useful functions
def first_key(dict):
    """
    Gives first key of a dictionary
    """
    res = next(iter(dict))
    return str(res)

def last_key(dict):
    """
    Returns last key of a dictionary
    """
    return list(dict)[-1]

def sort_frames(task_list):
    """
    Orders the frames by the first frame value
    """
    return sorted(task_list, key=lambda task: int(first_key(task['frames'])))

def name_sort(task_list):
    """
    Sorts by the name of the class
    """
    return sorted(task_list, key=lambda task: task['name'], reverse=True)


#Driver Code. Getting frames from annotations. Adds necessary parts to the new json
for task in data['annotations']:
    frame_key = last_key(task['frames'])
    previous_keyframe = frame_key
    new_list.append([frame_key,task['name']])
    task_list.append(task)

task_list = sort_frames(task_list)
task_list = name_sort(task_list)

#Creating shell JSON. Adding JSON and deleting certain fields for order purposes
annotators = data['annotators']
annotations = data['annotations']


del data['annotations']
del data['annotators']

#Creation of new Dictionary
data['annotations'] = []

#Repopulating Annotations section

#Creates new sequential frames from individual frames (only works with single frames)
temp_frame_dict = {}

min_frame = 0
max_frame = 1

for i in range(len(task_list)):

    task = task_list[i]

    frame_key = int(last_key(task['frames']))

    if not temp_frame_dict:
        min_frame = int(first_key(task['frames']))

    if i == 0:
        min_frame = int(first_key(task['frames']))

    if i == len(task_list)-1 and task['id'] != "NULL":
        max_frame = int(last_key(task['frames'])) + 1

        temp_dict = {}
        temp_dict['annotators'] = task['annotators']
        temp_dict['frames'] = task['frames']
        temp_dict['id'] = task['id']
        try:
            temp_dict['interpolate_algorithm'] = task['interpolate_algorithm']
            temp_dict['interpolated'] = task['interpolated']
        except:
            temp_dict['interpolate_algorithm'] = "linear-1.1"
            temp_dict['interpolated'] = True
        temp_dict['name'] = task['name']
        temp_dict['reviewers'] = task['reviewers']
        temp_dict['segments'] = [[min_frame,max_frame]]

        data['annotations'].append(temp_dict)
        break

    next_key = int(first_key(task_list[i+1]['frames']))

    current_class = task['name']
    temp_task = task
    temp_i = i
    
    #Constructs frames section of the new Darwin JSON
    if task["id"] != "NULL":
        temp_frame_dict = task['frames']
        while temp_task['name'] == current_class:
            if current_class == task_list[temp_i+1]["name"] and int(last_key(temp_frame_dict)) == int(first_key(task_list[temp_i+1]["frames"])) - 1:
                next_task = task_list[temp_i+1]
                last_temp = last_key(temp_frame_dict)
                try: 
                    poly_path = temp_frame_dict[str(last_key(temp_frame_dict))]["polygon"]["path"]
                    next_poly_path = task_list[temp_i+1]["frames"][str(first_key(task_list[temp_i+1]["frames"]))]["polygon"]["path"]
                    first_mask = gen_mask(poly_path,height,width)
                    next_mask = gen_mask(next_poly_path,height,width)

                    if overlap_bool.Overlap_Bool(first_mask,next_mask):
                        #Adds all frames within a section
                        for key in range(int(first_key(next_task['frames'])),int(last_key(next_task['frames'])) + 1):
                            temp_frame_dict[str(key)] = next_task['frames'][str(key)]
                    
                        #Prevents sections being included twice if they have already been merged
                        task_list[temp_i + 1]["id"] = "NULL"

                    else:
                        pass
                except:
                    try:
                        poly_path = temp_frame_dict[str(last_key(temp_frame_dict))]["complex_polygon"]["path"]
                        next_poly_path = task_list[temp_i+1]["frames"][str(first_key(task_list[temp_i+1]["frames"]))]["complex_polygon"]["path"]
                        first_mask = gen_mask(poly_path,height,width)
                        next_mask = gen_mask(next_poly_path,height,width)

                        if overlap_bool.Overlap_Bool(first_mask,next_mask):
                            for key in range(int(first_key(next_task['frames'])),int(last_key(next_task['frames'])) + 1):
                                temp_frame_dict[str(key)] = next_task['frames'][str(key)]
                    
                            #Prevents sections being included twice if they have already been merged
                            task_list[temp_i + 1]["id"] = "NULL"

                        else:
                            pass
                    except:
                        pass


            frame_key = int(last_key(temp_task["frames"]))          
            temp_task = task_list[temp_i + 1]
            temp_i += 1


        #temp_frame_dict[str(frame_key)] = task['frames'][str(frame_key)]
        min_frame = int(first_key(temp_frame_dict))
        max_frame = int(last_key(temp_frame_dict)) + 1


        temp_dict = {}
        temp_dict['annotators'] = task['annotators']
        temp_dict['frames'] = temp_frame_dict
        temp_dict['id'] = task['id']
        try:
            temp_dict['interpolate_algorithm'] = task['interpolate_algorithm']
            temp_dict['interpolated'] = task['interpolated']
        except:
            temp_dict['interpolate_algorithm'] = "linear-1.1"
            temp_dict['interpolated'] = True
        temp_dict['name'] = task['name']
        temp_dict['reviewers'] = task['reviewers']
        temp_dict['segments'] = [[min_frame,max_frame]]

        data['annotations'].append(temp_dict)

        temp_frame_dict = {}

#Adds Final Annotators Section
data['annotators'] = annotators

#Writing to new JSON file
with open(new_path,'w+') as f:
    json.dump(data,f,indent=2)  





