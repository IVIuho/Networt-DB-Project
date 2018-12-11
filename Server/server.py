import socketserver
from os.path import exists, isfile, getsize, join
from os import listdir, getcwd
import pymysql
import time

host = ""
port = 9009

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self): # 상대가 접속 요청을 할 때마다 실행이 됨
        fileName = self.request.recv(1024).decode() # 상대가 다운로드 받고 싶어하는 파일 이름을 수신함

        try:
            with open("shareDir.txt", "r") as f:
                shareDir = f.read()
        except FileNotFoundError:
            print("shareDir.txt 파일이 존재하지 않습니다. 서버를 껐다 다시 켜주십시오.")
            self.request.send(str([""]).encode())
            return

        if fileName.startswith(":"):
            func = fileName.replace(":", "").split()[0]
            arg = fileName.replace(":%s " % func, "")

            exec("self.%s(shareDir, arg)" % func)

        if not exists(join(shareDir, fileName)) or not isfile(join(shareDir, fileName)):
            return

        print("[%s] 연결됨" % self.client_address[0])
        print("[%s]에게 파일 [%s] 전송 시작..." % (self.client_address[0], fileName))
        startTime = time.time()
        
        conn = pymysql.connect(host = "localhost", user = "root", password = "root", autocommit = True, db = "downloadHistory", charset = "UTF8") # DB와 연결함
        cursor = conn.cursor() # 커서를 받아옴

        cursor.execute("select count from files where fileName = %s;", (fileName, )) # 커서를 통해서 명령어 입력, 인자로 튜플을 넣어줘야 한다.
        count = int(cursor.fetchone()[0]) # DB로부터 count를 받아온다

        cursor.execute("update files set count = %s where fileName = %s;", (count + 1, fileName)) # count + 1의 값으로 업데이트해준다.
        
        cursor.close() # 커서 객체의 연결을 끊음
        conn.close() # 커넥트 객체의 연결을 끊음

        try:
            with open(shareDir + "/" + fileName, "rb") as f:
                try:
                    data_transfered = self.request.sendfile(f)
                except Exception as e:
                    print("파일 [%s] 전송 실패" % fileName)
                    print(e)
                else:
                    _time = int(time.time() - startTime)
                    print("전송 완료 [%s], 전송량 [%s Byte]" % (fileName, data_transfered),
                        "전송 시간 : [%sh : %sm : %ss]" % (_time // 3600, (_time // 60) % 60, _time % 60), sep = "\n")

        except Exception as e:
            print("파일 [%s] 열기 실패" % fileName)
            print(e)

    def getFileList(self, *args):
        print("[%s] 파일 목록 요청" % self.client_address[0])
        data = listdir(args[0]) # 공유를 허용한 디렉토리의 파일 목록을 리스트로 받아옴
        self.request.send(str(data).encode()) # 리스트를 문자열로 변환하여 보냄

    def getFileSize(self, *args):
        print("[{}] [{}] 파일 용량 요청".format(self.client_address[0], args[1]))
        size = getsize(args[0] + "/" + args[1])
        self.request.send(str(size).encode())

def database_connect(shareDir):
    print("데이터베이스와 연결합니다.")

    conn = pymysql.connect(host = "localhost", user = "root", password = "root", autocommit = True, db = "downloadHistory", charset = "UTF8")
    cursor = conn.cursor()
    cursor.execute("set sql_notes = 0;")
    cursor.execute("create table if not exists files (fileName VARCHAR(50), count smallint, PRIMARY KEY (fileName));")
    
    fileList = listdir(shareDir)

    cursor.execute("select fileName from files;")
    temp = cursor.fetchall()
    sqlList = [i[0] for i in temp]

    for i in sqlList:
        if not i in fileList:
            cursor.execute("delete from files where fileName = %s;", (i, ))
            print("데이터베이스에서 %s를 지웠습니다." % i)

    for i in fileList:
        if not i in sqlList:
            cursor.execute("insert into files values (%s, %s);", (i, 0))
            print("데이터베이스에 %s를 추가했습니다." % i)

    cursor.close()
    conn.close()

def run_server():
    print("파일 서버를 시작합니다.")
    print("파일 서버를 끝내려면 Ctrl + C를 누르세요.")

    try:
        server = socketserver.ThreadingTCPServer((host, port), TCPHandler) # server = FileServer((host, port), TCPHandler)
        print(server.server_address)
        server.serve_forever()
    except KeyboardInterrupt:
        print("파일 서버를 종료합니다.")
        server.shutdown()
        server.server_close()

def main():
    try:
        with open("shareDir.txt", "r") as f:
            shareDir = f.read()
    except FileNotFoundError:
        with open("shareDir.txt", "w") as f:
            shareDir = input("공유를 원하는 경로를 입력해주세요. >> ")
            f.write(shareDir)

    database_connect(shareDir)
    run_server()
    
if __name__ == "__main__":    
    main()
