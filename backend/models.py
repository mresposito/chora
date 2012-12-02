from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User

import settings
import random, os, string
     
class UserProfile(models.Model):
  user  = models.ForeignKey(User, unique=True) 

  print_id   = models.CharField   ( max_length = 15, default="None" )
  print_path = models.CharField   ( max_length = 30, default="None" )

  songs = models.ManyToManyField( 'Song', related_name="users" )

  modified   = models.BooleanField( default=True )

  def getPath( self ):
    print self.print_id
    if self.print_id != "None":
      return self.print_path

    unique = create_id()
    self.print_id = unique

    dir_path =  os.path.join(settings.PRINT_DIR,  unique )
    if not os.path.exists( dir_path ):
      os.makedirs( dir_path ) 

    self.print_path = dir_path 
    self.save()
    return self.print_path

  def getPdfPath( self ):
    return os.path.join(os.path.join('prints', self.print_id), 'print.pdf')

def create_id():
  return ''.join(random.choice(string.letters+ string.digits) for x in range(15))

def create_user_profile(sender, instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

User.profile        = property(lambda u: u.get_profile()       )
User.songs          = property(lambda u: u.get_profile().songs )

class Song(models.Model):
  name          = models.CharField ( max_length = 50 )
  artist        = models.CharField ( max_length = 30 )
  album         = models.CharField ( max_length = 40, blank  = True )
  video         = models.CharField ( max_length = 90, blank  = True )
  permission    = models.CharField ( max_length = 3, default = 'rw' )
  content       = models.TextField ( max_length = 9000)

  votes         = models.IntegerField ( default = 0  )
  timeCreated   = models.CharField ( max_length = 10 )
  timeLastEdit  = models.CharField ( max_length = 10 )
  # many to one
  author        = models.ForeignKey( UserProfile )
  like          = models.ManyToManyField( UserProfile, related_name="like")
  dislike       = models.ManyToManyField( UserProfile, related_name="dislike")
  lastEdit      = models.ForeignKey( UserProfile, related_name="lastEdit" )

  def __repr__(self):
    return self.name
