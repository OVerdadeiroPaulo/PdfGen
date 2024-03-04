# menu.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QProgressBar
from pdf import PDFGenerator
from PyQt5.QtCore import Qt, QThread
import time


class PDFThread(QThread):
    def __init__(self, folderpath):
        super().__init__()
        self.folderpath = folderpath
        self.pdf_generator = PDFGenerator()

    def run(self):
        self.pdf_generator.create_pdf(self.folderpath)


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image to Pdf converter")
        self.setGeometry(100, 100, 222, 222)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.button = QPushButton("Choose Folder")
        self.button2 = QPushButton("Convert Pdfs")
        self.button2.setVisible(False)
        self.button.clicked.connect(self.on_button_click)
        self.button2.clicked.connect(self.on_button_click2)

        layout.addWidget(self.button)
        layout.addWidget(self.button2)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        central_widget.setLayout(layout)

    def on_button_click(self):
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath:
            self.folderpath = folderpath
            self.button2.setVisible(True)
            self.progress_bar.setVisible(False)

    def on_button_click2(self):
        if self.folderpath:
            self.progress_bar.setVisible(True)
            self.run_pdf_thread(self.folderpath)

    def run_pdf_thread(self, folderpath):
        self.pdf_thread = PDFThread(folderpath)
        self.pdf_thread.pdf_generator.progress_signal.connect(
            self.update_progress)
        self.pdf_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)


def main():
    app = QApplication(sys.argv)
    start_window = StartWindow()
    start_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
