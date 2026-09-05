import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QPushButton,QCheckBox,QRadioButton,QButtonGroup
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QSize,Qt 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700,700,500,500)
        self.button_group1 = QButtonGroup(self)
        self.button_group2 = QButtonGroup(self)
        self.radio1 = QRadioButton("Bun bo Hue",self)
        self.radio2 = QRadioButton("Com tam",self)
        self.radio3 = QRadioButton("Bun rieu",self)
        self.radio4 = QRadioButton("Pho bo",self)
        self.initUI()
    
    def initUI(self):
        self.radio1.setGeometry(0,0,200,100)
        self.radio2.setGeometry(0,100,100,100)
        self.radio3.setGeometry(0,200,100,100)
        self.radio4.setGeometry(0,300,100,100)
        self.setStyleSheet("font-size: 15px;" "font-family : Arial;" "padding : 10px")

        self.button_group1.addButton(self.radio1)
        self.button_group1.addButton(self.radio2)
        self.button_group2.addButton(self.radio3)
        self.button_group2.addButton(self.radio4)

        self.radio1.toggled.connect(self.radio_button_changed)
        self.radio2.toggled.connect(self.radio_button_changed)
        self.radio3.toggled.connect(self.radio_button_changed)
        self.radio4.toggled.connect(self.radio_button_changed)
    
    def radio_button_changed(self):
       radio_button = self.sender()
       if radio_button.isChecked():
        print(f"Ban chon {radio_button.text()}!")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
  main()        