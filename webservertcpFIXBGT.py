from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 6789
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:], 'rb')                                            # mode 'rb' (read binary) untuk membuka file dalam mode biner.
        outputdata = f.read()

        # Determine the content type based on the file extension
        if filename.endswith('.html'):                                         
            content_type = "text/html"                                          #membuka konten tipe text
        elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
            content_type = "image/jpeg"                                         #membuka konten tipe jpeg
        elif filename.endswith('.png'):
            content_type = "image/png"                                          #membuka konten tipe png
        else:
            content_type = "text/html"                                          # Default content type jika tidak terdapat kondisi yang sesuai

        # Send HTTP headers with the appropriate content type
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send(f"Content-Type: {content_type}\r\n\r\n".encode())

        # Send the content of the requested file to the client
        connectionSocket.sendall(outputdata)
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        connectionSocket.close()

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
