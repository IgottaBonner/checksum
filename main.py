import re
import sys
import os
import fnmatch
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush, QColor, QPainter, QCursor
from PyQt5.QtCore import Qt, QPoint, QUrl, QSize, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit

from Ui_1 import Ui_MainWindow


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.oldPos = self.pos()
        self.fill_functions()
        icon = QIcon()
        icon.addPixmap(
            QPixmap(resource_path("assets/icon.png")),
            QIcon.Normal,
            QIcon.Off,
        )
        self.setWindowIcon(icon)

        self.textEdit = CustomTextEdit(self)
        self.textEdit.setGeometry(QRect(60, 233, 61, 101))
        self.textEdit.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))
        self.textEdit.setStyleSheet(
            "background-color: rgba(255, 255, 255, 100);\n" "border:1 solid rgb(0,0,0);"
        )
        self.textEdit.setAcceptRichText(True)
        self.textEdit.setObjectName("textEdit")

        pixmap = QPixmap(resource_path("assets/papyrus.png"))
        scaled_pixmap = pixmap.scaled(self.size())
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)
        self.setMask(scaled_pixmap.mask())

        self.ui.pushButton.clicked.connect(self.close)
        icon = QIcon()
        icon.addPixmap(
            QPixmap(resource_path("assets/close.svg")), QIcon.Normal, QIcon.Off
        )
        self.ui.pushButton.setIcon(icon)

        pixmap = QPixmap(resource_path("assets/psb.png"))
        transparent_pixmap = QPixmap(pixmap.size())
        transparent_pixmap.fill(QColor(0, 0, 0, 0))
        painter = QPainter(transparent_pixmap)
        painter.setOpacity(0.8)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        self.ui.label_2.setPixmap(transparent_pixmap)

    def fill_functions(self):
        self.ui.lineEdit.returnPressed.connect(self.search)
        self.ui.lineEdit_2.returnPressed.connect(self.search)
        self.ui.lineEdit_3.returnPressed.connect(self.search)

    def search(self):
        text_1 = self.ui.lineEdit.text()
        text_2 = self.ui.lineEdit_2.text()
        text_3 = self.ui.lineEdit_3.text()
        finalkey = []
        finalsum = []
        self.textEdit.clear()
        self.ui.textEdit_2.clear()
        try:
            for filename in os.listdir("."):
                if fnmatch.fnmatch(filename, "*.txt"):
                    with open(filename, "r") as file:
                        content = file.read()
                        space = content.split("\n")
                        for im in space:
                            if re.fullmatch(
                                f"^\|\d+\|\d+\|\w*{text_1}\w*\|\d+\|\w*{text_2}\w*\|\d+\|\w*{text_3}\w*\|$",
                                im,
                            ):
                                finalkey.append(im.split("|")[1])
                                pre1 = re.search(r"\d+", im.split("|")[3])[0]
                                pre2 = re.search(r"\d+", im.split("|")[5])[0]
                                pre3 = re.search(r"\d+", im.split("|")[7])[0]
                                finalsum.append(f"{pre1}  {pre2}  {pre3}")
            self.textEdit.setText(("\n").join(finalkey))
            self.ui.textEdit_2.setText(("\n").join(finalsum))

        except:
            pass

    def findsum(self):
        text_4 = self.textEdit.toPlainText()
        final = []
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.textEdit_2.clear()
        try:
            for filename in os.listdir("."):
                if fnmatch.fnmatch(filename, "*.txt"):
                    with open(filename, "r") as file:
                        content = file.read()
                        space = content.split("\n")
                        for im in space:
                            if re.fullmatch(
                                f"^\|{text_4}\|\d+\|\w*\|\d+\|\w*\|\d+\|\w*\|$",
                                im,
                            ):
                                final.extend(
                                    [
                                        re.search(r"\d+", im.split("|")[3])[0],
                                        re.search(r"\d+", im.split("|")[5])[0],
                                        re.search(r"\d+", im.split("|")[7])[0],
                                    ]
                                )
            self.ui.lineEdit.setText(final[0])
            self.ui.lineEdit_2.setText(final[1])
            self.ui.lineEdit_3.setText(final[2])
        except:
            pass

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(CustomTextEdit, self).__init__(parent)
        self.mw = parent

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.mw.findsum()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
