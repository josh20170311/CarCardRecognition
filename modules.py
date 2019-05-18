import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

import GoogleAPI as G


class MyApp:
    def __init__(self, window, window_title, video_source=0):

        self.window = window
        self.window.title(window_title)

        self.video_source = video_source
        # Variables
        self.fileName = tkinter.StringVar()
        self.result = tkinter.StringVar()
        self.result.set("Result")
        self.fileName.set(time.strftime("%y-%m-%d-%H-%M-%S-snapshot", time.localtime()))

        # init. widgets
        self.initwidgets()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def getText(self):
        self.result.set(G.send(self.fileName.get() + ".jpg"))

    def initwidgets(self):

        self.vid = MyVideoCapture(self.video_source)
        self.canvas = tkinter.Canvas(self.window, width=self.vid.width, height=self.vid.height)
        self.lb = tkinter.Label(self.window, text="Result", textvariable=self.result, width=50)
        self.tb = tkinter.Entry(self.window, text="snapshot", textvariable=self.fileName, width=30)
        self.btn_snapshot = tkinter.Button(self.window, text="Snapshot", height=3, width=30, command=self.snapshot)
        self.btn_send = tkinter.Button(self.window, text="Recognize", width=50, command=self.getText)

        self.canvas.pack()
        self.lb.pack()
        self.tb.pack()
        self.btn_snapshot.pack()
        self.btn_send.pack()

    def snapshot(self):
        if self.fileName.get() == "":
            self.fileName.set("snapshot")
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("images/" + self.fileName.get() + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor = tkinter.N)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = 360
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
