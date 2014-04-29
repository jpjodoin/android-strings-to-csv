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

def escapeAndroidChar(text):
  text = text.replace('\'', "\\'")
  return text


pathToString = raw_input("Path to CSV file:")
outputFolder = raw_input("Path to Android project (output):")
defaultLanguage = raw_input("Default langage ISO-639-1 code. (write en if your default langage is english):")

outputFolder = os.path.join(outputFolder, "res")

csvSep = "\t"
#1) Read the file and build dictionnary for each langage
with codecs.open(pathToString, 'r', "utf-8") as f:
    langageDict = dict()
    lines = f.readlines()
    if len(lines) > 0:
      headerTmp = lines[0].strip().split(csvSep)
      langList = []
      for lang in headerTmp[1:]:
        if lang:
          langageDict[lang] = dict()
          langList.append(lang)
      for l in lines[1:]:
        l = l.strip().split(csvSep)
        key = l[0]
        for idx, item in enumerate(l[1:]):
          if item:
            #3) Escape character
            langageDict[langList[idx]][key] = escapeAndroidChar(item)
          else:
            print("Empty item for " + langList[idx])

#2) Create an XML document from each langage dictionnary
xmldict = dict()
for lang in langageDict:
  stringsDict = langageDict[lang]
  doc = minidom.Document()
  xmldict[lang] = doc
  rootNode = doc.createElement("resources")
  doc.appendChild(rootNode)

  stringsDict = collections.OrderedDict(sorted(stringsDict.items()))
  for key in stringsDict:
    if ',' in key:
      if ',0' in key: #first node. Order is guaranteed by the sort
        topNode = doc.createElement("string-array")
        topNode.setAttribute("name", key[0:key.find(',0')])
        rootNode.appendChild(topNode)
      node = doc.createElement("item")
      node.appendChild(doc.createTextNode(stringsDict[key]))
      topNode.appendChild(node)
    else:
      node = doc.createElement("string")
      node.setAttribute("name", key)
      node.appendChild(doc.createTextNode(stringsDict[key]))
      rootNode.appendChild(node)
  

#3) Write XML for each langage in the correct directory structure
for lang in langageDict:
  folderName = "values"
  if lang != defaultLanguage:
    folderName = "values-"+lang
  langFolder = os.path.join(outputFolder,folderName)
  if not os.path.exists(langFolder):
    os.makedirs(langFolder)
  stringPath = os.path.join(langFolder, "strings.xml")
  with open(stringPath, 'w') as f:
    xmlContain = xmldict[lang].toprettyxml(encoding="utf-8")
    #print(xmlContain)
    f.write(xmlContain)
