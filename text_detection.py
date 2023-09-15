from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import  QMainWindow,QApplication,QLabel,QPushButton,QTextEdit
from PyQt5 import uic
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import cv2
import pytesseract
import pyttsx3
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi('text.ui',self)
        self.title = self.findChild(QLabel,'title')
        self.image_label = self.findChild(QLabel,'imglabel')
        self.text_detect = self.findChild(QTextEdit, "textdetect")
        self.text = self.findChild(QPushButton,'text')
        self.word = self.findChild(QPushButton, 'word')
        self.character = self.findChild(QPushButton, 'character')
        self.voice = self.findChild(QPushButton, 'voice')
        self.show()
        self.text.clicked.connect(self.full_text)
        self.word.clicked.connect(self.full_word)
        self.character.clicked.connect(self.full_character)
        self.voice.clicked.connect(self.text_voice)

    def text_voice(self):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(self.text_detect.toPlainText())
        engine.runAndWait()
    def full_text(self):
        fname = QFileDialog.getOpenFileName(self,'Open file','','Image Files (*.jpg *.gif *.png)')
        print(fname)
        self.pixmap_size = QSize(self.image_label.width(),self.image_label.height())
        print(self.pixmap_size)
        self.pixmap = QPixmap(fname[0])
        self.pixmap=self.pixmap.scaled(self.pixmap_size)
        self.image_label.setPixmap(self.pixmap)
        img = cv2.imread(fname[0])
        img=cv2.resize(img,None,fx=1,fy=1)
        gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,81,11)

        text = pytesseract.image_to_string(img,lang='eng+tha')
        self.text_detect.setText(str(text))

    def full_word(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '', 'Image Files (*.jpg *.gif *.png)')
        print(fname)

        # self.image_label.setPixmap(self.pixmap)
        img = cv2.imread(fname[0])
        img = cv2.resize(img, None, fx=1, fy=1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 81, 11)
        conf = "--psm 3"
        words = pytesseract.image_to_data(img,config=conf, lang='eng+tha')
        b_string = " "
        for x,b in enumerate(words.splitlines()):
            if x != 0:
                b = b.split()
                if len(b) == 12:
                    x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                    cv2.rectangle(img,(x,y),(w+x,h+y),(0,0,255),1)
                    cv2.putText(img,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,0.5,(50,50,255),1)
                    b_string = b_string + b[11] + '\n '
        self.text_detect.setText(str(b_string))
        self.pixmap_size = QSize(self.image_label.width(), self.image_label.height())
        print(self.pixmap_size)
        self.pixmap = QPixmap(QImage(img.data, img.shape[1], img.shape[0], QImage.Format_Grayscale8))
        self.pixmap = self.pixmap.scaled(self.pixmap_size)
        self.image_label.setPixmap(self.pixmap)
        cv2.imshow('Result', img)
        cv2.waitKey(0)

    def full_character(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '', 'Image Files (*.jpg *.gif *.png)')
        print(fname)

        # self.image_label.setPixmap(self.pixmap)
        img = cv2.imread(fname[0])
        img = cv2.resize(img, None, fx=1, fy=1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 81, 11)

        characters = pytesseract.image_to_boxes(img)
        width, height = img.shape
        b_string=''
        for char in characters.splitlines():
            char = char.split(' ')

            x,y,w,h = int(char[1]),int(char[2]),int(char[3]),int(char[4])

            cv2.rectangle(img,(x,width - y),(w, width - h),(0,0,255),1)
            cv2.putText(img,char[0],(x,width - y + 10),cv2.FONT_HERSHEY_COMPLEX,0.5,(50,50,255),1)
            b_string = b_string + char[0] + '\n '
        self.text_detect.setText(str(b_string))
        self.pixmap_size = QSize(self.image_label.width(), self.image_label.height())
        print(self.pixmap_size)
        self.pixmap = QPixmap(QImage(img.data, img.shape[1], img.shape[0], QImage.Format_Grayscale8))
        self.pixmap = self.pixmap.scaled(self.pixmap_size)
        self.image_label.setPixmap(self.pixmap)
        cv2.imshow('Result', img)
        cv2.waitKey(0)
if __name__=='__main__':
    app=QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()
