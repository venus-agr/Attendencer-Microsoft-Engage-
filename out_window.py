# Created And edited by Venus Agrawal
# Last Edited in May 2022
#
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog,QMessageBox
import cv2
import face_recognition
import numpy as np
import datetime
import os
import csv

class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("./outputwindow.ui", self)
        # For Displaying Time And Date on our output window And also to save it in our excel file we create a date time object
        #Update time
        now = QDate.currentDate()   # New Variable
        current_date = now.toString('ddd dd MMMM yyyy')  # Conversion to string format as specified inside the bracket
        current_time = datetime.datetime.now().strftime("%I:%M %p")      # Now extraction of time from our variable
        self.Date_Label.setText(current_date)    #From our outputwindow.ui file we extract label names and assign them the values of date and time
        self.Time_Label.setText(current_time)    #Our labels for the above two boxes are Date_Label, Time_Label

        self.image = None

    @pyqtSlot()
    def startVideo(self, camera_name):
        """
        :param camera_name: link of camera or usb camera
        :return:
        """
        if len(camera_name) == 1:

        	self.capture = cv2.VideoCapture(int(camera_name))
        else:
        	self.capture = cv2.VideoCapture(camera_name)
        self.timer = QTimer(self)  # # Create Timer variable
        path = 'ImagesAttendance'  # Path variable for storing the path of our training images which will be used to train the face-recognition tool
        if not os.path.exists(path):
            os.mkdir(path)
        # known face encoding and known face name list
        images = [] # list for storing images on the path
        self.class_names = []  # list for storing names of people whose attendance is to be checked
        self.encode_list = []  # list for storing encoding of images. Encoding is basically face of a person converted into numerical data
        self.TimeList1 = []    # This list is used to store the clock in time of the attendee
        self.TimeList2 = []    # This list is used to store the clock out time of the attendee
        attendance_list = os.listdir(path)

        # Using a for loop to get all the images out of the attendance_list variable
        # Also using this loop to get the labels (names) of the images along with the images
        for cl in attendance_list:
            cur_img = cv2.imread(f'{path}/{cl}')
            images.append(cur_img)
            self.class_names.append(os.path.splitext(cl)[0])

            """ Converting our images from BGR TO RGB format as Our algorithm only accepts images in RGB format
                         for converting them into encodings"""
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(img)
            encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]

            self.encode_list.append(encodes_cur_frame)
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(10)  # emit the timeout() signal at x=40ms

    def face_rec_(self, frame, encode_list_known, class_names):
        """
        :param frame: frame from camera
        :param encode_list_known: known face encoding
        :param class_names: known face names
        :return:
        """
        # csv

        def mark_attendance(name):
            """
            :param name: detected face known or unknown one
            :return:
            """
            if self.ClockInButton.isChecked():  #If the clock in button is clicked then the following will be executed
                self.ClockInButton.setEnabled(False)  #First disabling the button so that user does not click it mutliple times
                with open('Attendance.csv', 'a') as f:
                        if (name != 'unknown'):   # If the person is not unknown and is from one of the photos provided in the ImageAttendence folder than
                            buttonReply = QMessageBox.question(self, 'Welcome ' + name, 'Are you Clocking In?' ,
                                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)  #This message will pop up asking for confirmation
                            if buttonReply == QMessageBox.Yes:

                                date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S") #Date time string variable created and assigned appropriate values
                                f.writelines(f'\n{name},{date_time_string},Clock In')  # Updating Our csv file with the clock in time and status
                                self.ClockInButton.setChecked(False)   #After successful completion of the above lines we set our button status to false

                                self.NameLabel.setText(name)   # We Update our name label with the persons name
                                self.StatusLabel.setText('Clocked In')   # Update our status bar
                                self.HoursLabel.setText('Measuring')     # For measuring the clock in time we show the status as measuring
                                self.MinLabel.setText('')


                                self.Time1 = datetime.datetime.now()
                                # Setting a new variable Time1
                                self.ClockInButton.setEnabled(True)
                                # After completing the complete process we again re-enable our button for next attendees
                            else:
                                print('Not clicked.')
                                self.ClockInButton.setEnabled(True)
