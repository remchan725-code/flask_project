import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QPushButton,QCheckBox
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QSize,Qt 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700,700,500,500)
        self.checkbox = QCheckBox("Do you love me ?",self)
        self.initUI()
    def initUI(self):
        self.checkbox.setGeometry(130,0,500,100)
        self.checkbox.setStyleSheet("Font-size: 30px;Font-Family: Arial;")
        self.checkbox.setChecked(False)
        self.checkbox.stateChanged.connect(self.checkbox_changed)
        # self.button = QPushButton("Click me!",self)
        # self.button.adjustSize()
        # self.button.setGeometry(400,0,1000,1000)
        # self.button.setStyleSheet("font-size: 50px;")
        # self.button.clicked.connect(self.on_click)
    def checkbox_changed(self,state):
        if state == Qt.Checked:
            print("Yes")
        else:
            print(":<")

    # def on_click(self):
    #     print("Button Clicked")
        # self.button.setIcon(QIcon("cat.jpg"))
        # self.button.setText("Boo")
        # self.button.setIconSize(QSize(1000,1000))
        # self.button.setDisabled(True)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
  main()        