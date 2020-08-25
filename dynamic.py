import os
import subprocess
import re
from tkinter import StringVar, Label, Tk, Frame, TOP


#记录日志：
def getJournal():
    #登录节点：
    #os.chdir(os.path.abspath(os.path.expanduser('~')))
    #os.chdir('platon-node')
    #subprocess.Popen('nohup platon --identity platon --datadir ./data --port 16789 --testnet --rpcport 6789 --rpcapi "db,platon,net,web3,admin,personal" --rpc --nodekey ./data/nodekey --cbft.blskey ./data/blskey --verbosity 3 --rpcaddr 127.0.0.1 --syncmode "full" > ./data/platon.log 2>&1 &', shell=True)
    
    #进入日志所在工作目录：
    os.chdir(os.path.abspath(os.path.expanduser('~')))
    os.chdir('platon-node/data')
    
    #记录日志内容的列表：
    global jlist
    
    #记录日志内容
    try:  
        record = subprocess.Popen('tail -n 100 platon.log', shell=True, stdout=subprocess.PIPE)
        p = record.stdout.read()
        jlist.append(p)
    except:
        pass
        
    return jlist


#记录less日志：
def getLess():
    #进入日志所在工作目录：
    os.chdir(os.path.abspath(os.path.expanduser('~')))
    os.chdir('platon-node/data')
    
    #记录less日志内容的列表：
    global lesslist
    
    #记录日志内容
    try:  
        record = subprocess.Popen('grep validator platon.log | less', shell=True, stdout=subprocess.PIPE)
        p = record.stdout.read()
        lesslist.append(p)
    except:
        pass
    
    return lesslist


#将日志内容写入特定目录下的文本文档中：
def writeJournal(jlist):
    #进入想存放日志内容文本的工作目录：
    os.chdir(os.path.abspath(os.path.expanduser('~')))
    os.chdir('/mnt/d/python')
    
    with open('journal.txt', 'w') as journal:
        while (len(jlist)):
            p = jlist.pop()
            print(p, file=journal)


#将less日志内容写入特定目录下的文本文档中：
def writeLess(lesslist):
    #进入想存放日志内容文本的工作目录：
    os.chdir(os.path.abspath(os.path.expanduser('~')))
    os.chdir('/mnt/d/python')
    
    with open('less.txt', 'w') as less:
        while (len(lesslist)):
            p = lesslist.pop()
            print(p, file=less)


#查找当前view数据：
def findView():
    #存放view数据的列表:
    global vlist
    
    #读取日志信息：
    with open('journal.txt', 'r') as journal:
        lines = journal.readlines()
        flines = len(lines)
    
    #查找并记录当前的view数据：
    for i in range(0, flines):
        vdata = re.findall(r'view=\d+', lines[i])
        if len(vdata) != 0: 
            vnum = vdata[0]
            if len(vlist) == 0:
                vlist.append(vnum[5:])
            else:
                if vnum[5:] != vlist[0]:
                    vlist.pop()
                    vlist.append(vnum[5:])
        
    return vlist    


#查找当前block的信息：
def getBlock():
    #存放block信息的列表：
    global block
    
    #读取日志信息：
    with open('journal.txt', 'r') as journal:
        lines = journal.readlines()
        flines = len(lines)
        
    #查找并记录当前的finishedblock数据：
    for i in range(0, flines):
        fbdata = re.findall(r'commitState=..blockNumber:\d+', lines[i])
        if len(fbdata) != 0:
            fbnum = re.findall(r'\d+', fbdata[0])
            if len(block) == 0:
                block.append(fbnum[0])
            else:
                if fbnum[0] != block[0]:
                    block[0] = fbnum[0]        
    
    #查找并记录当前的lockedblock数据：
    for i in range(0, flines):
        lbdata = re.findall(r'lockState=..blockNumber:\d+', lines[i])
        if len(lbdata) != 0:
            lbnum = re.findall(r'\d+', lbdata[0])
            if len(block) == 1:
                block.append(lbnum[0])
            else:
                if lbnum[0] != block[1]:
                    block[1] = lbnum[0]                
    
#查找并记录当前的prepareblock数据：
    for i in range(0, flines):
        pbdata = re.findall(r'qcState=..blockNumber:\d+', lines[i])
        if len(pbdata) != 0:
            pbnum = re.findall(r'\d+', pbdata[0])
            if len(block) == 2:
                block.append(pbnum[0])
            else:
                if lbnum[0] != block[2]:
                    block[2] = pbnum[0]                
    
    return block


