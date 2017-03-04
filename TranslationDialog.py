from PyQt4 import QtCore, QtGui
from SymbolEditorWidget import *

class TranslationDialog(QtGui.QDialog):

    def __init__(self, text, image, parent=None):
        super(TranslationDialog, self).__init__(parent)
        self.text = text
        self.symbol_image = image
        self.initUI()

    def initUI(self):

        hbox = QtGui.QHBoxLayout()

        self.save_button = QtGui.QPushButton("Save")
        hbox.addWidget(self.save_button)

        self.exit_button = QtGui.QPushButton("Exit")
        hbox.addWidget(self.exit_button)

        self.image_label = QtGui.QLabel()
        self.pixmap = QtGui.QPixmap.fromImage(self.symbol_image)
        self.image_label.setPixmap(self.pixmap)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        @QtCore.pyqtSlot()
        def save():
            fileFormat = "png"
            self.saveFile(fileFormat)

        self.save_button.clicked.connect(save)

        @QtCore.pyqtSlot()
        def close():
            self.close()

        self.exit_button.clicked.connect(close)

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def maybeSave(self):
        ret = QtGui.QMessageBox.warning(self, "Symbol Editor",
                                        "The image has been modified.\n"
                                        "Do you want to save your changes?",
                                        QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                                        QtGui.QMessageBox.Cancel)
        if ret == QtGui.QMessageBox.Save:
            print("yep")
            return self.saveFile('png')
        elif ret == QtGui.QMessageBox.Cancel:
            return False
        return True


    def saveFile(self, fileFormat):
        initialPath = QtCore.QDir.currentPath() + '/translations/' + self.text + '.' + fileFormat

        fileName = QtGui.QFileDialog.getSaveFileName(self, "Save As",
                                                     initialPath,
                                                     "%s Files (*.%s);;All Files (*)" % (
                                                     fileFormat.upper(), fileFormat))
        if fileName:
            print("saving")
            return self.saveImage(fileName, fileFormat)
        print("save failed")
        return False

    def saveImage(self, filename, fileformat):
        if self.symbol_image.save(filename, fileformat):
            return True
        else:
            return False

