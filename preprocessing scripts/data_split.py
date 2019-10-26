'''
This script divides the selected dataset into train-, valid- and testdataself.
70/25/5 split for Train/Valid/Test as default.

Search for "TODO" to find the fields that need to be configured!
'''
import os
import shutil as s
import random


'''
TODO: Select alternative split parameters if needed
      -> 70/25/5 split for Train/Valid/Test as default
'''
train_split_size = 0.70
valid_split_size = 0.25
test_split_size = 0.05


'''TODO:create the data_prep folder and move the data into this directory'''
path = os.getcwd()
names = os.listdir(path+'/data_prep/')


# create subfolder "image" and "xml" for further usage
folder_name_separation = ['image','xml']
for x in range(0,2):
        os.makedirs(path+'/'+folder_name_separation[x])

# split files in images/xml and copy to newly created folders
for files in names:
    if '.jpg' in files:
        s.copy(path+'/data_prep/'+files, path+'/image/'+files)
    if '.JPG' in files:
        s.copy(path+'/data_prep/'+files, path+'/image/'+files)
    if '.png' in files:
        s.copy(path+'/data_prep/'+files, path+'/image/'+files)
    if '.PNG' in files:
        s.copy(path+'/data_prep/'+files, path+'/image/'+files)
    if '.xml' in files:
        s.copy(path+'/data_prep/'+files, path+'/xml/'+files)


path_img = path+'/image/'
path_xml = path+'/xml/'

## number of images overall
img = os.listdir(path_img)
count_img = len(img)





# set data distribution for train, validation and test data.
# count_x describes the number of images for each data set to select.
count_train = round(count_img*train_split_size)
count_valid = round(count_img*valid_split_size)
count_test = round(count_img*test_split_size)

# create subfolders for train, validation and test data set
folder_name_data_sets = ['valid','train','test']

for x in range(0,3):
        os.makedirs(path+'/'+folder_name_data_sets[x])


path_valid = path + '/valid/'
path_train = path + '/train/'
path_test = path + '/test/'

# ---- select validation images ---- #
# shuffle all images before selection
random.shuffle(img)
# select predefined number of images for validation data set by random
img_valid = random.sample(img, count_valid)

# move selection to the related folder
for file in img_valid:
    if not os.path.exists(path_valid + file):
        s.move(path_img + file, path_valid + file)

# refresh list of available img in order to avoid error with next selection
img = os.listdir(path_img)
# ---- ------------------------ ---- #

# ----   select train images    ---- #
# shuffle all images before selection
random.shuffle(img)
# select predefined number of images for training data set by random
img_train = random.sample(img, count_train)

# move selection to the related folder
for file in img_train:
    if not os.path.exists(path_train + file):
        s.move(path_img + file, path_train + file)

# refresh list of available img in order to avoid error with next selection
img = os.listdir(path_img)
# ---- ------------------------ ---- #

# ----    select test images    ---- #
# shuffle all images before selection
random.shuffle(img)
# select predefined number of images for test data set by random
img_test = random.sample(img, count_test)

# move selection to the related folder
for file in img_test:
    if not os.path.exists(path_test + file):
        s.move(path_img + file, path_test + file)

# refresh list of available img in order to avoid error with next selection
img = os.listdir(path_img)
# ---- ------------------------ ---- #


# merge xml with separated img files again
img_valid = os.listdir(path_valid)
img_valid = [i.split('.')[0] for i in img_valid]

img_train = os.listdir(path_train)
img_train = [i.split('.')[0] for i in img_train]

img_test = os.listdir(path_test)
img_test = [i.split('.')[0] for i in img_test]

xml = os.listdir(path_xml)
xml = [i.split('.')[0] for i in xml]

# merge xml with separated img files again
for file in xml:
    if file in img_test:
        if not os.path.exists(path_test+file+'.xml'):
            s.move(path_xml+file+'.xml', path_test+file+'.xml')


for file in xml:
    if file in img_valid:
        if not os.path.exists(path_valid+file+'.xml'):
            s.move(path_xml+file+'.xml', path_valid+file+'.xml')


for file in xml:
    if file in img_train:
        if not os.path.exists(path_train+file+'.xml'):
            s.move(path_xml+file+'.xml', path_train+file+'.xml')

# remove the now empty intermediate directories
os.rmdir(path+'/image')
os.rmdir(path+'/xml')

print('dataset succesfully separated into train, vali and test set')
