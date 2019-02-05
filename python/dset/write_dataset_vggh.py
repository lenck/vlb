import json

sequence_name_list = ['bikes','trees','graf','wall','boat','bark','leuven','ubc']
description_list = ['Increasing blur','Increasing blur','Viewpoint angle','Viewpoint angle','Scale changes','Scale changes','Decreasing light','JPEG compression']
label_list = [
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, 5, 6],
        [0, 20, 30, 40, 50, 60],
        [0, 20, 30, 40, 50, 60],
        [1, 1.12, 1.38, 1.9, 2.35, 2.8],
        [1, 1.2, 1.8, 2.5, 3, 4], 
        [1, 2, 3, 4, 5, 6],
        [0, 60, 80, 90, 95, 98]]

json_data = {}
json_data['Dataset Name'] = 'VGG Affine'
json_data['Description'] = 'Standard Benchmark'
json_data['url'] = 'http://www.robots.ox.ac.uk/~vgg/research/affine/det_eval_files/'
json_data['Sequence Number'] = len(sequence_name_list)
json_data['Sequence Name List'] = sequence_name_list
json_data['Sequences'] = []

for idx, sequence_name in enumerate(sequence_name_list):
    sequence = {}
    sequence['Name'] = sequence_name
    sequence['Description'] = sequence_name 
    sequence['Label'] = description_list[idx]
    sequence['Images'] = []
    sequence['Image Number'] = 6

    for image_idx, image_label in enumerate(label_list[idx]):
        image = {}
        if sequence_name == 'boat':
            image['file'] = '{}/img{}.pgm'.format(sequence_name,image_idx+1)
        else:
            image['file'] = '{}/img{}.ppm'.format(sequence_name,image_idx+1)
            
        image['id'] = str(image_idx+1)
        image['label'] = str(image_label)
        sequence['Images'].append(image)

    sequence['Link Number'] = 5
    sequence['Links'] = []
    for i in range(1,6):
        link = {}
        link['source'] = str(1)
        link['target'] = str(i+1)
        link['file'] = '{}/H1to{}p'.format(sequence_name, i+1)
        sequence['Links'].append(link)
    json_data['Sequences'].append(sequence)

with open('./datasets/dataset_info/{}.json'.format('vggh'),'w') as json_file:
    json.dump(json_data, json_file, indent=2)
