"""CSC111 Winter 2021 Project Phase 2: Final Submission, Reviews Window (5)
Description
===============================
This Python module contains the reviews of the recipe selected by the user.
Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of TAs and professors
teaching CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.
This file is Copyright (c) 2021 Dana Al Shekerchi, Nehchal Kalsi, Kathy Lee, and Audrey Yoshino.
"""
from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout, QWidget, QDesktopWidget, QPushButton, \
    QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
import data_reading


class Reviews(QDialog, QWidget):
    """Class representing fifth window of program which displays reviews of a recipe as selected
    by the user in the third window."""

    def __init__(self, recipe_id: str, recipe_name: str, previous_window) -> None:
        """Initialize an instance of the Reviews window.
        """
        super().__init__()
        self.previous_window = previous_window

        self.recipe_title = QLabel("Reviews for " + recipe_name, self)
        self.recipe_title.setFont(QFont('Georgia', 15, QFont.Bold))
        self.recipe_title.setStyleSheet('color: rgb(210, 146, 68)')
        self.recipe_title.setFixedSize(600, 40)
        self.recipe_title.move(50, 40)

        all_reviews = data_reading.get_reviews(data_reading.REVIEWS_FILE)

        if recipe_id in all_reviews:
            reviews = all_reviews[recipe_id]

            self.lst_reviews = QListWidget()
            for i in range(len(reviews)):
                self.lst_reviews.insertItem(i, str(i + 1) + '. ' + reviews[i])
            self.lst_reviews.setFont(QFont('Georgia', 10))
            self.lst_reviews.setStyleSheet('color: rgb(35, 87, 77)')
            self.lst_reviews.move(50, 200)
            self.lst_reviews.setWordWrap(True)

        else:
            self.lbl_error = \
                QLabel("We're sorry, but reviews for \n this recipe are unavailable.", self)
            self.lbl_error.setFont(QFont('Georgia', 13, QFont.Bold))
            self.lbl_error.setStyleSheet('color: rgb(211, 104, 80)')
            self.lbl_error.setFixedSize(600, 60)
            self.lbl_error.move(50, 615)

            self.lst_reviews = QLabel()
            pixmap = QPixmap("visuals/error_image.png").scaled(400, 400, 1)
            self.lst_reviews.setPixmap(pixmap)

        self.title = "Look and Cook"
        self.left = 500
        self.top = 200
        self.width = 700
        self.height = 700
        self.init_window()
        self.center()
        self.setFixedSize(700, 700)
        self.setStyleSheet("background-color: rgb(240, 225, 204)")
        self.setWindowIcon(QIcon('visuals/L_C_Icon.PNG'))

    def init_window(self) -> None:
        """Open the fourth window on the user's screen with the provided dimensions.
        """
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(50, 50, 50, 70)

        self.lst_reviews.setFixedSize(600, 490)
        vbox.addWidget(self.lst_reviews, alignment=Qt.AlignCenter)

        self.setLayout(vbox)

        # Creates a back button
        back = QPushButton("Back", self)
        back.setGeometry((self.width // 2) - 50, self.height // 2 + 200, 70, 70)
        back.move(610, self.height - 90)
        back.setFont(QFont('Georgia', 10, QFont.Bold))
        back.setStyleSheet("border-radius: 35; background-color: rgb(210, 146, 68); "
                           "color: rgb(240, 225, 204)")
        back.clicked.connect(self.go_back)

        self.show()

    def center(self) -> None:  # Used top center the window on the desktop
        """Function to center third window on the provided desktop screen.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def go_back(self) -> None:
        """Take the user to the previous window.
        """
        self.hide()
        self.previous_window.show()
