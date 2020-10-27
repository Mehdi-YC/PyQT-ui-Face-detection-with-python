from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QScrollArea, QFileDialog, QMainWindow, QApplication, QPushButton, QTextEdit
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import QUrl, Qt
from defined_fonctions.htmlmanip import writeHtml
from defined_fonctions import detection
from defined_fonctions import pretraitement

import cv2
import sys
import os
import numpy as np


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.isLight = False
        self.isDrawed = False
        self.imageIsSet = False
        self.enabeled = False
        self.original = ""
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint
        )

        self.light = open("ressources/Qss/light.css", "r").read()
        self.dark = open("ressources/Qss/dark.css", "r").read()
        uic.loadUi("ressources/ui/aio.ui", self)

        self.tabWidget.setTabEnabled(0, True)
        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(2, False)
        self.tabWidget.setTabEnabled(3, False)

        self.tabWidget.setTabEnabled(1, False)
        self.imgChanger.clicked.connect(self.openFileNameDialog)
        self.Detection.clicked.connect(lambda: self.EnableDetection(True))
        self.Pretraitement.clicked.connect(
            lambda: self.EnablePretraitement(True))
        self.Reconaissance.clicked.connect(self.showReport)
        self.Rotation.clicked.connect(self.rotate)
        self.Miroir.clicked.connect(self.mirror_flip)
        self.tabWidget.currentChanged.connect(self.disableReport)

        self.scroll = QtWidgets.QScrollArea(self.Report)
        self.scroll.setGeometry(QtCore.QRect(0, 0, 795, 500))
        self.web = QWebView()
        self.web.setGeometry(QtCore.QRect(0, 0, 795, 1500))
        self.scroll.setWidget(self.web)
        self.web.setEnabled(False)

        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.DNez.clicked.connect(
            lambda: self.w_dectect_nose(self.original))
        self.DVisage.clicked.connect(
            lambda: self.w_dectect_face(self.original))
        self.DBouche.clicked.connect(
            lambda: self.w_dectect_mouth(self.original))
        self.DYeux.clicked.connect(
            lambda: self.w_dectect_eyes(self.original))
        self.Norm.clicked.connect(self.w_normalisation)
        self.Egaliser.clicked.connect(self.w_egalisation_hist)
        self.Median.clicked.connect(self.w_filtre_median)
        self.Denoising.clicked.connect(self.w_debruit_img)
        self.resset.clicked.connect(self.resset_img)
        self.wlcm.clicked.connect(self.goToMain)
        path = os.path.abspath(os.getcwd())
        self.gif = QMovie(path+"/welcome.gif")
        print(path+"\welcome.gif")
        self.label.setMovie(self.gif)
        self.gif.start()

        # extra
        self.ThemeButton.clicked.connect(self.extra)

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Select your Image", "./ressources/images/testImg/", "Image (*.PNG *.JPG)", options=options)
        if fileName:
            self.original = fileName
            self.changable = fileName
            pixmap = QPixmap(fileName)
            pixmap.scaled(self.MyImage.width(), self.MyImage.height())
            self.MyImage.setPixmap(pixmap)
            self.imageIsSet = True
            self.EnableButtons()

    # BUTTONS MANAGEMENT :
    def EnableDetection(self, state):
        if self.imageIsSet:
            self.DVisage.setEnabled(state)
            self.DNez.setEnabled(state)
            self.DYeux.setEnabled(state)
            self.DBouche.setEnabled(state)

    def EnablePretraitement(self, state):
        if self.imageIsSet:
            self.Norm.setEnabled(state)
            self.Denoising.setEnabled(state)
            self.Egaliser.setEnabled(state)
            self.Median.setEnabled(state)

    def EnableButtons(self, state=True):
        self.Miroir.setEnabled(state)
        self.Reconaissance.setEnabled(state)
        self.Detection.setEnabled(state)
        self.Rotation.setEnabled(state)
        self.Pretraitement.setEnabled(state)
        self.resset.setEnabled(state)

    # REPORT :
    def showReport(self):
        myfile = writeHtml(np.zeros((8, 8)), np.zeros((8, 8)),
                           "../images/testImg/"+self.original.split('/')[-1])

        self.web.load(QUrl.fromLocalFile(myfile))
        self.tabWidget.setTabEnabled(2, True)
        self.tabWidget.setCurrentIndex(2)
        self.enabeled = True

    def disableReport(self):
        if self.enabeled:
            self.tabWidget.setTabEnabled(1, False)
            self.enabeled = False


