from PyQt4 import QtCore, QtGui
from SymbolEditorWidget import *

class SymbolEditorDialog(QtGui.QDialog):

    def __init__(self, symbol, parent=None):
        super(SymbolEditorDialog, self).__init__(parent)

        self.symbol = symbol
        self.initUI()

    def initUI(self):

        hbox = QtGui.QHBoxLayout()

        self.save_button = QtGui.QPushButton("Save")
        hbox.addWidget(self.save_button)

        self.exit_button = QtGui.QPushButton("Exit")
        hbox.addWidget(self.exit_button)

        self.symbol_editor = SymbolEditorWidget(self)
        self.symbol_editor.clearImage()

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.symbol_editor)
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
        self.emit(QtCore.SIGNAL("new_image"))

    def maybeSave(self):
        if self.symbol_editor.isModified():
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
        initialPath = QtCore.QDir.currentPath() + '/symbols/' + self.symbol + '.' + fileFormat

        fileName = QtGui.QFileDialog.getSaveFileName(self, "Save As",
                                                     initialPath,
                                                     "%s Files (*.%s);;All Files (*)" % (
                                                     fileFormat.upper(), fileFormat))
        if fileName:
            print("saving")
            if self.symbol_editor.saveImage(fileName, fileFormat):
                self.close()
            else:
                return False
        return False



