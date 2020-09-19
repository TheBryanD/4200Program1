import socket
import struct
import sys


#creates packets of data to send
def createPacket(format, version, type, message):
    structInfo = struct.Struct(format)
    length = len(message)
    packedInfo = struct.pack(format, version, type, length, message.encode("UTF-8"))
    return packedInfo

#Lighton function
def Lighton():
    print("Lights are now on.")

#Lightoff function
def Lightoff():
    print("Lights are now off.")

while True:
    port = 0

    #step 1 - create the socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Parse command line arguments
    try:
        port = sys.argv[1]
        logFile = sys.argv[2]
        file = open(logFile, "a")

    except:
        print("Invalid command line arguments: Server.py <port> <logFile>")
        sys.exit(0)

    #step 2 - specify where the server should listen on, IP and port
    server_addr_obj = ('127.0.0.1', int(port))
    print("Address : ", server_addr_obj)
    print("Port : ", port)
    sock.bind(server_addr_obj)

    #step 3 - do the listening
    sock.listen(1)

    #step 4 - wait for the connection from client
    print("Waiting for connection from client.")
    connection_obj, client_addr = sock.accept()

    file.write("Received connection from {0}\n".format(client_addr))

    print("Client connected, address is: ", client_addr)

    #step 5 - keep listening
    unpacker = struct.Struct('iii8s')
    format = "iii8s"
    with connection_obj as conn_obj:
        try: 
            while True:
                packed_data = conn_obj.recv(unpacker.size)
                data = unpacker.unpack(packed_data)
                print("Received Data : Version: {0}, Message_Type: {1}, Length: {2}".format( data[0], data[1], data[2]))
                message = data[3].decode("utf-8").strip().strip('\x00')
                print("Message: ", message)
                if(message.rstrip() == "Hello" and data[0] == 17):
                    print("Sent: Hello")
                    file.write("Hello sent from client.\n")
                    helloPacket = createPacket(format, 17, 1, "Hello")
                    conn_obj.sendall(helloPacket)
                if(data[0] == 17):
                    if(data[1] == 1):
                        print("EXECUTING SUPPORTED COMMAND: LIGHTON")
                        file.write("EXECUTING SUPPORTED COMMAND: LIGHTON\n")
                        Lighton()
                        successPacket = createPacket(format, 17, 1, "SUCCESS")
                        conn_obj.sendall(successPacket)
                    elif(data[1] == 2):
                        print("EXECUTING SUPPORTED COMMAND: LIGHTOFF")
                        file.write("EXECUTING SUPPORTED COMMAND: LIGHTOFF\n")
                        Lightoff()
                        successPacket = createPacket(format, 17, 1, "SUCCESS")
                        conn_obj.sendall(successPacket)
                    else:
                        file.write("IGNORING UNKNOWN COMMAND: {0}\n".format(data[1]))
                        print("Error unsupported type.")
                    print("")
                else: 
                    print("Error: VERSION MISSMATCH")
                    file.write("ERROR: VERSION MISSMATCH\n")
                    print("")

  
        except KeyboardInterrupt: #CTRL+^C
            sock.close()
            file.close()
        except:
            sock.close()
            file.close()