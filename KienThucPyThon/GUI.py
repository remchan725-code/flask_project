import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My first GUI !")
        self.setGeometry(0, 0, 0, 0)  # Set the window size and position
        self.setWindowIcon(QIcon("cat.jpg"))

        label = QLabel("Hello", self)
        label.setFont(QFont("Arial", 20))
        label.setGeometry(50, 50, 200, 50)  
        label.setStyleSheet("color: blue;") 

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
  main()