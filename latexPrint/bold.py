import re

f = open( './chord.tex', 'r+')
n = open( './bold.tex', 'w+')
j=0
p = re. compile("[a-z]{4}")
chords = re. compile( "[A-Z]{1}[a-z]")

for line in f:
  if ( line[0] == chr(92) or line[0] == chr(123) or line[0] == '%' 
      or line[0]== '\n'):
    k=0
  elif (  p.search(line) == None or line.lower().find("intro")!=-1 
      or line.lower().find("riff")!=-1
      or line.lower().find("chorus")!=-1 
      or line.lower().find("verse")!=-1 or line.lower().find("ritornello")!=-1 
      or line.lower().find("madd9")!=-1 or line.lower().find("maj9")!= -1):

    line = line.replace("\n","")
    line= "{\\bf " + line + "}\n"
  n. write( line)

