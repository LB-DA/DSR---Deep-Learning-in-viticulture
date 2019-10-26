'''
This script is used to create mirror versions of images and create corresponding
xml files for the mirrored image versions.

Search for "TODO" to find the fields that need to be configured!
'''
import cv2
import numpy as np
import os
from tqdm import tqdm
import xml.etree.ElementTree as ET

#example_usage:
#image_path = 'C:/Users/Applied Data Science/Desktop/Belegarbeit/data/dataset_vine_hdbilder_all/data_prep'+'/'
image_path = '<TODO: please select the path of the images to be mirrored>'+'/'

# tqdm to show progress of the mirror-creation-process
for file in tqdm(os.listdir(image_path)):
    # split file at "." in order to assign correct filename later
    file_name, file_extension = file.split(".")
    # apply whole process for each image
    if file_extension in ['JPG','PNG','jpg','png']:
        image = cv2.imread(os.path.join(image_path, file))
        # get height and width parameters of the image for the mirror calculation
        h, w, d = image.shape
        # vertical flip of the image as image augmentation
        image_mirror = cv2.flip(image,1)
        # save the newly created mirror version of the processed image
        cv2.imwrite(file_name+"_mirror.jpg", image_mirror)

        # get corresponding xml files for the flipped images
        xml_file = file_name+".xml"
        table = ET.parse(image_path + xml_file).getroot()

        ## get filename variable
        filename = table.find('filename').text


        class_names = []
        x_mins = []
        y_mins = []
        x_maxs = []
        y_maxs = []

        # define
        for object in table.findall('object'):
            class_name = object.find('name').text
            class_names.append(class_name)
            for bndbox in object.findall('bndbox'):
                # get original x,y labels of boxes
                x_min = bndbox.find('xmin').text
                y_min = bndbox.find('ymin').text
                x_max = bndbox.find('xmax').text
                y_max = bndbox.find('ymax').text
                # tranform original x,y labels to mirror x,y labels
                # new x_min/x_max of the flipped image equals the total width of the image - the old x_max/x_mins
                # since we are vertically flipping the image, y coordinates stay the same
                # all values have to be strings in order to write them to the xml file
                x_min_mirror = str(w-int(x_max))
                y_min_mirror = y_min
                x_max_mirror = str(w-int(x_min))
                y_max_mirror = y_max

                x_mins.append(x_min_mirror)
                y_mins.append(y_min_mirror)
                x_maxs.append(x_max_mirror)
                y_maxs.append(y_max_mirror)

        # --------------------- <WRITE .XML> ------------------------#
        #open a .xml-file in append-mode
        file = open(file_name+'_mirror'+'.xml', 'a')

        ANNO = '<?xml version="1.0" ?><annotation>'
        file.write(ANNO)

        #element structure
        folder = ET.Element('folder')
        filename = ET.Element('filename')
        path = ET.Element('path')
        source = ET.Element('source')
        database = ET.SubElement(source,'database')
        size = ET.Element('size')
        width = ET.SubElement(size,'width')
        height = ET.SubElement(size,'height')
        depth = ET.SubElement(size,'depth')
        segmented = ET.Element('segmented')

        #values
        folder.text = 'lukas'
        filename.text = file_name+'_mirror'+'.jpg'
        path.text = 'PATH'
        database.text = 'Unknown'
        width.text = str(w)
        height.text = str(h)
        depth.text = str(d)
        segmented.text = '0'

        STRING = ET.tostring(folder).decode('utf-8') + ET.tostring(filename).decode('utf-8') + ET.tostring(path).decode('utf-8') + ET.tostring(source).decode('utf-8') + ET.tostring(size).decode('utf-8') + ET.tostring(segmented).decode('utf-8')
        file.write(STRING)


        for i in range(len(class_names)):

            object = ET.Element('object')
            name = ET.SubElement(object, 'name')
            pose = ET.SubElement(object, 'pose')
            truncated = ET.SubElement(object, 'truncated')
            difficult = ET.SubElement(object, 'difficult')
            bndbox = ET.SubElement(object, 'bndbox')
            xmin = ET.SubElement(bndbox, 'xmin')
            ymin = ET.SubElement(bndbox, 'ymin')
            xmax = ET.SubElement(bndbox, 'xmax')
            ymax = ET.SubElement(bndbox, 'ymax')

            pose.text = 'Unspecified'
            truncated.text = '0'
            difficult.text = '0'


            name.text = class_names[i]
            xmin.text = x_mins[i]
            ymin.text = y_mins[i]
            xmax.text = x_maxs[i]
            ymax.text = y_maxs[i]

            file.write(ET.tostring(object).decode('utf-8'))
            #---------------- </GENERATE XML LABEL ELEMENTS> ------------ #

        ANNOC = '</annotation>'
        file.write(ANNOC)

        file.close()
