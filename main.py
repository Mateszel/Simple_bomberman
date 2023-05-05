from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPen, QBrush
from PyQt5.Qt import Qt
from PyQt5.QtCore import QTimer, QDateTime
from random import randint
import keyboard
import sys



lives = 1
less_enemies = 0
Map_of_game_data = []


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Bomberman 1.0"
        self.top = 200
        self.left = 500
        self.width = 1000
        self.height = 724
        self.player_lives = lives

        # map and player info
        self.map_of_game = [[0 for x in range(12)] for y in range(12)]
        for i in range(6):
            for j in range(6):
                self.map_of_game[i * 2][j * 2] = 1
        self.Player = Player(0, 1)
        self.map_of_game[0][1] = 4

        self.Enemies = []
        self.Enemies.append(Enemy(5, 5))
        self.map_of_game[5][5] = 3
        self.Enemies.append(Enemy(7, 8))
        self.map_of_game[7][8] = 3
        if less_enemies == 0:
            self.Enemies.append(Enemy(2, 7))
            self.map_of_game[2][7] = 3

        self.Obstacles = []
        for i in range(9):
            self.Obstacles.append(Obstacle(randint(1, 4)*2 + 1, randint(1, 4)*2 + 1))
            self.map_of_game[self.Obstacles[i].x][self.Obstacles[i].y] = 2

        self.bomb_tick = 0
        self.do_count = 0
        self.bomb_x = 0
        self.bomb_y = 0

        self.mob_tick = 0
        self.map_time = 0

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGraphicView()

        self.show()

    def createGraphicView(self):
        self.scene = QGraphicsScene()
        self.greenBrush = QBrush(Qt.black)
        self.grayBrush = QBrush(Qt.gray)
        self.redBrush = QBrush(Qt.red)
        self.pen = QPen(Qt.yellow)
        self.pen_white = QPen(Qt.white)
        self.whiteBrush = QBrush(Qt.white)

        graphicView = QGraphicsView(self.scene, self)
        graphicView.setGeometry(0, 0, 1000, 724)

        self.shapes()

        # timer
        self.timer = QTimer()
        self.timer.start(33)
        self.timer.timeout.connect(self.shapes)

    # noinspection PyInconsistentIndentation
    def shapes(self):

        self.scene.clear()
        if keyboard.is_pressed('a'):
            if self.detect_collision(-1, 0) == 1:
                self.map_of_game[self.Player.x][self.Player.y] = 0
                self.Player.x -= 1
                self.map_of_game[self.Player.x][self.Player.y] = 4
            elif self.detect_collision(-1, 0) == 2:
                if self.player_lives == 1:
                    self.map_of_game[self.Player.x][self.Player.y] = 0
                    self.Player.x = 15
                    self.Player.y = 15
                else:
                    self.player_lives = self.player_lives - 1
        elif keyboard.is_pressed('d'):
            if self.detect_collision(1, 0) == 1:
                self.map_of_game[self.Player.x][self.Player.y] = 0
                self.Player.x += 1
                self.map_of_game[self.Player.x][self.Player.y] = 4
            elif self.detect_collision(1, 0) == 2:
                if self.player_lives == 1:
                    self.map_of_game[self.Player.x][self.Player.y] = 0
                    self.Player.x = 15
                    self.Player.y = 15
                else:
                    self.player_lives = self.player_lives - 1
        elif keyboard.is_pressed('w'):
            if self.detect_collision(0, -1) == 1:
                self.map_of_game[self.Player.x][self.Player.y] = 0
                self.Player.y -= 1
                self.map_of_game[self.Player.x][self.Player.y] = 4
            elif self.detect_collision(0, -1) == 2:
                if self.player_lives == 1:
                    self.map_of_game[self.Player.x][self.Player.y] = 0
                    self.Player.x = 15
                    self.Player.y = 15
                else:
                    self.player_lives = self.player_lives - 1
        elif keyboard.is_pressed('s'):
            if self.detect_collision(0, 1) == 1:
                self.map_of_game[self.Player.x][self.Player.y] = 0
                self.Player.y += 1
                self.map_of_game[self.Player.x][self.Player.y] = 4
            elif self.detect_collision(0, 1) == 2:
                if self.player_lives == 1:
                    self.map_of_game[self.Player.x][self.Player.y] = 0
                    self.Player.x = 15
                    self.Player.y = 15
                else:
                    self.player_lives = self.player_lives - 1
        elif keyboard.is_pressed(' '):
            self.do_count = 1
            self.bomb_x = self.Player.x
            self.bomb_y = self.Player.y
            self.place_bomb(self.bomb_x, self.bomb_y)

        if self.mob_tick == 10:
            self.mob_movement()
            self.mob_tick = 0
        else:
            self.mob_tick += 1

        if self.do_count == 1:
            self.bomb_tick += 1
            self.place_bomb(self.bomb_x, self.bomb_y)

        if self.bomb_tick == 30:
            self.detonate_bomb(self.bomb_x, self.bomb_y)
            self.bomb_tick = 0
            self.do_count = 0

        show_player = self.scene.addEllipse(self.Player.x*40+5, self.Player.y*40+5, 30, 30, self.pen, self.grayBrush)

        for i in range(12):
            for j in range(12):
                global Map_of_game_data
                Map_of_game_data.append(self.map_of_game[i][j])
                if self.map_of_game[i][j] == 1:
                    obstacle = self.scene.addRect(0 + i * 40, 0 + j * 40, 40, 40, self.pen, self.greenBrush)
                elif self.map_of_game[i][j] == 2:
                    obstacle = self.scene.addRect(0 + i * 40, 0 + j * 40, 40, 40, self.pen, self.grayBrush)
                elif self.map_of_game[i][j] == 3:
                    self.scene.addEllipse(0 + i * 40+5, 0 + j * 40 + 5, 30, 30, self.pen, self.redBrush)


    def mob_movement(self):
        for i in range(len(self.Enemies)):
            destiny = randint(0, 4)
            if destiny == 0 and self.detect_collision_bot(-1, 0, i) == 1:
                self.map_of_game[self.Enemies[i].x][self.Enemies[i].y] = 0
                self.Enemies[i].x -= 1
                self.map_of_game[self.Enemies[i].x][self.Enemies[i].y] = 3
            elif destiny == 1 and self.detect_collision_bot(1, 0, i) == 1:
                self.map_of_game[self.Enemies[i].x][self.Enemies[i].y] = 0
                self.Enemies[i].x += 1
                self.map_of_game[self.Enemies[i].x][self.Enemies[i].y] = 3
            elif destiny == 2 and self.detect_collision_bot(0, -1, i) == 1:
                self.map_of_game[self.Enemies[i].x][self.Enemies[i].y] = 0
                self.Enemies[i].y -= 1
                self.map_of_game[self.Enemies[i].x][self.Enemies[i].y] = 3
            elif destiny == 3 and self.detect_collision_bot(0, 1, i) == 1:
                self.map_of_game[self.Enemies[i].x][self.Enemies[i].y] = 0
                self.Enemies[i].y += 1
                self.map_of_game[self.Enemies[i].x][self.Enemies[i].y] = 3

    def place_bomb(self, curr_x, curr_y):
        bomb = self.scene.addEllipse(curr_x * 40 + 10, curr_y * 40 + 10, 20, 20, self.pen, self.redBrush)

    def detonate_bomb(self, curr_x, curr_y):
        if self.map_of_game[curr_x][curr_y] == 2 or self.map_of_game[curr_x][curr_y] == 3:
            self.map_of_game[curr_x][curr_y] = 0
            if self.map_of_game[curr_x][curr_y] == 3:
                for i in range(len(self.Enemies)):
                    if self.Enemies[i].x == curr_x and self.Enemies[i].y == curr_y:
                        del self.Enemies[i]
        if self.map_of_game[curr_x+1][curr_y] == 2 or self.map_of_game[curr_x+1][curr_y] == 3:
            self.map_of_game[curr_x+1][curr_y] = 0
            if self.map_of_game[curr_x+1][curr_y] == 3:
                for i in range(len(self.Enemies)):
                    if self.Enemies[i].x == curr_x+1 and self.Enemies[i].y == curr_y:
                        del self.Enemies[i]
        if self.map_of_game[curr_x][curr_y+1] == 2 or self.map_of_game[curr_x][curr_y+1] == 3:
            self.map_of_game[curr_x][curr_y+1] = 0
            if self.map_of_game[curr_x][curr_y+1] == 3:
                for i in range(len(self.Enemies)):
                    if self.Enemies[i].x == curr_x and self.Enemies[i].y == curr_y+1:
                        del self.Enemies[i]
        if self.map_of_game[curr_x][curr_y-1] == 2 or self.map_of_game[curr_x][curr_y-1] == 3:
            self.map_of_game[curr_x][curr_y-1] = 0
            if self.map_of_game[curr_x][curr_y-1] == 3:
                for i in range(len(self.Enemies)):
                    if self.Enemies[i].x == curr_x and self.Enemies[i].y == curr_y-1:
                        del self.Enemies[i]
        if self.map_of_game[curr_x-1][curr_y] == 2 or self.map_of_game[curr_x-1][curr_y] == 3:
            self.map_of_game[curr_x-1][curr_y] = 0
            if self.map_of_game[curr_x-1][curr_y] == 3:
                for i in range(len(self.Enemies)):
                    if self.Enemies[i].x == curr_x - 1 and self.Enemies[i].y == curr_y:
                        del self.Enemies[i]
        bomb = self.scene.addEllipse(curr_x * 40 + 10, curr_y * 40 + 10, 20, 20, self.pen_white, self.whiteBrush)
        explosion = self.scene.addRect(curr_x * 40, curr_y * 40, 40, 40, self.pen_white, self.redBrush)
        explosion = self.scene.addRect(curr_x * 40 + 40, curr_y * 40, 40, 40, self.pen_white, self.redBrush)
        explosion = self.scene.addRect(curr_x * 40 - 40, curr_y * 40, 40, 40, self.pen_white, self.redBrush)
        explosion = self.scene.addRect(curr_x * 40, curr_y * 40 + 40, 40, 40, self.pen_white, self.redBrush)
        explosion = self.scene.addRect(curr_x * 40, curr_y * 40 - 40, 40, 40, self.pen_white, self.redBrush)

    def detect_collision(self, move_x, move_y):
        x_p, y_p = self.Player.x, self.Player.y
        if x_p+move_x < 0 or x_p+move_x > 10:
            return 0
        if y_p+move_y < 0 or y_p+move_y > 10:
            return 0
        if self.map_of_game[x_p + move_x][y_p + move_y] == 1:
            return 0
        if self.map_of_game[x_p + move_x][y_p + move_y] == 2:
            return 0
        if self.map_of_game[x_p + move_x][y_p + move_y] == 3:
            return 2
        return 1

    def detect_collision_bot(self, move_x, move_y, idx):
        x_p, y_p = self.Enemies[idx].x, self.Enemies[idx].y
        if x_p+move_x < 0 or x_p+move_x > 10:
            return 0
        if y_p+move_y < 0 or y_p+move_y > 10:
            return 0
        if self.map_of_game[x_p + move_x][y_p + move_y] == 1:
            return 0
        if self.map_of_game[x_p + move_x][y_p + move_y] == 2:
            return 0
        return 1


