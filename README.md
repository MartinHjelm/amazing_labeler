# The amazing image labeler
Python application for labeling images.

Label images by button presses. Jump back and forward between images, labels the ones you want. Keeps track of labels in a csv file so that a labeling session can be ended and then started up again. 

**Requirements**: Python3, Pillow uses [tkinter](https://docs.python.org/3/library/tk.html) for the GUI.

### Usage
    python3 img_labler.py [-h] --imgpath IMGPATH [--labels [LABELS [LABELS ...]]] [--labelfile LABELFILE]

Input a image path, a list of labels or a file containing the lables. The application, by default, stores the labelings in a csv file with the following structure: ```[file_index, label_index, label_name, file_path]```

### Making Modifications
It is possible to modify default image sizes, which file extensions to look for, the name of csv file to save to, etc. It is possible to just specify labels and directories directly in the py file ignoring the CLI parsing. 

It would surely be possible to switch the images to some other media form like videos or sound, or text-files while keeping the same structure.