# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'one_screen.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QLabel,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1800, 1051)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1800, 1000))
        MainWindow.setMaximumSize(QSize(1800, 1051))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setMinimumSize(QSize(1800, 1000))
        self.centralwidget.setMaximumSize(QSize(1800, 1000))
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(10, 10, 10, 10)
        self.upper_widget = QWidget(self.centralwidget)
        self.upper_widget.setObjectName(u"upper_widget")
        self.upper_widget.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.upper_widget.sizePolicy().hasHeightForWidth())
        self.upper_widget.setSizePolicy(sizePolicy2)
        self.upper_widget.setMinimumSize(QSize(1700, 1000))
        self.upper_widget.setMaximumSize(QSize(1650, 1000))
        self.upper_widget.setLayoutDirection(Qt.LeftToRight)
        self.verticalLayout = QVBoxLayout(self.upper_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridGroupBox = QGroupBox(self.upper_widget)
        self.gridGroupBox.setObjectName(u"gridGroupBox")
        sizePolicy2.setHeightForWidth(self.gridGroupBox.sizePolicy().hasHeightForWidth())
        self.gridGroupBox.setSizePolicy(sizePolicy2)
        self.gridLayout_2 = QGridLayout(self.gridGroupBox)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(1, 1, 1, 1)
        self.real_img = QLabel(self.gridGroupBox)
        self.real_img.setObjectName(u"real_img")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.real_img.sizePolicy().hasHeightForWidth())
        self.real_img.setSizePolicy(sizePolicy3)
        self.real_img.setMinimumSize(QSize(800, 450))
        self.real_img.setMaximumSize(QSize(800, 450))
        self.real_img.setAutoFillBackground(False)
        self.real_img.setStyleSheet(u"background-color : rgb(255,0,0);")
        self.real_img.setMargin(0)

        self.gridLayout_2.addWidget(self.real_img, 0, 0, 1, 1)

        self.widget = QWidget(self.gridGroupBox)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(700, 300))
        self.widget.setMaximumSize(QSize(700, 300))
        self.widget.setLayoutDirection(Qt.LeftToRight)
        self.widget.setAutoFillBackground(False)
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btn_start = QPushButton(self.widget)
        self.btn_start.setObjectName(u"btn_start")
        sizePolicy1.setHeightForWidth(self.btn_start.sizePolicy().hasHeightForWidth())
        self.btn_start.setSizePolicy(sizePolicy1)
        self.btn_start.setMinimumSize(QSize(500, 50))
        self.btn_start.setMaximumSize(QSize(600, 50))
        self.btn_start.setFocusPolicy(Qt.NoFocus)

        self.verticalLayout_2.addWidget(self.btn_start, 0, Qt.AlignHCenter)

        self.btn_auto_parking = QPushButton(self.widget)
        self.btn_auto_parking.setObjectName(u"btn_auto_parking")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.btn_auto_parking.sizePolicy().hasHeightForWidth())
        self.btn_auto_parking.setSizePolicy(sizePolicy4)
        self.btn_auto_parking.setMinimumSize(QSize(500, 50))
        self.btn_auto_parking.setMaximumSize(QSize(500, 50))
        self.btn_auto_parking.setFocusPolicy(Qt.NoFocus)

        self.verticalLayout_2.addWidget(self.btn_auto_parking, 0, Qt.AlignHCenter)

        self.btn_refind_path = QPushButton(self.widget)
        self.btn_refind_path.setObjectName(u"btn_refind_path")
        sizePolicy4.setHeightForWidth(self.btn_refind_path.sizePolicy().hasHeightForWidth())
        self.btn_refind_path.setSizePolicy(sizePolicy4)
        self.btn_refind_path.setMinimumSize(QSize(500, 50))
        self.btn_refind_path.setMaximumSize(QSize(500, 50))

        self.verticalLayout_2.addWidget(self.btn_refind_path, 0, Qt.AlignHCenter)


        self.gridLayout_2.addWidget(self.widget, 2, 1, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.virtual_img = QLabel(self.gridGroupBox)
        self.virtual_img.setObjectName(u"virtual_img")
        self.virtual_img.setMinimumSize(QSize(800, 450))
        self.virtual_img.setMaximumSize(QSize(800, 450))
        self.virtual_img.setLayoutDirection(Qt.LeftToRight)
        self.virtual_img.setStyleSheet(u"background-color : rgb(255,0,0);\n"
"")

        self.gridLayout_2.addWidget(self.virtual_img, 2, 0, 1, 1)

        self.check_free_space = QLabel(self.gridGroupBox)
        self.check_free_space.setObjectName(u"check_free_space")
        self.check_free_space.setEnabled(True)
        self.check_free_space.setMinimumSize(QSize(800, 450))
        self.check_free_space.setMaximumSize(QSize(800, 450))
        self.check_free_space.setStyleSheet(u"background-color : rgb(255,0,0);")

        self.gridLayout_2.addWidget(self.check_free_space, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.gridGroupBox)


        self.gridLayout_3.addWidget(self.upper_widget, 0, 1, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1800, 22))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.btn_start.clicked.connect(MainWindow.start_act)
        self.btn_refind_path.clicked.connect(MainWindow.refind_path_act)
        self.btn_auto_parking.clicked.connect(MainWindow.auto_parking_act)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"IOT CAR", None))
        self.real_img.setText("")
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"start", None))
        self.btn_auto_parking.setText(QCoreApplication.translate("MainWindow", u"auto_parking", None))
        self.btn_refind_path.setText(QCoreApplication.translate("MainWindow", u"refind_path", None))
        self.virtual_img.setText("")
        self.check_free_space.setText("")
    # retranslateUi

