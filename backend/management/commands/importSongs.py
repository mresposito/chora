# django stuff
# utils
import os, sys, pdb
import json, subprocess, shutil
import re
# library links
from backend.models import Song
from django.contrib.auth.models import User
#cross site forgery exempt
# exceptions
from django.core.exceptions import ObjectDoesNotExist

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
  args = ""
  help ='Import images into the system'

  def handle(self, *args, **options):
    for path in args:
      inFile = path
      inLines = open( inFile, 'r' )
      
      importLines( inLines )
    
    User.objects.get(username='mre').save()
def importLines( lines ):
  content = []
  reading = False

  for line in lines:
    if '\section' in line:
      artist = getName( line )
    if '\subsection' in line:
      song   = getName( line )

    if '\\begin{Ve' in line:
      reading = True
      continue

    if '\\end{Ve' in line:
      reading = False
      addSong( artist, song, content )
      content = []

    if reading:
      content.append(checkLine(line))

def getName(line):
  artist = re.search( '{.*}', line ).group(0)
  return artist.replace('{','').replace('}','')

def addSong( artist, song, content ):
  me = User.objects.get(username='mre')
  date = "10/10/10"

  toAdd = Song( name=song, artist=artist, album='' , content='<br>'.join(content),
        author=me.get_profile(), lastEdit=me.get_profile(),
        timeLastEdit= date, timeCreated= date
        )
        
  toAdd.save()

  me. songs.add( toAdd )

def checkLine(line):
  if '{\\bf' in line:
    line = line.replace('{\\bf','').replace('}','')
  return line.replace('\n','')
