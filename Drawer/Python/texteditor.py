from tkinter import *
import tkinter.font as tkf
import tkinter.scrolledtext as ScrolledText
import os
from PIL import Image, ImageFont, ImageDraw, ImageTk
import main
from PIL import ImageFont
import re

root = Tk()

bcgColor = '#%02x%02x%02x' % (40, 41, 35)
selectedColor = '#%02x%02x%02x' % (58, 57, 47)
textColor = '#%02x%02x%02x' % (144, 145, 139)

pinkColor = '#%02x%02x%02x' % (249, 35, 95)
blueColor = '#%02x%02x%02x' % (104, 216, 236)
yelloColor = '#%02x%02x%02x' % (231, 219, 102)
orangeColor = '#%02x%02x%02x' % (252, 130, 32)
greenColor = '#%02x%02x%02x' % (161, 226, 44)
grayColor = '#%02x%02x%02x' % (144, 145, 132)
numColor = '#%02x%02x%02x' % (171, 127, 253)
selectColor = '#%02x%02x%02x' % (53, 53, 46)
hintColor = '#%02x%02x%02x' % (44, 117, 197)

selectHintSelColor = '#%02x%02x%02x' % (92, 93, 88)
selectHintBackgroundColor = '#%02x%02x%02x' % (51, 52, 46)
root.configure(bg=bcgColor)

text = Text(root, font="Monaco 14", wrap='word', bg=bcgColor, bd = -1, highlightbackground=bcgColor, highlightthickness=0, insertbackground="white", fg="white")
text.place(x=45, y=2, height=16*53)
text.insert("1.0", "")
root.geometry("640x480")
hintList = Listbox(root, highlightbackground='white')
hintList.config(bg=bcgColor, bd=0, width=12, height = 1)
hintList.select_set(0)
hintList.pack()



codeOutput = ""
def find_all(T, S):
    starts = [match.start() for match in re.finditer(re.escape(S), T)]
    return starts


def findNearest(str, dels):
    minIndex = 9999
    for d in dels:
        if str.find(d) <= minIndex:
            minIndex = str.find(d)
    return minIndex

def delName(arr, name):
    outarr = []
    for i in arr:
        if i != name:
            outarr.append(i)
    return outarr

def getUnical(arr):
    outarr = []
    for i in arr:
        if not i in outarr:
            outarr.append(i)
    return outarr

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

globalVars = []

def search(df):
    global text, globalVars, codeOutput
    codeOutput = ""
    globalVars = []
    lines = text.get("1.0", END).splitlines()
    curLine = int(str(text.index(INSERT)).split(".")[0])-1
    curChar = int(str(text.index(INSERT)).split(".")[1])
    id = 0

    for i in lines:
        if len(i) != 0:
            for tagName in text.tag_names():
                if not tagName in ["default", "sel"]:
                    text.tag_remove(tagName, "%d.0" % (curLine+1),  index2="%d.%d" % (curLine+1, len(i)))
            codeOutput += i + "\n"
            copy = i
            parts = []
            for delim in DELIMETERS:
                copy = "|".join(copy.split(delim))
            parts = getUnical(delName(copy.split("|"), ""))
            if "=" in parts and not i.startswith(" "*4):
                if parts[2] in keywords and keywords[parts[2]] == 'function':
                    globalVars.append(parts[0])
            elif not i.startswith(" "*4):
                if parts[1] in keywords and keywords[parts[1]] == 'operation':
                    globalVars.remove(parts[2])
            for part in parts:
                if part in keywords:
                    tag = keywords[part]
                    for p in find_all(i, part):
                        text.tag_add(tag, "%d.%d" % (curLine+1, p),  "%d.%d" % (curLine+1, p + len(part)))
            for var in globalVars:
                codeOutput += "draw(%s)\n" % (var)
            l = i[-curChar:]
            p = parts
            last = p[len(p)-1]
            hintPosib = []
            hintWords = []
            for fullWord, posibilities in hints.items():
                for pos in posibilities:
                    if pos[0] == last:
                        hintPosib.append([fullWord, pos[1]])
                        hintWords.append(fullWord)
            drawHints(curLine+1, l.rfind(last), l,hintWords)
        id+=1


