# menu.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QProgressBar, QCheckBox,QLabel
from pdf import PDFGenerator
from PyQt5.QtCore import Qt, QThread

class PDFThread(QThread):
    def __init__(self, folderpath, type, files=None):
        super().__init__()
        self.folderpath = folderpath
        self.type = type
        self.files = files if files is not None else []
        self.pdf_generator = PDFGenerator()

    def run(self):
        if self.type == 0:
            self.pdf_generator.create_pdf(self.folderpath)
        else:
            self.pdf_generator.create_pdf_multiple(self.files, self.folderpath)


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image to Pdf converter")
        self.setGeometry(100, 100, 222, 222)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.files = []

        layout = QVBoxLayout()
        self.label = QLabel(f"{len(self.files)} files selected")
        self.label.setVisible(False)
        self.checkbox = QCheckBox("Multipaged")
        self.button = QPushButton("Choose Folder")
        self.button2 = QPushButton("Convert to Pdf")
        self.button3 = QPushButton("Select Files")
        self.button4 = QPushButton("Choose Output Folder")
        self.button3.setVisible(False)
        self.button4.setVisible(False)
        self.button2.setVisible(False)
        self.button.clicked.connect(self.on_button_click)
        self.button2.clicked.connect(self.on_button_click2)
        self.button3.clicked.connect(self.on_button_click3)
        self.button4.clicked.connect(self.on_button_click4)
        self.checkbox.stateChanged.connect(lambda state : self.on_checkbox(state))
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)
        layout.addWidget(self.button2)


        

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        central_widget.setLayout(layout)


    def on_checkbox(self,state):
        self.button.setVisible(state!=2)
        self.button3.setVisible(state==2)
        self.button4.setVisible(state==2)
        self.progress_bar.setVisible(state==2)

        self.label.setVisible(state==2)

    def on_button_click(self):
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath:
            print(folderpath)
            self.folderpath = folderpath
            self.button2.setVisible(True)
            self.progress_bar.setVisible(False)

    def on_button_click2(self):
        if self.folderpath:
            self.progress_bar.setVisible(True)
            self.run_pdf_thread(self.folderpath)

    def on_button_click3(self):
        file_path, _ = QFileDialog.getOpenFileName()
        if file_path:
            self.files.append(file_path)
            self.label.setText(f"{len(self.files)} files selected")


    def on_button_click4(self):
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath:
            self.button2.setVisible(True)
            self.folderpath = folderpath
            self.progress_bar.setVisible(False)

    def run_pdf_thread(self, folderpath):
        # Determine the type based on the checkbox state
        type = 1 if self.checkbox.isChecked() else 0
        self.pdf_thread = PDFThread(folderpath, type, self.files)
        self.pdf_thread.pdf_generator.progress_signal.connect(self.update_progress)
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
