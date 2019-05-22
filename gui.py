import tkinter
import cv2
import PIL.Image
import PIL.ImageTk
import time
from tkinter import messagebox
import os

import GoogleAPI as G


class MyApp:
    def __init__(self, window=tkinter.Tk(), window_title="VLPR", video_source=0):

        self.window = window
        self.window.title(window_title)
        self.window.geometry("1366x768")
        self.video_source = video_source
        # Variables
        self.fileName = tkinter.StringVar(value=time.strftime("%y-%m-%d-%H-%M-%S-snapshot", time.localtime()))
        self.result = tkinter.StringVar(value="Result")
        self.lastselect = 0  # listbox

        # init. widgets
        self.initwidgets()
        self.makemenu()
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 50
        self.update()

        self.window.mainloop()

    def OCR(self):
        self.result.set(G.send("images/" + self.fileName.get() + ".jpg"))

    def initwidgets(self):

        self.vid = MyVideoCapture(self.video_source)

        self.canvas = tkinter.Canvas(self.window, width=self.vid.width, height=self.vid.height)
        self.preview = PIL.ImageTk.PhotoImage(file="TR/images/noimagefile.jpg")
        self.preview_canvas = tkinter.Canvas(self.window, width=self.preview.width(), height=self.preview.height())
        self.preview_canvas.create_image(0, 0, image=self.preview, anchor=tkinter.NW)
        self.messagebox = messagebox.Message()

        self.lb = tkinter.Label(self.window, text="Result", textvariable=self.result, font=("arial", 30))
        self.btn_snapshot = tkinter.Button(self.window, width=10, height=1, text="Snapshot", command=self.snapshot,
                                           font=("arial", 30), bg='green', fg='white')
        self.btn_send = tkinter.Button(self.window, width=10, height=1, text="Recognize", command=self.OCR,
                                       font=("arial", 30), bg='blue', fg='white')
        self.btn_quit = tkinter.Button(self.window, width=10, height=1, text="QUIT", command=self.window.quit,
                                       font=("arial", 30), bg='red', fg='white')
        self.listb = tkinter.Listbox(self.window, height=20, width=65, font=("arial", 15))
        self.makeimageslist()

        self.listb.selection_handle(command=self.selection_event())

        self.canvas.grid(column=0, row=0)
        self.preview_canvas.place(x=0, y=480)
        self.listb.grid(column=1, row=0)
        self.lb.grid(column=1, row=1)
        self.btn_snapshot.grid(column=1, row=2)
        self.btn_send.grid(column=1, row=3)
        self.btn_quit.grid(column=1, row=4)

    def makemenu(self):
        self.main_menu = tkinter.Menu(self.window)
        self.window.config(menu=self.main_menu)
        self.file_menu = tkinter.Menu(tearoff=False)
        self.main_menu.add("cascade", label="File", menu=self.file_menu)
        self.file_menu.add("command", label='Save File', command=self.window.quit)
        self.file_menu.add("command", label='Open Image', command=self.window.quit)
        self.file_menu.add("command", label='quit', command=self.window.quit)
        self.file_menu.add("command", label='quit', command=self.window.quit)
        self.file_menu.add("command", label='quit', command=self.window.quit)
        self.main_menu.add("command", label="about", command=self.about)

    def about(self):
        messagebox.showinfo(title='about', message='message', detail='detail')

    def snapshot(self):
        if self.fileName.get() == "":
            self.fileName.set("snapshot")
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("images/" + self.fileName.get() + ".png", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        self.makeimageslist()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW, )

        self.selection_event()
        self.window.after(self.delay, self.update)

    def makeimageslist(self):
        self.listb.delete(0, last=self.listb.size() - 1)
        imlist = os.listdir('./images')
        for x in imlist:
            self.listb.insert(imlist.index(x), str(x))

    def selection_event(self):
        if self.listb.curselection() != () and self.listb.curselection() != self.lastselect:
            self.preview = tkinter.PhotoImage(file='images/'+self.listb.get(self.listb.curselection()))
            self.preview = self.preview.zoom(24)
            self.preview = self.preview.subsample(int(self.preview.height()/250))
            self.preview_canvas.create_image(0, 0, image=self.preview, anchor=tkinter.NW)
            self.lastselect = self.listb.curselection()


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
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
            return (0, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
