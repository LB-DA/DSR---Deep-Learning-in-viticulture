"""
This script is used to Create train/validation/test data in TFRecord format.

 Users should configure the input/output locations for the Dataset CSV/TFRecord files as
 well as the image dataset path for the TFRecord files. Furthermore the Users has to
 configure correspongind label map for TFRecord File. As default the label map for vine
 models is preselected. If you want to create tfrecord data for berry models please
 change the corresponding label map settings below by changing the comment lines.


 IMPORTANT!: From tensorflow/models/ use each of the following command lines to execute the script and create TFRecord files!
 Create train data command:
    python create_tfrecord_file.py --csv_input=<TODO_configure: location of csv file>/train_labels.csv  --output_path=<TODO_configure: destination of TFRecord file output>/train.record

 Create valid data command:
    python create_tfrecord_file.py --csv_input=<TODO_configure: location of csv file>/valid_labels.csv  --output_path=<TODO_configure: destination of TFRecord file output>/valid.record

 Create test data command:
    python create_tfrecord_file.py --csv_input=<TODO_configure: location of csv file>/test_labels.csv  --output_path=<TODO_configure: destination of TFRecord file output>/test.record


Search for "TODO" to find the fields that need to be configured!
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import os
import io
import pandas as pd
import tensorflow as tf
from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS



''' TODO: select Label Map to be configured
    Label Map for Vine Models is set as default
'''
# configure correspongind label map for TFRecord File
''' Vine Label Map '''
def class_text_to_int(row_label):
    if row_label == 'vine':
        return 1
    elif row_label == 'metalstick':
        return 2
    elif row_label == 'woodenstick':
        return 3
    else:
        None

''' Berry Label Map (green) '''
'''
def class_text_to_int(row_label):
    if row_label == 'berry_green':
        return 1
    elif row_label == 'cluster_green':
        return 2
    else:
        None
'''

''' Berry Label Map (red)'''
'''
def class_text_to_int(row_label):
    if row_label == 'berry_red':
        return 1
    elif row_label == 'cluster_red':
        return 2
    else:
        None
'''
#

def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    # convert coordinates into percentage values for tensorflow
    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    # set path of overall image Dataset (containing all images: train+validation+test)
    path = os.path.join(os.getcwd(), '<TODO: select location of all image files>')
    # get filenames of specific group from corresponding csv file
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.app.run()
