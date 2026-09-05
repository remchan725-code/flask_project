import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QWidget,QHBoxLayout,QVBoxLayout,QGridLayout
from PyQt5.QtGui import QIcon,QFont,QPixmap
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700,300,500,500)
        self.initUI()
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setWindowIcon(QIcon("cat.jpg"))

        label1 = QLabel("#1",self)
        label2 = QLabel("#2",self)
        label3 = QLabel("#3",self)
        label4 = QLabel("#4",self)
        label5 = QLabel("#5",self)

        label1.setStyleSheet("background-color: purple")
        label2.setStyleSheet("background-color: green")
        label3.setStyleSheet("background-color: red")
        label4.setStyleSheet("background-color: blue")
        label5.setStyleSheet("background-color: yellow")


        #vbox = QVBoxLayout() #hbox = horical
        #hbox = QHBoxLayout()
        gbox = QGridLayout()

        gbox.addWidget(label1,0,0)
        gbox.addWidget(label2,0,2)
        gbox.addWidget(label3,1,3)
        gbox.addWidget(label4,1,7)
        gbox.addWidget(label5,2,4)


        #vbox.addWidget(label1)
        #vbox.addWidget(label2)
        #vbox.addWidget(label3)
        #vbox.addWidget(label4)
        #vbox.addWidget(label5)

        #hbox.addWidget(label1)
        #hbox.addWidget(label2)
        #hbox.addWidget(label3)
        #hbox.addWidget(label4)
        #hbox.addWidget(label5)

        #central_widget.setLayout(vbox)
        central_widget.setLayout(gbox)
        #central_widget.setLayout(hbox)

        #label = QLabel(self)
        #label.setGeometry(0,0,500,500)
        #pixmap = QPixmap("cat.jpg")
        #label.setPixmap(pixmap)
        #label.adjustSize()
        #label.setScaledContents(True)

        #label.setGeometry(self.width() - label.width()
        #,self.height() - label.height()
        #,label.width(),label.height())

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
  main()