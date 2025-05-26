import socket
import base64

#function to reliably send and recieve messages 
def send_and_recieve(sock, message, server_address):
    
    retries =5 #number of retries 
    timeout =3 #initial timeout in seconds 
    


    while retries>0:
        try:
            sock.sendto(message.encode(),server_address)
            response, _ = sock.recvfrom(4096)
            return response.decode()
        except socket.timeout:
            print("Timeout, retrying...")
            retries -=1
            timeout +=2
    return None
def download_file(server_hostname, server_port,file_name):
     #create UPD socket
    server_address = (server_hostname,server_port)
    client_socket = socket.socker(socket.AF_INET,socket.SOCK_DGRAM)

    #send initial download request 
    response = send_and_recieve(client_socket, f"DOWNLOAD {filename}") 

    if not response:
        print(f"server not responding, failed to download {filename}")
        return
    
    if response.startswith("ERR"):
        print(f"server responded:{response}")
        return
            
    #Extract file details from server's ok response 
    _,_,_,filesize, _, transfer_port = response.split()
    filesize = int(filesize)
    transfer_port = int(transfer_port)
    print (f"File '{file_name}' of size {filesize} bytes will be downloaded from port {transfer_port}")

    #connects to the new transfer port
    transfer_address = (server_hostname, transfer_port)
    bytes_recieved =0
    chunk_size = 1000 #bytes
    local_fiename = f"downloaded_{file_name}"

    with open(local_fiename, "wb") as file:
        while bytes_received < filesize:
            start = bytes_recieved
            end = min(bytes_received + chunk_size - 1, filesize - 1)

            chunk_request = f"FILE {file_name} GET START {start} END {end}"
            chunk_response = send_and_recieve(client_socket, chunk_request, transfer_address)

            if not chunk_response:
                print("Failed to receive chunk. Aborting.")
                return

            parts = chunk_response.split(" DATA ")
            header, encoded_data = parts[0], parts[1]

            # Decode Base64 data and write to file
            data_bytes = base64.b64decode(encoded_data)
            file.write(data_bytes)

            bytes_received += len(data_bytes)
            print(f"Received bytes {start}-{end} (Total received: {bytes_received}/{filesize})")

          # After file fully received, send CLOSE message
        close_response = send_and_recieve(client_socket, f"FILE{file_name} CLOSE", transfer_address)
        if close_response and close_response.endswith("CLOSE_OK"):
            print(f"Successfully downloaded '{filename}'")
        else:
            print("Error closing the file transfer.")

    client_socket.close()

def main(hostname, port, file_list):
    with open(file_list, "r") as file:
        filenames = file.read().splitlines()

    for filename in filenames:
        print(f"Starting download: {filename}")
        download_file(hostname, port, filename)
        print("\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python UDPclient.py <hostname> <port> <file_list>")
    else:
        main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
