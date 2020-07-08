from sys import argv
import os

filename = "Output.rtf"
if os.path.isfile(filename):
    os.remove(filename)

target = open("New data.txt",'r')
output = open(filename,'w')
raw = target.read()
lines = []
ongoing = False
bracket = False
line = ""
for char in raw:
    if ongoing == False:
        line = char
        ongoing = True
        if char != "<":
            bracket = False
        else:
            bracket = True
    else:
        if bracket == False:
            if char == "<":
                lines.append(line)
                line = ""
                bracket = True
        line = line + char
    if char == ">" and bracket == True:
        ongoing = False
        bracket = False
        lines.append(line)
    elif char == "<":
        if bracket == False:
            ongoing = False
            lines.append(line)
    #print(line)
lines = lines[4:]

ongoing = False
stack = []
queue = []
Set1 = ("Message Date", "Time", "SessionID")
Set2 = ("From", "To", "Application")
out = ""
for stuff in lines:
    l = stuff.find("<")
    r = stuff.find(">")
    if l >= 0:
        if stuff[1] == "/":
            l = 2
            tag = stuff[l:r]
        else:
            tag = stuff[1:r]
    else:
        tag = ""

    if Set1[0] in stuff and Set1[1] in stuff and Set1[2] in stuff and l>=0:
        for datas in Set1:
            pos = stuff.find(datas) + len(datas) + 2
            pos2 = stuff.find('"', pos)
            out = out + stuff[pos:pos2] + " | "

    elif tag in Set2:
        if ongoing == True:
            if stack[-1] == tag:
                ongoing = False
                stack = stack[:-1]
                out = tag + ": " + queue[0]
                queue = queue[1:]
        else:
            ongoing = True
            stack.append(tag)
            
    elif "User FriendlyName" in stuff:
        pos = stuff.find('"')+1
        pos2 = stuff.find('"',pos)
        queue.append(stuff[pos:pos2])

    elif "/Message" in stuff:
        out = ""

    elif "Text" in stuff:
        if ongoing == True:
            if stack[-1] == "Text":
                ongoing = False
                stack = stack[:-1]
                out = '"'
                while queue:
                    out = out + queue[0] + " "
                    queue = queue[1:]
                out = out + '"'
        else:
            ongoing = True
            stack.append("Text")

    elif "<" not in stuff:
        queue.append(stuff)

    else:
        if ongoing:
            queue = queue[1:]
        out = stuff
        
    if not ongoing:
        output.write(out)
        output.write("\n")
        out = ""

target.close()
output.close()
