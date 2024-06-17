import os, sys
import csv
import cv2
try:
    import numpy as np
except:
    print("Failed to import numpy package.")
    sys.exit(-1)
try:
    import imageio
except:
    print("Please install the module 'imageio' for image processing, e.g.")
    print("pip install imageio")
    sys.exit(-1)

# print an error message and quit
def print_error(message, user_fault=False):
    sys.stderr.write('ERROR: ' + str(message) + '\n')
    if user_fault:
      sys.exit(2)
    sys.exit(-1)


# if string s represents an int
def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


def read_label_mapping(filename, label_from='raw_category', label_to='nyu40id'):
    assert os.path.isfile(filename)
    mapping = dict()
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            mapping[row[label_from]] = int(row[label_to])
    # if ints convert 
    if represents_int(mapping.keys()[0]):
        mapping = {int(k):v for k,v in mapping.items()}
    return mapping


# input: scene_types.txt or scene_types_all.txt
def read_scene_types_mapping(filename, remove_spaces=True):
    assert os.path.isfile(filename)
    mapping = dict()
    lines = open(filename).read().splitlines()
    lines = [line.split('\t') for line in lines]
    if remove_spaces:
        mapping = { x[1].strip():int(x[0]) for x in lines }
    else:
        mapping = { x[1]:int(x[0]) for x in lines }        
    return mapping


# color by label
def visualize_label_image(filename, image):
    height = image.shape[0]
    width = image.shape[1]
    vis_image = np.zeros([height, width, 3], dtype=np.uint8)
    color_palette = create_color_palette()
    for idx, color in enumerate(color_palette):
        vis_image[image==idx] = color
    imageio.imwrite(filename, vis_image)


# color by different instances (mod length of color palette)
def visualize_instance_image(filename, image):
    height = image.shape[0]
    width = image.shape[1]
    vis_image = np.zeros([height, width, 3], dtype=np.uint8)
    color_palette = create_color_palette()
    instances = np.unique(image)
    for idx, inst in enumerate(instances):
        vis_image[image==inst] = color_palette[inst%len(color_palette)]
    imageio.imwrite(filename, vis_image)

def visualize_label(filename):
    color_palette = create_color_palette()
    H,W=200,200
    img_tmp=np.ones([H,W,3])
    lis_image=[]
    lis_tmp=[]
    nyu40_label=['void',
                'wall','floor','cabinet','bed','chair',
                'sofa','table','door','window','bookshelf',
                'picture','counter','blinds','desk','shelves',
                'curtain','dresser','pillow','mirror','floor',
                'clothes','ceiling','books','refrigerator','tv',
                'paper','towel','shower curtain','box','white board',
                'person','night stand','toilet','sink','lamp',
                'bathtub','bag','other struct','otherfurn','other prop']
    
    for i in range(1,41):
        labels=color_palette[i]
        labels_vis=(img_tmp*labels).astype('uint8')
        key=nyu40_label[i]

        cv2.putText(labels_vis, key,  (20, int(labels_vis.shape[0]-20)), 
            fontFace= cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale = 0.6, 
            color = (255, 255, 255), 
            thickness = 2)
        lis_tmp.append(labels_vis)
        lis_tmp.append(255*np.ones((H, 10, 3)).astype('uint8'))
        if i%5==0:
            img_cat=np.concatenate(lis_tmp, axis=1)
            lis_image.append(img_cat)
            lis_image.append(255*np.ones((10, img_cat.shape[1], 3)).astype('uint8'))
            lis_tmp=[]
        i+=1
        
    img_labels=np.concatenate(lis_image, axis=0)
    cv2.imwrite(filename, img_labels[...,::-1])

# color palette for nyu40 labels
def create_color_palette():
    return [
       (0, 0, 0),
       (174, 199, 232),		# wall
       (152, 223, 138),		# floor
       (31, 119, 180), 		# cabinet
       (255, 187, 120),		# bed
       (188, 189, 34), 		# chair
       (140, 86, 75),  		# sofa
       (255, 152, 150),		# table
       (214, 39, 40),  		# door
       (197, 176, 213),		# window
       (148, 103, 189),		# bookshelf
       (196, 156, 148),		# picture
       (23, 190, 207), 		# counter
       (178, 76, 76),  
       (247, 182, 210),		# desk
       (66, 188, 102), 
       (219, 219, 141),		# curtain
       (140, 57, 197), 
       (202, 185, 52), 
       (51, 176, 203), 
       (200, 54, 131), 
       (92, 193, 61),  
       (78, 71, 183),  
       (172, 114, 82), 
       (255, 127, 14), 		# refrigerator
       (91, 163, 138), 
       (153, 98, 156), 
       (140, 153, 101),
       (158, 218, 229),		# shower curtain
       (100, 125, 154),
       (178, 127, 135),
       (120, 185, 128),
       (146, 111, 194),
       (44, 160, 44),  		# toilet
       (112, 128, 144),		# sink
       (96, 207, 209), 
       (227, 119, 194),		# bathtub
       (213, 92, 176), 
       (94, 106, 211), 
       (82, 84, 163),  		# otherfurn
       (100, 85, 144)
    ]

if __name__=='__main__':
    visualize_label('./nyu40.png')