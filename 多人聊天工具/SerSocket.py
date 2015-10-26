#encoding = utf-8

from socket import *
import time
import threading
import copy

HOST = 'localhost'
PORT = 12445
BUF = 1024
WAITTOTAL = 0
MAXUSERNUM = 5
CONNECTUSER = 0
MESSAGEBUFFER = []  #一个由[待发送的用户数，消息缓存]组成的列表


#class MyThread(threading.Thread):
#    def __init__(self, func, args):
#        threading.Thread.__init__(self)
#        self.func = func
#        self.args = args
#    
#    def run(self):
#        apply(self.func,self.args)

        
def subSer(SerSocket,userIndex):
    global WAITTOTAL, CONNECTUSER
    while True:
        
        WAITTOTAL = WAITTOTAL+1
        print 'thread %d start waiting at:%s, WAITTOTAL = %d\n'%(userIndex,time.ctime(), WAITTOTAL)
        CliSocket,addr = SerSocket.accept()
        WAITTOTAL = WAITTOTAL-1
        CONNECTUSER = CONNECTUSER+1
        print 'user %d :connected from %s'%(userIndex,addr)
#        while True:
        Threads = []
        t = threading.Thread(target=send, args=(CliSocket,userIndex,))
#        print 'subSer\'s thread isDaemon is',t.isDaemon()
        Threads.append(t)
        t = threading.Thread(target=receive, args=(CliSocket,userIndex,))
#        print 'subSer\'s thread isDaemon is',t.isDaemon()
        Threads.append(t)
        
        for i in range(len(Threads)):
            Threads[i].start()
        
        for i in range(len(Threads)):
            Threads[i].join()
        print 'close the connection to user %d'%userIndex    
        CliSocket.close()
        
def send(CliSocket,userIndex):
    global MESSAGEBUFFER, CONNECTUSER
    
    while True:
#        redata = raw_input()
    
    #用MESSAGEBUFFER存储消息，如果MESSAGEBUFFER不为空，表示有要发送的消息
        if MESSAGEBUFFER:
#            print 'current online user total:',CONNECTUSER
            data = MESSAGEBUFFER[0][1]
            CliSocket.send(data)
            MESSAGEBUFFER[0][0] = MESSAGEBUFFER[0][0] - 1
    #每次执行一次发送，将剩余待发的用户数减一，如果为0，表示全部发送完成，清除当前的消息缓存
            if not MESSAGEBUFFER[0][0]:
                MESSAGEBUFFER.pop(0)
#            if redata == 'quit':
#                print 'Ser send break'
#                break
#        print 'execute sending...\n'
            print 'sending to all users [%s]'%(time.ctime(), )
    

def receive(CliSocket,userIndex):
    global MESSAGEBUFFER, CONNECTUSER
    while True:
        data = 'user '+str(userIndex)+' said:"'+CliSocket.recv(BUF)+'"'
        
        if data == 'quit':
            CliSocket.send('quit')
            print 'Ser receive break'
            break
        MESSAGEBUFFER.append(copy.deepcopy([CONNECTUSER,data]))
        print '[%s get message from user %d]'%(time.ctime(), userIndex)

def main():
    ADDR = (HOST, PORT)
    SerSocket = socket(AF_INET, SOCK_STREAM)
    SerSocket.bind(ADDR)
#    print 'Sloop %d start at:%s\n'%(loopn, time.ctime())
    print 'all start at:%s'%( time.ctime())
    SerSocket.listen(MAXUSERNUM)    
    
    Threads = []
    
    for i in range(MAXUSERNUM):
        tPORT = PORT+i
#        t = MyThread(Sloop, (HOST, tPORT, i))
        t = threading.Thread(target = subSer, args = (SerSocket,i,))
        t.setDaemon(True)
        Threads.append(t)
    
    for i in range(MAXUSERNUM):
#        print 'start %d at %s'%(i, time.ctime())
        Threads[i].start()
    time.sleep(10) 
#    for i in range(MAXUSERNUM):
#        print 'join %d at %s'%(i, time.ctime())
#        Threads[i].join()
#    print 'start checking WAITTOTAL at: %s'%time.ctime()
    while WAITTOTAL!=MAXUSERNUM:
        time.sleep(30)
        pass
    SerSocket.close()
    print 'all end at:%s\n'%( time.ctime())
    
    
if __name__=="__main__":
    main()
    
    
    
    