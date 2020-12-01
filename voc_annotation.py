import xml.etree.ElementTree as ET
from os import getcwd

sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["orange","watermelon","lemon","mango","peach","apple","banana","pear","grape","strawberry","boluo"]

def convert_annotation( a, list_file):
    in_file = open('D:/Desktop/yolo3-keras-master/VOC2012/Annotations/%s.xml'%(a),'r', encoding='UTF-8')
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

wd = getcwd()

for year, image_set in sets:
    image_ids = open('allname1.txt', 'r')
    a = []
    for line in image_ids.readlines():
        line = line.strip()
        a.append(str(line))

    list_file = open('all.txt', 'w')
    for i in range(len(a)):
        list_file.write('%s/VOC2012/JPEGImages/%s.jpg'%(wd,a[i]))
        convert_annotation(a[i], list_file)
        list_file.write('\n')
    list_file.close()
image_ids.close()