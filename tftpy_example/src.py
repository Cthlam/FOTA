from tftpy import TftpClient


Server_ip = "192.168.1.24"
local_file = "FileToSend.txt"               # Put filename here
FILE = open(".\\" + local_file)
remote_destination = "file_received.bin"    # Only given if want to save the file in a different name

client = TftpClient(host=Server_ip, port=69)
client.upload(local_file,FILE)