import socket, os, time
from shutil import copyfile
from datetime import datetime, timedelta

max_video_wait_time = 30
acync_process = None
connection_socket = socket.socket()
host = socket.gethostname()
port = 11111
default_temp_video_file_location = "opt/bin/video/temp/temp_video.mp4"
default_video_file_location = "opt/bin/video/video.mp4"
connection_socket.bind((host, port))
buffer_size = 1024
connection_socket.listen(5)
while True:
    connection, address = connection_socket.accept()
    print('Got connection from', address)
    command = str(connection.recv(buffer_size))
    if 'START_VIDEO' in command:
        command = command[len('START_VIDEO')+4:len(command)-2] + " %s &" % default_temp_video_file_location
        os.system(command)
    elif 'STOP_VIDEO' in command:
        command = command[len('STOP_VIDEO')+4:len(command)-2]
        os.system(command)
        if os.path.isfile(default_temp_video_file_location):
            start_time = datetime.now()
            while True:
                copyfile(default_temp_video_file_location, default_video_file_location)
                time.sleep(1)
                if os.path.getsize(default_video_file_location) == os.path.getsize(default_temp_video_file_location):
                    break
                if datetime.now() - start_time > timedelta(seconds=max_video_wait_time):
                    break
            file_obj = open(default_video_file_location, 'rb')
            file_bytes = file_obj.read(buffer_size)
            while file_bytes:
                connection.send(file_bytes)
                file_bytes = file_obj.read(buffer_size)
            file_obj.close()
            time.sleep(1)
            os.remove(default_temp_video_file_location)
            time.sleep(1)
            os.remove(default_video_file_location)
    connection.close()

