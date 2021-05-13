"""CSC111 Winter 2021 Project Phase 2: Final Submission, Recipes Results Program Window (3)

Description
===============================
This Python module contains the visualization of the recipes search results program window.

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
    QPushButton, QCompleter, QLineEdit, QListWidget, QMessageBox, QComboBox, QApplication, \
    QHBoxLayout
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont, QIcon
import data_reading
import sort_srch_rslts
import data_type
from display_recipe_dialogue import IndividualRecipe


class RecipesDialogue(QDialog, QWidget):
    """Class representing third window of program which displays the search results of recipes given
    the user's input ingredients and specification a maximum time for recipes displayed.
        """
    def __init__(self, user_ingredients: list, time: int, previous_window):
        """Class representing third window of program which displays the recipes filtered by the
        ingredients inputted by the user.
        """
        super().__init__()
        self.display_recipe_dialogue = None
        self.previous_window = previous_window

        # Items imported from ingredients_dialogue
        self.user_ingredients = user_ingredients
        self.time = time

        # Added All the widgets needed
        self.lbl_title = QLabel("We found some recipes for you!", self)
        self.lbl_title.setFont(QFont('Georgia', 17, QFont.Bold))
        self.lbl_title.setStyleSheet('color: rgb(210, 146, 68)')
        self.lbl_title.setFixedSize(475, 40)
        self.lbl_title.move(125, 20)

        self.lbl_filter = QLabel("Filter by:", self)
        self.lbl_filter.setFont(QFont('Georgia', 12, QFont.Bold))
        self.lbl_filter.setStyleSheet('color: rgb(211, 104, 80)')
        self.lbl_filter.setFixedSize(100, 25)
        self.lbl_filter.move(150, 80)

        self.lbl_recipe = QLabel("Enter a recipe name", self)
        self.lbl_recipe.setFont(QFont('Georgia', 12, QFont.Bold))
        self.lbl_recipe.setStyleSheet('color: rgb(211, 104, 80)')
        self.lbl_recipe.setFixedSize(205, 25)

        # Creates dependent combo-boxes for time and ingredient sort.
        self.combo_type = QComboBox(self)
        self.combo_type.addItem('Ingredients', [])  # index 0
        self.combo_type.addItem('Time', ['Ascending', 'Descending'])    # index 1
        self.combo_type.move(250, 80)
        self.combo_type.resize(145, 30)
        self.combo_type.setFont(QFont('Georgia', 12))
        self.combo_type.setStyleSheet('color: rgb(35, 87, 77)')

        self.combo_option = QComboBox(self)
        self.combo_option.move(405, 80)
        self.combo_option.resize(145, 30)
        self.combo_option.setFont(QFont('Georgia', 12))
        self.combo_option.setStyleSheet('color: rgb(35, 87, 77)')

        self.combo_type.currentIndexChanged.connect(self.update_combo_option)
        self.update_combo_option(self.combo_type.currentIndex())

        # Getting all the recipes needed
        self.data = data_reading.read_recipes(data_reading.RECIPES_FILE)
        data_reading.clean_ingredients(self.data)
        self.graph = data_type.load_graph("data/clean_recipes.csv")
        ingrdnt_sorted_recipes = sort_srch_rslts.ingrdnt_sort(self.data, self.user_ingredients,
                                                              self.graph)

        # varied options for viewing recipes
        self.sorted_recipes_ings = sort_srch_rslts.time_bound(ingrdnt_sorted_recipes, self.time)
        self.sorted_recipes_time_asc = sort_srch_rslts.time_sort(self.sorted_recipes_ings, False)
        self.sorted_recipes_time_des = sort_srch_rslts.time_sort(self.sorted_recipes_ings, True)

        # Displays all the sorted recipes in a list
        self.recipes = QListWidget()
        self.recipe_names = [x[1][0] for x in self.sorted_recipes_ings]
        for i in range(len(self.recipe_names)):
            self.recipes.insertItem(i, self.recipe_names[i])
        self.recipes.setFont(QFont('Georgia', 10))
        self.recipes.setStyleSheet('color: rgb(35, 87, 77)')

        self.recipe_of_choice = QLineEdit(self)

        # Sets up the screen with all the needed elements
        self.title = "Look and Cook - Recipe Results"
        self.left = 500
        self.top = 200
        self.width = 700
        self.height = 700
        self.init_window()
        self.center()
        self.setFixedSize(700, 700)
        self.setStyleSheet("background-color: rgb(240, 225, 204)")
        self.setWindowIcon(QIcon('visuals/L&C Icon.PNG'))

    def init_window(self) -> None:
        """Open the third window on the user's screen with the provided dimensions.
        """
        # Sets up screen
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

        # Creates an autocomplete system to use when typing the ingredients
        completer = QCompleter(self.recipe_names)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.lbl_recipe.move(248, self.height - 190)

        self.recipe_of_choice.setCompleter(completer)
        self.recipe_of_choice.move(250, self.height - 160)
        self.recipe_of_choice.setFixedSize(200, 30)
        self.recipe_of_choice.setFont(QFont('Georgia', 12))
        self.recipe_of_choice.setStyleSheet('color: rgb(35, 87, 77)')

        # Creates a button for when the user has made their choice
        choose = QPushButton("View Recipe!", self)
        choose.setGeometry((self.width // 2) - 50, self.height // 2 + 200, 200, 70)
        choose.move(250, self.height - 110)
        choose.setFont(QFont('Georgia', 12, QFont.Bold))
        choose.setStyleSheet('border-radius: 35; background-color: rgb(210, 146, 68); '
                             'color: rgb(240, 225, 204)')
        choose.clicked.connect(self.chosen)

        # Creates a back button
        back = QPushButton("Back", self)
        back.setGeometry((self.width // 2) - 50, self.height // 2 + 200, 70, 70)
        back.move(580, self.height - 110)
        back.setFont(QFont('Georgia', 10, QFont.Bold))
        back.setStyleSheet("border-radius: 35; background-color: rgb(210, 146, 68); "
                           "color: rgb(240, 225, 204)")
        back.clicked.connect(self.go_back)

        # Centers the list
        vbox = QVBoxLayout()
        vbox.setContentsMargins(150, 100, 100, 170)
        self.recipes.setFixedSize(400, 375)
        vbox.addWidget(self.recipes)
        self.setLayout(vbox)

        self.combo_type.activated.connect(self.reorder_recipes_combo_type)
        self.reorder_recipes_combo_type(self.combo_type.currentIndex())

        self.combo_option.activated.connect(self.reorder_recipes_combo_option)
        self.reorder_recipes_combo_option(self.combo_option.currentIndex())

        # Displays everything on the window
        self.show()

    def center(self) -> None:
        """Function to center third window on the provided desktop screen.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def chosen(self) -> None:
        """Select the chosen recipe and display it on the fourth page.

        If the input recipe is not a valid recipe, raise an error and raise a pop up that
        says 'the inputted information is incorrect.'
        """
        # Does not allow user to pass through if they did not pick a valid choice or is empty
        if self.recipe_of_choice.text() == '' or self.recipe_of_choice.text() not in \
                self.recipe_names:
            warning = QMessageBox()
            warning.setWindowTitle("Error!")
            warning.setWindowIcon(QIcon('visuals/L&C Icon.PNG'))
            warning.setText('Please check that your input is a valid recipe name.')
            warning.setIcon(QMessageBox.Critical)
            warning.exec_()
        else:
            self.hide()
            self.display_recipe_dialogue = IndividualRecipe(self.recipe_of_choice.text())
            self.display_recipe_dialogue.show()

    def update_combo_option(self, index) -> None:
        """Update the options in the dependent combo-box."""
        self.combo_option.clear()
        options = self.combo_type.itemData(index)

        if index == 0:
            self.combo_option.setDisabled(True)
        else:
            self.combo_option.setDisabled(False)

        if options:
            self.combo_option.addItems(options)

    def reorder_recipes_combo_type(self, index) -> None:
        """Reorder the recipes based on the option selected in the combo_type combo-box."""
        if index == 0:  # ingredients
            self.recipes.clear()
            self.recipe_names = [x[1][0] for x in self.sorted_recipes_ings]
            for i in range(len(self.recipe_names)):
                self.recipes.insertItem(i, self.recipe_names[i])

        else:  # time
            self.recipes.clear()
            self.recipe_names = [x[1][0] for x in self.sorted_recipes_time_asc]
            for i in range(len(self.recipe_names)):
                self.recipes.insertItem(i, self.recipe_names[i])

    def reorder_recipes_combo_option(self, index) -> None:
        """Reorder the recipes based on the option selected in the combo_option combo-box."""
        if index == 0:  # ascending
            self.recipes.clear()
            self.recipe_names = [x[1][0] for x in self.sorted_recipes_time_asc]
            for i in range(len(self.recipe_names)):
                self.recipes.insertItem(i, self.recipe_names[i])

        else:   # descending
            self.recipes.clear()
            self.recipe_names = [x[1][0] for x in self.sorted_recipes_time_des]
            for i in range(len(self.recipe_names)):
                self.recipes.insertItem(i, self.recipe_names[i])

    def go_back(self) -> None:
        """Take the user to the previous window.
        """
        self.hide()
        self.previous_window.show()
