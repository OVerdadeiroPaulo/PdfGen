import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from reportlab.lib.utils import ImageReader 
from PyQt5.QtCore import QObject, pyqtSignal

class PDFGenerator(QObject):
    progress_signal = pyqtSignal(int)



    def create_pdf(self,folder):
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
        chunk = int (100/len(listofImages))

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

