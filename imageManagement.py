from tkinter import *
import tkinter
import os
from PIL import Image, ImageTk
from functools import partial
from tkinter import messagebox



class imageMangement:
    def __init__(self):
        self.window = tkinter.Toplevel()
        self.window.title('視窗')  # 窗口标题
        # window.resizable(False, False)  # 固定視窗大小
        self.windowWidth = 1600  # 視窗寬
        self.windowHeight = 900  # 視窗高
        self.screenWidth, screenHeight = self.window.maxsize()  # 獲得螢幕寬和高
        self.window.geometry("1366x768")
        self.window.wm_attributes('-topmost', 1)  # 視窗置頂

        self.deletebtn = tkinter.Button(self.window, text="刪除",command=self.deleteImgage,width=20, height=10,bg="pink",fg="white",font="30")
        self.deletebtn.place(x=500, y=500)
        self.name = StringVar()
        self.lab = tkinter.Label(self.window, textvariable=self.name)



        self.lab.grid(column=1, row=2)

        self.show_canvas()
        self.x_place=450
        self.y_place=0
        self.show_Thumbnail()


        self.window.mainloop()





    # 空畫布
    def show_canvas(self):
        self.preview = ImageTk.PhotoImage(file="noimagefile.jpg")
        self.preview_canvas = tkinter.Canvas(self.window, width=self.preview.width(), height=self.preview.height())
        self.preview_canvas.create_image(0, 0, image=self.preview, anchor=tkinter.NW)
        #self.preview_canvas.delete("all")  # 清空畫布
        self.preview_canvas.grid(column=1, row=0)
        #self.preview_canvas.pack(side=LEFT, padx=5, pady=5)

    # 點擊縮圖顯示圖片
    def show_Image(self,n):
        self.pil_image = Image.open(n)
        self.w, self.h = self.pil_image.size  # 獲取圖片的原始大小
        self.preview = ImageTk.PhotoImage(file="noimagefile.jpg") #重新抓一次大小
        self.pil_image_resized = self.resize(self.w, self.h, self.preview.width(),self.preview.height() )  # 縮放圖片讓它保持比例，同時限制在一個矩形框範圍內

        self.preview = ImageTk.PhotoImage(self.pil_image_resized)
        self.preview_canvas.create_image(0, 0, image=self.preview, anchor=tkinter.NW)
        self.preview_canvas.grid(column=1, row=0)
        n_split=n.split("/")
        self.name.set(n_split[1])

        self.selectImgae=n


    #顯示縮圖
    def show_Thumbnail(self):
        self.w_box = 150
        self.h_box = 100

        self.tk_images=list()
        imlist = os.listdir('./images')
        for x in imlist:
            if self.x_place>1000:
                self.x_place=450
                self.y_place = self.y_place + 100
            self.x_place = self.x_place + 150
            self.y_place = self.y_place + 0
            self.fileName="images/"+x

            self.pil_image=Image.open(self.fileName)
            self.w, self.h = self.pil_image.size  # 獲取圖片的原始大小
            self.pil_image_resized = self.resize(self.w, self.h, self.w_box, self.h_box)  # 縮放圖片讓它保持比例，同時限制在一個矩形框範圍內
            self.tk_images.append(ImageTk.PhotoImage(self.pil_image_resized))
            self.img = tkinter.Button(self.window, image=self.tk_images[imlist.index(x)], width=self.w_box, height=self.h_box, command=partial(self.show_Image,self.fileName),bd=0)
            self.img.place(x=self.x_place, y=self.y_place)

        self.window.mainloop()

    def resize(self,w, h, w_box, h_box):
        self.f1 = 1.0 * w_box / w
        self.f2 = 1.0 * h_box / h
        self.factor = min([self.f1, self.f2])
        self.width = int(w * self.factor)
        self.height = int(h * self.factor)
        return self.pil_image.resize((self.width, self.height), Image.ANTIALIAS)

    def deleteImgage(self):
        os.remove(self.selectImgae)
        self.x_place = 450
        self.y_place = 0
        self.show_Thumbnail()
