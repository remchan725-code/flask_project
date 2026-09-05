import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QLineEdit, QComboBox, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QGroupBox,QRadioButton)
from PyQt5.QtCore import Qt
class StudentCardApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tao the sinh vien")
        self.setGeometry(400,200,400,350)
        self.initUI()
    def initUI(self):
        main_layout = QVBoxLayout()
        self.lbl_title = QLabel("nhap thong tin sinh vien".upper())
        self.lbl_title.setAlignment(Qt.AlignCenter)

        self.rad_male = QRadioButton("Nam")
        self.rad_female = QRadioButton("Nữ")
        self.rad_male.setChecked(True) 
     
        gender_layout = QHBoxLayout()
        gender_layout.addWidget(self.rad_male)
        gender_layout.addWidget(self.rad_female)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Nhap ho va ten")
        self.combo_major = QComboBox()

        self.combo_major.addItems(["IT","Kinh te","Ngon ngu Anh"])

        self.btn_create = QPushButton("Tao the")
        self.btn_reset = QPushButton("Xoa")
        button_layout = QHBoxLayout()

        self.lbl_result = QLabel("Chua co thong tin")
        self.lbl_result.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout()

        main_layout.addWidget(self.lbl_title)

        main_layout.addWidget(QLabel("Họ và tên:"))
        main_layout.addWidget(self.input_name)

        main_layout.addWidget(QLabel("Giới tính:"))
        main_layout.addLayout(gender_layout)

        main_layout.addWidget(QLabel("Chuyên ngành:"))
        main_layout.addWidget(self.combo_major)

        main_layout.addLayout(button_layout)

        main_layout.addWidget(self.btn_create)
        main_layout.addWidget(self.btn_reset)
        
        main_layout.addWidget(QLabel("--- Kết quả ---"))
        main_layout.addWidget(self.lbl_result)

        self.setLayout(main_layout)

        self.btn_create.clicked.connect(self.generate_card)
        self.btn_reset.clicked.connect(self.reset_form)

        self.setup_styles()
        
        self.btn_create.clicked.connect(self.generate_card)
        
        self.setup_styles()

    def generate_card(self):
        name = self.input_name.text().strip().upper()
        major = self.combo_major.currentText()

        if name:
            text = f"🪪 THẺ SINH VIÊN\nHọ tên: {name}\nNgành: {major}"
            self.lbl_result.setText(text)
            # Đổi style khung kết quả khi có dữ liệu
            self.lbl_result.setStyleSheet("""
                QLabel {
                    background-color: #e8f8f5;
                    color: #117a65;
                    border: 2px dashed #117a65;
                    border-radius: 8px;
                    padding: 15px;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)
        else:
            self.lbl_result.setText("⚠️ Vui lòng nhập họ tên!")
            self.lbl_result.setStyleSheet("color: red; font-weight: bold;")

    def setup_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c5980;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentCardApp()
    window.show()
    sys.exit(app.exec_())