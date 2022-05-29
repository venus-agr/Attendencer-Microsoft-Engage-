import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget,QFileDialog
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import *
import cv2

import os

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("SignUpProgram.ui", self)

        # First of all setting up all the labels for our Sign Up page like a single line that can take name as input
        # Second a button to open a browsing menu for selecting the image.
        self.label_3 = QtWidgets.QLineEdit(self) # Linelabel
        self.label_3.setGeometry(QtCore.QRect(320,120,161,20)) # Setting the size of the Text Input Bar
        self.label_3.setObjectName("lineEdit")   # Giving it a new object name for future use
        self.button.clicked.connect(self.addimage)  # Connecting our button to the desired event
        self.Quit.clicked.connect(self.close)    # A quit button


    # This function describes all the events that will be fired when the key will be pressesd
    def addimage(self):
        #Add the image
        val_username = self.label_3.text()  # Taking the text in that input bar in a new variable
        val_username = val_username + '.jpg'
        fname = QFileDialog.getOpenFileName(self, 'Open File', 'c\\', 'ImageFiles(*.jpg)') # Taking the input of the path where the current image of our user exists
        imagePath = fname[0]


        # Below is the code for saving our image in the ImagesAttendance Folder

        """
        :IMPORTANT:
        
        
        For running this successfully you must change the filePath variable with your current directory of ImagesAttendance folder.
        Please make sure you have put the correct directory and changed all backword slashes to forward slashes. Otherwise due to slashes it might give error
        """
        img = cv2.imread(imagePath)
        filename = val_username

        filePath ='ImagesAttendance'
        os.chdir(filePath)
        cv2.imwrite(filename, img)
        self.label_3.setText(" ")



# main
app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(430)
widget.setFixedWidth(765)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
