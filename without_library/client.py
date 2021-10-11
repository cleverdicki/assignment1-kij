# Modification from https://github.com/bozhu/AES-Python
import socket
import os
import sys
import numpy as np

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

try:
    s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
    )

    def sub_bytes(s):                               
        for i in range(4):
            for j in range(4):
                s[i][j] = s_box[s[i][j]]
        return s

    def shift_rows(s):                              
        s[1][0], s[1][1], s[1][2], s[1][3] = s[1][1], s[1][2], s[1][3], s[1][0]
        s[2][0], s[2][1], s[2][2], s[2][3] = s[2][2], s[2][3], s[2][0], s[2][1]
        s[3][0], s[3][1], s[3][2], s[3][3] = s[3][3], s[3][0], s[3][1], s[3][2]

    def add_round_key(s, k):                        
        for i in range(4):
            for j in range(4):
                s[i][j] ^= k[i][j]
        return s

    xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1) 

    def mix_single_column(a):                       
        t = a[0] ^ a[1] ^ a[2] ^ a[3]
        u = a[0]
        a[0] ^= t ^ xtime(a[0] ^ a[1])
        a[1] ^= t ^ xtime(a[1] ^ a[2])
        a[2] ^= t ^ xtime(a[2] ^ a[3])
        a[3] ^= t ^ xtime(a[3] ^ u)


    def mix_columns(s):                             
        for i in range(4):
            mix_single_column(s[i])
        numpy_array = np.array(s)
        transpose = numpy_array.T
        transpose_list = transpose.tolist()
        return transpose_list

    r_con = ((0x01, 0x00, 0x00, 0x00), (0x02, 0x00, 0x00, 0x00), 
            (0x04, 0x00, 0x00, 0x00),(0x08, 0x00, 0x00, 0x00),
            (0x10, 0x00, 0x00, 0x00), (0x20, 0x00, 0x00, 0x00),
            (0x40, 0x00, 0x00, 0x00),(0x80, 0x00, 0x00, 0x00),
            (0x1B, 0x00, 0x00, 0x00),(0x36, 0x00, 0x00, 0x00))

    def addbitwise(a,b):                            
        n=len(a)
        h=[0 for i in range(n)]
        for i in range(n):
            h[i]=a[i]^b[i]
        return h

    def subword(mat):                                
        for i in range(4):
            mat[i]=s_box[mat[i]]
        return mat

    def rotword(mat):                               
        mat[0],mat[1],mat[2],mat[3]=mat[1],mat[2],mat[3],mat[0]
        return mat


    def key_expansion(r_con,key):                   
        w=[0 for i in range(44)]
        for i in range(4):
            w[i]=[key[4*i],key[4*i+1],key[4*i+2],key[4*i+3]]
        for i in range(4,44):
            temp =[w[i-1][j] for j in range(4)]
            if i%4==0:
                temp=addbitwise(subword(rotword(temp)),r_con[int(i/4)-1])
            w[i]=addbitwise(w[i-4],temp)
        return w

    def tostate1(x):
        if type(x[0])==int:
          a1=[x[i] for i in range(0,13,4)]           
          a2=[x[i] for i in range(1,14,4)]
          a3=[x[i] for i in range(2,15,4)]
          a4=[x[i] for i in range(3,16,4)]
          state=[a1,a2,a3,a4]
        else:
           a1=[ord(x[i])-97 for i in range(0,13,4)]   
           a2=[ord(x[i])-97 for i in range(1,14,4)]
           a3=[ord(x[i])-97 for i in range(2,15,4)]
           a4=[ord(x[i])-97 for i in range(3,16,4)]
           state=[a1,a2,a3,a4]
        return state

    def toreal(state):                              
        y=[0 for i in range(16)]
        t=0
        for j in range(4):
            for i in range(4):
                y[t]=state[i][j]
                t=t+1
        return y

    def roundkeytomatrix(Roundkey,i):               
        w=[Roundkey[j] for j in range(i*4,4*i+4)]
        numpy_array = np.array(w)
        transpose = numpy_array.T
        transpose_list = transpose.tolist()
        return transpose_list


    def encrypt(x,Roundkey):
        state=tostate1(x)                             
        matkey=roundkeytomatrix(Roundkey,0)           
        state=add_round_key(state,matkey) 
        for i in range(1,10):
            state=sub_bytes(state)                    
            shift_rows(state)                         
            numpy_array = np.array(state)             
            transpose = numpy_array.T                 
            state = transpose.tolist()                
            state=mix_columns(state)                  
            matkey=roundkeytomatrix(Roundkey,i)       
            state=add_round_key(state,matkey)         

        state=sub_bytes(state)                        
        shift_rows(state)                             
        matkey=roundkeytomatrix(Roundkey,10)          
        state=add_round_key(state,matkey)             
        y=toreal(state)                                
        return y

    def start_ency(text,kunci):                            
        hasil=[]
        n=len(text)
        if n%16==0:                                   
            for i in range(int(n/16)):  
                x=text[16*i:16*i +16]                 
                hasil.append(encrypt(x,kunci))
        else:
            m=n%16
            for i in range(m):                        
              text.append(0x19)                       
            for i in range(int((n+m)/16)):
              x=text[16*i:16*i +16]                   
              hasil.append(encrypt(x,kunci))
        return hasil

    def check_file(file):
        while len(file) % 16 != 0:
            file = file + b'0'
        return file

    message = "plain_text.txt"
    filelocation = os.path.abspath(message)
    with open(filelocation, 'rb') as f:
        data = f.read()

    checked_data = check_file(data)

    key = [0x2b,0x7e,0x15,0x16,0x28,0xae,0xd2,0xa6,0xab,0xf7,0x15,0x88,0x09,0xcf,0x4f,0x3c]

    kunci = key_expansion(r_con, key)
    encrypted_data = start_ency(checked_data, kunci)
    data_send = bytes(encrypted_data[0])
    print(data_send)

    client_socket.send(data_send)
    sys.stdout.write('>> \n')
    sys.stdout.write(client_socket.recv(1024).decode())
    client_socket.close()

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)