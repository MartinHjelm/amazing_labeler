#!/usr/bin/env python

######################################################
#
# The amazing image labeler - img labeling in Python.
# Written by Martin Hjelm (martinhjelm@kth.se)
#
######################################################



import argparse
from collections import namedtuple
import csv
from functools import partial
import os
import sys

from tkinter import Tk, Frame, Label, Button, LEFT, font
from PIL import ImageTk, Image

ImgIdxRange = namedtuple('ImgIdxRange', 'min,max')


class ImgLabler:

    def __init__(self, master, img_path, labels, file_ext=('jpg','jpeg','png','gif'), fname_csv='labeling'):

        # Setup labels and log
        self.labels = labels
        self.log_dic = {}
        self.fname_csv = fname_csv if fname_csv.lower().endswith('.csv') else fname_csv+'.csv'
        self._load_csv()

        # Get list of img files
        self.file_list = [img_path + '/' + x for x in os.listdir(img_path) if x.lower().endswith(file_ext)]
        self.file_list.sort()

        # Setup tracking of the current image index we are viewing
        self.idx_range = ImgIdxRange(min=0, max=len(self.file_list))
        self.curr_idx = 0

        # Create GUI
        self.master = master
        self._create_gui()

        self._update_img()
        self._update_label()
        
        

    def _create_gui(self):
        '''Creates the full GUI for the application.'''

        bg_color = '#EFEFEF'
        self.master.title("THE AMAZING IMAGE LABLER!")
        self.master.geometry("1024x750")
        self.master.configure(background=bg_color)


        # TOP PADDER
        self.padder0 = Label(self.master, pady=1, bg=bg_color)
        helv = font.Font(family='Helvetica', size=1, weight='normal')
        self.padder0['font'] = helv
        self.padder0.pack()

        # LABEL BUTTONS
        self.frame_label_buttons = Frame(self.master, pady=5, padx=5, background='white',  highlightbackground="black",
                                       highlightcolor="black", highlightthickness=1,)
        
        self.label = Label(self.frame_label_buttons, text=' ', pady=5,padx=5, highlightbackground="black",
                                       highlightcolor="black", highlightthickness=1)
        self.padder1 = Label(self.frame_label_buttons, text='', pady=5,padx=5)        
        self.label.pack(side=LEFT)
        self.padder1.pack(side=LEFT)
        self.label_buttons = self._generate_label_buttons(self.labels)
        [button.pack(side=LEFT) for button in self.label_buttons]
        self.frame_label_buttons.pack()

        # TOP IMAGE PADDER
        self.padder2 = Label(self.master, pady=1, bg=bg_color)
        helv = font.Font(family='Helvetica', size=1, weight='normal')
        self.padder2['font'] = helv
        self.padder2.pack()

        # IMAGE
        self.frame_image = Frame(self.master, pady=25, padx=25, width=325, height=485, bd=5, 
        highlightbackground="black", highlightcolor="black", highlightthickness=1, bg='white')
        # Set up first image
        fname = self.file_list[self.curr_idx]
        img = Image.open(fname)
        img = img.resize((320, 480), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.img_panel = Label(self.frame_image, image=img)
        self.img_panel.image = img
        self.img_panel.pack()
        self.frame_image.pack()

        # BOTTOM IMAGE PADDER
        self.padder3 = Label(self.master, text='', pady=2, bg=bg_color)
        self.padder3.pack()

        # FORWARD AND BACK BUTTONS
        self.frame_nav_buttons = Frame(self.master, pady=5, padx=5, highlightbackground="black",
                                       highlightcolor="black", highlightthickness=1, bg='white')
        self.back_button = Button(self.frame_nav_buttons, text="Back", command=self._move_back_callback)
        self.back_button.pack(side=LEFT)
        # self.close_button = Button(self.frame_nav_buttons, text="Close", command=self.master.quit)
        # self.close_button.pack(pady=25, padx=25,side=LEFT)
        self.forward_button = Button(self.frame_nav_buttons, text="Forward", background=bg_color, command=self._move_forward_callback)
        self.forward_button.pack(side=LEFT)
        self.frame_nav_buttons.pack()


    def _generate_label_buttons(self, labels):
        '''Generates a list that contains buttons for each given label.'''
        button_list = []
        helv = font.Font(family='Helvetica', size=14, weight='normal')
        for idx, label in enumerate(labels):
            callback = partial(self._label_button_callback, idx=idx, label=label)
            button_list.append(Button(self.frame_label_buttons, text=label, command=callback, padx=10, pady=10))
            button_list[idx]['font'] = helv
        return button_list


    def _label_button_callback(self, idx, label):
        '''Updates img and labels, and saves results to csv file.'''
        print(self.curr_idx, idx, label, self.file_list[self.curr_idx])
        self.log_dic[self.curr_idx] = [self.curr_idx, idx, label, self.file_list[self.curr_idx]]
        if self._update_img_idx(direction=1):
            self._update_img()
        self._update_label()
        self._save_to_csv()


    def _update_label(self):
        '''Updates the label panel if a img has ben previously labeled.'''
        if self.curr_idx in self.log_dic:
            self.label['text'] = self.log_dic[self.curr_idx][2]
            self.label['bg'] = 'red'
        else:
            self.label['text'] = ''
            self.label['bg'] = 'white'


    def _update_img(self):
        '''Updates the current GUI img that we are labeling.'''
        fname = self.file_list[self.curr_idx]
        if fname is not None:
            # Get img
            img = Image.open(fname)
            # Resize if bigger than 800x800
            basewidthx, basewidthy = 500, 300
            sx, sy = img.size[0], img.size[1]
            # Select biggest dimension to
            if img.size[0] > img.size[1]:
                if img.size[0] > basewidthx:
                    wpercent = (basewidthx / float(img.size[1]))
                    sx = int((float(img.size[0]) * float(wpercent)))
                    sy = basewidthx
            else:
                if img.size[1] > basewidthy:
                    sx = basewidthy
                    wpercent = (basewidthy / float(img.size[0]))
                    sy = int((float(img.size[1]) * float(wpercent)))

            img = img.resize((sx, sy), Image.ANTIALIAS)
            # OLD
            # wpercent = (basewidth/float(img.size[0]))
            # hsize = int((float(img.size[1])*float(wpercent)))
            # img = img.resize((basewidth,hsize), Image.ANTIALIAS)

            img = ImageTk.PhotoImage(img)
            # Update panel with new image
            self.img_panel.image = img
            self.img_panel.configure(image=img)
            self.img_panel.image = img


    def _update_img_idx(self, direction):
        '''Updates the pointer to the current img, checks for end and start of file list.'''
        self.curr_idx += direction

        # Check update range
        if self.curr_idx < self.idx_range.min:
            self.curr_idx = self.idx_range.min
            return False
        if self.curr_idx >= self.idx_range.max:
            self.curr_idx = self.idx_range.max - 1
            return False

        return True


    def _move_forward_callback(self):
        '''Callback for forward button. Moves idx forward and upates images and labels.'''
        if self._update_img_idx(direction=1):
            self._update_img()
            self._update_label()


    def _move_back_callback(self):
        '''Callback for back button. Moves idx back and upates images and labels.'''
        if self._update_img_idx(direction=-1):
            self._update_img()
            self._update_label()


    def _save_to_csv(self):
        '''Writes the current labeled imgs to a csv file.'''
        with open('labeling.csv', 'w') as out:
            csv_out = csv.writer(out)
            csv_out.writerow(['img_idx','label_idx', 'label', 'fname'])
            for key in sorted(self.log_dic, key=self.log_dic.get):
                csv_out.writerow(self.log_dic[key])


    def _load_csv(self):
        '''On startup reads the default or a given csv file of the labels and puts them into the log dictionary.'''
        try:
            with open('labeling.csv', 'r') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=',')
                next(csv_reader, None)  # Skip header
                for row in csv_reader:
                    rowlist = [int(row[0]), int(row[1]), row[2], row[3]]
                    self.log_dic[rowlist[0]] = rowlist
        except FileNotFoundError:
            pass