def makeHint(String):
    hint = []
    for i in range(1, len(String)):
        hint.append([String[:i], String[i:]])
    return hint
def compileHints(keys):
    global functionConstructors, keywords
    dic = {}
    newOptions = []
    for key, tag in keys.items():
        if not RepresentsInt(key):
            name = key
            for custom, constructor in functionConstructors.items():
                if custom == key:
                    name = functionConstructors[key]
                    parts = []
                    copy = name
                    for delim in DELIMETERS:
                        copy = "|".join(copy.split(delim))
                    parts = getUnical(delName(copy.split("|"), ""))[1:]
                    for p in parts:
                        newOptions.append(p)
            dic[key] = makeHint(name)
    newOptions = getUnical(newOptions)
    for op in newOptions:
        keywords[op] = "hintoption"
    return dic

def all_nums(str):
    return [(i,c) for i,c in enumerate(str) if c.isdigit()]

DELIMETERS = ["(", ")", " ", "\n", "\t", ":", "[", "]", ",", ".", "*", "/", "-", "+", "_"]

def GetTextDimensions(text, fnt):
    font = ImageFont.truetype('Helvetica-Regular.ttf', fnt)
    size = font.getsize(text)
    return size

def drawHints(line, char, fullLine, name):
    global hintList
    if len(name) == 0:
        hintList.config(bg=bcgColor)
        hintList.delete(0, END)
        hintList.place(x=-100)
        return None
    else:
        (w, h) = GetTextDimensions(fullLine[char], 14)
        hintList.config(bg=selectHintBackgroundColor)
        hintList.config(height=len(name))
        hintList.delete(0, END)
        for i in range(len(name)):
            hintList.insert(i, " "+name[i])
            hintList.itemconfig(i, foreground='white')
            hintList.itemconfig(i, {'bg':selectHintBackgroundColor})
        hintList.select_set(hintSelected % (hintList.size()))
        hintList.itemconfig(hintSelected, {'selectbackground':selectHintSelColor})
        hintList.itemconfig(hintSelected, {'selectforeground': "white"})
        if char==0:
            hintList.pack(anchor="sw", padx=34+w, pady=(line+1)*h+12)
        else:
            hintList.pack(anchor="sw", padx=34+(char*w), pady=(line+1)*h+12)
        # hintList.place(x=(char*(w+1)), y=h+10)

def aceptHint(evnt):
    if len(hintList.curselection()) > 0:
        name = hintList.get(hintList.curselection()[0]).strip()
        lines = text.get("1.0", END).splitlines()
        curLine = int(str(text.index(INSERT)).split(".")[0])-1
        curChar = int(str(text.index(INSERT)).split(".")[1])
        line = lines[curLine]
        copy = line
        parts = []
        word = []
        cnt = ""
        for delim in DELIMETERS:
            copy = "|".join(copy.split(delim))
            parts = copy.split("|")
        word = parts[len(parts)-1]
        if name != "":
            contin = hints[name]
            for way in contin:
                if way[0] == word:
                    cnt = way[1]
                    break
        text.insert(str(curLine+1)+"."+str(line.rfind(word)+len(word)), cnt)
        drawHints(0,0, "", [])
        return 'break'

hintSelected = 0

rectbracket = 2162779
circlebracket = 1638440
altlkey = 1048832
altrkey = 524387

def changeHint(event):
    mult = int(str(event).split("char=\'\\uf70")[1].split("\' ")[0].replace("0", "-1"))
    global hintSelected
    if hintList.get(ACTIVE).strip() != "":
        sel=str(hintList.curselection())
        if sel == "()":
            hintList.select_set(hintList.size()-1)
            hintSelected = hintList.size()-1
        elif hintList.size() > 1:
            sel = (int(sel.split("(")[1].split(",")[0])+(1*mult)) % (hintList.size())
            hintSelected = sel
            hintList.select_set(hintSelected)
            hintList.itemconfig(hintSelected, {'selectbackground':selectHintSelColor})
            hintList.itemconfig(hintSelected, {'selectforeground': "white"})
