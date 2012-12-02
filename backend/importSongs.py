# django stuff
# utils
import os, sys, pdb
import json, subprocess, shutil
import re
# library links
from backend.forms  import newSong
from backend.models import Song
#cross site forgery exempt
# exceptions
from django.core.exceptions import ObjectDoesNotExist

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
  args = ""
  help ='Import images into the system'

  def handle(self, *args, **options):
    print "helloo!"
