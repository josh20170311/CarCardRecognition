import tkinter
import tkinter.ttk
import cv2
import PIL.Image
import PIL.ImageTk
import time
from tkinter import messagebox
from tkinter import filedialog
import os


import GoogleAPI as G
import ALPR as A
import checkout_system as C

class MyApp:
    # consts
    IMAGE_DIR = "images/"
    NOFILEIMAGE_DIR = "noimagefile.jpg"

    def __init__(self, window=tkinter.Tk(), window_title="ALPR", video_source=1):

        # create a top-window
        self.window = window
        self.window.title(window_title)
        self.window.geometry("1366x768")
        self.video_source = video_source

        # Constants
        self.BASE_X = 900
        self.BASE_Y = 500

        # Variables
        self.timeStamp = ""
        self.fileName = tkinter.StringVar(value=os.listdir(self.IMAGE_DIR)[0])
        self.result = tkinter.StringVar(value="Result")
        self.last_index = 0  # listbox
        self.current_image = self.fileName.get()

        # init. widgets
        self.initwidgets()
        self.makemenu()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        # start the app
        self.window.mainloop()

    def initwidgets(self):

        # camera
        self.vid = MyVideoCapture(self.video_source)

        # Image
        self.preview = PIL.ImageTk.PhotoImage(file=self.NOFILEIMAGE_DIR)

        # canvas
        self.canvas = tkinter.Canvas(self.window, width=self.vid.width, height=self.vid.height)
        self.preview_canvas = tkinter.Canvas(self.window, width=self.vid.width, height=self.vid.height)
        self.preview_canvas.create_image(0, 0, image=self.preview, anchor=tkinter.NW)

        # message box
        self.messagebox = messagebox.Message()

        # label
        self.lb = tkinter.Label(self.window, text="Result", textvariable=self.result, font=("arial", 15))

        # button
        self.btn_snapshot = tkinter.Button(self.window, width=10, height=1, text="Snapshot", command=self.snapshot,
                                           font=("arial", 15), bg='green', fg='white')
        self.btn_send = tkinter.Button(self.window, width=10, height=1, text="Google API",
                                       command=self.result_from_google, font=("arial", 15), bg='blue', fg='white')
        self.btn_delete = tkinter.Button(self.window, width=10, height=1, text="DELETE", command=self.delete,
                                         font=("arial", 15), bg='red', fg='white')
        self.btn_quit = tkinter.Button(self.window, width=10, height=1, text="QUIT", command=self.window.destroy,
                                       font=("arial", 15), bg='red', fg='white')

        # listbox
        self.listb = tkinter.Listbox(self.window, height=20, width=58, font=("arial", 15))

        # combobox
        self.cb = tkinter.ttk.Combobox(self.window, width=58, textvariable=self.fileName)


        # pre-process
        self.makeimageslist()
        self.listb.selection_handle(command=self.selection_event())

        # layout
        self.canvas.grid(column=0, row=0, ipadx=0, padx=50)
        self.preview_canvas.grid(column=1, row=0)
        self.cb.grid(column=0, row=1)

        self.lb.place(x=self.BASE_X, y=self.BASE_Y)
        self.btn_snapshot.place(x=self.BASE_X, y=self.BASE_Y + 50)
        self.btn_send.place(x=self.BASE_X, y=self.BASE_Y + 100)
        self.btn_delete.place(x=self.BASE_X, y=self.BASE_Y + 150)
        self.btn_quit.place(x=self.BASE_X, y=self.BASE_Y + 200)

    def makemenu(self):
        self.main_menu = tkinter.Menu(self.window)
        self.window.config(menu=self.main_menu)
        self.file_menu = tkinter.Menu(tearoff=False)
        self.main_menu.add("cascade", label="File", menu=self.file_menu)
        self.file_menu.add("command", label='Save File', command=self.savefile)
        self.file_menu.add("command", label='Open Image', command=self.opentheimage)
        self.file_menu.add("command", label='Quit', command=self.window.destroy)
        self.main_menu.add("command", label="About", command=self.about)

    def savefile(self):  # under construction
        pass

    def opentheimage(self):  # under construction
        askfilename = filedialog.askopenfilename(filetypes=(("png files", "*.png"), ("all files", "*.*")))
        print(askfilename)

    def about(self):  # under construction
        messagebox.showinfo(title='about', detail='Reference : \nPython OpenCV - show a video in a Tkinter window by Paul')

    def makeimageslist(self):
        imlist = os.listdir('./images')
        self.cb['values'] = imlist

    def selection_event(self):
        if self.listb.curselection() != () and self.listb.curselection() != self.last_index:
            self.fileName.set(self.listb.get(self.listb.curselection()))
            self.preview = tkinter.PhotoImage(file='images/' + self.listb.get(self.listb.curselection()))

            #  self.preview = self.preview.zoom(24)  # zoom in
            #  self.preview = self.preview.subsample(int(self.preview.height() / 250))  # zoom out

            self.preview_canvas.create_image(0, 0, image=self.preview, anchor=tkinter.NW)
            self.last_index = self.listb.curselection()

    def snapshot(self):
        self.timeStamp = self.getTimeStamp()
        self.fileName.set("snapshot.png")

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("images/" + self.fileName.get(), cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        self.makeimageslist()

    def delete(self):  # under construction
        app2 = C.Checkout()

    def getTimeStamp(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def result_from_google(self):
        result = G.send(imagefile=self.IMAGE_DIR + self.fileName.get())
        messagebox.showinfo(title="result", detail=result)
        with open("carinfo.txt", "a") as f:
            f.write(result+","+self.getTimeStamp()+"\n")
            f.flush()
        # messagebox.showinfo(title='nothing', message='nothing', detail='you have to uncomment the function')

    def ALPR(self):  # under construction
        print(self.IMAGE_DIR + self.current_image)
        org = cv2.imread(self.IMAGE_DIR + self.current_image)
        print(A.alpr(image=org))
        # messagebox.showinfo(message=A.alpr(image=org))
        # self.result.set(A.alpr(image=self.vid.get_frame()[1]))

    def update(self):
        # Get a frame from the video source
        success, frame = self.vid.get_frame()
        print(self.cb.get())

        t, rec = A.alpr(image=frame)
        self.result.set(t)

        if success:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(rec))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.selection_event()
        self.window.after(self.delay, self.update)


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


app = MyApp()