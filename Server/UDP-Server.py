import socket 
import threading 
import os
import random
import base64

def client_handler (client_address, file_name, server_socket):
    #choosing the port
    transfer_port=random.randint(20000,51000)

    #creat socket for file transfer
    transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    transfer_socket.bind(('',transfer_port))

    if not os.path.isfile(file_name):
        response = f"ERR {file_name} NOT_FOUND"
        server_socket.sendto(response.encode(), client_address)
        return
    
    filesize = os.path.getsize(file_name)
    response = f"OK {file_name} SIZE {filesize} PORT {transfer_port}"
    server_socket.sendto(response.encode(), client_address)

    # Start sending file in chunks
    def main (server_port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('', server_port))
        print(f"server listening on port {server_port}")

        while True:
            message, client_addres = server_socket.recvfrom(1024)
            decoded_msg = message.decode()
            if decoded_msg.startswith("DOWNLOAD"):
                _, filename = decoded_msg.split()
                threading.Thread(target=client_handler, args=(client_address, file_name,server_socket)).start()

                if __name__=="__main__":
                    import sys
                    if len(sys.argv) !=2:
                        print ("usage:python UDPserver.py<port>")
                    else:
                        main(int(sys.argv[1]))


