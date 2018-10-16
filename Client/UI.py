# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\user\Desktop\FileDownloader\Networt-DB-Project\Client/design.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_FileDownloader(object):
    def setupUi(self, FileDownloader):
        FileDownloader.setObjectName(_fromUtf8("FileDownloader"))
        FileDownloader.resize(480, 640)
        FileDownloader.setMinimumSize(QtCore.QSize(480, 640))
        FileDownloader.setMaximumSize(QtCore.QSize(480, 640))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("나눔고딕"))
        font.setPointSize(12)
        FileDownloader.setFont(font)
        FileDownloader.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.MainWidget = QtGui.QWidget(FileDownloader)
        self.MainWidget.setMinimumSize(QtCore.QSize(480, 640))
        self.MainWidget.setMaximumSize(QtCore.QSize(480, 640))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("나눔고딕"))
        font.setPointSize(12)
        self.MainWidget.setFont(font)
        self.MainWidget.setAutoFillBackground(False)
        self.MainWidget.setObjectName(_fromUtf8("MainWidget"))
        self.input_IP = QtGui.QLineEdit(self.MainWidget)
        self.input_IP.setGeometry(QtCore.QRect(10, 50, 241, 31))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_IP.sizePolicy().hasHeightForWidth())
        self.input_IP.setSizePolicy(sizePolicy)
        self.input_IP.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.input_IP.setInputMask(_fromUtf8(""))
        self.input_IP.setText(_fromUtf8(""))
        self.input_IP.setMaxLength(15)
        self.input_IP.setFrame(True)
        self.input_IP.setEchoMode(QtGui.QLineEdit.Normal)
        self.input_IP.setObjectName(_fromUtf8("input_IP"))
        self.btn_connect = QtGui.QPushButton(self.MainWidget)
        self.btn_connect.setEnabled(True)
        self.btn_connect.setGeometry(QtCore.QRect(260, 50, 61, 31))
        self.btn_connect.setFlat(False)
        self.btn_connect.setObjectName(_fromUtf8("btn_connect"))
        self.label_connect = QtGui.QLabel(self.MainWidget)
        self.label_connect.setGeometry(QtCore.QRect(330, 50, 141, 31))
        self.label_connect.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_connect.setObjectName(_fromUtf8("label_connect"))
        self.btn_download = QtGui.QPushButton(self.MainWidget)
        self.btn_download.setGeometry(QtCore.QRect(370, 490, 101, 31))
        self.btn_download.setObjectName(_fromUtf8("btn_download"))
        self.label_download = QtGui.QLabel(self.MainWidget)
        self.label_download.setGeometry(QtCore.QRect(10, 530, 461, 61))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_download.sizePolicy().hasHeightForWidth())
        self.label_download.setSizePolicy(sizePolicy)
        self.label_download.setMaximumSize(QtCore.QSize(461, 71))
        self.label_download.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_download.setWordWrap(True)
        self.label_download.setObjectName(_fromUtf8("label_download"))
        self.input_file = QtGui.QLineEdit(self.MainWidget)
        self.input_file.setGeometry(QtCore.QRect(10, 490, 351, 31))
        self.input_file.setFocusPolicy(QtCore.Qt.NoFocus)
        self.input_file.setReadOnly(True)
        self.input_file.setObjectName(_fromUtf8("input_file"))
        self.input_path = QtGui.QLineEdit(self.MainWidget)
        self.input_path.setGeometry(QtCore.QRect(10, 10, 321, 31))
        self.input_path.setReadOnly(True)
        self.input_path.setObjectName(_fromUtf8("input_path"))
        self.btn_path = QtGui.QPushButton(self.MainWidget)
        self.btn_path.setGeometry(QtCore.QRect(340, 10, 131, 31))
        self.btn_path.setObjectName(_fromUtf8("btn_path"))
        self.list_item = QtGui.QListWidget(self.MainWidget)
        self.list_item.setEnabled(True)
        self.list_item.setGeometry(QtCore.QRect(10, 130, 461, 351))
        self.list_item.setFrameShape(QtGui.QFrame.StyledPanel)
        self.list_item.setFrameShadow(QtGui.QFrame.Sunken)
        self.list_item.setProperty("showDropIndicator", False)
        self.list_item.setObjectName(_fromUtf8("list_item"))
        self.label_desc = QtGui.QLabel(self.MainWidget)
        self.label_desc.setGeometry(QtCore.QRect(10, 99, 211, 31))
        self.label_desc.setObjectName(_fromUtf8("label_desc"))
        self.btn_disconnect = QtGui.QPushButton(self.MainWidget)
        self.btn_disconnect.setEnabled(True)
        self.btn_disconnect.setGeometry(QtCore.QRect(260, 89, 61, 31))
        self.btn_disconnect.setFlat(False)
        self.btn_disconnect.setObjectName(_fromUtf8("btn_disconnect"))
        self.bar_progress = QtGui.QProgressBar(self.MainWidget)
        self.bar_progress.setGeometry(QtCore.QRect(7, 602, 461, 21))
        self.bar_progress.setProperty("value", 0)
        self.bar_progress.setOrientation(QtCore.Qt.Horizontal)
        self.bar_progress.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.bar_progress.setObjectName(_fromUtf8("bar_progress"))
        FileDownloader.setCentralWidget(self.MainWidget)

        self.retranslateUi(FileDownloader)
        QtCore.QMetaObject.connectSlotsByName(FileDownloader)

    def retranslateUi(self, FileDownloader):
        FileDownloader.setWindowTitle(_translate("FileDownloader", "파일 다운로더", None))
        self.input_IP.setPlaceholderText(_translate("FileDownloader", "서버의 IP를 입력해주세요.", None))
        self.btn_connect.setText(_translate("FileDownloader", "접속", None))
        self.label_connect.setText(_translate("FileDownloader", "접속 대기 중...", None))
        self.btn_download.setText(_translate("FileDownloader", "다운로드", None))
        self.label_download.setText(_translate("FileDownloader", "다운로드 대기 중...", None))
        self.input_file.setPlaceholderText(_translate("FileDownloader", "다운로드 받을 파일을 더블클릭하세요.", None))
        self.input_path.setPlaceholderText(_translate("FileDownloader", "다운로드 디렉토리를 지정해주세요.", None))
        self.btn_path.setText(_translate("FileDownloader", "디렉토리 설정", None))
        self.label_desc.setText(_translate("FileDownloader", "서버의 공유 파일 리스트", None))
        self.btn_disconnect.setText(_translate("FileDownloader", "해제", None))
        self.bar_progress.setFormat(_translate("FileDownloader", "%p%", None))

