from azure.storage.blob import BlobServiceClient
from azure.iot.device import IoTHubDeviceClient
from threading import Thread
import time

class CloudConnection(Thread):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        # ket noi toi iot hub
        self.CONNECTION_STRING = "HostName=iothubfota.azure-devices.net;DeviceId=raspberry;SharedAccessKey=U2cxEvr04sn36+GusEwCF+Uj3pgz5X8M50x9/6eIhgI="

        # Kết nối tới Azure Storage Account
        self.connection_string = "DefaultEndpointsProtocol=https;AccountName=fotacloudstorage;AccountKey=aozpWuq3QLgGjDXLNUlECc4t5OZ8iBHf0kYFJ7xIJSyLFqr4uVKigdb2SuvpKd8ZL/7iQ5hhowXI+AStEdDfNw==;EndpointSuffix=core.windows.net"
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        # Tên container cần kiểm tra
        self.container_name = "firmwarestorage"
        # Lưu trữ danh sách tên file trước đó
        self.previous_files = []

        # Biến đánh dấu lần đầu chạy
        self.first_run = True

    def get_file_names(self):
        container_client = self.blob_service_client.get_container_client(self.container_name)
        blobs = container_client.list_blobs()
        file_names = [blob.name for blob in blobs]
        return file_names
    
    def run(self):
        
        self.current_files = self.get_file_names()

        # Kiểm tra sự thay đổi nếu không phải lần đầu chạy
        if not self.first_run:
            added_files = [file for file in self.current_files if file not in self.previous_files]
            
            # In ra thông báo nếu có sự thay đổi
            if added_files:
                print("Đã phát hiện sự thay đổi trong container")
                print("Các file mới được thêm:")
                for file in added_files:
                    print(file)
                    # Hỏi người dùng có muốn tải xuống file hay không
                    user_input = input("Bạn có muốn tải xuống file này? (y/n): ")
                    if user_input.lower() == 'y':
                        # Tải xuống file
                        container_client = self.blob_service_client.get_container_client(self.container_name)
                        blob_client = container_client.get_blob_client(file)
                        with open(file, "wb") as f:
                            f.write(blob_client.download_blob().read())
                        print("File đã được tải xuống thành công!")
                        device_client= IoTHubDeviceClient.create_from_connection_string(self.CONNECTION_STRING)
                        device_client.connect()
                        message= "Da download firmware moi thanh cong"
                        device_client.send_message(message)
                        device_client.disconnect()
                        
        # Lưu trữ danh sách tên file hiện tại để so sánh trong lần kiểm tra tiếp theo
        self.previous_files = self.current_files

        # Đánh dấu lần đầu chạy đã qua
        self.first_run = False

        # Đợi một khoảng thời gian trước khi kiểm tra lại
        time.sleep(3)  # Đợi 60 giây (có thể điều chỉnh thời gian theo nhu cầu)
