
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from TranslationDialog import *


class TranslatorWidget(QWidget):

    def __init__(self, symbols, parent=None):
        super(TranslatorWidget, self).__init__(parent)


        self.symbols = symbols
        self.text_field = QLineEdit(self)
        self.translate_button = QPushButton("Translate")
        self.translation_dialog = None

        hbox = QHBoxLayout()
        hbox.addWidget(self.text_field)
        hbox.addWidget(self.translate_button)

        @pyqtSlot()
        def on_translate_clicked():
            self.translate()

        self.translate_button.clicked.connect(on_translate_clicked)

        self.setLayout(hbox)

    def translate(self):
        text = self.text_field.text()
        text_array = list(text)
        image_array = []
        output_image_width = 0
        symbol_count = 0
        print(text_array)
        for sym in text_array:
            symbol_count += 1
            if sym in self.symbols:
                loaded_image = QImage()
                if not loaded_image.load('symbols/' + sym + '.png'):
                    print("ERROR LOADING")

                #w = loaded_image.width()
                #output_image_width += w
                image_array.append(loaded_image)

        image_count = len(image_array)
        output_image_width = 1000
        output_image_height = image_count/10
        output_image_height = (round(output_image_height) +1) * 100

        new_image = QImage(QSize(output_image_width, output_image_height), QImage.Format_RGB32)
        new_image.fill(QtGui.qRgb(255, 255, 255))
        painter = QPainter(new_image)

        current_x_pos = 0
        current_y_pos = 0

        for idx, img in enumerate(image_array):
            painter.drawImage(QPoint(current_x_pos, current_y_pos),img)
            print("idx", idx)
            current_x_pos += img.width()
            if idx != 0 and idx % 10 == 0:
                current_y_pos += 100
                current_x_pos = 0
        print("DONE")
        self.translation_dialog = TranslationDialog(text,new_image,self)
        self.translation_dialog.exec()



