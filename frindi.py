from glob import glob
import tkinter
from tkinter import *
from tkinter import messagebox as mess
from tkinter import ttk
import tkinter.simpledialog as tsd
import os
import cv2
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import dlib 
from scipy.spatial import distance
from imutils import face_utils
from random import randint
import sys

#Functions=========================================================== 

#keluar
def on_closing():
    if mess.askyesno("Quit", "Apakah ingin keluar aplikasi?"):
        window.destroy()
#kontak
def contact():
    mess._show(title="Contact Me",message="Jika membutuhkan bantuan silakan hubungi 'friendymangimbulude@gmail.com'")

#tentang
def about():
    mess._show(title="About",message="Aplikasi ini dikembangkan oleh frindi mangimbulude")

#tombol clear
def clear():
    txt.delete(0, 'end')
    txt2.delete(0, 'end')
    res = "1)Ambil Gambar  ===> 2)Simpan"
    message1.configure(text=res)

#Cek Path
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

#cek haarcascade file
def check_haarcascadefile():
    exists = os.path.isfile("model/haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='fechar file missing', message='some file is missing.Please contact me for help')
        window.destroy()

#cek password ganti pasword
def save_pass():
    assure_path_exists("Pass_Train/")
    exists1 = os.path.isfile("Pass_Train\pass.txt")
    if exists1:
        tf = open("Pass_Train\pass.txt", "r")
        str = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Password not set', 'Silakan masukan katasandi baru', show='*')
        if new_pas == None:
            mess._show(title='Null Password Entered', message='Katasandi tidak diatur, silakan coba lagi!')
        else:
            tf = open("Pass_Train\pass.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered!', message='Katasandi baru sukses di atur!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == str):
        if(newp == nnewp):
            txf = open("Pass_Train\pass.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Masukan lagi katasandi baru!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Silakan masukan katasandi lama yang benar')
        return
    mess._show(title='Password Changed', message='Katasandi berhasil diubah!!')
    master.destroy()

#ganti password
def change_pass():
    global master
    master = tkinter.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Admin Password")
    master.configure(background="white")
    lbl4 = tkinter.Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tkinter.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tkinter.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tkinter.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tkinter.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tkinter.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tkinter.Button(master,text="Cancel", command=master.destroy, fg="white" , bg="#13059c", height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tkinter.Button(master, text="Save", command=save_pass, fg="black", bg="#00aeff", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#tanyakan password
def psw():
    assure_path_exists("Pass_Train/")
    exists1 = os.path.isfile("Pass_Train\pass.txt")
    if exists1:
        tf = open("Pass_Train\pass.txt", "r")
        str_pass = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Katasandi tidak diatur, Silakan masukan kembali')
        else:
            tf = open("Pass_Train\pass.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='Kantasandi baru berhasil diatur!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == str_pass):
        TrainImages()

    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='Masukan katasandi yang benar!')

def psw2():
    assure_path_exists("Pass_Train/")
    exists1 = os.path.isfile("Pass_Train\pass.txt")
    if exists1:
        tf = open("Pass_Train\pass.txt", "r")
        str_pass = tf.read()
    else:
        mess._show(title='No Password Entered', message='Silakan Daftar Untuk Menyetel Kata sandi!')
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == str_pass):
        TrackImages()

    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='Masukan Kata sandi yang benar')


#ambil gambar
def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists(r"User/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile(r"User\User.csv")
    if exists:
        with open(r"User\User.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open(r"User\User.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "model/haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.05, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # cv2.putText(img, "Face Detected", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
                cv2.putText(img, str(str(sampleNum)+" images captured"), (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0))
                # incrementing sample number
                sampleNum = sampleNum + 1
                # simpan data set foto ke folder data set
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # tampikan frame
                cv2.imshow('Taking Images', img)
            # wait for 1 miliseconds
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # berhenti ketika mencapai 100foto
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open(r'User\User.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)
            
########################################################################################
#Melatih model
def TrainImages():
    check_haarcascadefile()
    assure_path_exists("Pass_Train/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "model/haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("Pass_Train\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))
    

############################################################################################3
#mengambil label 
def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empty face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

#rectangle style
def draw_ped(img, label, x0, y0, xt, yt, color=(255,127,0), text_color=(255,255,255)):

    (w, h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.rectangle(img,
                  (x0, y0 + baseline),  
                  (max(xt, x0 + w), yt), 
                  color, 
                  2)
    cv2.rectangle(img,
                  (x0, y0 - h),  
                  (x0 + w, y0 + baseline), 
                  color, 
                  -1)  
    cv2.putText(img, 
                label, 
                (x0, y0),                   
                cv2.FONT_HERSHEY_SIMPLEX,     
                0.5,                          
                text_color,                
                1,
                cv2.LINE_AA) 
    cv2.putText(img, "Jumlah Kedipam: {}".format(total), (10, 90),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(img, "Berkedip Sebanyak: {}".format(bil), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return img

###########################################################################################
#mengenali wajah
def TrackImages():
    
    #funsinyA
    check_haarcascadefile()
    assure_path_exists("Login/")
    assure_path_exists(r"User/")
    msg = ''
    i = 0
    j = 0
    recognizer =cv2.face.LBPHFaceRecognizer_create() 
    exists3 = os.path.isfile("Pass_Train\Trainner.yml")
    if exists3:
        recognizer.read("Pass_Train\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "model/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    #blink
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('model/shape_predictor_68_face_landmarks.dat')

    def eye_aspect_ratio(eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])

        C = distance.euclidean(eye[0], eye[3])
        eye = (A + B) / (2.0 * C)

        return eye

    global count
    count = 0
    global total
    total = 0
    global bil
    bil = randint(1, 5)
    masuk = False
    
    
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile(r"User\User.csv")
    if exists1:
        df = pd.read_csv(r"User\User.csv")
    else:
        mess._show(title='Details Missing', message='User details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        faces1 = detector(gray)
        
            
        for face in faces1:
            landmarks = predictor(gray,face)

            landmarks = face_utils.shape_to_np(landmarks)
            leftEye = landmarks[42:48]
            rightEye = landmarks[36:42]

            leftEye = eye_aspect_ratio(leftEye)
            rightEye = eye_aspect_ratio(rightEye)

            eye = (leftEye + rightEye) / 2.0

            if eye<0.3:
                count+=1
            else:
                if count>=3:
                    total+=1

                count=0
                
        for (x, y, w, h) in faces:
            # cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            global bb
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                login = [str(ID), '', bb, '', str(date), '', str(timeStamp)]
                
                masuk = True

            else:
                Id = 'Unknown'
                bb = str(Id)
            # cv2.putText(im, str(bb), (x, y + h), font, 1, (0, 251, 255), 2)
            im = draw_ped(im, bb, x, y, x + w, y + h, color=(0,255,255), text_color=(50,50,50))
            
        
        
        cv2.imshow('Mengenali Wajah', im)
        
        
        
        if (cv2.waitKey(1) == ord('q') or total == bil):
            break
    
        
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Login\Login_" + date + ".csv")
    if exists:
        with open("Login\Login_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(login)
        csvFile1.close()
    else:
        with open("Login\Login_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(login)
        csvFile1.close()
        
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()
    if masuk == True:
        print("selamat datang \nanda berhasil !!!")
        halaman3()
    

#Front End===========================================================
window = Tk()
window.title("Aplikasi login")
window.overrideredirect(False)
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
window.resizable(True,True)
bg = PhotoImage( file = "Gambar/bg2.png")
label1 = Label( window, image = bg)
# label1.config(width=2000)
label1.place(x = 0,y = 0)
# window.configure(background='#355454')

#Help menubar----------------------------------------------
menubar=Menu(window)
help=Menu(menubar,tearoff=0)
help.add_command(label="Ubah Password",command=change_pass)
help.add_command(label="Contact Us",command=contact)
help.add_separator()
help.add_command(label="Exit",command=on_closing)
menubar.add_cascade(label="Help",menu=help)

# add ABOUT label to menubar-------------------------------
menubar.add_command(label="About",command=about)

#This line will attach our menu to window
window.config(menu=menubar)

#main window------------------------------------------------
message3 = tkinter.Label(window, text="Aplikasi Login" ,fg="white",bg="#12324b" ,width=60 ,height=1,font=('times', 29, ' bold '), bd=2)
message3.place(x=10, y=10,relwidth=1)

frame1 = tkinter.Frame()
frame2 = tkinter.Frame()
frame3 = tkinter.Frame()


def halaman1():
    frame2.destroy()
    frame3.destroy()
    #frames-------------------------------------------------
    global frame1
    frame1 = tkinter.Frame(window, bg="#3ca2f5")
    frame1.place(relx=0.5, rely=0.5, relwidth=0.60, relheight=0.80, anchor=CENTER)

    #frame_headder
    
    fr_head2 = tkinter.Label(frame1, text="Login", fg="white",bg="#276aa0" ,font=('times', 17, ' bold ') )
    fr_head2.place(x=0,y=0,relwidth=1)

    #BUTTONS----------------------------------------------

    trackImg = tkinter.Button(frame1, text="Processed Login", command=psw2, fg="black", bg="white", height=1, activebackground = "white" ,font=('times', 16, ' bold '))
    trackImg.place(relx=0.5, rely=0.2, anchor=CENTER,relwidth=0.40)

    quitWindow = tkinter.Button(frame1, text="Quit", command=window.destroy, fg="black", bg="white", width=35, height=1, activebackground = "white", font=('times', 16, ' bold '))
    quitWindow.place(relx=0.5, rely=0.4, anchor=CENTER,relwidth=0.40)
    
    moveee = tkinter.Button(frame1, text="Register", command=halaman2, fg="black", bg="white", width=35, height=1, activebackground = "white", font=('times', 16, ' bold '))
    moveee.place(relx=0.5, rely=0.3, anchor=CENTER,relwidth=0.40)
    
    #closing lines------------------------------------------------
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()
    
def halaman2():
    global frame2
    frame1.destroy()
    #frame
    frame2 = tkinter.Frame(window, bg="#3ca2f5")
    frame2.place(relx=0.5, rely=0.5, relwidth=0.40, relheight=0.80, anchor=CENTER)
    
    fr_head1 = tkinter.Label(frame2, text="Register", fg="white",bg="#276aa0" ,font=('times', 17, ' bold ') )
    fr_head1.place(x=0,y=0,relwidth=1)
    
    #registretion frame
    lbl = tkinter.Label(frame2, text="Masukan ID dan Nama",width=20  ,height=1  ,fg="black"  ,bg="#3ca2f5" ,font=('times', 17, ' bold ') )
    lbl.place(relx=0.5, rely=0.2, anchor=CENTER,)

    global txt
    txt = tkinter.Entry(frame2,width=32 ,fg="black",bg="#e1f2f2",highlightcolor="#00aeff",highlightthickness=3,font=('times', 15, ' bold '))
    txt.place(relx=0.5, rely=0.3, anchor=CENTER,relwidth=0.75)

    # lbl2 = tkinter.Label(frame2, text="Enter Name",width=20  ,fg="black"  ,bg="white" ,font=('times', 17, ' bold '))
    # lbl2.place(relx=0.5, rely=0.3, anchor=CENTER,)
    global txt2
    txt2 = tkinter.Entry(frame2,width=32 ,fg="black",bg="#e1f2f2",highlightcolor="#00aeff",highlightthickness=3,font=('times', 15, ' bold ')  )
    txt2.place(relx=0.5, rely=0.4, anchor=CENTER,relwidth=0.75)

    global message0
    message0=tkinter.Label(frame2,text="Ikuti Langkah Berikut...!",bg="#3ca2f5" ,fg="black"  ,width=39 ,height=1,font=('times', 16, ' bold '))
    message0.place(relx=0.5, rely=0.6, anchor=CENTER,)

    global message1
    message1 = tkinter.Label(frame2, text="1)Ambil Gambar  ===> 2)Simpan Profil" ,bg="#3ca2f5" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
    message1.place(relx=0.5, rely=0.7, anchor=CENTER,)

    global message
    message = tkinter.Label(frame2, text="" ,bg="#3ca2f5" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
    message.place(relx=0.5, rely=0.1, anchor=CENTER,)
    
    #Display total registration----------
    res=0
    exists = os.path.isfile(r"User\User.csv")
    if exists:
        with open(r"User\User.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                res = res + 1
        res = (res // 2) - 1
        csvFile1.close()
    else:
        res = 0
    message.configure(text='Total Registrations : '+str(res))
    
    clearButton = tkinter.Button(frame2, text="Clear", command=clear, fg="white", bg="#13059c", width=11, activebackground = "white", font=('times', 12, ' bold '))
    clearButton.place(relx=0.3, rely=0.5, anchor=CENTER,relwidth=0.29)

    kembali = tkinter.Button(frame2, text="Kembali", command=halaman1, fg="white", bg="#13059c", width=11, activebackground = "white", font=('times', 12, ' bold '))
    kembali.place(relx=0.7, rely=0.5, anchor=CENTER,relwidth=0.29)

    takeImg = tkinter.Button(frame2, text="Ambil Gambar", command=TakeImages, fg="black", bg="#00aeff", width=34, height=1, activebackground = "white", font=('times', 16, ' bold '))
    takeImg.place(relx=0.5, rely=0.8, anchor=CENTER,relwidth=0.40)

    trainImg = tkinter.Button(frame2, text="Simpan Profil", command=psw, fg="black", bg="#00aeff", width=34, height=1, activebackground = "white", font=('times', 16, ' bold '))
    trainImg.place(relx=0.5, rely=0.9, anchor=CENTER,relwidth=0.40)
    
    # quitWindow = tkinter.Button(frame2, text="Quit", command=window.destroy, fg="white", bg="#13059c", width=35, height=1, activebackground = "white", font=('times', 16, ' bold '))
    # quitWindow.place(x=30, y=450,relwidth=0.89)
    
    #closing lines------------------------------------------------
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

bb = 'Unknown'
def halaman3():
    frame1.destroy()
    global frame3
    if bb == 'Unknown':
        frame3.destroy()
        halaman1()
    else:
        frame1.destroy()
        #frame
        frame3 = tkinter.Frame(window, bg="#3ca2f5")
        frame3.place(relx=0.5, rely=0.5, relwidth=0.60, relheight=0.80, anchor=CENTER)
        
        fr_head1 = tkinter.Label(frame3, text="Hallo  "+bb, fg="white",bg="#276aa0" ,font=('times', 17, ' bold ') )
        fr_head1.place(x=0,y=0,relwidth=1)
        kembali = tkinter.Button(frame3, text="Loguot", command=halaman1, fg="black", bg="#00aeff", width=34, height=1, activebackground = "white", font=('times', 16, ' bold '))
        kembali.place(relx=0.5, rely=0.8, anchor=CENTER,relwidth=0.40)

        keluar = tkinter.Button(frame3, text="Quit", command=window.destroy, fg="black", bg="#00aeff", width=34, height=1, activebackground = "white", font=('times', 16, ' bold '))
        keluar.place(relx=0.5, rely=0.9, anchor=CENTER,relwidth=0.40)
        print("selamat datang")
        #closing lines------------------------------------------------
        window.protocol("WM_DELETE_WINDOW", on_closing)
        window.mainloop()
    
# run app
halaman1()
