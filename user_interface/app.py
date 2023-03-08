import sys, os
import backend
from listen import Listen
from pygame import mixer
from gtts import gTTS
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMenuBar, QAction
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QSize

from PyQt5 import QtTest

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.sound = True
        self.setup()
        self.rooms = ['Select']
        self.floors = ['Select', '1', '2', '3']
        self.floor_num = "Select"
        self.room_num = "Select";
        self.dark_mode = True
        self.state = "Floor"

        self.select_floor()
        self.show()

    def keyPressEvent(self, event):
        if event.key() == 47:
            self.playHelpMenu()
        if event.key() == 42:
            self.changeMode()
        if event.key() == 45:
            self.muteSound()
        if event.key() == 48:
            self.combobox1.showPopup()
        if event.key() == Qt.Key_Q:
            print("Bye!")
            sys.exit()
        if event.key() == Qt.Key_Enter:
            if (self.button.isEnabled()):
                if (self.state == "Select"):
                    self.directions()
                else:
                    self.navigating()
            else:
                event.accept()
        event.accept()

    def setup(self):
        self.setWindowTitle("Autonomous Building Guide")
        self.setFixedWidth(900)
    
        with open("dark/stylesheet.qss", "r") as f:
            content = f.readlines()
        text = ""
        for i in content:
            text += i
        self.setStyleSheet(text)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.audio("Welcome",'Welcome to Beamish Munro Hall. My name is George. I will guide you to your destination within the building. Press H if you would like to hear the help menu.')

        self.first()

    def first(self):
        self.state = "Select"

        self.layoutH1 = QHBoxLayout()
        self.layoutH2 = QHBoxLayout()
        self.layoutH3 = QHBoxLayout()
        self.layoutH4 = QHBoxLayout()
        self.layoutH5 = QHBoxLayout()

        self.layout.addLayout(self.layoutH1)
        self.layout.addLayout(self.layoutH2)
        self.layout.addLayout(self.layoutH3)
        self.layout.addLayout(self.layoutH5)

        self.pixmap = QPixmap('./icons/Dot.png')
        self.pixmap = self.pixmap.scaled(20,20)
        self.pixmap2 = QPixmap('./icons/Dot2.png')
        self.pixmap2 = self.pixmap2.scaled(20,20)

        self.dot1 = QLabel()
        self.dot2 = QLabel()
        self.dot3 = QLabel()
        self.dot4 = QLabel()

        self.dot1.setPixmap(self.pixmap)
        self.dot2.setPixmap(self.pixmap2)
        self.dot3.setPixmap(self.pixmap2)
        self.dot4.setPixmap(self.pixmap2)
 
        # Optional, resize label to image size
        self.layoutH3.addWidget(self.dot1)
        self.layoutH3.addWidget(self.dot2)
        self.layoutH3.addWidget(self.dot3)
        self.layoutH3.addWidget(self.dot4)
        
        self.help = QPushButton()
        self.help.setIcon(QIcon("icons/unmute_black.png"))
        self.help.setIconSize(QSize(60, 60))
        self.help.setFont(QFont("Asap",50))
        self.help.setFixedWidth(100)
        self.help.clicked.connect(self.playHelpMenu)
        self.layoutH5.addWidget(self.help)

        self.mute = QPushButton()
        self.mute.setIcon(QIcon("icons/Help.png"))
        self.mute.setIconSize(QSize(60, 60))
        self.mute.setFixedWidth(100)
        self.mute.clicked.connect(self.muteSound)
        self.layoutH5.addWidget(self.mute)

        self.mic = QPushButton()
        self.mic.setIcon(QIcon("icons/mic.png"))
        self.mic.setIconSize(QSize(60, 60))
        self.mic.setFixedWidth(100)
        self.mic.clicked.connect(self.handleSpeech)
        self.layoutH5.addWidget(self.mic)

    def audio(self,filename, message):
        if (self.sound):
            files = os.listdir('sound')
            filename += ".mp3"
            if (filename in files):
               mixer.init()
               mixer.music.load("sound/" + filename)
               mixer.music.play()
            else:
                language = 'en'
                myobj = gTTS(text=message, lang=language, slow=False)
                myobj.save("sound/" + filename)
                mixer.init()
                mixer.music.load("sound/" + filename)
                mixer.music.play()

    def select_floor(self):
        self.state = "Floor"
        self.l1 = QLabel('Select Floor')
        self.l1.setFont(QFont("Asap",50))
        self.combobox1 = QComboBox()
        self.combobox1.setFixedWidth(500)
        self.l1.setAlignment(Qt.AlignHCenter)
        self.combobox1.setFont(QFont("Asap",50))
        self.combobox1.addItems(self.floors)
        self.combobox1.currentTextChanged.connect(self.setFloor)
        self.layoutH1.addWidget(self.l1)
        self.layoutH2.addWidget(self.combobox1)

        self.button = QPushButton()
        self.button.setIcon(QIcon("./icons/Arrow.png"))
        self.button.setIconSize(QSize(60, 60))
        self.button.setEnabled(False)
        self.layoutH2.addWidget(self.button)
       
        self.button.setFixedWidth(100)
        self.button.clicked.connect(self.handleButtonPress)
    
    def setFloor(self,value):
        self.floor_num = value
        if (self.floor_num != 'Select'):
            self.button.setEnabled(True)
        else:
            self.button.setEnabled(False)

    def handleButtonPress(self):
        if (self.state == "Floor"):
            self.listRooms()
        elif (self.state == "Room"):
            self.directions()

    def listRooms(self):
        self.layoutH2.removeWidget(self.button)
        self.cancel = QPushButton()
        self.cancel.setIcon(QIcon("./icons/Back.png"))
        self.cancel.setIconSize(QSize(60, 60))
        self.cancel.setFixedWidth(100)
        self.layoutH2.addWidget(self.cancel)
        self.layoutH2.addWidget(self.button)
        self.button.setEnabled(False)
        self.cancel.clicked.connect(self.cancelState)
        self.state = "Room"
        self.dot2.setPixmap(self.pixmap)
        self.rooms = ["Select"]
        rooms = backend.listByFloor(self.floor_num)
        for i in rooms:
            self.rooms.append(i)
        self.combobox1.clear()
        self.l1.setText('Select Room')
        self.combobox1.addItems(self.rooms)
        self.combobox1.currentTextChanged.connect(self.setRoom)
        self.audio("RoomOptions","Room options are ")
        QtTest.QTest.qWait(2000)

        for i in self.rooms:
            if i != "Select":
                self.audio(i,i)
                QtTest.QTest.qWait(1000)        

    def setRoom(self,value):
        self.room_num = value
        print(self.room_num)
        if (self.room_num != 'Select'):
            self.button.setEnabled(True)
        else:
            self.button.setEnabled(False)

    # Confirm destination
    def destination(self,value):
        if (value != "Select" and value != " "):
            text = "You have selected room " + value + ". Press continue if that is correct."
            self.audio("Select" + value, text)
            self.room_num = value
            self.button.setEnabled(True)
        if (value == "Select"):
            self.button.setEnabled(False)

    # List Obstacles in Path
    def directions(self):
        self.state = "Obstacles"
        self.dot3.setPixmap(self.pixmap)
        
        self.clearWidget(self.layoutH2, self.combobox1)
        self.clearWidget(self.layoutH2, self.button)
        self.clearWidget(self.layoutH2, self.cancel)

        self.l1.setText("Hazards in path: ")
        
        obstacles = backend.getObstackeList();
        ob = ""
        for i in obstacles:
            ob += i + " "
        self.l2 = QLabel(ob)
        self.l2.setFont(QFont("Asap",50))
        self.l2.setAlignment(Qt.AlignHCenter)
        self.layoutH1.addWidget(self.l2)

        self.c = QPushButton()
        self.c.setIcon(QIcon("./icons/Arrow.png"))
        self.c.setIconSize(QSize(60, 60))
        self.cancel = QPushButton()
        self.cancel.setIcon(QIcon("./icons/Back.png"))
        self.cancel.setIconSize(QSize(60, 60))
        self.layoutH2.addWidget(self.cancel)
        self.layoutH2.addWidget(self.c)
        self.c.clicked.connect(self.navigating)
        self.cancel.clicked.connect(self.cancelState)

    def deleteItemsOfLayout(self,layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())

    def cancelState(self):
        self.deleteItemsOfLayout(self.layout)
        self.first()
        self.select_floor()

    # Screen when navigating to destination
    def navigating(self):
        self.dot4.setPixmap(self.pixmap)
        self.l1.setText("Going to room " + self.room_num)
        backend.sendRoom(self.room_num)

        self.clearWidget(self.layoutH2, self.l2)
        self.clearWidget(self.layoutH2, self.c)
        self.clearWidget(self.layoutH2, self.cancel)
        # Clear screen

        # Robot should begin moving here
        self.audio("Going" + self.room_num, "Going to room " + self.room_num)
        QtTest.QTest.qWait(3000)
        self.onRoute()

    def onRoute(self):
        while(True):
            direction = backend.getDirections()
            if (direction is not None):
                self.l1.setText(direction)
                self.audio(direction,direction)
                QtTest.QTest.qWait(2000)
                break
        self.l1.setText("Arrived!")
        self.audio("Arrived", "You have arrived at your destination.")

    # Clear Widget
    def clearWidget(self, base, item):
        base.removeWidget(item)
        item.deleteLater()
        item = None

    def muteSound(self):
        if (self.sound):
            self.mute.setIcon(QIcon('icons/mute_black.png'))
            self.audio("Soundoff","Sound off")
            QtTest.QTest.qWait(1000)
            self.sound = False
        else:
            self.mute.setIcon(QIcon('icons/unmute_black.png'))
            self.sound = True
            self.audio("Soundon","Sound on")
            QtTest.QTest.qWait(1000)

    def playHelpMenu(self):
        text = "Help Menu. M to mute/unmute. B to change to light/dark mode."
        self.audio("Help",text)

    def handleSpeech(self):
        l = Listen()
        QtTest.QTest.qWait(500)        
        if (self.state == "Floor"):
            self.audio("Listening_floor", "Which floor would you like to go to?")
            QtTest.QTest.qWait(1000)        
            text = l.listening()
            text = l.text_to_number(text)
            print("I heard " + text)
            self.audio("You said " + text, "You said " + text)
            QtTest.QTest.qWait(1000)
            if text in self.floors:
                self.setFloor(text)
                self.listRooms()
            else:
                self.audio("Invalid floor", "Invalid Floor Number")
        elif (self.state == "Room"):
            self.audio("Listening_room", "Which room would you like to go to?")
            QtTest.QTest.qWait(1000)        
            text = l.listening()
            text = l.text_to_number(text)
            print("I heard " + text)
            self.audio("You said " + text, "You said " + text)
            QtTest.QTest.qWait(1000)
            if text in self.rooms:
                self.setRoom(text)
                self.directions()
            else:
                self.audio("Invalid room", "Invalid Room Number")
        else:
             self.audio("No talk", "I don't want to talk to you")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = App()
    window.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')