class Window_start(QDialog):

    # constructor
    def __init__(self):
        super(Window_start, self).__init__()

        # setting window title
        self.setWindowTitle("Config")

        # setting geometry to the window
        self.setGeometry(100, 100, 300, 400)

        # creating a group box
        self.formGroupBox = QGroupBox("Form 1")

        # creating spin box to select age
        self.ageSpinBar = QSpinBox()

        # creating checkbox
        self.checkbox_powerup = QCheckBox('Additional life')
        self.checkbox_powerup.stateChanged.connect(self.clickBox)

        self.checkbox_powerup_1 = QCheckBox('Additional health')
        self.checkbox_powerup_1.stateChanged.connect(self.clickBox_1)

        self.checkbox_powerup_2 = QCheckBox('Less enemies')
        self.checkbox_powerup_2.stateChanged.connect(self.clickBox_2)

        # creating combo box to select degree
        self.degreeComboBox = QComboBox()

        # creating a line edit
        self.nameLineEdit = QLineEdit()

        # calling the method that create the form
        self.createForm()

        # creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # adding action when form is accepted
        self.buttonBox.accepted.connect(self.getInfo)

        # adding action when form is rejected
        self.buttonBox.rejected.connect(self.reject)

        # creating a vertical layout
        mainLayout = QVBoxLayout()

        # adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)

        # adding button box to the layout
        mainLayout.addWidget(self.buttonBox)

        # setting lay out
        self.setLayout(mainLayout)

        # variable
        self.add_live = 0
        self.curr_lives = 0

    # get info method called when form is accepted
    def getInfo(self):
        # printing the form information
        print("Ip and port : {0}".format(self.nameLineEdit.text()))
        self.curr_lives = int(self.ageSpinBar.text()) + self.add_live
        print("Lives for player : {0}".format(self.ageSpinBar.text()))
        global lives
        lives = self.curr_lives
        # closing the window
        self.close()

    # creat form method
    def createForm(self):
        # creating a form layout
        layout = QFormLayout()

        # adding rows
        # for name and adding input text
        layout.addRow(QLabel("Ip and port: "), self.nameLineEdit)

        # for age and adding spin box
        layout.addRow(QLabel("Lives for player:"), self.ageSpinBar)

        # for powerups
        layout.addRow(QLabel("Which powerup: "), self.checkbox_powerup)

        layout.addRow(QLabel(""), self.checkbox_powerup_1)

        layout.addRow(QLabel(""), self.checkbox_powerup_2)

        # setting layout
        self.formGroupBox.setLayout(layout)

        # choosing player
        self.label = QLabel('Who plays?')
        self.rbtn1 = QRadioButton('Single player')
        self.rbtn2 = QRadioButton('Two players')
        self.rbtn3 = QRadioButton('Bot / AI')
        self.label2 = QLabel("")

        self.rbtn1.toggled.connect(self.onClicked)
        self.rbtn2.toggled.connect(self.onClicked)
        self.rbtn3.toggled.connect(self.onClicked)

        layout.addWidget(self.label)
        layout.addWidget(self.rbtn1)
        layout.addWidget(self.rbtn2)
        layout.addWidget(self.rbtn3)
        layout.addWidget(self.label2)

    def onClicked(self):
        radioBtn = self.sender()

    def clickBox(self, state):
        if state == QtCore.Qt.Checked:
            self.add_live = 1
            print('Checked')
        else:
            self.add_live = 0
            print('Unchecked')

    def clickBox_1(self, state):
        if state == QtCore.Qt.Checked:
            print('Checked_1')
        else:
            print('Unchecked_1')

    def clickBox_2(self, state):
        if state == QtCore.Qt.Checked:
            print('Checked_2')
            global less_enemies
            less_enemies = 1
        else:
            print('Unchecked_2')


app = QApplication(sys.argv)

# create the instance of our Window
window = Window_start()

# showing the window
window.show()

app.exec()

App = QApplication(sys.argv)
window = Window()
App.exec()
