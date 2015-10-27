#encoding = utf-8

from socket import *
import time
import threading

HOST = 'localhost'  #服务器的地址
PORT = 12445        #服务器的端口
BUF = 1024

ADDR = (HOST, PORT)



#while True:
#    data = raw_input('>\n')
#    if not data:
#        break
#    print '[%s] \n %s'%(time.ctime(), data)
#    CliSocket.send(data)
#    redata = CliSocket.recv(BUF)
#    if not redata:
#        break
#    print '[%s] \n %s'%(time.ctime(), redata)
#    
#CliSocket.close()

def send(CliSocket):
    while True:
        data = raw_input('')
        CliSocket.send(data)
        if data == 'quit':
            print 'cli send break'
            break
#        print 'I said "%s" [%s]'%(data, time.ctime(),)
        

def receive(CliSocket):
    while True:
        redata = CliSocket.recv(BUF)
        if redata == 'quit':
            print 'cli receive break'
            CliSocket.send('quit')
            break
        print '%s %s '%(time.ctime(),redata,  )

def main():
    CliSocket = socket(AF_INET, SOCK_STREAM)
    CliSocket.connect(ADDR)

    print 'Connected to ',ADDR,' now you can input message below and press enter to send!'

    Threads = []
    t = threading.Thread(target=send, args=(CliSocket,))
    Threads.append(t)
    t = threading.Thread(target=receive, args=(CliSocket,))
    Threads.append(t)
    
    for i in range(len(Threads)):
        Threads[i].start()
    
    for i in range(len(Threads)):
        Threads[i].join()
    
    print 'The conversation is closing...'    
    CliSocket.close()
    
if __name__=="__main__":
    main()
    