# BUTTONS FUNCTIONS------------------------------
    # EXTRA :

    def goToMain(self):
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget.setTabEnabled(1, True)
        self.tabWidget.setTabEnabled(0, False)
        self.tabWidget.setTabEnabled(3, True)

    def resset_img(self):
        self.hist.clear()
        self.MyImage.clear()
        self.isLight = False
        self.isDrawed = False
        self.imageIsSet = False
        self.enabeled = False
        self.original = ""
        self.EnableButtons(False)

    def extra(self):
        if self.isLight:
            self.setStyleSheet(self.dark)
            self.ThemeButton.setText("☾  Theme")
            self.isLight = False
            if self.isDrawed:
                pixmap2 = QPixmap("hist.dark.jpg")
                pixmap2.scaled(self.hist.width(), self.hist.height())
                self.hist.setPixmap(pixmap2)

        else:
            self.setStyleSheet(self.light)
            self.ThemeButton.setText("☼ Theme")
            self.isLight = True
            if self.isDrawed:
                pixmap2 = QPixmap("hist.jpg")
                pixmap2.scaled(self.hist.width(), self.hist.height())
                self.hist.setPixmap(pixmap2)

    def rotate(self):
        img = cv2.imread(self.changable)
        img_rotate_90_clockwise = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite('ressources/images/rotated/rotated90.PNG',
                    img_rotate_90_clockwise)
        self.changable = 'ressources/images/rotated/rotated90.PNG'
        pixmap = QPixmap(self.changable)
        pixmap.scaled(self.MyImage.width(), self.MyImage.height())
        self.MyImage.setPixmap(pixmap)

    def mirror_flip(self):
        img = cv2.imread(self.changable)
        img_mirror_flip = cv2.flip(img, 1)
        cv2.imwrite('ressources/images/mirror/mirror.PNG',
                    img_mirror_flip)
        self.changable = 'ressources/images/mirror/mirror.PNG'
        pixmap = QPixmap(self.changable)
        pixmap.scaled(self.MyImage.width(), self.MyImage.height())
        self.MyImage.setPixmap(pixmap)

    # DETECTION :

    def w_dectect_nose(self, img):
        path = detection.dectect_nose(img)
        pixmap = QPixmap(path)
        pixmap.scaled(self.MyImage.width(), self.MyImage.height())
        self.MyImage.setPixmap(pixmap)
        self.EnableDetection(False)

    def w_dectect_face(self, img):
        path = detection.face_detect(img)
        pixmap = QPixmap(path)
        pixmap.scaled(self.MyImage.width(), self.MyImage.height())
        self.MyImage.setPixmap(pixmap)
        self.EnableDetection(False)

    def w_dectect_mouth(self, img):
        path = detection.detect_mouth(img)
        pixmap = QPixmap(path)
        pixmap.scaled(self.MyImage.width(), self.MyImage.height())
        self.MyImage.setPixmap(pixmap)
        self.EnableDetection(False)

    def w_dectect_eyes(self, img):
        path = detection.eyes_detect2(img)
        pixmap = QPixmap(path)
        pixmap.scaled(self.MyImage.width(), self.MyImage.height())
        self.MyImage.setPixmap(pixmap)
        self.EnableDetection(False)

    # PRETRAITEMENT :
    def w_normalisation(self):
        path = pretraitement.normalisation(self.original)
        pixmap = QPixmap(path)
        pixmap.scaled(self.MyImage.width(), self.MyImage.height())
        self.MyImage.setPixmap(pixmap)
        self.EnablePretraitement(False)

    def w_egalisation_hist(self):
        path = pretraitement.egalisation_hist(self.original)
        pixmap = QPixmap(path)
        pixmap.scaled(self.MyImage.width(), self.MyImage.height())
        self.MyImage.setPixmap(pixmap)

        if self.isLight:
            pixmap2 = QPixmap("hist.jpg")
            pixmap2.scaled(self.hist.width(), self.hist.height())
            self.hist.setPixmap(pixmap2)
        else:
            pixmap2 = QPixmap("hist.dark.jpg")
            pixmap2.scaled(self.hist.width(), self.hist.height())
            self.hist.setPixmap(pixmap2)
        self.isDrawed = True

        self.EnablePretraitement(False)

    def w_filtre_median(self):
        path = pretraitement.filtre_median(self.original)
        pixmap = QPixmap(path)
        pixmap.scaled(self.MyImage.width(), self.MyImage.height())
        self.MyImage.setPixmap(pixmap)
        self.EnablePretraitement(False)

    def w_debruit_img(self):
        path = pretraitement.debruit_img(self.original)
        pixmap = QPixmap(path)
        pixmap.scaled(self.MyImage.width(), self.MyImage.height())
        self.MyImage.setPixmap(pixmap)
        self.EnablePretraitement(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    app.exec_()
