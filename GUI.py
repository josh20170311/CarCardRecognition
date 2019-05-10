import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import license_module as m

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        #Variables
        self.fileName = tkinter.StringVar()
        self.Status = tkinter.StringVar()
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
        # Label that put the status on board
        self.lb_status = tkinter.Label(window,text = "status : camara open",width = 50)
        self.lb_status.pack(anchor = tkinter.E, expand = True)
        # Label that put
        self.lb_status = tkinter.Label(window,text = "status : camara open",width = 50)
        self.lb_status.pack(anchor = tkinter.E, expand = True)
        #TextBox that set the name of snapshot
        self.tb = tkinter.Entry(window,text = "snapshot",textvariable = self.fileName,width = 50)
        self.tb.pack(anchor = tkinter.W , expand = True)
        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot" , width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.W, expand=True)
        # Button that sends snapshot to the azure api
        self.btn_send=tkinter.Button(window, text="Send to Azure API", width=50, command=self.Send)
        self.btn_send.pack(anchor=tkinter.W, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()
    def Send():
        

    def snapshot(self):
        if self.fileName.get() == "":
            self.fileName.set("snapshot")
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite(self.fileName.get()+".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
 
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

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
App(tkinter.Tk(), "CarCardRecognition",video_source = 1)