#查找当前25个验证节点的信息：
def get25():
    #存放验证节点信息的字典和列表：
    global validators
    indexDList = []
    addressDList = []
    indexNList = []
    addressSList = []
    
    #读取less日志信息：
    with open('less.txt', 'r') as less:
        lines = less.readlines()
        flines = len(lines)
    
    for i in range(0, flines):
        iaa = re.findall(r'.."index..":\d+,.."address..":..".{42,42}..",.."nodeID..":..".{128,128}', lines[i])
        #r'.."index..":\d+,.."address..":..".{42,42}'
        #r'.."index..":\d+,.."address..":..".{42,42}..",.."nodeID..":..".{128,128}'
    #获取验证节点的index信息：
    for i in range(0, len(iaa)):
        indexdata = re.findall(r'index..":\d+', iaa[i])
        indexDList.append(indexdata[0])
    
    for i in range(0, len(indexDList)):
        indexString = indexDList[i]
        index = int(indexString[9:])
        indexNList.append(index)
   
    #获取验证节点的address信息：
    for i in range(0, len(iaa)):
        addressdata = re.findall(r'nodeID..":..".+', iaa[i])
        addressDList.append(addressdata[0])

    for i in range(0, len(addressDList)):
        addressString = addressDList[i]
        address = addressString[13:]
        addressSList.append(address)

    while (len(indexNList) >= 25):
        for i in range(0, 25):
            validators[indexNList[i]] = addressSList[i]
        for i in range(0, 25):
            del indexNList[0]
            del addressSList[0]
    return validators


class Watch(Frame):
    msec = 1000
    def __init__(self, parent=None, **kw):
            global validators
            Frame.__init__(self, parent, kw)
            self._running = False
            self.vtext = StringVar()
            self.ftext = StringVar()
            self.ltext = StringVar()
            self.ptext = StringVar()
            self.etext = StringVar()
            self.rtext = StringVar()
            self.valtext = []
            for i in range(0, 25):
                self.valtext.append(validators[i])
                self.valtext[i] = StringVar()
            self.makeWidgets()
            self.flag  = True
    def makeWidgets(self):
        #显示epoch信息：
        le = Label(self, textvariable=self.etext)
        le.pack()

        #显示round信息：
        lr = Label(self, textvariable=self.rtext)
        lr.pack()
    
        #显示view信息：
        lv = Label(self, textvariable=self.vtext, width=2)
        lv.pack()
    
        #显示finishedblock信息：
        lf = Label(self, textvariable=self.ftext)
        lf.pack()
    
        #显示lockedblock信息：
        ll = Label(self, textvariable=self.ltext)
        ll.pack()
    
        #显示prepareblock信息：
        lp = Label(self, textvariable=self.ptext)
        lp.pack()
    
        #显示25个验证节点的信息：
        lval = Label(self, text='Validators:')
        lval.pack()
        for i in range(0, 25):
            Label(self, textvariable=self.valtext[i]).pack()
    def _update(self):
        self._settime()
        self.timer = self.after(self.msec, self._update)
    def _settime(self):
        global jlist
        global lesslist
        global vlist
        global block
        global validators
        jlist = getJournal()
        writeJournal(jlist)
        lesslist = getLess()
        writeLess(lesslist)
        vlist = findView()
        block = getBlock()
        self.vtext.set(vlist[0])
        if int(vlist[0]) == 0:
            validators = get25()
            for i in range(0, 25):
                self.valtext[i].set(validators[i])
        self.ftext.set(block[0])
        self.ltext.set(block[1])
        self.ptext.set(block[2])
        self.etext.set((int(block[0]) % 10750) + 1)
        self.rtext.set((int(block[0]) % 250) + 1)
    def start(self):
        global validators
        self._update()
        validators = get25()
        for i in range(0, 25):
            self.valtext[i].set(validators[i])
        self.pack(side = TOP)

if __name__ == '__main__':
    def main():
        
        global jlist
        global lesslist
        global vlist
        global block
        global validators
        jlist = getJournal()
        writeJournal(jlist)
        lesslist = getLess()
        writeLess(lesslist)
        vlist = findView()
        block = getBlock()
        validators = get25()
        
        root = Tk()
        root.title("platon-node")
        root.geometry('620x600')
        
        Label(root, text='EPOCH:  (1~10750)').place(x=20, y=0)
        Label(root, text='ROUND:  (1~250)').place(x=20, y=17)
        Label(root, text='VIEW:  (0~24)').place(x=20, y=34)
        Label(root, text='BLOCK NUMBER:').place(x=20, y=51)
        
        Label(root, text='finished:').place(x=120, y=51)
        Label(root, text='locked:').place(x=120, y=68)
        Label(root, text='prepare:').place(x=120, y=85)
        for i in range(0, 25):
            Label(root, text=i).place(x=50, y=120+17*i)
        mw = Watch(root)
        mw.start()
        root.mainloop()
    
    
    jlist = [] #记录日志内容的列表
    lesslist = [] #记录less日志内容的列表
    vlist = [] #存放当前view数据的列表
    block = [] #存放当前block的信息的列表
    validators = {} #存放当前25个验证节点的信息的字典
    
    main()