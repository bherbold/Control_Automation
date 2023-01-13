import threading

import csv

# int_line_edit_ui.py

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys

# Writing the base class 'Thread'
class AsyncWrite(threading.Thread):

    def __init__(self):
        # calling superclass init
        threading.Thread.__init__(self)

    def run(self):
        UserInput()


# A simple widget consisting of a QLabel and a QLineEdit that
# uses a QIntValidator to ensure that only integer inputs are
# accepted. This class could be implemented in a separate
# script called, say, labelled_int_field.py
class LabelledIntField(QWidget):
    def __init__(self, title, initial_value=None):
        QWidget.__init__(self)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel()
        self.label.setText(title)
        self.label.setFixedWidth(100)
        self.label.setFont(QFont("Arial", weight=QFont.Bold))
        layout.addWidget(self.label)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setFixedWidth(40)
        self.lineEdit.setValidator(QIntValidator())
        if initial_value != None:
            self.lineEdit.setText(str(initial_value))
        layout.addWidget(self.lineEdit)
        layout.addStretch()

    def setLabelWidth(self, width):
        self.label.setFixedWidth(width)

    def setInputWidth(self, width):
        self.lineEdit.setFixedWidth(width)

    def getValue(self):
        return int(self.lineEdit.text())


# -------------------------------------------------------------------


class UnserInputWindow(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        # Ensure our window stays in front and give it a title
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Set your temperature")
        self.setFixedSize(400, 200)

        # Create and assign the main (vertical) layout.
        vlayout = QVBoxLayout()
        self.setLayout(vlayout)

        self.addIntInputsPanel(vlayout)
        vlayout.addStretch()
        self.addButtonPanel(vlayout)
        self.show()

    # --------------------------------------------------------------------
    def addIntInputsPanel(self, parentLayout):
        hlayout = QHBoxLayout()
        self.sdiv = LabelledIntField('Set your Temperature in °C (max 52)', 45)

        hlayout.addWidget(self.sdiv)
        hlayout.addStretch()
        parentLayout.addLayout(hlayout)

    # --------------------------------------------------------------------
    def addButtonPanel(self, parentLayout):
        self.button = QPushButton("Set")
        self.button.clicked.connect(self.buttonAction)

        hlayout = QHBoxLayout()
        hlayout.addStretch()
        hlayout.addWidget(self.button)
        parentLayout.addLayout(hlayout)

    # --------------------------------------------------------------------
    def buttonAction(self):

        with open('../Data_Management/UserTemperature.csv', 'w', newline='') as csvFile:
            # Create a CSV reader
            writer = csv.writer(csvFile)
            writer.writerow([min(self.sdiv.getValue(),52)])
            csvFile.close()

    # --------------------------------------------------------------------


def UserInput():
    app = QApplication(sys.argv)
    windowTemp = UnserInputWindow()  # <<-- Create an instance
    windowTemp.show()
    sys.exit(app.exec_())

