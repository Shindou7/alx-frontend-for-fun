#!/usr/bin/python3
"""
    Parsing bold syntax
"""
import sys
from os import path
import hashlib

markD = {"#": "h1", "##": "h2", "###": "h3", "####": "h4", "#####": "h5", "######": "h6", "-": "ul", "*": "ol"}

if len(sys.argv) < 3:
    sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
    exit(1)

if not path.exists(sys.argv[1]) or not str(sys.argv[1]).endswith(".md"):
    sys.stderr.write("Missing " + sys.argv[1] + '\n')
    exit(1)

def inlineMarkdown(line, pattern):
    flag = False
    while pattern in line:
        if not flag:
            if pattern == "**":
                line = line.replace(pattern, "<b>", 1)
                flag = True
            else:
                line = line.replace(pattern, "<em>", 1)
                flag = True
        else:
            if pattern == "**":
                line = line.replace(pattern, "</b>", 1)
                flag = False
            else: 
                line = line.replace(pattern, "</em>", 1)
                flag = False
    return line

def md5Markdown(line):
    while "[[" in line and "]]" in line:
        start_idx = line.find("[[")
        end_idx = line.find("]]")
        toHash = line[start_idx + 2:end_idx]
        md = hashlib.md5(toHash.encode()).hexdigest()
        line = line.replace("[[" + toHash + "]]", md)
    return line

def caseMarkdown(line):
    while '((' in line and '))' in line:
        start_idx = line.find('((')
        end_idx = line.find('))')
        toRep = line[start_idx:end_idx + 2]
        toRep = toRep.replace('c', '').replace('C', '')
        line = line.replace(line[start_idx:end_idx + 2], toRep[2:-2])
    return line 

with open(sys.argv[1], mode='r') as fr, open(sys.argv[2], mode='w+') as fw:
    first = 0
    f = 0
    read = fr.readlines()
    for i, line in enumerate(read):
        # For inline markdown
        line = inlineMarkdown(line, "**")
        line = inlineMarkdown(line, "__")
        line = md5Markdown(line)
        line = caseMarkdown(line) 

        # split by spaces
        lineSplit = line.split(' ')
        if lineSplit[0] in markD:
            # Headings
            if lineSplit[0].startswith('#'):
                tag = markD[lineSplit[0]]
                toWrite = line.replace("{} ".format(lineSplit[0]), "<{}>".format(tag))
                toWrite = toWrite[:-1] + ("</{}>\n".format(tag))
                fw.write(toWrite)
            # Lists
            elif lineSplit[0].startswith("-") or lineSplit[0].startswith("*"):
                tag = markD[lineSplit[0]]
                if not first:
                    toWrite = "<{}>\n".format(tag)
                    fw.write(toWrite)
                    first = lineSplit[0]
                toWrite = line.replace("{} ".format(lineSplit[0]), "<li>")
                toWrite = toWrite[:-1] + ("</li>\n")
                fw.write(toWrite)
                if i == len(read) - 1 or not read[i + 1].startswith("{} ".format(first)):
                    toWrite = "</{}>\n".format(tag)
                    fw.write(toWrite)
                    first = 0
        else:
            if line[0] != "\n":
                if not f:
                    fw.write("<p>\n")
                    f = 1
                fw.write(line)
                if i != len(read) - 1 and read[i + 1][0] != "\n" and read[i + 1][0] not in markD:
                    fw.write("<br/>\n")
                else: 
                    fw.write("</p>\n")
                    f = 0
    exit(0)
