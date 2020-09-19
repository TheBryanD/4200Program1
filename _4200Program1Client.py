import socket
import struct
import sys
import time


#creates packets of data to send
def createPacket(format, version, type, message):
    structInfo = struct.Struct(format)
    length = len(message)
    packedInfo = struct.pack(format, version, type, length, message.encode("UTF-8"))
    return packedInfo

#step 1 - create the socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#Parse command line arguments
try:
    ip = sys.argv[1]
    port = int(sys.argv[2])
    logFile = sys.argv[3]
    file = open(logFile, "a")
except Exception as ex:
    print("Invalid command line arguments: Client.py <ip> <port> <log file>")
    print(ex)
    sys.exit(0)


#step 2 - Connect
server_addr = (ip, port)
print("Connecting to {0}...".format(server_addr))

sock.connect(server_addr)

print("Connected to: ", server_addr)

#create struct
format = "iii8s"
packedInfo = createPacket(format, 17, 1, "Hello")
#print("This is the packed struct: ", packedInfo)

#step 3 - send Binary data
print("Sending: ", packedInfo)
sock.sendall(packedInfo)

#Receive Hello Packet from server
unpacker = struct.Struct('iii8s')
packed_data = sock.recv(unpacker.size)
data = unpacker.unpack(packed_data)
print("Received Data : Version: {0}, Message_Type: {1}, Length: {2}".format( data[0], data[1], data[2]))
message = data[3].decode('utf-8').strip().strip('\x00')
print("Received Message: ", message)
if(data[0] == 17):
    file.write("VERSION ACCEPTED\n")
    packedInfo = createPacket(format, 17, 2, "LIGHTOFF")
    sock.sendall(packedInfo)
else:
    file.write("VERSION MISMATCH\n")


packed_data = sock.recv(unpacker.size)
data = unpacker.unpack(packed_data)
print("Received Data : Version: {0}, Message_Type: {1}, Length: {2}".format( data[0], data[1], data[2]))
message = data[3].decode('utf-8').strip().strip('\x00')
print("Received Message: ", message)
file.write("Message Received: {0}\n".format(message))




time.sleep(1)
print("Closing Socket")
sock.close()
file.close()
