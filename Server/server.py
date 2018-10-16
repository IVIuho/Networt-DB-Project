import socketserver
from os.path import exists, isfile, getsize
from os import listdir, getcwd
import pymysql

host = ""
port = 9009

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self): # 상대가 접속 요청을 할 때마다 실행이 됨
        print("[%s] 연결됨" % self.client_address[0])
        fileName = self.request.recv(1024).decode() # 상대가 다운로드 받고 싶어하는 파일 이름을 수신함

        try:
            with open("shareDir.txt", "r") as f:
                shareDir = f.read()
        except FileNotFoundError:
            print("shareDir.txt 파일이 존재하지 않습니다. 서버를 껐다 다시 켜주십시오.")
            self.request.send(str([""]).encode())
            return

        if fileName.startswith(":"):
            size = getsize(shareDir + "/" + fileName.replace(":", ""))
            self.request.send(str(size).encode())

        if fileName == ".":
            data = listdir(shareDir) # 공유를 허용한 디렉토리의 파일 목록을 리스트로 받아옴
            self.request.send(str(data).encode()) # 리스트를 문자열로 변환하여 보냄

        if not exists(shareDir + "/" + fileName) or not isfile(shareDir + "/" + fileName):
            return

        print("[%s]에게 파일 [%s] 전송 시작..." % (self.client_address[0], fileName))
        
        conn = pymysql.connect(host = "localhost", user = "root", password = "root", db = "downloadHistory", charset = "UTF8")
        cursor = conn.cursor()
        
        cursor.execute("select count from files where fileName = %s;", (fileName, ))
        count = int(cursor.fetchone()[0])

        cursor.execute("update files set count = %s where fileName = %s;", (count + 1, fileName))
        conn.commit()
        
        cursor.close()
        conn.close()

        try:
            with open(shareDir + "/" + fileName, "rb") as f:
                try:
                    data_transfered = 0
                    data = f.read()

                    while data:
                        data_transfered += self.request.send(data)
                        data = f.read(1024)
                except Exception as e:
                    print("파일 [%s] 전송 실패" % fileName)
                    print(e)

                else:
                    print("전송 완료 [%s], 전송량 [%d Byte]" % (fileName, data_transfered))

        except Exception as e:
            print("파일 [%s] 열기 실패" % fileName)
            print(e)

class FileServer(socketserver.TCPServer, socketserver.ThreadingMixIn):
    pass

def database_connect(shareDir):
    print("데이터베이스와 연결합니다.")

    conn = pymysql.connect(host = "localhost", user = "root", password = "root", db = "downloadHistory", charset = "UTF8")
    cursor = conn.cursor()
    cursor.execute("create table if not exists files (fileName VARCHAR(50), count smallint, PRIMARY KEY (fileName));")
    
    sqlList = list()
    fileList = listdir(shareDir)

    cursor.execute("select fileName from files;")
    temp = cursor.fetchall()
    for i in temp:
        sqlList.append(i[0])

    print(sqlList)
    print(fileList)

    for i in sqlList:
        if not i in fileList:
            cursor.execute("delete from files where fileName = %s;", (i, ))
            print("데이터베이스에서 %s를 지웠습니다." % i)

    for i in fileList:
        if not i in sqlList:
            cursor.execute("insert into files values (%s, %s);", (i, 0))
            print("데이터베이스에 %s를 추가했습니다." % i)

    conn.commit()

    cursor.close()
    conn.close()

def run_server():
    print("파일 서버를 시작합니다.")
    print("파일 서버를 끝내려면 Ctrl + C를 누르세요.")

    try:
        server = FileServer((host, port), TCPHandler)
        print(server.server_address)
        server.serve_forever()

    except KeyboardInterrupt:
        print("파일 서버를 종료합니다.")
        server.shutdown()
        server.server_close()

try:
    with open("shareDir.txt", "r") as f:
        shareDir = f.read()
except FileNotFoundError:
    with open("shareDir.txt", "w") as f:
        shareDir = input("공유를 원하는 경로를 입력해주세요. >> ")
        f.write(shareDir)

database_connect(shareDir)
run_server()
