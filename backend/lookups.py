from selectable.base import ModelLookup
from selectable.registry import registry, LookupAlreadyRegistered
from backend.models import Song

class EntryLookup(ModelLookup):
  model = Song
  search_fields = ('name__icontains',)

  def get_query(self, request, term):
    results = super(EntryLookup, self).get_query(request, term)
    state = request.GET.get('state', '')
    if state:
        results = results.filter(state=state)
    return results
  
  def get_item_label(self, item):
    return u'%s'% item.name

  def get_item_value(self, item):
    return u'%s'% item.name

  def __repr__ ( self ):
    return "%s"% self.name

try:
  registry.register(EntryLookup)
except LookupAlreadyRegistered:
  pass
