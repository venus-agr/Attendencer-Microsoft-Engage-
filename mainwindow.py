# Coded And Modified By Venus Agrawal
# Last Updated in May 2022

import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
import resource
# from model import Model
from out_window import Ui_OutputDialog
"""
Like Any Other PyQt5 program we begin our code by creating a class named after our First Window.
Inside this class we can perform various functions that will fire when particular actions are performed in the window

"""

class Ui_Main(QDialog):
    def __init__(self):
        super(Ui_Main, self).__init__()
        # To Load the .ui file and connect it with this python file for editing
        loadUi("Attendencer.ui", self)
        # By using the label for the push button used in the form we can connect it to a event as shown below
        self.runButton.clicked.connect(self.Intermediate)
        # The self parameter is a reference to the current instance of the class, and is used to access variables that belongs to the class.

        self._new_output_wind = None # New variable used for controlling output window
        self.VideoStart_ = None # New Variable used for starting video capturing
        #  When the pushbutton that is named Begin! will be clicked a new function will be called named runSlot.
    def REDO(self):
        """
        Set the text of lineEdit once it becomes valid
        """

        #define a video capture object
        self.VideoStart_ = "0"

    @pyqtSlot()
    def Intermediate(self):
        """
        This Funtion is Called when the user presses the Begin! Button
        """
        print("Event Triggered")
        # Now Calling the refresh
        self.REDO()
        # Called the refreshAll function
        print(self.VideoStart_)
        # This print function is to keep a check that the program is running properly or not.
        ui.hide()  # hide the main window
        self.outputWindow_()  # Create and open new output window

    def outputWindow_(self):
        """
        Function is Used to create a New Window for visual output.
        """
        self._new_output_wind = Ui_OutputDialog()

        # Assigning our object a new value of output dialog box instead of its previous none value
        self._new_output_wind.show()
        # Calling the inbuilt show function for video display
        self._new_output_wind.startVideo(self.VideoStart_)
        # To begin the video display
        print("Video Display Has Begun!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Main()
    ui.show()
    sys.exit(app.exec_())
#        Code Runs with zero errors And we are directed to the Output Window