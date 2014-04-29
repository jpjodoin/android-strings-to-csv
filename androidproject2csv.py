"""
The MIT License (MIT)

Copyright (c) 2014 Jean-Philippe Jodoin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import os, collections
from xml.dom import minidom
import codecs
from OrderedSet import OrderedSet

def unescapeAndroidChar(text):
  text = text.replace("\\'", '\'')
  return text

csvSep = "\t"
defaultLangage = raw_input("Default langage ISO-639-1 code. (write en if your default langage is english):")
pathToProject = raw_input("Path to Android project file:")
outputFilepath = raw_input("Path to CSV file (output):")

ressourcePath = os.path.join(pathToProject,"res")
folderList = os.listdir(ressourcePath)
langageDict = dict()
for f in folderList:
  if f.startswith("values"):
    lang = defaultLangage
    tmp = f.split("-")
    if len(tmp) == 2:
      lang = tmp[1]
    print(lang)
    langageDict[lang] = dict()
    stringsDict = langageDict[lang]
    valuesPath = os.path.join(ressourcePath,f)
    if os.path.isdir(valuesPath):
      filePath = os.path.join(valuesPath, "strings.xml")
      if os.path.exists(filePath):
        #Open String XML
        #print(filePath)
        xmldoc = minidom.parse(filePath)
        rootNode = xmldoc.getElementsByTagName("resources")
        if len(rootNode) == 1:          
          nodeList = rootNode[0].childNodes
          for n in nodeList:
            attr = n.attributes
            if attr != None:
              tag = n.tagName
              if tag == 'string':
                key = attr['name'].nodeValue
                value = n.childNodes[0].nodeValue
                stringsDict[key] = value.strip()
                #print(key + " = " + value)
              elif tag == 'string-array':
                name = attr['name'].nodeValue
                itemList = n.getElementsByTagName("item")
                for idx, item in enumerate(itemList):
                  key = str(name)+","+str(idx)
                  value = item.childNodes[0].nodeValue
                  #print(key + " = " + value)
                  stringsDict[key] = value.strip()
              else:
                print("Unknown node")
        else:
          print('Invalid ressource file. We expect a ressources node')
        #for s in itemlist :          
          #print(s)

#Get all key list
uniqueKeys = set()
for k in langageDict:
  stringsDict = langageDict[k]
  for keys in stringsDict:
    uniqueKeys.add(keys)
uniqueKeys = OrderedSet(sorted(uniqueKeys))
#Write CSV
with codecs.open(outputFilepath, 'w', "utf-8") as f:
  f.write(u'\ufeff') #UTF8 Marker
  f.write("key"+csvSep)
  for k in langageDict:
    f.write(k + csvSep)
  for key in uniqueKeys:
    f.write("\n")
    f.write(key+csvSep)
    for k in langageDict:
      stringsDict = langageDict[k]
      if key in stringsDict:
        f.write(unescapeAndroidChar(stringsDict[key]) + csvSep)
      else:
        f.write(" ")
        print("Undefined string for key " + str(key) + " in " + str(k))

