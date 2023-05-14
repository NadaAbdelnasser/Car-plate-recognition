import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from easyocr import Reader
import easyocr
from PIL import Image,ImageTk
import os
import pyarabic.araby as araby



root=Tk()

fram=Frame(root)
fram.pack(side=BOTTOM,padx=5,pady=5)
root.title("Image Viewer")
root.geometry("400x450")
lbl=Label(root)
lbl.pack()
btn=Button(fram, text="Select Image", command=lambda: img())
btn.pack(side=tk.LEFT)

btn2=Button(fram, text="Exit", command=lambda: exit())
btn2.pack(side=tk.LEFT, padx=5)


def img():
    filetype = (("JPG File", ".jpg"), ("PNG File", ".png"), ("All file ", "how are you .txt"))
    filename = filedialog.askopenfilename(filetypes=filetype)
    car = cv2.imread(filename)
    car = cv2.resize(car, (800, 600))
    gray = cv2.cvtColor(car, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 10, 200)
    cont, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cont = sorted(cont, key=cv2.contourArea, reverse=True)[:5]

    for c in cont:
        arc = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * arc, True)
        if len(approx) == 4:
            plate_cnt = approx
            break
    (x, y, w, h) = cv2.boundingRect(plate_cnt)
    plate = gray[y:y + h, x:x + w]

    reader = Reader(['en'], gpu=False, verbose=False)
    detection = reader.readtext(plate)
    print(detection)

    if len(detection) == 0:
        text = "Impossible to read the text from the license plate"
        cv2.putText(car, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 3)
        cv2.imshow('Image', car)
        cv2.waitKey(0)
    else:
        cv2.drawContours(car, [plate_cnt], -1, (0, 255, 0), 3)
        text = f"{detection[0][1]} {detection[0][2] * 100:.2f}%"
        cv2.putText(car, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        cv2.imshow('Image', car)
        cv2.waitKey(0)
        cv2.imshow('license plate', plate)
        cv2.waitKey(0)
        print(text)




root.mainloop()
