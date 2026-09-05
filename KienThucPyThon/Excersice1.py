import sys
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QPushButton,QHBoxLayout,QMainWindow
from PyQt5.QtGui import QIcon,QFont

# class LoginWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Form dang nhap")
#         self.setGeometry(100,100,300,200)
#         self.setWindowIcon(QIcon("cat.jpg"))

#         self.user_input = QLineEdit(self)
#         self.user_input.setPlaceholderText("Nhap username".lower())
        
#         self.pass_input = QLineEdit(self)
#         self.pass_input.setPlaceholderText("Nhap password")
#         self.pass_input.setEchoMode(QLineEdit.Password)

#         self.btn_login = QPushButton("Dang nhap",self)
#         self.lbl_result = QLabel("",self)

#         layout = QVBoxLayout()
#         layout.addWidget(self.user_input)
#         layout.addWidget(self.pass_input)
#         layout.addWidget(self.btn_login)
#         layout.addWidget(self.lbl_result)
#         self.setLayout(layout)

#         self.btn_login.clicked.connect(self.check_login)
#     def check_login(self):
#         username = self.user_input.text()
#         password = self.pass_input.text()
#         text = self.user_input.text()
        

#         if username == "admin" and password == "123456":
#             self.lbl_result.setText("Dang nhap thanh cong!")
#             self.lbl_result.setStyleSheet("color: green;")
#             self.lbl_result.setText(f"Xin chao {text} !")
#             self.lbl_result.setStyleSheet("color: green;")
#         else:
#             self.lbl_result.setText("Sai tài khoản hoặc mật khẩu!")
#             self.lbl_result.setStyleSheet("color: red;")
#     def submit(self):
#         text = self.user_input.text()
#         print(f"Xin chao {text} !")
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button1 = QPushButton("#1")
        self.button2 = QPushButton("#2")
        self.button3 = QPushButton("#3")
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.button1)
        hbox.addWidget(self.button2)
        hbox.addWidget(self.button3)

        central_widget.setLayout(hbox)

        self.button1.setObjectName("Button1")
        self.button2.setObjectName("Button2")
        self.button3.setObjectName("Button3")


        # Đưa đoạn CSS vào bên trong hàm initUI
        self.setStyleSheet("""
            QPushButton {
                font-size: 40px;
                font-family: Arial;
                padding: 20px 40px;
                margin: 30px;
                border: 3px solid;
                border-radius : 15px;
            }
            QPushButton#Button1:hover{
                background-image: url("cat.jpg");
                background-repeat: no-repeat;
                background-position: center;
                color : transparent;
                border-image: url("cat.jpg") 0 0 0 0 stretch stretch;
                border-width: 0px;
            }

            }
            QPushButton#Button2:hover{
               background-image: url("cat2.jpg");
                background-repeat: no-repeat;
                background-position: center;
                color : transparent;
                border-image: url("cat2.jpg") 0 0 0 0 stretch stretch;
                border-width: 0px;
            }

            QPushButton#Button3:hover{
                background-color: blue;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())