import os
import sys
import string
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from TranslatorWidget import TranslatorWidget
from SymbolWidget import SymbolWidget

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        #create symbols that can be used
        self.symbols = list(string.ascii_lowercase)
        self.symbols.append(" ")
        #self.symbols = ['a', "b", "c", "d", "e"]
        self.symbol_widgets = []

        translator_widget = TranslatorWidget(self.symbols, self)

        vbox = QVBoxLayout()

        vbox.addWidget(translator_widget)

        for sym in self.symbols:
            _symbol_widget = SymbolWidget(sym, self)
            vbox.addWidget(_symbol_widget)
            self.symbol_widgets.append(_symbol_widget)

        box = QGroupBox('All symbols:')
        box.setLayout(vbox)

        scroll = QScrollArea()
        scroll.setWidget(box)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(600)
        scroll.setFixedWidth(400)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

def main():
    app = QApplication([])
    mw = QMainWindow()
    mw.setWindowTitle("pap translator")
    w = MainWidget(parent=mw)
    mw.setCentralWidget(w)
    mw.show()


    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

