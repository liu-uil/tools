#encoding = utf-8

import sys, os

def main():
    print sys.path  
    print os.path.abspath(__file__)
    print os.path.dirname(__file__)
    CurDir = os.path.dirname(__file__)
    print CurDir
    filesInCurDir = os.listdir(CurDir)
    print filesInCurDir
    print os.path.abspath(os.path.pardir)
    fileOpened = open(filesInCurDir[1])
    fileContent = fileOpened.readline()
    print fileContent
    fileOpened.close()
    if os.path.exists('tmp'):
        os.rmdir('tmp')
    os.mkdir('tmp')
    os.popen('xcopy %s tmp\\'%CurDir)
    
if __name__=="__main__":
    main()