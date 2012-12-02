from django import forms
from django.forms import ModelForm
from backend.models import Song
from selectable.forms import AutoCompleteWidget
from backend.lookups import EntryLookup

class newSong( forms.Form ):
  song_id = forms.DecimalField( label="song id"  , required=False)
  name    = forms.CharField   ( label=" Song name", max_length=30)
  artist  = forms.CharField   ( label="Artist"   , max_length=30)
  album   = forms.CharField   ( label="Album"    , max_length=30, required=False)
  content = forms.CharField   ( label="Content"  , max_length=4000,
      widget=forms.Textarea(attrs={'rows':50, 'cols':100}))

class searchForm(forms.Form):
  q = forms.CharField(
    label='',
    widget=AutoCompleteWidget(EntryLookup, attrs={'id':'searchField', 'placeholder':"Search"}),
    required=False,
  )
