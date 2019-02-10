import json

sequence_name_list = ['A','G','L','map2photo','S']
description_list = ['Viewpoint Appearance','Viewpoint','ViewPoint Lighting','Map to Photo','Modality']
label_list = [
        ['arch', 'obama', 'vprice0', 'vprice1', 'vprice2', 'yosemite'],
        ['adam', 'boat','ExtremeZoomA','face','fox','graf','mag','shop','there','vin'],
        ['amos1','bdom','brugge_square', 'GC2','light','madrid',\
                'notredame15','paintedladies','rushmore','trevi','vatican'],
        ['map1', 'map2', 'map3', 'map4', 'map5', 'map6'],
        ['angiogram','brain1','EO-IR-2',\
                'maunaloa','mms68','mms75','treebranch']
        ]
#label_list = [
#        ['arch', 'obama', 'vprice0', 'vprice1', 'vprice2', 'yosemite']
#        ]

json_data = {}
json_data['Dataset Name'] = 'W1BS'
json_data['Description'] = 'Baseline Stereo Benchmark'
json_data['url'] = 'http://cmp.felk.cvut.cz/wbs/datasets/W1BS_with_patches.tar.gz'
json_data['Sequence Number'] = len(sequence_name_list)
json_data['Sequence Name List'] = sequence_name_list
json_data['Sequences'] = []

for idx, sequence_name in enumerate(sequence_name_list):
    sequence = {}
    sequence['Name'] = sequence_name
    sequence['Description'] = sequence_name 
    sequence['Label'] = description_list[idx]
    sequence['Images'] = []
    sequence['Image Number'] = len(label_list[idx])*2
    sequence['Link Number'] = len(label_list[idx])
    sequence['Links'] = []

    for image_idx, image_label in enumerate(label_list[idx]):
        image = {}
        image['file'] = '{}/1/{}.bmp'.format(sequence_name,image_label)
        image['id'] = str(image_label) + '_1'
        image['label'] = str(image_label) + '_1'
        sequence['Images'].append(image)
        image = {}
        image['file'] = '{}/2/{}.bmp'.format(sequence_name,image_label)
        image['id'] = str(image_label) + '_2'
        image['label'] = str(image_label) + '_2'
        sequence['Images'].append(image)

        link = {}
        link['source'] = str(image_label) + '_1'
        link['target'] = str(image_label) + '_2'
        link['file'] = '{}/h/{}.txt'.format(sequence_name, image_label)
        sequence['Links'].append(link)
    json_data['Sequences'].append(sequence)

with open('./datasets/dataset_info/{}.json'.format('W1BS'),'w') as json_file:
    json.dump(json_data, json_file, indent=2)
