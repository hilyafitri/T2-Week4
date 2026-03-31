# Nama  : Hilya Fitri
# NIM   : F1D02310009
# Kelas : C
# Tugas : T2 Week 4 - Kalkulator Event Handling

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QComboBox,
    QMessageBox, QHBoxLayout
)
from PySide6.QtCore import Qt


class Kalkulator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kalkulator")
        self.setFixedWidth(320)

        self.setStyleSheet("""
            QWidget {
                background-color: #f5f6f7;
                font-family: Segoe UI;
                font-size: 13px;
            }

            QLabel {
                color: #333;
            }

            QLineEdit {
                padding: 8px;
                border: 2px solid #dcdfe6;
                border-radius: 6px;
                background-color: white;
                color: black;
            }

            QLineEdit:focus {
                border: 2px solid #4a90e2;
            }

            QComboBox {
                padding: 8px;
                border: 2px solid #dcdfe6;
                border-radius: 6px;
                background-color: white;
                color: black;
            }

            QPushButton {
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }

            QPushButton#btnHitung {
                background-color: #dcdfe6;
                color: #888;
            }

            QPushButton#btnHitung:enabled {
                background-color: #4a90e2;
                color: white;
            }

            QPushButton#btnHitung:enabled:hover {
                background-color: #357abd;
            }
            QPushButton#btnClear {
                background-color: #e74c3c;
                color: white;
            }

            QPushButton#btnClear:hover {
                background-color: #c0392b;
            }
                           
            QMessageBox {
                background-color: white;
            }

            QMessageBox QLabel {
                color: black;
                font-size: 13px;
            }

            QMessageBox QPushButton {
                background-color: #dcdfe6;
                color: black;
                padding: 6px 12px;
                border-radius: 4px;
                min-width: 60px;
            }

            QMessageBox QPushButton:hover {
                background-color: #c0c4cc;
            }
        """)
        
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Masukkan angka pertama")

        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Masukkan angka kedua")

        self.operasi = QComboBox()
        self.operasi.addItems(["+ Tambah", "- Kurang", "× Kali", "÷ Bagi"])

        self.btn_hitung = QPushButton("Hitung (Enter)")
        self.btn_hitung.setObjectName("btnHitung")
        self.btn_hitung.setEnabled(False)

        self.btn_clear = QPushButton("Clear (Esc)")
        self.btn_clear.setObjectName("btnClear")

        self.label_hasil = QLabel("Hasil: -")
        self.label_hasil.setStyleSheet("margin-top: 10px;")

        self.label_error = QLabel("")
        self.label_error.setStyleSheet("color: #e74c3c; font-size: 12px;")

        layout = QVBoxLayout()
        layout.setSpacing(10)

        layout.addWidget(QLabel("Angka Pertama"))
        layout.addWidget(self.input1)

        layout.addWidget(QLabel("Operasi"))
        layout.addWidget(self.operasi)

        layout.addWidget(QLabel("Angka Kedua"))
        layout.addWidget(self.input2)

        layout.addWidget(self.label_error)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_hitung)
        btn_layout.addWidget(self.btn_clear)

        layout.addLayout(btn_layout)
        layout.addWidget(self.label_hasil)

        self.setLayout(layout)

        # ===== EVENT HANDLING =====
        self.input1.textChanged.connect(self.validasi_input)
        self.input2.textChanged.connect(self.validasi_input)

        self.btn_hitung.clicked.connect(self.hitung)
        self.btn_clear.clicked.connect(self.clear_form)

    def validasi_input(self):
        valid1 = self.is_angka(self.input1.text())
        valid2 = self.is_angka(self.input2.text())

        self.set_border(self.input1, valid1)
        self.set_border(self.input2, valid2)

        if valid1 and valid2:
            self.label_error.setText("")
            self.btn_hitung.setEnabled(True)
        else:
            self.label_error.setText("⚠ Input harus berupa angka!")
            self.btn_hitung.setEnabled(False)

    def is_angka(self, text):
        try:
            float(text)
            return True
        except:
            return False

    def set_border(self, widget, valid):
        if valid or widget.text() == "":
            widget.setStyleSheet("""
                border: 2px solid #dcdfe6;
                border-radius: 6px;
                color: black;
                background-color: white;
            """)
        else:
            widget.setStyleSheet("""
                border: 2px solid #e74c3c;
                border-radius: 6px;
                color: black;
                background-color: white;
            """)

    def hitung(self):
        a = float(self.input1.text())
        b = float(self.input2.text())
        op = self.operasi.currentText()

        try:
            if "+" in op:
                hasil = a + b
            elif "-" in op:
                hasil = a - b
            elif "×" in op:
                hasil = a * b
            elif "÷" in op:
                if b == 0:
                    raise ZeroDivisionError
                hasil = a / b

            self.label_hasil.setText(f"Hasil: {hasil}")

        except ZeroDivisionError:
            self.label_error.setText("Tidak bisa dibagi nol!")

    def clear_form(self):
        self.input1.clear()
        self.input2.clear()
        self.label_hasil.setText("Hasil: -")
        self.label_error.setText("")
        self.btn_hitung.setEnabled(False)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.btn_hitung.isEnabled():
                self.hitung()
        elif event.key() == Qt.Key_Escape:
            self.clear_form()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Konfirmasi",
            "Yakin ingin keluar?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Kalkulator()
    window.show()
    sys.exit(app.exec())