def compile(event):
    key = event.keycode
    curLine = int(str(text.index(INSERT)).split(".")[0])-1
    curChar = int(str(text.index(INSERT)).split(".")[1])
    if key == rectbracket:
        text.insert(str(curLine+1)+"."+str(curChar), "]")
        text.mark_set("insert", "%d.%d" % (curLine+1,curChar))
    if key == circlebracket:
        text.insert(str(curLine+1)+"."+str(curChar+1), ")")
        text.mark_set("insert", "%d.%d" % (curLine+1,curChar))
    redraw(None)
    search(None)
    if key in [altlkey, altrkey]:
        main.loop(codeOutput+"\ndraw", globalVars)
    try:
        char = str(repr(event)).split("char")[1].split("delta")[0].split("\'")[1].split("\'")[0]
        if char == "\\r":
            onVoid(None)
    except:
        a= 0

def onVoid(evnt):
    cur = text.index(INSERT)
    l = int(cur.split(".")[0])
    prev = text.get("1.0", END).splitlines()[l-2]
    if prev.endswith(":"):
        text.insert(str(l+1)+".0", (" " * 4))

def tab(arg):
    global text
    curLine = int(str(text.index(INSERT)).split(".")[0])
    try:
        if text.get(SEL_FIRST, SEL_LAST) != "":
            text.insert("%d.0" % (curLine), " " * 4)
        else:
            text.insert(INSERT, " " * 4)
        return 'break'
    except:
        text.insert(INSERT, " " * 4)
        return 'break'

def redraw(args):
    canvas = Canvas(root, width=16*2, height=500, bg=bcgColor, highlightbackground=bcgColor, bd=-1)
    canvas.place(x=0)
    linenums = {}
    num = 1
    contents = text.get("1.0", END)
    for i, line in enumerate(contents.splitlines(), 1):
        i = str(i) + '.0'
        linetext = text.get(i, "%s+1line" % i)
        linenums[i] = str(num)
        num += 1

    i = text.index("@0,0")
    while True :
        dline = text.dlineinfo(i)
        if dline is None: 
            break

        linenum = linenums.get(i)
        if linenum is not None:
            y = dline[1]
            if int(linenum) == int(text.index(INSERT).split(".")[0]):
                canvas.create_rectangle(0,y+4,32,y+16, fill=selectedColor, outline=selectedColor)
            canvas.create_text(int(16*(22/16)),y+3,anchor="ne", text=linenum, fill=grayColor, font=('Soda Light 3', 12))

        i = text.index("%s+1line" % i)

def addNumbers():
    global keywords
    for i in range(1000):
        keywords[str(i)] = "number"

text.config(selectbackground=selectColor)
text.tag_config('operator', foreground=pinkColor)
text.tag_config('function', foreground=blueColor)
text.tag_config('operation', foreground=orangeColor)
text.tag_config('number', foreground=numColor)
text.tag_config('hintoption', background=hintColor, foreground='black')
text.tag_config('default', foreground='white')

keywords = {
            "import": 'operator',
            "if": 'operator',
            "else": 'operator',
            "elif": 'operator',
            "==": 'operator',
            "!=": 'operator',
            "or": 'operator',
            "not": 'operator',
            "and": 'operator',

            "Rect": 'function',
            "Circle": 'function',
            "Line": 'function',
            "def": 'function',
            "void": 'function',
            "draw": 'function',

            "CONCAT": 'operation',
            "CUTA": 'operation',
            "CUTB": 'operation',
            "AND": 'operation'
            }

functionConstructors = {
            "Rect": "Rect(posx, posy, width, height)",
            "Circle": "Circle([posx, posy], radius)",
            "Line": "Line([fromx, fromy], [tox, toy])",
            "CONCAT": "CONCAT(shape)",
            "CUTA": "CUTA(shape)",
            "CUTB": "CUTB(shape)",
            "AND": "AND(shape)"
}

addNumbers()
hints = compileHints(keywords)
redraw(text)
search(None)
# search(None)

text.bind("<Tab>", tab)
text.bind("<Return>", aceptHint)
text.bind("<Down>", changeHint)
text.bind("<Up>", changeHint)
hintList.bind("<<ListboxSelect>>", aceptHint)

text.bind("<KeyRelease>", compile)


def start():
    root.mainloop()
