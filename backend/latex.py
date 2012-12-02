# application modules
from backend.forms  import newSong
from backend.models import Song
import settings
# utils
import os, sys, pdb, re
import json, subprocess, shutil

MAX_LINE_LENGHT = 45
MAX_NUM_LINES   = 3

def makeTex( user ):
  
  profile = user.get_profile()
  # set up folders and files
  template_file = os.path.join( settings.LATEX_DIR , "template.tex" )
  output_dir    = profile. getPath()
  output_tex    = os.path.join( output_dir, "print.tex"  )
  output_pdf    = os.path.join( output_dir, "print.pdf"  )

  inLines  = open( template_file, 'r' ).readlines()

  # get songs
  songs = Song.objects.filter(author=profile).order_by("author")

  # copy headers
  outLines = prepareHeader( inLines, user.username )
  writeSongs( outLines, songs )

  # create new file
  with open( output_tex , 'w+' ) as f:
    map( lambda x:f.write(x.encode('utf8')), outLines)
  
  cmd = "/usr/texbin/xelatex -interaction=nonstopmode %s " % output_tex
  out = subprocess.call(cmd, shell=True, cwd=output_dir)
  
  return profile.getPdfPath()

def prepareHeader( inLines, name ):
  outLines = []
  for line in inLines:
    if "USERNAME" in line:
      outLines.append( boldTexLine("Created for "+ name ) +"\\\\" )
      continue
    if "START" in line:
      break
    outLines. append( line )

  return outLines

def writeSongs(outLines, songs):
  last_artist = None
  for song in songs:
    if last_artist != song.artist:
      last_artist = song.artist
      outLines.append("\section{%s}\n" % last_artist)
    
    multi_cols = len ( filter( lambda x: len(x)> MAX_LINE_LENGHT ,
      song.content.split('<br>') ))== 0
    
    outLines.append("\subsection{%s}\n"% song.name  )
    if multi_cols:
      outLines.append("\\begin{multicols}{2}")

    outLines.append("\\begin{Verbatim}[commandchars=\\\\\\{\}]\n")
    map( lambda x:outLines.append(x+"\n"), HTMLToLatex(song.content) )
    outLines.append( "\n" ) ## leave blank line after text
    outLines.append("\end{Verbatim}\n")

    if multi_cols:
      outLines.append("\end{multicols}")
    if song != songs[::-1]:
      outLines.append("\\newpage\n")

  outLines.append("\end{document}")

def boldTexLine( line ):
  return "{\\bf " + line + "}"

def boldify( lines ):
  p = re. compile("[a-z]{4}")
  outLines = []

  for line in lines:
    newLine = line
    if len( line ) < 1 or line[0]== '\n':
      pass
    elif (  p.search(line) == None or line.lower().find("intro")!=-1 
        or line.lower().find("riff")!=-1
        or line.lower().find("chorus")!=-1 
        or line.lower().find("verse")!=-1 or line.lower().find("ritornello")!=-1 
        or line.lower().find("madd9")!=-1 or line.lower().find("maj9")!= -1):
      line = line.replace("\n","")
      newLine = boldTexLine( line )

    outLines.append(newLine)
  return outLines

def HTMLToLatex( content ):
  return boldify( content.split('<br>')  )

