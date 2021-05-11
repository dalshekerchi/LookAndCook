"""CSC111 Winter 2021 Project Phase 2: Final Submission, Ingredients Program Window (2)

Description
===============================
This Python module contains the visualization of the ingredients selection program window.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of TAs and professors
teaching CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 Dana Al Shekerchi, Nehchal Kalsi, Kathy Lee, and Audrey Yoshino.
"""
from PyQt5.QtWidgets import QLabel, QDialog, QWidget, QDesktopWidget, QLineEdit, \
    QListWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
import data_reading


class IndividualRecipe(QDialog, QWidget):
    """Class representing fourth window of program which displays a single recipe as selected
    by the user in the third window."""

    def __init__(self, recipe_name: str) -> None:
        """Initialize an instance of the IndividualRecipe window.
        """
        super().__init__()
        self.recipe_name = recipe_name

        self.recipe_title = QLabel(self.recipe_name, self)
        self.recipe_title.setFont(QFont('Georgia', 14, QFont.Bold))
        self.recipe_title.setStyleSheet('color: rgb(211, 104, 80)')
        self.recipe_title.setFixedSize(600, 40)
        self.recipe_title.move(50, 40)

        self.selected_recipe = QLineEdit()  # get recipe id, if possible
        self.data = data_reading.read_recipes(data_reading.RECIPES_FILE)
        data_reading.clean_ingredients(self.data)

        self.id = 0

        for x in self.data:
            if self.data[x][0] == self.recipe_name:
                self.id = x

        self.lbl_time_author = QLabel('Cook Time: ' + self.data[self.id][6] + '   |   Author: '
                                      + self.data[self.id][3], self)
        self.lbl_time_author.setFont(QFont('Georgia', 10))
        self.lbl_time_author.setStyleSheet('color: rgb(35, 87, 77)')
        self.lbl_time_author.setFixedSize(600, 40)
        self.lbl_time_author.move(50, 70)

        self.lbl_ingred = QLabel('Ingredients', self)
        self.lbl_ingred.setFont(QFont('Georgia', 12, QFont.Bold))
        self.lbl_ingred.setStyleSheet('color: rgb(211, 104, 80)')
        self.lbl_ingred.setFixedSize(600, 40)
        self.lbl_ingred.move(50, 120)

        self.lbl_direction = QLabel('Directions', self)
        self.lbl_direction.setFont(QFont('Georgia', 12, QFont.Bold))
        self.lbl_direction.setStyleSheet('color: rgb(211, 104, 80)')
        self.lbl_direction.setFixedSize(600, 40)
        self.lbl_direction.move(50, 380)

        self.ingredients_names = list(self.data[self.id][7])

        self.lst_ingredients = QListWidget()
        for i in range(len(self.ingredients_names)):
            self.lst_ingredients.insertItem(i, self.ingredients_names[i])
        self.lst_ingredients.setFont(QFont('Georgia', 10))
        self.lst_ingredients.setStyleSheet('color: rgb(35, 87, 77)')

        self.directions = list(self.data[self.id][8])
        self.lst_directions = QListWidget()
        for i in range(len(self.directions)):
            self.lst_directions.insertItem(i, str(i + 1) + '. ' + self.directions[i])
        self.lst_directions.setFont(QFont('Georgia', 10))
        self.lst_directions.setStyleSheet('color: rgb(35, 87, 77)')
        self.lst_directions.move(50, 200)

        self.title = "Look and Cook"
        self.left = 500
        self.top = 200
        self.width = 700
        self.height = 450
        self.init_window()
        self.center()
        self.setFixedSize(700, 700)
        self.setStyleSheet("background-color: rgb(240, 225, 204)")
        self.setWindowIcon(QIcon('visuals/L&C Icon.PNG'))

        self.line_edit = None
        self.user_input = None

    def init_window(self) -> None:
        """Open the fourth window on the user's screen with the provided dimensions.
        """
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(50, 100, 200, 30)
        self.lst_ingredients.setFixedSize(600, 200)
        vbox.addWidget(self.lst_ingredients)

        self.lst_directions.setFixedSize(600, 200)
        vbox.addWidget(self.lst_directions)
        self.setLayout(vbox)

        self.show()

    def center(self) -> None:  # Used top center the window on the desktop
        """Function to center third window on the provided desktop screen.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
