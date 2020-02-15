import ctypes
import os
import threading
import cv2
import numpy as np
from os import listdir,mkdir
from os.path import isfile, join
from tkinter import *
from tkinter.font import  Font
from PIL import ImageTk, Image
face_cascade = cv2.CascadeClassifier('face_cas.xml')


count=0
def Signup():
    L1 = Label(root, text='                                                                           ', font=f3).place(
        x=300, y=420)

    def sign_up():
        sig = sign.get()
        Label(root_signup, text='                                   ').place(x=200, y=180)
        if sig == 'Kundan':
            root_signup.destroy()
            x = listdir('C:/Face UnLock Face_Data')
            if len(x) == 0:
                pass
            else:
                for i in x:
                    os.remove('C:/Face UnLock Face_Data/%s' % i)

            data_path = 'C:/Face UnLock Face_Data/'
            onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
            Labels = []
            for i, files in enumerate(onlyfiles):
                Labels.append(i)
            Labels = np.asarray(Labels, dtype=np.int32)
            x1 = len(Labels)
            # root.destroy()
            root_S = Toplevel()
            root_S.geometry("210x200+1200+330")
            app = Frame(root_S, bg="white")
            app.place(x=1, y=1)
            lmain = Label(app)
            lmain.grid()
            camera = cv2.VideoCapture(0)

            def video_stream():
                ret, image = camera.read()
                frame = cv2.flip(image, 1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                n = 0
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                    n = faces.shape[0]
                    face_img = frame[y:y + h, x:x + w]

                if n == 0:
                    cv2.putText(frame, 'No Face found', (10, 450), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                else:
                    global count
                    count += 1
                    face = cv2.resize(face_img, (200, 200))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                    cv2.imwrite('C:/Face UnLock Face_Data/user' + str(count + x1) + '.jpg', face)

                    cv2.putText(face, str(count), (5, 180), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                if count < 20:
                    img = Image.fromarray(face)
                    imgtk = ImageTk.PhotoImage(image=img)
                    lmain.imgtk = imgtk
                    lmain.configure(image=imgtk)
                    lmain.after(1, video_stream)
                else:
                    camera.release()
                    root_S.destroy()

            video_stream()
            root_S.attributes("-topmost", True)
            root_S.mainloop()
        else:
            Label(root_signup, text='Invalid Password').place(x=200, y=180)

    root_signup = Toplevel()
    root_signup.geometry('360x500+900+100')
    img1 = ImageTk.PhotoImage(Image.open("12_lock.jpg"))
    panel = Label(root_signup, image=img1).place(x=1, y=20)
    sign = StringVar()
    l3 = Label(root_signup, text="Hackacthon Battle", fg='brown', font=f1).place(x=70, y=10)
    l3 = Label(root_signup, text=" Sign Up with Face_Lock", fg='darkblue', font=f1).place(x=60, y=40)
    l3 = Label(root_signup, text=" Enter Password ", fg='blue', font=f1).place(x=100, y=380)
    E1 = Entry(root_signup, show='*', textvariable=sign, font=f3).place(x=90, y=420)
    but = Button(root_signup, text='Login', command=sign_up, width=20, height=1, font=f3, bg='green').place(x=80,
                                                                                                            y=460)
    root_signup.resizable('false', 'false')
    root_signup.mainloop()

def recogonise_lock():
    root.destroy()
    root_PC = Tk()
    root_PC.geometry("500x400+100+30")
    app = Frame(root_PC, bg="white")
    app.place(x=1, y=1)
    lmain = Label(app)
    lmain.grid()

    data_path = 'D:/Face UnLock Face_Data/'
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    Training_Data, Labels = [], []
    for i, files in enumerate(onlyfiles):
        image_path = data_path + onlyfiles[i]
        images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        Training_Data.append(np.asarray(images, dtype=np.uint8))
        Labels.append(i)
    Labels = np.asarray(Labels, dtype=np.int32)
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(Training_Data), np.asarray(Labels))
    ct = 0
    p = 0
    camera = cv2.VideoCapture(0)

    def video_stream():
        global ct, p
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        n = 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            face = gray[y:y + h, x:x + w]
            face = cv2.resize(face, (200, 200))
            n = face.shape[0]
            j, k = model.predict(face)
            confidence = int(100 * (1 - (k) / 300))
        if n > 0:
            p = 0
            if k > 30:
                if confidence < 75:

                    ct += 1
                    # cv2.putText(frame, 'Unauthentic User', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
                    if ct == int(p1) * 25:
                        ctypes.windll.user32.LockWorkStation()
                else:
                    # cv2.putText(frame, 'Genuine User', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 120, 125), 3)
                    ct = 0

        elif n == 0:
            p += 1
            if p == int(p1) * 25:
                ppp = ctypes.windll.user32.LockWorkStation()

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(1, video_stream)

    video_stream()

    root_PC.attributes("-topmost", True)
    root_PC.mainloop()

root = Tk()
root.geometry('300x500+500+200')
root.title('AutoLock Windows Screen')
try:
    mkdir('D:/Face UnLock Face_Data/')
except:
    pass
f1 = Font(family="Time New Roman", size=15, weight="bold", underline=1)
f3 = Font(family="Time New Roman", size=13, weight="bold")

def get_value():
    global p1
    try:
        mkdir('D:/Face UnLock Face_Data/')
    except:
        pass
    p1 = x1.get()
    if p1=="":
        l1 = Label(root, text='...........Please Enter Time................', fg='White',bg='skyblue',font=f1,).place(x=5, y=460)
    elif not p1.isdigit():
        l1 = Label(root, text='........Please Enter Valid Time.............', fg='White', bg='skyblue', font=f1, ).place(x=5, y=460)
    else:
        l1 = Label(root, text='............................................', fg='White', bg='skyblue', font=f1, ).place(x=5, y=460)
        recogonise_lock()

frame=Frame(root,height=600,width=10).pack(side=RIGHT)
img = ImageTk.PhotoImage(Image.open("Auto.jpg"))
panel = Label(frame, image = img)
panel.pack(side = "left", fill = "both", expand = "yes")
x1 = StringVar()
x2 = StringVar()
l1 = Label(root, text=' AutoLock Windows \n Screen', fg='skyblue',font=f1).place(x=50, y=10)
l1 = Label(root, text=' Set Lock Timer (In Seconds) ', fg='White',bg='skyblue',font=f1,).place(x=5, y=250)
l1 = Label(root, text='  Based On Face Recognition   ', fg='White',bg='skyblue',font=f1,).place(x=5, y=80)
e1 = Entry(root, textvariable=x1,font=f3,width=20,fg='White',bg='skyblue').place(x=55, y=300)
b = Button(root, text='Enter', command=get_value, width=18, height=1, bg='darkblue',font=f3,fg='White').place(x=60, y=350)
b1 = Button(root, text='Sign Up', command=Signup, width=18, height=1, bg='darkblue',font=f3,fg='White').place(x=60, y=400)


root.resizable('false','false')
root.mainloop()