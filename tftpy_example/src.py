from tftpy import TftpClient


Server_ip = "192.168.0.123"
local_file = ""                             # Put filename here
remote_destination = "file_received.bin"    # Only given if want to save the file in a different name

client = TftpClient(host=Server_ip, port=69)
client.upload(local_file)