#!/usr/bin/env python

import os

from time import sleep
import tkinter

class dirlist(object):
    def __init__(self, initdir='/'):
        self.top=Tk()
        self.label=Label(self.top, text='DDL')
        self.label.pack()

        self.cwd=StringVar(self.top)
        self.dirl = Label(self.top,)
        
        self.dirl.pack()
        

        self.dirfm=Frame(self.top)
        self.dirsb=Scrollbar(self.dirfm)
        self.dirsb.pack(side=RIGHT, fill=Y)
        self.dirs=Listbox(self.dirfm, height=15, width=50, yscrollcommand=self.dirsb.set)
        self.dirs.bind('<Double-1>', self.setDirAndGo)
        self.dirsb.config(command=self.dirs.yview)
        self.dirs.pack(side=LEFT, fill=BOTH)
        self.dirfm.pack()
        
        self.dirn=Entry(self.top, width=50,textvariable=self.cwd)
        
        self.dirn.bind('<Return>', self.doLS)
        self.dirn.pack()

        self.bfm=Frame(self.top)
        self.clr = Button(self.bfm, text='clear',command=self.clrDir,activeforeground='white',activebackground='blue')
        self.ls=Button(self.bfm,text='print current directory to terminal',command=self.doLS,)
        #self.openinwindow = Button(self.bfm, text='quit',command=self.top.quit,)
        self.clr.pack(side=LEFT)
        self.ls.pack(side=LEFT)
        #self.quit.pack(side=LEFT)
        self.bfm.pack()
        
       

        if initdir:
            self.cwd.set(os.curdir)
            self.doLS()
    def clrDir(self, ev=None):
        self.cwd.set('')
     
    def setDirAndGo(self,ev=None):
        self.last=self.cwd.get()
        self.dirs.config()
        check = self.dirs.get(self.dirs.curselection())
        if not check:
            check = os.curdir
        self.cwd.set(check)
        self.doLS()
    def doLS(self, ev=None):
        error = ''
        tdir = self.cwd.get()
        if not tdir: 
            tdir=os.curdir
            
        if not os.path.exists(tdir):
            error = tdir+'no such file'
        elif not os.path.isdir(tdir):
            error = tdir + 'noidir'
        if error:
            self.cwd.set(error)
            self.top.update()
            sleep(2)
            if not(hasattr(self,'last') and self.last):
                self.last=os.curdir
            self.cwd.set(self.last)
            self.dirs.config(selectbackground='LightSkyBlue')
            self.top.update()
            return
        self.cwd.set('fetch dir contents')
        self.top.update()
        dirlist=os.listdir(tdir)
        dirlist.sort()
        os.chdir(tdir)
        self.dirl.config(text=os.getcwd())
        self.dirs.delete(0,END)
        self.dirs.insert(END, os.curdir)
        self.dirs.insert(END, os.pardir)
        for eachFile in dirlist:
            self.dirs.insert(END, eachFile)
        self.cwd.set(os.curdir)
        
        exportdir = self.dirl.cget("text")
      
        self.dirs.config(selectbackground='LightSkyBlue')
        
        #need to have exportdir return as string for the texteditor.py file to access
        #so it can be put into the pathway text area in texteditor.py and then opened
        
        return exportdir

def main():
    d = dirlist(os.curdir)
   
    
    mainloop()
if __name__ == '__main__':
    main()
