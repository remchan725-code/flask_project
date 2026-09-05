import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon,QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My first GUI !")
        self.setGeometry(500,500,500,500)  # Set the window size and position
        self.setWindowIcon(QIcon("cat.jpg"))

        label = QLabel("Hello", self)
        #label1 = QLabel("Xin chao",self)
        label.setFont(QFont("Arial", 20))
        #label1.setFont(QFont("Arial",200))
        #label1.adjustSize()
        label.setGeometry(50, 50, 200, 50)  
        label.setStyleSheet("color: blue;") 
        #label1.setGeometry(50,50,30,60)
        #label1.setStyleSheet("color: red;")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
  main()