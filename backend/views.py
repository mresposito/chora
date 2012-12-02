# django stuff
from django.http import HttpResponse, HttpResponseForbidden
from django.http import HttpResponseServerError, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
# authentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# utility fuctions
from utils. utils   import *
from utils. timer   import Timer
# application modules
from backend.forms  import newSong
from backend.models import Song, UserProfile
from backend.latex  import makeTex
from backend.forms import searchForm
# exceptions
from django.core.exceptions import ObjectDoesNotExist
import settings
import pdb

## funs
@login_required
def home(request):
  songs     = request.user.songs.all().order_by('artist')
  num_songs = len( songs )
  return render_to_response('home.html', {"ordered":order(songs),
    "num_songs": num_songs, 'searchForm':searchForm()},
      context_instance=RequestContext(request))

@login_required
def editSong( request ):
  if request.method == 'POST':
    form = newSong(request.POST)

    if form.is_valid():
      song_id = form.cleaned_data['song_id'] 
      name    = form.cleaned_data['name'   ].rstrip().lstrip() 
      album   = form.cleaned_data['album'  ].rstrip().lstrip()
      artist  = form.cleaned_data['artist' ].rstrip().lstrip()
      content = form.cleaned_data['content']

      user = request.user.get_profile()
      if song_id != None:
        toAdd       = Song.objects.get(id = song_id)
        author      = toAdd.author
        createdDate = toAdd.timeCreated
      else:
        author      = user
        createdDate = todaysDate()

      # change authorship for the song
      if song_id == None  \
          or 'w' not in toAdd. permission:

        toAdd = Song( name=name, artist=artist, album=album, content=content,
            author=author, lastEdit= user,
            timeLastEdit= todaysDate(), timeCreated= createdDate)
      else:
        toAdd.name         = name   
        toAdd.album        = album  
        toAdd.artist       = artist 
        toAdd.content      = contentToHTML(content)
        toAdd.lastEdit     = user
        toAdd.timeLastEdit = todaysDate()

      toAdd.save()
      user.songs.add( toAdd )

      return HttpResponseRedirect('/viewSong?song=%s' % toAdd.id)
  elif request.GET.has_key('song'):
    try:
      form = newSong(fillForm(request.GET['song']))
      song_id = request.GET['song']
    except ObjectDoesNotExist:
      raise Http404
  else:
    song_id = 0
    form = newSong()

  return render_to_response('editSong.html', {'form':form, 'song_id':song_id,
      'searchForm':searchForm()}, context_instance=RequestContext(request))

@get_required
def viewSong( request ):
  try:
    request_id = request.GET['song']
  except MultiValueDictKeyError:
    raise Http404

  song = Song.objects.get(id = request_id)
  if request.user.is_authenticated():
    like    = request.user.profile in song. like.all()
    dislike = request.user.profile in song. dislike.all()
    have_it = song in request.user.songs.all()
  else:
    have_it = False
    like    = False
    dislike = False
  
  numLikes = len( song.like.all() ) - len( song.dislike.all() )
  return render_to_response('viewSong.html', {'song':song, \
      'num_share': len(song.users.all()), 'have_it': have_it,
      'like' : like, 'dislike': dislike, 'numLikes':numLikes,
      'searchForm': searchForm()} \
      , context_instance=RequestContext(request))

def userLogin(request):
  if request.method == 'GET':
    return render_to_response('registration/login.html', { 'searchForm':searchForm() },
        context_instance=RequestContext(request))
  try:
    from django.contrib.auth import authenticate, login
    print request.POST
    user = authenticate(username=request.POST['username'],password=request.POST['password'])
    if user is not None:
      login(request,user)
      return HttpResponseRedirect( '/home' )

    return render_to_response('registration/login.html', {'message':'Username or password does not exist', 'searchForm': searchForm()},
        context_instance=RequestContext(request))

  except UserProfile.DoesNotExist:
    return render_to_response('registration/login.html', {'message':'Username or password does not exist', 'searchForm': searchForm()},
        context_instance=RequestContext(request))

def createUser(request):
  if request.method == 'GET':
    return render_to_response('registration/createUser.html', {'searchForm': searchForm()},
        context_instance=RequestContext(request))

  userName = request.REQUEST.get('username', None)
  userPass = request.REQUEST.get('password', None)

  # TODO: check if already existed
  if userName and userPass:
     created = User.objects.create_user(userName, userName, userPass)
     if created:
       created.save()
       print "successfully created"
       return HttpResponseRedirect('/home/')
        # user was created
     else:
        # user was retrieved
      return render_to_response('registration/createUser.html', {'message':'The user is already registered.', 'searchForm': searchForm()},
        context_instance=RequestContext(request))
  else:
    pass
     # request was empty

  return render(request,'home.html')

@login_required
def printSongs( request ):

  with Timer( ):
    pdfFile = makeTex( request.user )

  return HttpResponseRedirect("/static/"+pdfFile)

@login_required
@post_required
def toggleSongToCollection( request ):
  try:
    request_id = request.POST['song']
  except MultiValueDictKeyError:
    raise Http404
  
  song = Song.objects.get(id = request_id)
  if song not in request.user.songs.all():
    request.user.songs.add( song )
@login_required
@post_required
def toggleVote ( request):
  try:
    request_id = request.POST['song']
    like       = request.POST['like'] == 'true'
  except MultiValueDictKeyError:
    raise Http404

  song = Song.objects.get( id = request_id )
  user = request.user.profile
  if like:
    if user in song. dislike.all():
      song.dislike. remove ( user )
    song. like. add ( user )
  else:
    if user in song. like.all():
      song.like. remove ( user )
    song. dislike. add ( user )

  song.save()
  return HttpResponseRedirect('/home/')

@login_required
@get_required
def deleteSong( request ):
  try:
    request_id = request.GET['song']
  except MultiValueDictKeyError:
    raise Http404

  # remove from user list
  try:
    songToRemove = Song.objects.get( id = request_id )
  except ObjectDoesNotExist:
    raise Http404
  
  request.user.songs.remove( songToRemove )
  
  # if the song is in no users' list, remove.
  if not  songToRemove.users.all(): 
    songToRemove.delete()

  return HttpResponseRedirect("/home/")

def search(request):
  if 'q' in request.GET:
    entry_list = Song.objects.filter(
      name__contains=request.GET['q']
    )
    if entry_list.count() == 1:
      return HttpResponseRedirect('/viewSong?song=%d'%entry_list.all()[0].id)

    return render_to_response("search.html",
        {'entry_list':entry_list, 'searchForm':searchForm()},
      context_instance=RequestContext(request))
  else:
    return render_to_response("search_error.html",
      {'error':'Search query missing.', 'searchForm':searchForm() },
      context_instance=RequestContext(request))

### HELPER FUNCTIONS ###
def fillForm( song_id ):
  song = Song.objects.get(id = song_id)
  return {
      "song_id" : song.id,
      "name"    : song.name,
      "artist"  : song.artist,
      "album"   : song.album,
      "content" : HTMLToContent(song.content)
    }

def order( songs ): 
  if len( songs ) < 1:
    return
  prev = songs[0].artist
  ordered = []
  SGS     = []
  for song in songs:
    if prev != song.artist:
      ordered.append( {'artist': prev, 'songs': SGS} )
      prev    = song.artist
      SGS     = []
    SGS. append( song ) 
  # add last artist  
  ordered.append( {'artist': prev, 'songs': SGS} )
  return sorted(ordered, key=lambda x:x['artist'])
