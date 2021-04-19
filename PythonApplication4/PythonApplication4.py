import serial
import struct 

ser = serial.Serial("COM4",115200,timeout = 0.1)
b_reply = ser.read(23) 
#b_reply = ser.read_all()

print(b_reply)
#reply =struct.unpack('23B',b_reply)
reply=b_reply.decode()
print(reply)
ser.close()
#reply=list(reply)
print(reply.split("\r\n"))



        

    
    



