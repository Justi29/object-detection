import time
import tkinter as tk
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
import PIL.Image, PIL.ImageTk
import cv2
import main
import os

# Class representing main window visible in GUI
class App:
    def __init__(self):

         self.window = tk.Tk()
         self.window.title("Traffic Analyser")

         # Adding all widgets
         self.window.geometry('300x220')
         self.window.resizable(False, False)
         self.video_window = 0
         self.filename = ""     # path to the video

         # selecting a video for an analysis
         self.lbl_vid_choice = tk.Label(self.window, text="Choose a video\n for analysis", font="Verdana 10 bold")
         self.lbl_vid_choice.grid(column=0, row=1)
         self.bt_vid_choice = tk.Button(self.window, text="Search files", command=self.search_btn, fg="magenta", font="Verdana 8")
         self.bt_vid_choice.grid(column=1, row=1)
         self.l_accept = tk.Label(self.window, text="No selected items", fg="grey", font="Verdana 8 italic")
         self.l_accept.grid(column=1, row=2)

         # starting analysis
         self.l_an_start = tk.Label(self.window, text="Analyse \n the video", font="Verdana 10 bold")
         self.l_an_start.grid(column=0, row=3)
         self.bt_an_start = tk.Button(self.window, text="Start analysis", command=self.analyse_btn, fg="red", state="disabled", font="Verdana 8")
         self.bt_an_start.grid(column=1, row=3)
         self.l_analyse = tk.Label(self.window, fg="grey", text="", font="Verdana 8 italic")
         self.l_analyse.grid(column=1, row=4)

         # saving the results to CSV file
         self.l_vid_choice = tk.Label(self.window, text="Save results\n to csv file", font="Verdana 10 bold")
         self.l_vid_choice.grid(column=0, row=5)
         self.bt_save_csv = tk.Button(self.window, text="Save CSV", fg="blue", command=self.save_csv_btn, state="disabled", font="Verdana 8")
         self.bt_save_csv.grid(column=1, row=5)
         self.l_save = tk.Label(self.window, fg="grey", text="", font="Verdana 8 italic")
         self.l_save.grid(column=1, row=6)

         # playing analysed video
         self.l_vid_choice = tk.Label(self.window, text="Play analysed\n video", font="Verdana 10 bold")
         self.l_vid_choice.grid(column=0, row=7)
         self.bt_play_vid = tk.Button(self.window, text="Play", command=self.play_btn, fg="blue", state="disabled", font="Verdana 8")
         self.bt_play_vid.grid(column=1, row=7)

         self.window.mainloop()    # run Tkinter main window

# Action listeners
    def search_btn(self):
        acceptable_types = [('Video files', '*.mp4 *.avi')]     # acceptable input video types
        self.filename = askopenfilename(filetypes=acceptable_types)
        self.l_accept["text"] = ".../" + os.path.split(self.filename)[1]
        if self.filename != "":
            self.bt_an_start["state"] = "active"


    def analyse_btn(self):
        self.bt_an_start["state"] = "disabled"
        self.l_analyse["text"] = " Video processing ..."
        self.traffic_analyser = main.Traffic_Analyser(self.filename)    # creating a Traffic_Analyser object defined in main.py
        self.traffic_analyser.video_analyse()                           # start analysis
        # enabling playing video and saving the results
        self.l_analyse["text"] = "Video processing finished!"
        self.bt_play_vid["state"] = "active"
        self.bt_save_csv["state"] = "active"
        self.bt_an_start["state"] = "active"


    def save_csv_btn(self):
        self.bt_save_csv["state"] = "disabled"
        self.l_save["text"] = "Creating a csv file ..."
        self.traffic_analyser.write_timestamps()                        # saving the results
        self.l_save["text"] = "File created!"
        self.bt_save_csv["state"] = "disabled"

    def play_btn(self):
        self.video_window = tk.Toplevel(self.window)                    # creating a new video playback window
        self.video_window.title("Analysed video")
        self.vid = MyVideoCapture(self.traffic_analyser.output_video_file)
        self.canvas = tk.Canvas(self.video_window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()
        self.delay = 15
        self.update()


    def update(self):
        ret, frame = self.vid.get_frame()                               # getting a frame from the video source

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.video_window.after(self.delay, self.update)


# Class representing playback of the analysed video window
class MyVideoCapture:
     def __init__(self, video_source=0):

         self.vid = cv2.VideoCapture(video_source)                      # opening the video source
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)

         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)            # getting video source width and height
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

     def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
             else:
                 return (ret, None)
         else:
             return (None)

     # Release the video source when the object is destroyed
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()

# Create a window and pass it to the Application object
App()
