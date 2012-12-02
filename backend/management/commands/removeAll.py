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
    Song.objects.all().delete()
