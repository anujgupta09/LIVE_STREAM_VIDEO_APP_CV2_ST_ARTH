# These program transfer and recieve data simultaneously (client as well as server)
# in the send function put details of yur system ip port to create socket 

import socket,cv2,pickle,struct,threading     # importing necessary libraries

def send():

  server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  my_ip = '192.168.43.131'
  my_port = 9999
  socket_address = (my_ip,my_port)

  server_socket.bind(socket_address)

  server_socket.listen(5)
  print("System listening to form CONNECTION on  :  ",socket_address , "  <<<<<<<  your system")


  while True:
    client_socket,addr = server_socket.accept()
    print('CONNECTED WITH >>>>>   ',addr,  "   <<<<< other systems address")
    if client_socket:
      vid = cv2.VideoCapture(0)
        
      while(vid.isOpened()):
        img,frame = vid.read()
        a = pickle.dumps(frame)
        message = struct.pack("Q",len(a))+a
        client_socket.sendall(message)
            
        cv2.imshow('>>>>>>>>>>> ANUJ GUPTA <<<<<<<<<<<<',frame)
        key = cv2.waitKey(1) & 0xFF
        if key ==ord('q'):
          client_socket.close()


#-----------------------------------------------------------------------------------------------------------------------------------------------------------


def recieve():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.43.26'
    port = 9999
    client_socket.connect((host_ip,port))
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4096)
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
    
        while len(data) < msg_size:
            data += client_socket.recv(4096)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow(">>>>>>>>>>>>> NITESH GUPTA CALL  (   ( ( CONNECTED )  )   )  <<<<<<<<<<<<",frame)
        key = cv2.waitKey(1) & 0xFF
        if key  == ord('q'):
            break
    client_socket.close()

# implementing multi threading for both side connection (( sending and recieving at the same time ))

send123=threading.Thread(target=send)
recieve123=threading.Thread(target=recieve)

send123.start()
recieve123.start()