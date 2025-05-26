import socket

def send_and_recieve(sock, message, server_address):
    sock.sttimeout(5)#set timeout of 5 seconds
    retries =5
    while retries>0:
        try:
            sock.sendto(message.encode(),server_address)
            response, _ = sock.recvfrom(4096)
            return response.decode()
        except socket.timeout:
            print("Timeout, retrying...")
            retries -=1
            return None
        def main(hostname, posrt,file_list):
            server_address = (hostname,port)
            client_socket = socket.socker(socket.AF_INET,socket.SOCK_DGRAM)

            for file_name in files_to_download:
                request = f"DOWNLOAD{file_name}"
                response=send_an_recieve(client_socket,request,server_address)

                if response and response.startwith("ok"):
                    print(f"recieved:{response}")
                     # Next steps: handle file chunk downloading here
    else:
        print(f"error or no response:{response}")
        if __name__=="__main__":
            import sys
            if len(sys.argv) !=4:
                print("usafe:python UDPclient.py <hostname> <port> <file_list>")
            else:
                main(sys.argv[1],int(sys.argv[2]), sys.argv[3])
