# v7-polygon-frame-merger
A script that merges individual V7 frames of the same annotation class and that have an IoU greater than 0


## Instructions on how to use this
1. Install repo

2. Run merger.py on an exported Darwin json file for which you would like to merge the annotations. The origin file is the `filePath` variable and the target/new file is designated by the `new_path` variable.

3. Uploaded the newly created file to a dataset and file of your choice. Remember to change the filename and dataset to the desired destination within the new JSON file


## Notes:

-Currently only polygons and complex-polygons are merged. Other annotation types are left

-Subannotations are not currently supported
