import socket
from os.path import exists
from os import mkdir

def get_file(fileName):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(fileName.encode())

        data = sock.recv(1024)
        if not data:
            print("파일 [%s] : 서버에 존재하지 않거나 전송중 오류 발생" % fileName)
            return

        if not exists(path):
            mkdir(path)
            print("%s 폴더 생성" % path)

        with open("%s/%s" % (path, fileName), "wb") as f:
            try:
                data_transfered = 0
                
                while data:
                    f.write(data)
                    data_transfered += len(data)
                    data = sock.recv(1024)

            except Exception as e:
                print("파일 [%s] 전송 실패" % fileName)
                print(e)

            else:
                directory = "D:/Download/%s" % fileName
                print("전송 완료 [%s], 전송량 [%d]" % (directory, data_transfered))

def get_fileList():
    with socket.socket() as sock:
        sock.connect((host, port))
        sock.sendall(".".encode())
        
        data = sock.recv(1024)
        print(data.decode())

def wait():
    while True:
        try:
            fileName = input("다운로드 받을 파일 이름을 입력하세요. << ")
            if not fileName == "":
                # get_file(fileName)
                get_fileList()
                print()
                
        except KeyboardInterrupt:
            print("파일 다운로드를 종료합니다.")
            return

try:
    with open("path.txt", "r") as f:
        path = f.read()
except FileNotFoundError:
    path = input("파일 다운로드를 원하는 경로를 입력해주세요. 슬래시(/)로 구분합니다. << ")
    with open("path.txt", "w") as f:
        f.write(path)

host = input("파일 서버의 IP 주소를 입력해주세요. << ")
port = 9009

print("파일 다운로드를 시작합니다.")
print("파일 다운로드를 끝내려면 Ctrl + C를 누르세요.")
wait()
