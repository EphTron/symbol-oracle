import sys

from PyQt4 import QtCore, QtGui

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from SymbolEditorDialog import *

class SymbolWidget(QtGui.QWidget):
    def __init__(self, symbol, parent=None):
        super(SymbolWidget,self).__init__(parent)

        self.symbol = symbol
        self.initUI()

    def initUI(self):
        print("Welcome Symbol Widget ", self.symbol)
        self.editor_dialog = SymbolEditorDialog(self.symbol, self)

        self.label = QLabel("Symbol " + self.symbol)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.label)

        self.image_label = QLabel()
        if self.symbol == " ":
            self.pixmap = QPixmap('symbols/' + "space" + '.png')
        else:
            self.pixmap = QPixmap('symbols/' + self.symbol + '.png')
        self.image_label.setPixmap(self.pixmap)
        self.layout.addWidget(self.image_label)

        self.edit_button = QPushButton("Edit")
        self.layout.addWidget(self.edit_button)

        @pyqtSlot()
        def on_click():
            self.editor_dialog.exec()


        self.edit_button.clicked.connect(on_click)
        QObject.connect(self.editor_dialog, SIGNAL("new_image"), self.update_symbol)

        self.setLayout(self.layout)

    def update_symbol(self):
        print("new image foo")
        if self.symbol == " ":
            self.pixmap = QPixmap('symbols/' + "space" + '.png')
        else:
            self.pixmap = QPixmap('symbols/' + self.symbol + '.png')
        self.image_label.setPixmap(self.pixmap)
