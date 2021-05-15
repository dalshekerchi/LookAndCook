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
from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout, QWidget, QDesktopWidget, \
    QPushButton, QCompleter, QLineEdit, QListWidget, QMessageBox, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QFont
import data_reading
from recipes_dialogue import RecipesDialogue


class IngredientsDialogue(QDialog, QWidget):
    """Class representing second window of program which displays ingredients and allows users to
    input ingredients and specify a maximum time for recipes displayed.
    """

    def __init__(self) -> None:
        """Initialize an instance of the ingredients window
        """
        super().__init__()

        # Set up the screen background
        self.recipes_dialogue = None
        self.setStyleSheet("background-color: rgb(240, 225, 204)")
        self.setWindowIcon(QIcon('visuals/L_C_Icon.PNG'))

        # Initialized all widgets needed
        self.lbl_selected = QLabel("Your List", self)
        self.lbl_selected.setFont(QFont('Georgia', 12, QFont.Bold))
        self.lbl_selected.setStyleSheet('color: rgb(211, 104, 80)')
        self.lbl_selected.setFixedSize(200, 25)
        self.lbl_selected.move(80, 100)

        self.max_add_label = QLabel("(10 ingredients max.)", self)
        self.max_add_label.setFont(QFont('Georgia', 9))
        self.max_add_label.setStyleSheet('color: rgb(35, 87, 77)')
        self.max_add_label.move(57, 125)
        self.max_add_label.resize(200, 20)

        self.max_time_label = QLabel("Maximum cooking time in minutes (optional):", self)
        self.max_time_label.setFont(QFont('Georgia', 12, QFont.Bold))
        self.max_time_label.setStyleSheet('color: rgb(211, 104, 80)')
        self.max_time_label.setFixedSize(250, 80)
        self.max_time_label.setWordWrap(True)

        self.lbl_all = QLabel("All Ingredients", self)
        self.lbl_all.setFont(QFont('Georgia', 12, QFont.Bold))
        self.lbl_all.setStyleSheet('color: rgb(211, 104, 80)')
        self.lbl_all.setFixedSize(200, 25)
        self.lbl_all.move(375, 100)

        self.lbl_select = QLabel("Select your ingredients!", self)
        self.lbl_select.setFont(QFont('Georgia', 17, QFont.Bold))
        self.lbl_select.setStyleSheet('color: rgb(210, 146, 68)')
        self.lbl_select.setFixedSize(400, 40)
        self.lbl_select.move(180, 40)

        self.time_selected = QSpinBox(self)
        self.time_selected.setStyleSheet('color: rgb(35, 87, 77)')

        self.time_selected.setFont(QFont('Georgia', 10))
        self.time_selected.setRange(0, 50000)

        self.all_ingredients = QListWidget()
        self.all_ingredients.setFont(QFont('Georgia', 10))
        self.all_ingredients.setStyleSheet('color: rgb(35, 87, 77)')

        self.line_edit = None
        self.user_input = None

        # Sets up all the line edits
        self.ingredient1 = QLineEdit(self)
        self.ingredient1.setStyleSheet(
            'background-color: rgb(224, 182, 157); color: rgb(35, 87, 77)')
        self.ingredient1.setFont(QFont('Georgia', 10))
        self.ingredient2 = QLineEdit(self)
        self.ingredient2.setStyleSheet(
            'background-color: rgb(224, 182, 157); color: rgb(35, 87, 77)')
        self.ingredient2.setFont(QFont('Georgia', 10))
        self.ingredient3 = QLineEdit(self)
        self.ingredient3.setStyleSheet(
            'background-color: rgb(224, 182, 157); color: rgb(35, 87, 77)')
        self.ingredient3.setFont(QFont('Georgia', 10))
        self.ingredient4 = QLineEdit(self)
        self.ingredient4.setStyleSheet(
            'background-color: rgb(224, 182, 157); color: rgb(35, 87, 77)')
        self.ingredient4.setFont(QFont('Georgia', 10))
        self.ingredient5 = QLineEdit(self)
        self.ingredient5.setStyleSheet(
            'background-color: rgb(224, 182, 157); color: rgb(35, 87, 77)')
        self.ingredient5.setFont(QFont('Georgia', 10))
        self.ingredient6 = QLineEdit(self)
        self.ingredient6.setStyleSheet(
            'background-color: rgb(224, 182, 157); color: rgb(35, 87, 77)')
        self.ingredient6.setFont(QFont('Georgia', 10))
        self.ingredient7 = QLineEdit(self)
        self.ingredient7.setStyleSheet(
            'background-color: rgb(224, 182, 157); color: rgb(35, 87, 77)')
        self.ingredient7.setFont(QFont('Georgia', 10))
        self.ingredient8 = QLineEdit(self)
        self.ingredient8.setStyleSheet(
            'background-color: rgb(224, 182, 157); color: rgb(35, 87, 77)')
        self.ingredient8.setFont(QFont('Georgia', 10))
        self.ingredient9 = QLineEdit(self)
        self.ingredient9.setStyleSheet(
            'background-color: rgb(224, 182, 157); color: rgb(35, 87, 77)')
        self.ingredient9.setFont(QFont('Georgia', 10))
        self.ingredient10 = QLineEdit(self)
        self.ingredient10.setStyleSheet(
            'background-color: rgb(224, 182, 157); color: rgb(35, 87, 77)')
        self.ingredient10.setFont(QFont('Georgia', 10))

        # Gets all the ingredients from the data
        self.ingredient = [self.ingredient1, self.ingredient2, self.ingredient3, self.ingredient4,
                           self.ingredient5, self.ingredient6, self.ingredient7,
                           self.ingredient8, self.ingredient9, self.ingredient10]
        data = data_reading.read_recipes(data_reading.RECIPES_FILE)
        data_reading.clean_ingredients(data)
        self.clean = sorted(list(data_reading.get_ingredients(data)))
        for i in range(len(self.clean)):
            self.all_ingredients.insertItem(i, self.clean[i])

        # Sets up the screen with all the needed elements
        self.title = "Look and Cook - Ingredients Selection"
        self.left = 500
        self.top = 200
        self.width = 700
        self.height = 700
        self.init_window()
        self.center()
        self.setFixedSize(700, 700)

    def init_window(self) -> None:
        """Open the second window on the user's screen with the provided dimensions.
        """
        # Sets up screen
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

        # Moves the labels to the right position
        self.max_time_label.move(250, self.height - 230)
        self.time_selected.move(550, self.height - 200)

        # Creates an autocomplete system to use when typing the ingredients
        completer = QCompleter(sorted(self.clean))
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        # Places all the line edits on the window
        self.ingredient1.setCompleter(completer)
        self.ingredient1.move(50, 160)
        self.ingredient1.setFixedSize(160, 30)

        height = 200
        for x in self.ingredient[1:]:
            x.setCompleter(completer)
            x.move(50, height)
            x.setFixedSize(160, 30)
            x.setDisabled(True)
            height += 40

        # Places list in the middle on the window
        vbox = QVBoxLayout()
        vbox.setContentsMargins(250, 0, 120, 120)
        self.all_ingredients.setFixedSize(400, 300)
        vbox.addWidget(self.all_ingredients)
        # self.all_ingredients.itemDoubleClicked.connect(self.add_ingredient)
        self.setLayout(vbox)

        # Creates an add_item item button
        add_item = QPushButton("Add", self)
        add_item.setGeometry((self.width // 2) - 50, self.height // 2 + 200, 70, 70)
        add_item.move(50, self.height - 120)
        add_item.setFont(QFont('Georgia', 8, QFont.Bold))
        add_item.setStyleSheet('border-radius: 35; background-color: rgb(211, 104, 80); '
                               'color: rgb(240, 225, 204)')
        add_item.clicked.connect(self.add_item)

        # Creates an remove_item item button
        remove_item = QPushButton("Remove", self)
        remove_item.setGeometry((self.width // 2) - 50, self.height // 2 + 200, 70, 70)
        remove_item.move(140, self.height - 120)
        remove_item.setFont(QFont('Georgia', 8, QFont.Bold))
        remove_item.setStyleSheet('border-radius: 35; background-color: rgb(211, 104, 80); '
                                  'color: rgb(240, 225, 204)')
        remove_item.clicked.connect(self.remove_item)

        # Creates an clear list item button
        clear_list = QPushButton("Clear List", self)
        clear_list.setGeometry((self.width // 2) - 50, self.height // 2 + 200, 190, 70)
        clear_list.move(250, self.height - 120)
        clear_list.setFont(QFont('Georgia', 12, weight=QtGui.QFont.Bold))
        clear_list.setStyleSheet('border-radius: 35; background-color: rgb(211, 104, 80); '
                                 'color: rgb(240, 225, 204)')
        clear_list.clicked.connect(self.clear_list)

        # Creates a submit button
        submit = QPushButton("Find Recipes", self)
        submit.setGeometry((self.width // 2) - 50, self.height // 2 + 200, 190, 70)
        submit.move(460, self.height - 120)
        submit.setFont(QFont('Georgia', 12, weight=QtGui.QFont.Bold))
        submit.setStyleSheet('border-radius: 35; background-color: rgb(210, 146, 68); '
                             'color: rgb(240, 225, 204)')
        submit.clicked.connect(self.submit)

        # Displays everything on the window
        self.show()

    def center(self) -> None:
        """Function to center second window on the provided desktop screen.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def add_item(self) -> None:
        """Enables search box for user to input a new ingredient."""
        for x in range(len(self.ingredient) - 1, 0, -1):
            if self.ingredient[x - 1].isEnabled():
                self.ingredient[x].setDisabled(False)

    def remove_item(self) -> None:
        """Removes the last ingredient of the list."""
        for x in self.ingredient[::-1][:-1]:
            if x.isEnabled():
                x.setDisabled(True)
                x.clear()
                return

    def clear_list(self) -> None:
        """Clears all ingredients in user's list."""
        for x in self.ingredient:
            x.clear()
            if x != self.ingredient1:
                x.setDisabled(True)
        self.time_selected.clear()

    # def add_ingredient(self) -> None:
    #     """Add the clicked ingredient to the ingredients list."""
    #     print(item)

    def submit(self) -> None:
        """Create button to submit user input and proceed to the third page, which displays the
       recipes.

       If there is an ingredient listed twice in the input, raise an error pop up that says
       "Ingredient [duplicated ingredient] appears more than once" or "Ingredients [duplicated
       ingredients] appear more than once" if there are multiple duplicated ingredients.

       If there are remaining unfilled ingredient boxes, raise an error pop up that says
       "Did not fill all the needed information".

       If the user has inputted an invalid ingredient that does not appear in the list of
       ingredients at the center, raise an error pop up that says "The ingredient [invalid
       ingredient] is invalid" or "The ingredients [invalid ingredients] are invalid" if there
       are more than 1 invalid ingredients.
       """
        ingredients_set = set()
        duplicates = ''
        count = 0
        for x in self.ingredient:
            if x.isEnabled() and x.text() in ingredients_set:
                duplicates += x.text()
                count += 1
            else:
                ingredients_set.add(x.text())

        if len(duplicates) != 0:  # This occurs when the user inputs the same ingredient twice
            contains_duplicates = QMessageBox()
            contains_duplicates.setWindowTitle("Error! - Duplicates")
            contains_duplicates.setWindowIcon(QIcon('visuals/L&C Icon.PNG'))
            if count == 1:  # Only one ingredient appears more than once
                contains_duplicates.setText(
                    f'Sorry, the ingredient {duplicates} appears more than once.')
            else:  # Muliple ingredients
                contains_duplicates.setText(
                    f'Sorry, the ingredients {duplicates} appear more than once.')
            contains_duplicates.setIcon(QMessageBox.Critical)
            x = contains_duplicates.exec_()

        elif any([x.isEnabled() and x.text() == '' for x in
                  self.ingredient]):  # Checks if there are any empty textboxes
            warning = QMessageBox()
            warning.setWindowTitle("Error!")
            warning.setWindowIcon(QIcon('visuals/L&C Icon.PNG'))
            warning.setText('Sorry, you did not fill all the necessary information. Please check '
                            'that your ingredients list is correct and there are no empty spots.')
            warning.setIcon(QMessageBox.Critical)
            x = warning.exec_()

        elif not all([x.text() in self.clean for x in self.ingredient if
                      x.isEnabled()]):  # Checks if there are any  items that are not valid
            invalid_ingredient = ''
            count = 0
            for x in self.ingredient:
                if x.text() not in self.clean and x.isEnabled():
                    invalid_ingredient += x.text() + ', '

                    count += 1
            invalid_ingredient = invalid_ingredient.strip(', ')

            invalid = QMessageBox()
            invalid.setWindowTitle("Error! - Invalid Ingredient")
            invalid.setWindowIcon(QIcon('visuals/L&C Icon.PNG'))

            if count == 1:  # One ingredient
                invalid.setText(f"Sorry, the ingredient '{invalid_ingredient}' is invalid.")
            else:  # More than one
                invalid.setText(f"Sorry, the ingredients '{invalid_ingredient}' are invalid.")
            invalid.setIcon(QMessageBox.Critical)
            x = invalid.exec_()

        else:  # If everything is correct
            self.hide()
            user_input = [x.text() for x in self.ingredient if x.isEnabled()]

            # Goes to the next dialogue
            self.recipes_dialogue = \
                RecipesDialogue(user_input, int(self.time_selected.text()), self)
            self.recipes_dialogue.show()
