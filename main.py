"""Look And Cook: Main Program Window (1)

Description
===============================
This Python module contains the visualization of the main title program window.
"""
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QVBoxLayout, QWidget, QDesktopWidget, \
    QPushButton
from PyQt5.QtCore import Qt
import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QIcon, QFont
from ingredients_dialogue import IngredientsDialogue
from typing import Union


class MainWindow(QDialog, QWidget):
    """Opens the initial starting window for Look and Cook.

    Contains the logo, start button, and code to handle a click event.
    """
    title: str
    left: int
    top: int
    width: int
    height: int
    ingredients_dialogue: Union[None, IngredientsDialogue]

    def __init__(self) -> None:
        """Initialize an instance of MainWindow.
        """
        super().__init__()
        # Sets up the screen with all the needed elements
        self.title = "Look and Cook"
        self.left = 500
        self.top = 200
        self.width = 700
        self.height = 700
        self.init_window()
        self.center()
        self.ingredients_dialogue = None
        self.setFixedSize(700, 700)
        self.setStyleSheet("background-color: rgb(240, 225, 204)")
        self.setWindowIcon(QIcon('visuals/L_C_Icon.PNG'))
        self.setWindowTitle("Look and Cook")

    def center(self) -> None:
        """Center MainWindow on the provided desktop screen.
       """
        # Creates a window in the center of the screen using the screen size
        # frame = self.frameGeometry()
        # window = QDesktopWidget().availableGeometry().center()
        # frame.moveCenter(window)
        # # self.move(frame.topLeft())

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # frameGm = self.frameGeometry()
        # screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        # centerPoint = QApplication.desktop().screenGeometry(screen).center()
        # frameGm.moveCenter(centerPoint)
        # self.move(frameGm.topLeft())

    def init_window(self) -> None:
        """Open the main window on the user's screen with the provided dimensions.
        """
        # Sets up screen
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

        # Centers the title in the center of the page
        vbox = QVBoxLayout()
        image = QLabel()
        pixmap = QPixmap("visuals/L_C_Logo.png").scaled(500, 500, 1)
        image.setPixmap(pixmap)
        vbox.addWidget(image, alignment=Qt.AlignCenter)
        self.setLayout(vbox)

        # Start button
        btn_start = QPushButton("Start!", self)
        btn_start.setGeometry((self.width // 2) - 50, self.height // 2 + 200, 100, 100)
        btn_start.move((self.width // 2) - 50, self.height // 2 + 200)
        btn_start.setStyleSheet("border-radius: 50; background-color: rgb(210, 146, 68); "
                                "color: rgb(240, 225, 204)")
        btn_start.setFont(QFont('Tisa', 13, weight=QtGui.QFont.Bold))
        btn_start.clicked.connect(self.clicked)

        # Opens the window
        self.show()

    def clicked(self) -> None:
        """Link the start button to the second window displaying ingredient choices.
        """
        self.hide()
        if self.ingredients_dialogue is None:
            self.ingredients_dialogue = IngredientsDialogue()
            self.ingredients_dialogue.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
