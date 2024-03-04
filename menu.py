"""
menu.py - Image to Pdf Converter GUI

This script provides a graphical user interface (GUI) for converting images to PDFs.
It uses PyQt5 for the GUI components and PDFGenerator class from the pdf module for PDF creation.

Dependencies:
- PyQt5
- pdf module (containing PDFGenerator class)
- Pillow (PIL) for image handling

Usage:
Run the script using Python 3.

Example:
    $ python3 menu.py
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QProgressBar, QCheckBox,QLabel
from pdf import PDFGenerator
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QColor


class PDFThread(QThread):
    """
    PDFThread - Custom QThread for PDF generation

    This class inherits from QThread and is responsible for creating PDFs
    either from a single folder or multiple selected files.

    Attributes:
        folderpath (str): The path to the folder containing images (for single folder conversion).
        type (int): Type of conversion (0 for single folder, 1 for multiple files).
        files (list): List of file paths (for multiple files conversion).
        pdf_generator (PDFGenerator): Instance of the PDFGenerator class for PDF creation.
    """
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
    """
    StartWindow - Main GUI window

    This class creates the main window for the Image to Pdf Converter GUI.

    Attributes:
        folderpath (str): The path to the selected folder.
        files (list): List of selected file paths.
        pdf_thread (PDFThread): Instance of the PDFThread class for PDF generation.
    """
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
        self.buttons = []
        button_text = ["Choose Folder","Select Files","Choose Output Folder","Convert to Pdf",]
        for text in button_text:
            self.buttons.append(QPushButton(text))
        self.checkbox = QCheckBox("Multipaged")

        for button in self.buttons[1:]:
            button.setVisible(False)

        actions = [self.on_button_click,self.on_button_click2,self.on_button_click3,self.on_button_click4]
        for i in range (4):
            self.buttons[i].clicked.connect(actions[i])
        self.checkbox.stateChanged.connect(lambda state : self.on_checkbox(state))
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)
        for button in self.buttons:
            layout.addWidget(button)
            


        

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        central_widget.setLayout(layout)

        self.setStyleSheet("background-color: whitesmoke; ")


    def on_checkbox(self,state):
        """Callback for checkbox state change."""
        self.buttons[0].setVisible(state!=2)
        self.buttons[1].setVisible(state==2)
        self.buttons[3].setVisible(state>5)
        if state!=2:
            self.progress_bar.setVisible(state==2)

        self.label.setVisible(state==2)

    def on_button_click(self):
        """Callback for 'Choose Folder' button click."""
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath:
            print(folderpath)
            self.folderpath = folderpath
            self.buttons[3].setVisible(True)
            self.progress_bar.setVisible(False)
    def on_button_click2(self):
        """Callback for 'Select Files' button click."""
        file_path, _ = QFileDialog.getOpenFileName()
        if file_path:
            self.files.append(file_path)
            self.label.setText(f"{len(self.files)} files selected")
            self.buttons[2].setVisible(True)

    def on_button_click3(self):
        """Callback for 'Choose Output Folder' button click."""
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath:
            self.buttons[3].setVisible(True)
            self.folderpath = folderpath
            self.progress_bar.setVisible(False)

    def on_button_click4(self):
        """Callback for 'Convert to Pdf' button click."""
        if self.folderpath:
            self.progress_bar.setVisible(True)
            self.run_pdf_thread(self.folderpath)



    def run_pdf_thread(self, folderpath):
        """Run PDFThread for PDF generation."""
        type = 1 if self.checkbox.isChecked() else 0
        self.pdf_thread = PDFThread(folderpath, type, self.files)
        self.pdf_thread.pdf_generator.progress_signal.connect(self.update_progress)
        self.pdf_thread.start()

    def update_progress(self, value):
        """Callback for updating progress bar."""
        self.progress_bar.setValue(value)


def main():
    """
    Main function to start the application.

    This function initializes the PyQt application, creates an instance of the
    StartWindow, and starts the application event loop.

    Parameters:
    None

    Returns:
    None
    """
    app = QApplication(sys.argv)
    start_window = StartWindow()
    start_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
