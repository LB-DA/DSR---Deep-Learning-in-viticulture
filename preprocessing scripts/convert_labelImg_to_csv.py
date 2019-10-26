"""
This script is used to convert xml label files created by labelImg with
corresponding images into csv files. Users should configure the path for the
image directory as well as the output directory for the csv files.

IMPORTANT!: The image directory must already contain the three subfolders
for train, validation and test images.  Furthermore the user has to create
the destination output directory for the csv_files of each image subfolder.
We recommend creating a directory named "data_<name of data>" and using this
directory as output directory for the create_tfrecord_file.py script in the
next step (generate_tfrecord.py) as well.

Search for "TODO" to find the fields that need to be configured!
"""
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []
    # read filename, width, height, class, xmin, ymin, xmax and ymax for
    # each label of each xml file and append to xml_list
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    # set column names for all entries for the xml-dataframe
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    # create xml-dataframe with xml_list and defined column names
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def main():
    # repeat procedure for each dataset (train, valid, test)
    for directory in ['train','valid','test']:
        image_path = os.path.join(os.getcwd(), '<TODO_configure: image directory>/{}'.format(directory))
        xml_df = xml_to_csv(image_path)
        # convert dataframe into csv
        xml_df.to_csv('<TODO_configure: output directory for csv files (should be created beforehand)>/{}_labels.csv'.format(directory), index=None)
        print('Successfully converted xml to csv.')


main()
