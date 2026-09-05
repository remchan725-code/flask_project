import sys
from PyQt5.QtWidgets import QApplication,QLabel,QPushButton,QVBoxLayout,QHBoxLayout,QWidget
from PyQt5.QtCore import QTimer,QTime,Qt

class StopWatch(QWidget):
    def __init__(self):
        super().__init__()
        self.time = QTime(0,0,0,0)
        self.time_label = QLabel("00:00:00:00",self)
        self.start_button = QPushButton("Start",self)
        self.stop_button = QPushButton("Stop",self)
        self.reset_button = QPushButton("Reset",self)
        self.timer = QTimer(self)
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Stop Watch")
        vbox.addWidget(self.time_label)
        
        self.setLayout(vbox)
        self.time_label.setAlignment(Qt.AlignCenter)
        hbox = QHBoxLayout()

        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        hbox.addWidget(self.reset_button)

        self.setStyleSheet("""
            QPushButton,QLabel{
                padding: 20px;
                font-weight : bold;
            }
            QPushButton{
            
                font-size : 50px;
            }
            QLabel{
                font-size : 50px;
                background-color : rgba(23, 135, 227,1);
                border-radius : 20px;
            }
        
        """)
        self.start_button.clicked.connect(self.start)
        self.start_button.clicked.connect(self.start)
        self.start_button.clicked.connect(self.start)
        self.timer.timeout.connect(self.update_display)

    def start(self):
        self.timer.start(10)
    def stop(self):
        self.timer.stop(10)
    def reset(self):
        pass
if __name__ == "__main":
    app = QApplication(sys.argv)
    StopWatches = StopWatch()
    StopWatches.show()
    sys.exit(app.exec_()) 