import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
# import license_module as m
# import recognition_module as m
import GoogleAPI as G


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("1280x600")
        self.video_source = video_source
        # Variables
        self.fileName = tkinter.StringVar()
        self.result = tkinter.StringVar()
        self.result.set("Result")
        self.fileName.set(time.strftime("%y-%m-%d-%H-%M-%S-snapshot", time.localtime()))
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.place(x=1270-self.vid.width, y=10)
        # Result Label
        self.lb = tkinter.Label(window, text="Result", textvariable=self.result, width=50)
        self.lb.place(x=10, y=500)
        # TextBox that set the name of snapshot
        self.tb = tkinter.Entry(window, text="snapshot", textvariable=self.fileName, width=30)
        self.tb.place(x=10, y=530)
        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(window, text="Snapshot",height = 3, width=30, command=self.snapshot)
        self.btn_snapshot.place(x=10, y=550)
        # Button that sends snapshot to Google api
        self.btn_send = tkinter.Button(window, text="Recognize", width=50, command=self.Run)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def Run(self):
        self.result.set(G.send(self.fileName.get() + ".jpg"))

    def snapshot(self):
        if self.fileName.get() == "":
            self.fileName.set("snapshot")
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("images/"+self.fileName.get() + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

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
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


# Create a window and pass it to the Application object
App(tkinter.Tk(), "CarCardRecognition", video_source=1)
