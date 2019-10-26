these are the scripts for data preprocessing:
-> a more detailed description of the scripts can be found in the documentation of these scripts

first: mirror the output data of the labelImg tool with the script "image_mirror" / output of labelImg is a xml file containing the label information of the specific image
	-> use this script to double the date by mirroring images and label information in the xml files

second: apply the train/test split with the script "data_split". It is a randomized way to split up data into train/test/valid data

third: convert_labelImg_to_csv -> convert the label output of the labelImg tool from xml to csv format
	-> csv format is needed in order to create the tf.record files

fourth: transform image data and csv data of the labeled images into the tf.record format. this format is needed in order to train models with TensorFlow

