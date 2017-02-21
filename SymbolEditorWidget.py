from PyQt4 import QtCore, QtGui

class SymbolEditorWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(SymbolEditorWidget, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_StaticContents)
        self.modified = False
        self.scribbeling = False
        self.penWidth = 4
        self.penColor = QtCore.Qt.black
        imageSize = QtCore.QSize(100,100)
        #self.symbolImage = QtGui.QImage()
        self.symbolImage =QtGui.QImage(imageSize, QtGui.QImage.Format_RGB32)
        #vbox.addWidget(self.symbolImage)
        self.lastPoint = QtCore.QPoint
        self.setFixedSize(100,100)

    def openImage(self, filename):
        loadedImage = QtGui.QImage()
        if not loadedImage.load(fileName):
            return False

        w = loadedImage.width()
        h = loadedImage.height()
        #self.mainWindow.resize(w,h)

        self.symbolImage = loadedImage
        self.modified = False
        self.update()

    def saveImage(self, filename, fileformat):
        visibleImage = self.symbolImage
        self.resizeImage(visibleImage, self.size())

        if visibleImage.save(filename, fileformat):
            self.modified = False
            return True
        else:
            return False

    def setPenColor(self, newcolor):
        self.penColor = newcolor

    def setPenWidth(self, newwidth):
        self.penWidth = newwidth

    def clearImage(self):
        self.symbolImage.fill(QtGui.qRgb(255,255,255))
        self.modified = True
        self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.lastPoint = event.pos()
            self.scribbeling = True

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton and self.scribbeling:
            self.drawLineTo(event.pos())

    def mouseReleaseEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton and self.scribbeling:
            self.drawLineTo(event.pos())
            self.scribbeling = False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(event.rect(), self.symbolImage)


    def resizeEvent(self, event):
        self.resizeImage(self.symbolImage, event.size())
        super(SymbolEditorWidget, self).resizeEvent(event)
        print("Resize", event.size())


    def drawLineTo(self, endpoint):
        painter = QtGui.QPainter(self.symbolImage)
        painter.setPen(QtGui.QPen(self.penColor, self.penWidth,
                                  QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                  QtCore.Qt.RoundJoin))
        painter.drawLine(QtCore.QPoint(self.lastPoint), QtCore.QPoint(endpoint))
        self.modified = True

        self.update()
        self.lastPoint = QtCore.QPoint(endpoint)


    def resizeImage(self, image, newsize):
        print(newsize)
        if image.size() == newsize:
            return

        newImage = QtGui.QImage(newsize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.qRgb(255,255,255))
        painter = QtGui.QPainter(newImage)
        painter.drawImage(QtCore.QPoint(0,0), image)
        self.symbolImage = newImage

    def print_(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        printDialog = QtGui.QPrintDialog(printer, self)
        if printDialog.exec_() == QtGui.QDialog.Accepted:
            painter = QtGui.QPainter(printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size, QtCore.Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(),
                                size.width(),size.height())
            painter.setWindow(self.symbolImage.rect())
            painter.drawImage(0,0,self.symbolImage)
            painter.end()

    def isModified(self):
        return self.modified

    def getPenColor(self):
        return self.penColor

    def getPenWidth(self):
        return self.penWidth



