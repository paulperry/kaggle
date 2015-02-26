
"""
'Convert train.vw and test.vw to csv format'
Two files are outputs of gen_vw_features.py by Triskelion.
See 'Feature engineering and beat the benchmark (~0.59347)'
http://www.kaggle.com/c/acquire-valued-shoppers-challenge/forums/t/7688/feature-engineering-and-beat-the-benchmark-0-59347
"""

import csv

vwTrainfile = 'data/train.vw'
vwTestfile = 'data/test.vw'

csvTrainfile = 'data/train.csv'
csvTestfile = 'data/test.csv'

def vw2csv(inVWfile, outCSVfile, fieldnames = set()):
    f=open(inVWfile)
    lines=f.readlines()
    f.close()

    list_of_dict = []
    for line in lines:
        obj_dict = {}
        obj = line.strip().split(' ')
        # obj[:5]: ['1', "'12262064", '|f' 'offer_quantity:1', 'has_bought_brand_company:1']
        obj_dict.update({'id':obj[1][1:], 'repeter':obj[0]})
        obj_dict.update({key:value for key, value in [pair.split(':') for pair in obj[3:]]})
        list_of_dict.append(obj_dict)
    
    if len(fieldnames) == 0:
        for i in range(1000):
            fieldnames.update(list_of_dict[i].keys())
    # Move 'id', 'repeter' to the front
    fieldnames = list(fieldnames)
    fieldnames.remove('repeter')
    fieldnames.remove('id')
    fieldnames.insert(0, 'repeter')
    fieldnames.insert(0, 'id')
    # header row
    header = {key:key for key in fieldnames}
    list_of_dict.insert(0, header)

    with open(outCSVfile, mode = 'wb') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writerows(list_of_dict)
    return fieldnames

if __name__ == '__main__':
    fieldnames = vw2csv(vwTrainfile, csvTrainfile)
    vw2csv(vwTestfile, csvTestfile, fieldnames = fieldnames)