def parse_clis():

    # PARSE COMMAND LINE ARGS
    CLI = argparse.ArgumentParser()
    CLI.add_argument(
        "--imgpath",  # name on the CLI - drop the `--` for positional/required parameters
        type=str,
        required=True
    )
    CLI.add_argument(
        "--labels",
        nargs="*",
        type=str,
    )
    CLI.add_argument(
        "--labelfile",
        type=str,
    )

    args = CLI.parse_args()

    if args.labels is None and args.labelfile is None:
        CLI.error("At least one of \033[96m--labels\033[0m or \033[96m--labelfile\033[0m is required")

    # Turn given labels into a list
    labels = []
    if args.labelfile is not None:
        try:
            # Read csv file of labels
            with open(args.labelfile, newline='') as csvfile:
                label_reader = csv.reader(csvfile, delimiter=',')
                labels = []
                for row in label_reader:
                    labels.extend(row)
        except FileNotFoundError:
            print('Label file {} not found. Exiting...'.format(args.labelfile))
            sys.exit()
    else:
        labels = args.labels

    # Pre-check input for correctness to stop annoying mistakes early on
    if len(labels) < 2:
        raise ValueError('At least a list of two labels are needed for a meaningful labeling...')
    if not os.path.isdir(args.imgpath):
        raise ValueError('The path \033[96m{:s}\033[0m is not a directory or does not exist.'.format(args.imgpath))
    if not os.listdir(args.imgpath):
        raise ValueError('The path \033[96m{:s}\033[0m seems to be empty.'.format(args.imgpath))

    return args.imgpath, labels



if __name__ == '__main__':

    # Comment in, to specify path and labels directly.
    # img_path = 'MyImgPath'
    # labels = ['Cat1', 'Cat2', 'Cat3']
    # Comment out if specifying directly.
    img_path, labels = parse_clis()
    
    root = Tk()
    img_labler_obj = ImgLabler(master=root, img_path=img_path, labels=labels)
    root.mainloop()
