import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from reportlab.lib.utils import ImageReader 
from PyQt5.QtCore import QObject, pyqtSignal
from datetime import datetime
current_time = datetime.now()
formatted_time = current_time.strftime("%d%H%M%S")

class PDFGenerator(QObject):
    progress_signal = pyqtSignal(int)

    """
    A class for generating PDFs from images using ReportLab and PIL.

    Attributes:
    - progress_signal (pyqtSignal): Signal for indicating the progress of the PDF generation.

    Methods:
    - create_pdf(folder): Create a PDF from a folder of images.
    - create_pdf_multiple(files, folder): Create a multipaged PDF from a list of image files.
    """

    def create_pdf(self,folder):
        
        """
        Create a PDF from a folder of images.

        Args:
        - folder (str): The path to the folder containing images.
        """
        
        output_directory =os.path.join( folder ,"pdfs")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        script_dir = os.path.dirname(__file__)
        enders= [".jpg",".png",".bmp",".gif",".ppm",".webp","jpeg"]
        listofFiles= os.listdir(folder)
        listofImages= []
        for image in listofFiles:
            for ender in enders:
                if image.endswith(ender):
                    listofImages.append(image)
        index=0
        if listofImages:
            chunk = int(100 / len(listofImages))
        else:
            chunk = 100
        if not listofImages :
            self.progress_signal.emit(100)

        for images in listofImages:
            for ender in enders:
             if images.endswith(ender):
                 new_name = images.replace(ender,"_"+ender[1:])

                 new_name+= ".pdf"

                 c = canvas.Canvas(os.path.join(output_directory,new_name), pagesize=letter)

                 image_path = os.path.join(folder, images)

                 if image_path and os.path.exists(image_path):
                     img = Image.open(image_path)

                     reportlab_image = ImageReader(img)

                     c.drawImage(reportlab_image, 0, 0, width=letter[0], height=letter[1], preserveAspectRatio=False)
                 else: print(image_path)


                 c.save()
                 index+=chunk
                 if listofImages.index(images)== len(listofImages)-1:
                     index = 100
                 self.progress_signal.emit(index)
    def create_pdf_multiple(self, files, folder):
        """
        Create a multipaged PDF from a list of image files.

        Args:
        - files (list): List of paths to image files.
        - folder (str): The path to the output folder.
        """
        output_directory = os.path.join(folder, "pdfs")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        enders = [".jpg", ".png", ".bmp", ".gif", ".ppm", ".webp", "jpeg"]
        index = 0

        if files:
            chunk = int(100 / len(files))
        else:
            chunk = 100

        c = canvas.Canvas(os.path.join(output_directory, f"{formatted_time}.pdf"), pagesize=letter)

        for image_path in files:
            for ender in enders:
                if image_path.lower().endswith(ender):
                    if os.path.exists(image_path):
                        img = Image.open(image_path)
                        reportlab_image = ImageReader(img)
                        c.drawImage(reportlab_image, 0, 0, width=letter[0], height=letter[1], preserveAspectRatio=False)
                        c.showPage()
                    else:
                        print(f"File not found: {image_path}")

            index += chunk
            if files.index(image_path) == len(files) - 1:
                index = 100
            self.progress_signal.emit(index)

        c.save()