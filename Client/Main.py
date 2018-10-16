import sys
from PyQt4 import QtCore
from PyQt4.QtGui import *
from os.path import exists
from os import mkdir, getcwd
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
        except FileNotFoundError:
            self.path = "."
            pass

    def btn_path_clicked(self):
        path = QFileDialog.getExistingDirectory(self, options = QFileDialog.ShowDirsOnly)

        if path == "":
            return

        self.input_path.setText(path)
        self.path = path
        with open("path.txt", "w") as f:
            f.write(self.path)

    def btn_connect_clicked(self):
        def connect():
            with socket.socket() as sock:
                self.label_connect.setText("연결 중...")
                self.input_IP.setEnabled(True)
                self.btn_connect.setEnabled(False)
                self.btn_disconnect.setEnabled(False)
                
                try:
                    sock.connect((self.input_IP.text(), 9009))
                except TimeoutError:
                    self.label_connect.setText("잘못된 IP 주소")
                    return
                except Exception as e:
                    self.label_connect.setText("오류 발생")
                    print(e)
                    return
                else:
                    self.label_connect.setText("접속 완료")
                    self.input_IP.setEnabled(False)
                    sock.sendall(".".encode())

                    data = literal_eval(sock.recv(1024).decode())
                    self.list_item.clear()
                    self.list_item.addItems(data)
                finally:
                    self.btn_connect.setEnabled(True)
                    self.btn_disconnect.setEnabled(True)
                    self.input_file.setText("")

        t = threading.Thread(target = connect)
        t.start()

    def btn_disconnect_clicked(self):
        self.label_connect.setText("접속 대기 중...")
        self.input_IP.setEnabled(True)
        self.input_IP.setText("")
        self.list_item.clear()
        self.input_file.setText("")

    def btn_download_clicked(self):
        def download():
            with socket.socket() as sock:
                fileName = self.input_file.text()
                if fileName == "":
                    return

                self.label_download.setText("서버와 연결 대기 중...")
                self.btn_download.setEnabled(False)
                
                try:
                    sock.connect((self.input_IP.text(), 9009))
                except OSError:
                    self.label_download.setText("서버와 접속되지 않음")
                    self.btn_download.setEnabled(True)
                    return
                except Exception as e:
                    self.label_download.setText("오류 발생")
                    self.btn_download.setEnabled(True)
                    print(e)
                    return

                sock.sendall(fileName.encode())
                
                self.label_download.setText("파일 [%s] : 다운로드 중" % fileName)
                self.btn_path.setEnabled(False)
                self.btn_connect.setEnabled(False)
                self.btn_disconnect.setEnabled(False)
                self.list_item.setVisible(False)

                with open("%s/%s" % (self.path, fileName), "wb") as f:
                    try:
                        data = sock.recv(1024)
                        data_transfered = 0
                        while data:
                            progress = int((data_transfered / self.size) * 100)
                            self.bar_progress.setValue(progress)
                            
                            f.write(data)
                            data_transfered += len(data)
                            data = sock.recv(1024)
                        self.bar_progress.setValue(100)
                    except Exception as e:
                        print(e)
                        self.label_download.setText("파일 [%s] 전송 실패" % fileName)
                    else:
                        self.label_download.setText("다운로드 완료 [%s], 전송량 [%d Byte]" % (fileName, data_transfered))
                    finally:
                        self.btn_path.setEnabled(True)
                        self.btn_connect.setEnabled(True)
                        self.btn_disconnect.setEnabled(True)
                        self.list_item.setVisible(True)
                        self.btn_download.setEnabled(True)

        t = threading.Thread(target = download)
        t.start()

    def list_item_clicked(self, item):
        self.input_file.setText(item.text())
        with socket.socket() as sock:
            fileName = item.text()
            sock.connect((self.input_IP.text(), 9009))
            sock.sendall(str(":" + fileName).encode())
            self.size = int(sock.recv(1024).decode())
            self.label_download.setText("파일 [%s]의 크기 : [%s Byte]" % (fileName, self.size))
            self.bar_progress.setValue(0)

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = XDialog(window)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
