import socketserver
from os.path import exists, isfile
from os import listdir, getcwd

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

        if fileName == ".":
            data = listdir(shareDir) # 공유를 허용한 디렉토리의 파일 목록을 리스트로 받아옴
            self.request.send(str(data).encode()) # 리스트를 문자열로 변환하여 보냄

        if not exists(shareDir + "/" + fileName) or not isfile(shareDir + "/" + fileName):
            return

        print("[%s]에게 파일 [%s] 전송 시작..." % (self.client_address[0], fileName))
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
                    print("전송 완료 [%s], 전송량 [%d]" % (fileName, data_transfered))

        except Exception as e:
            print("파일 [%s] 열기 실패" % fileName)
            print(e)

class FileServer(socketserver.TCPServer, socketserver.ThreadingMixIn):
    pass

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

run_server()
