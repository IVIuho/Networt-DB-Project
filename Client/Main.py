import sys
from PyQt4 import QtCore
from PyQt4.QtGui import *
import socket
from ast import literal_eval
import threading

import UI

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class XDialog(QDialog, UI.Ui_FileDownloader):
    def __init__(self, window):
        QDialog.__init__(self)
        self.setupUi(window)
        QtCore.QObject.connect(self.btn_path, QtCore.SIGNAL(_fromUtf8("clicked()")), self.btn_path_clicked)
        QtCore.QObject.connect(self.btn_connect, QtCore.SIGNAL(_fromUtf8("clicked()")), self.btn_connect_clicked)
        QtCore.QObject.connect(self.btn_disconnect, QtCore.SIGNAL(_fromUtf8("clicked()")), self.btn_disconnect_clicked)
        QtCore.QObject.connect(self.btn_download, QtCore.SIGNAL(_fromUtf8("clicked()")), self.btn_download_clicked)
        QtCore.QObject.connect(self.list_item, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), self.list_item_clicked)

        try:
            with open("path.txt", "r") as f:
                self.path = f.read()
                self.input_path.setText(self.path)
                self.input_path.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        except FileNotFoundError:
            self.path = "."

    def btn_path_clicked(self):
        path = QFileDialog.getExistingDirectory(self, options = QFileDialog.ShowDirsOnly)

        if path == "":
            return

        self.input_path.setText(path)
        self.input_path.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.path = path
        with open("path.txt", "w") as f:
            f.write(self.path)

    def btn_connect_clicked(self):
        class subThread(QtCore.QThread):
            def __init__(self, gui, parent = None):
                super().__init__(parent)
                self.gui = gui
                
            def run(self):
                if self.gui.input_IP.text() == "":
                    return
                
                with socket.socket() as sock:
                    self.gui.label_connect.setText("연결 중...")
                    self.gui.label_connect.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                    self.gui.input_IP.setEnabled(False)
                    self.gui.btn_connect.setEnabled(False)
                    self.gui.btn_disconnect.setEnabled(False)
                    
                    try:
                        sock.connect((self.gui.input_IP.text(), 9009))
                    except TimeoutError:
                        self.gui.label_connect.setText("잘못된 IP 주소")
                        self.gui.label_connect.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                        self.gui.input_IP.setEnabled(True)
                        return
                    except OSError as e:
                        if e.errno == 10061:
                            self.gui.label_connect.setText("서버 오프라인")
                            self.gui.label_connect.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                            self.gui.input_IP.setEnabled(True)
                            return
                    except Exception as e:
                        self.gui.label_connect.setText("오류 발생")
                        self.gui.label_connect.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                        self.gui.input_IP.setEnabled(True)
                        print(e)
                        return
                    else:
                        self.gui.label_connect.setText("접속 완료")
                        self.gui.label_connect.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                        sock.sendall(":getFileList".encode())

                        data = literal_eval(sock.recv(1024).decode())
                        self.gui.btn_disconnect.setEnabled(True)
                        self.gui.list_item.clear()
                        self.gui.list_item.addItems(data)

                        for i in range(self.gui.list_item.count()):
                            self.gui.list_item.item(i).setTextColor(QColor(255, 255, 255))
                        # self.gui.list_item.item(self.gui.list_item.count() - 1).setTextColor(QColor(255, 255, 255)) 172.31.99.15
                        self.gui.btn_download.setEnabled(True)
                    finally:
                        self.gui.btn_connect.setEnabled(True)
                        self.gui.input_file.setText("")
                        self.gui.input_file.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                        self.gui.label_download.setText("다운로드 대기 중...")
                        self.gui.label_download.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                        
        t = subThread(self, self)
        t.start()

    def btn_disconnect_clicked(self):
        self.label_connect.setText("접속 대기 중...")
        self.label_connect.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.input_IP.setEnabled(True)
        self.input_IP.setText("")
        self.input_IP.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.btn_disconnect.setEnabled(False)
        self.list_item.clear()
        self.input_file.setText("")
        self.input_file.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.btn_download.setEnabled(False)
        self.label_download.setText("다운로드 대기 중...")
        self.label_download.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.label_progress.setText("0%")
        self.label_progress.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))

    def btn_download_clicked(self):
        class subThread(QtCore.QThread):
            def __init__(self, gui, path, size, parent = None):
                super().__init__(parent)
                self.gui = gui
                self.path = path
                self.size = size

            def run(self):
                with socket.socket() as sock:
                    fileName = self.gui.input_file.text()
                    if fileName == "":
                        return

                    self.gui.label_download.setText("서버와 연결 대기 중...")
                    self.gui.label_download.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                    self.gui.btn_download.setEnabled(False)
                    
                    try:
                        sock.connect((self.gui.input_IP.text(), 9009))
                    except OSError:
                        self.gui.label_download.setText("서버와 접속되지 않음")
                        self.gui.label_download.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                        self.gui.btn_download.setEnabled(True)
                        return
                    except Exception as e:
                        self.gui.label_download.setText("오류 발생")
                        self.gui.label_download.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                        self.gui.btn_download.setEnabled(True)
                        print(e)
                        return

                    sock.sendall(fileName.encode())
                    
                    self.gui.label_download.setText("파일 [%s] : 다운로드 중" % fileName)
                    self.gui.label_download.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                    self.gui.btn_path.setEnabled(False)
                    self.gui.btn_connect.setEnabled(False)
                    self.gui.btn_disconnect.setEnabled(False)
                    self.gui.list_item.setEnabled(False)

                    with open("%s/%s" % (self.path, fileName), "wb") as f:
                        try:
                            data = sock.recv(1024)
                            data_transfered = 0
                            while data:
                                progress = int((data_transfered / self.size) * 100)
                                self.gui.label_progress.setText("%s%%" % str(progress))
                                self.gui.label_progress.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                                    
                                f.write(data)
                                data_transfered += len(data)
                                data = sock.recv(1024)
                            self.gui.label_progress.setText("100%")
                            self.gui.label_progress.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                        except Exception as e:
                            print(e)
                            self.gui.label_download.setText("파일 [%s] 전송 실패" % fileName)
                            self.gui.label_download.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                        else:
                            self.gui.label_download.setText("다운로드 완료 [%s], 전송량 [%d Byte]" % (fileName, data_transfered))
                            self.gui.label_download.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
                        finally:
                            self.gui.btn_path.setEnabled(True)
                            self.gui.btn_connect.setEnabled(True)
                            self.gui.btn_disconnect.setEnabled(True)
                            self.gui.list_item.setEnabled(True)
                            self.gui.btn_download.setEnabled(True)

        t = subThread(self, self.path, self.size, self)
        t.start()

    def list_item_clicked(self, item):
        self.input_file.setText(item.text())
        self.input_file.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        with socket.socket() as sock:
            fileName = item.text()
            sock.connect((self.input_IP.text(), 9009))
            sock.sendall(str(":getFileSize {}").format(fileName).encode())
            self.size = int(sock.recv(1024).decode())
            self.label_download.setText("파일 [%s]의 크기 : [%s Byte]" % (fileName, self.size))
            self.label_download.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
            self.label_progress.setText("0%")
            self.label_progress.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = XDialog(window)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
