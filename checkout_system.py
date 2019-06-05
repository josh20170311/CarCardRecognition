from tkinter import *
import cv2
import os
import datetime
from dateutil.parser import parse

# 待優化項目： 按確認不會一直跑東西出來QQ
# 使用前請先確認imgFolderPath是圖片放置區／carinfoobject取的路徑是資訊放置處
# 資料格式 : [車牌],[時間]
# 時間格式範例： "2019-05-08 23:58:09"

def preprocess():
    imgFolderPath = r"./images/"  # 放檔案資料夾路徑
    # ---------------------處理車牌TXT資料-----------#
    carinfoobject = open(r"./carinfo.txt", "r+")
    carinfodict = {}
    carinfo = carinfoobject.readline()

    while carinfo != "":
        carinfolist = carinfo.split(",")
        carinfolist[1] = carinfolist[1].replace("\n", "")
        carinfodict[carinfolist[0]] = carinfolist[1]
        carinfo = carinfoobject.readline()
    carinfoobject.close()
    print(carinfodict)
    print("carinfo檔案處理完成")


class Checkout:
    def __init__(self):
        preprocess()
        self.checkout = Toplevel()
        self.checkout.geometry("300x300")
        self.checkout.maxsize(300, 300)
        self.checkout.title("停車繳費系統")

        self.l1 = Label(self.checkout, text="\n\n請輸入您的車牌號碼\n")
        self.l1.pack()
        self.board = StringVar()
        self.e1 = Entry(self.checkout, textvariable=self.board)
        self.e1.pack()

        self.b1 = Button(self.checkout, text="確認", command=self.confirm)
        self.b1.pack()
        self.b2 = Button(self.checkout, text="重設", command=self.reset)
        self.b2.pack()

        self.StringVar_plateNumber = StringVar(value="您的車牌號碼是: ")
        self.StringVar_entryTime = StringVar(value="入場時間: ")
        self.StringVar_exitTime = StringVar(value="離場時間: ")
        self.StringVar_fee = StringVar(value="費用: ")

        self.l2 = Label(self.checkout, textvariable=self.StringVar_plateNumber)
        self.l3 = Label(self.checkout, textvariable=self.StringVar_entryTime)
        self.l4 = Label(self.checkout, textvariable=self.StringVar_exitTime)
        self.l5 = Label(self.checkout, textvariable=self.StringVar_fee)
        self.b3 = Button(self.checkout, text="重新查詢", command=self.searchagain)

        self.l2.pack()
        self.l3.pack()
        self.l4.pack()
        self.l5.pack()
        self.b3.pack()

        # self.checkout.mainloop()

    def reset(self):  #
        self.e1.delete(0, END)

    def searchagain(self):
        self.e1.delete(0, END)
        self.StringVar_entryTime.set("")
        self.StringVar_exitTime.set("")
        self.StringVar_plateNumber.set("")
        self.StringVar_fee.set("")

    def confirm(self):  #
        boardnum = self.board.get()
        print(imgFolderPath + boardnum + ".png")
        if os.path.exists(imgFolderPath + boardnum + ".png"):
            now = datetime.datetime.now()
            self.currentTime = str(now.strftime("%Y-%m-%d %H:%M:%S"))
            self.StringVar_plateNumber.set("您的車牌號碼是: "+boardnum)
            self.StringVar_entryTime.set("入場時間: "+carinfodict[boardnum])
            self.StringVar_exitTime.set("離場時間: "+self.currentTime)
            self.StringVar_fee.set("費用: "+self.fee())
        else:
            print("找不到您的車牌！請重新輸入！")

    def fee(self):  ###########################################
        fee = 0
        boardnum = self.board.get()
        # ========分析入場時間==========#
        entertime = carinfodict[boardnum]  ###########
        tmpe = entertime.split(" ")
        eyear, emonth, eday = self.parseDate(tmpe[0])  # tmp[0]放的是日期
        ehour, eminute, esecond = self.parseTime(tmpe[1])

        # =========擷取離場時間========#
        tmpl = self.currentTime.split(" ")
        lyear, lmonth, lday = self.parseDate(tmpl[0])
        lhour, lminute, lsecond = self.parseTime(tmpl[1])

        # ==========計算費用============#

        enter = datetime.datetime(eyear, emonth, eday, ehour, eminute, esecond)
        leave = datetime.datetime(lyear, lmonth, lday, lhour, lminute, lsecond)

        hour = int(lhour) - int(ehour)
        minute = int(lminute) - int(eminute)
        second = int(lsecond) - int(esecond)

        day = (leave - enter).days
        if day > 0:
            fee = day * 24 * 40 + (24 - int(ehour)) * 40 + int(lhour) * 40
        elif day == 0:
            fee = hour * 40
        return str(fee)

    def parseDate(self, date):
        tmp = date.split("-")
        year = tmp[0]
        month = tmp[1]
        day = tmp[2]
        return int(year), int(month), int(day)

    def parseTime(self, time):
        tmp = time.split(":")
        hour = tmp[0]
        minute = tmp[1]
        second = tmp[2]
        return int(hour), int(minute), int(second)


# ck = Checkout()