# Now For the clock Out button similar procedure is followed, There are a few changes that I have mentioned in front of those lines below.
            elif self.ClockOutButton.isChecked():
                self.ClockOutButton.setEnabled(False)
                with open('Attendance.csv', 'a') as f:
                        if (name != 'unknown'):
                            buttonReply = QMessageBox.question(self, 'Cheers ' + name, 'Are you Clocking Out?',
                                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if buttonReply == QMessageBox.Yes:
                                date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
                                f.writelines(f'\n{name},{date_time_string},Clock Out')
                                self.ClockOutButton.setChecked(False)

                                self.NameLabel.setText(name)
                                self.StatusLabel.setText('Clocked Out')
                                self.Time2 = datetime.datetime.now()

                                # Below is the code for calculating the total time for which the user was clocked in.
                                self.ElapseList(name)
                                self.TimeList2.append(datetime.datetime.now())
                                CheckInTime = self.TimeList1[-1]
                                CheckOutTime = self.TimeList2[-1]
                                self.ElapseHours = (CheckOutTime - CheckInTime)
                                self.MinLabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60)%60) + 'm')
                                self.HoursLabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60**2)) + 'h')
                                self.ClockOutButton.setEnabled(True)
                            else:
                                print('Not clicked.')
                                self.ClockOutButton.setEnabled(True)

        # From here the face-recognition code begins
        faces_cur_frame = face_recognition.face_locations(frame)
        encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)
        # After extracting all the encodings

        # If there are multiple faces in the webcame image then we will find encodings for each face and find the minimum value of image distance among those faces

        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            match = face_recognition.compare_faces(encode_list_known, encodeFace, tolerance=0.50)
            face_dis = face_recognition.face_distance(encode_list_known, encodeFace) #this is use to find the best match with given image in the Attendance folder
            name = "unknown"
            best_match_index = np.argmin(face_dis) # We find the index of the image encodings with the least distance because the lesser the distance the better the match.

            # Now to put a rectange around the image we use this if else statement
            # here i have take color of the rectange as green(0,255,0) but we can also choose different color
            if match[best_match_index]:
                name = class_names[best_match_index].upper()
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(frame, (x1, y1), (x2, y2), (223, 255, 223), 3)
                cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2)
            mark_attendance(name)

        return frame

    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    #Now the below function is used to append the clock in and clock out time of the user in the csv file of ours
    def ElapseList(self,name):
        with open('Attendance.csv', "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 2

            Time1 = datetime.datetime.now()
            Time2 = datetime.datetime.now()
            for row in csv_reader:
                for field in row:
                    if field in row:
                        if field == 'Clock In':  # if status is updated as clock in then this statement runs
                            if row[0] == name:

                                Time1 = (datetime.datetime.strptime(row[1], '%y/%m/%d %H:%M:%S'))
                                self.TimeList1.append(Time1)
                        if field == 'Clock Out': # If status becomes clock out we append this information in the csv file
                            if row[0] == name:

                                Time2 = (datetime.datetime.strptime(row[1], '%y/%m/%d %H:%M:%S'))
                                self.TimeList2.append(Time2)






    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, self.encode_list, self.class_names, 1)

    # Below function basically manages the displaying and resizing of our image in accordance with the image label that we are using in Our GUI
    # Also update_frame function does nothing but to take input from our webcame and feed it in the displayImage function

    def displayImage(self, image, encode_list, class_names, window=1):
        """
        :param image: frame from camera
        :param encode_list: known face encoding list
        :param class_names: known face names
        :param window: number of window
        :return:
        """
        image = cv2.resize(image, (640, 480))
        try:
            image = self.face_rec_(image, encode_list, class_names)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)
