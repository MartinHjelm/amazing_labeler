# The amazing image labeler
Python application for labeling images.

Label images by button presses. Jump back and forward between images, labels the ones you want. Keeps track of labels in a csv file so that a labeling session can be ended and then started up again. 

**Requirements**: Python3, Pillow, Tkinter.

### Usage
    python3 img_labler.py [-h] --imgpath IMGPATH [--labels [LABELS [LABELS ...]]] [--labelfile LABELFILE]

By default the application stores the labelings in a csv file with the following structure: ```[file_index, label_index, label_name, file_path]``

### Making Modifications
