import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QLineEdit
from PyQt6.QtGui import QFont
from game import Game

class GameLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Game Launcher')
        self.setGeometry(100, 100, 300, 300)

        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create start game tab
        self.start_game_tab = QWidget()
        self.tabs.addTab(self.start_game_tab, "Start Game")
        self.init_start_game_tab()

        # Create options tab
        self.options_tab = QWidget()
        self.tabs.addTab(self.options_tab, "Options")
        self.init_options_tab()

    def init_start_game_tab(self):
        layout = QVBoxLayout()

        # Add large label
        game_label = QLabel('GAME', self)
        font = QFont()
        font.setPointSize(30)  # Set font size to 30
        game_label.setFont(font)

        # Center the label horizontally
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(game_label)
        hbox.addStretch(1)

        layout.addLayout(hbox)

        # Add start button
        start_button = QPushButton('Start Game', self)
        start_button.setFixedSize(300, 150)  # Set button size to 300x150
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button)

        self.start_game_tab.setLayout(layout)

    def init_options_tab(self):
        layout = QVBoxLayout()

        # Hide launcher checkbox
        self.hide_launcher_checkbox = QCheckBox('Hide launcher when running game')
        layout.addWidget(self.hide_launcher_checkbox)

        # Width input
        self.width_input = QLineEdit(self)
        self.width_input.setPlaceholderText("Width")
        layout.addWidget(self.width_input)

        # Height input
        self.height_input = QLineEdit(self)
        self.height_input.setPlaceholderText("Height")
        layout.addWidget(self.height_input)

        self.options_tab.setLayout(layout)

    def start_game(self):
        if self.hide_launcher_checkbox.isChecked():
            self.hide()

        width = int(self.width_input.text()) if self.width_input.text() else 1366
        height = int(self.height_input.text()) if self.height_input.text() else 768

        game_instance = Game(width, height)
        game_instance.run()

        if self.hide_launcher_checkbox.isChecked():
            self.show()

def main():
    app = QApplication(sys.argv)
    launcher = GameLauncher()
    launcher.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()