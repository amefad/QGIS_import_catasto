# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_importa_imu.ui'
#
# Created: Mon Jun 03 11:12:31 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_importa_imu(object):
    def setupUi(self, importa_imu):
        importa_imu.setObjectName(_fromUtf8("importa_imu"))
        importa_imu.resize(451, 553)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(importa_imu.sizePolicy().hasHeightForWidth())
        importa_imu.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        importa_imu.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        importa_imu.setWindowIcon(icon)
        importa_imu.setAutoFillBackground(True)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.dockWidgetContents)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 431, 22))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.filtercombobox = QtGui.QComboBox(self.dockWidgetContents)
        self.filtercombobox.setGeometry(QtCore.QRect(50, 10, 391, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filtercombobox.sizePolicy().hasHeightForWidth())
        self.filtercombobox.setSizePolicy(sizePolicy)
        self.filtercombobox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.filtercombobox.setFont(font)
        self.filtercombobox.setObjectName(_fromUtf8("filtercombobox"))
        self.Listafile = QtGui.QTreeView(self.dockWidgetContents)
        self.Listafile.setGeometry(QtCore.QRect(10, 90, 431, 381))
        self.Listafile.setSortingEnabled(False)
        self.Listafile.setObjectName(_fromUtf8("Listafile"))
        self.selPath = QtGui.QLineEdit(self.dockWidgetContents)
        self.selPath.setGeometry(QtCore.QRect(60, 480, 291, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selPath.setFont(font)
        self.selPath.setObjectName(_fromUtf8("selPath"))
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setGeometry(QtCore.QRect(10, 480, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.selButton = QtGui.QPushButton(self.dockWidgetContents)
        self.selButton.setGeometry(QtCore.QRect(360, 480, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selButton.setFont(font)
        self.selButton.setObjectName(_fromUtf8("selButton"))
        self.radioUpdateImport = QtGui.QRadioButton(self.dockWidgetContents)
        self.radioUpdateImport.setGeometry(QtCore.QRect(20, 50, 431, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioUpdateImport.setFont(font)
        self.radioUpdateImport.setObjectName(_fromUtf8("radioUpdateImport"))
        importa_imu.setWidget(self.dockWidgetContents)

        self.retranslateUi(importa_imu)
        QtCore.QObject.connect(self.Listafile, QtCore.SIGNAL(_fromUtf8("activated(QModelIndex)")), self.selPath.paste)
        QtCore.QMetaObject.connectSlotsByName(importa_imu)

    def retranslateUi(self, importa_imu):
        importa_imu.setWindowTitle(QtGui.QApplication.translate("importa_imu", "Importa file SOG TIT FAB TER", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("importa_imu", "Filtro", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("importa_imu", "file:", None, QtGui.QApplication.UnicodeUTF8))
        self.selButton.setText(QtGui.QApplication.translate("importa_imu", "Vai", None, QtGui.QApplication.UnicodeUTF8))
        self.radioUpdateImport.setText(QtGui.QApplication.translate("importa_imu", "Importa tutti i file cxf insieme ", None, QtGui.QApplication.UnicodeUTF8))

