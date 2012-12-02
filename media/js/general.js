function VerifyDelete()
{ return confirm('You sure you want to delete this song?'); }

function deleteSong( number ) 
{
  if (VerifyDelete())
    window.location = '/deleteSong?song='+ number.toString();
}

function addSongToCollection( number ) 
{
  doCSRFstuff();
  var postdata = { song: number, };
  $.post('/toggleSongToCollection/',postdata,function(data) {location.reload();});
}

$(function(){
  $('[id=search]').bind('autocompleteselect', function(event, ui){
    $(this).val(ui.item.value);
    $(this).parents("form").submit();
  });
});

function checkVoteCodition ( tag ) 
{
  if (checkArrowOrange( tag ))
  {
    changeCount( tag.indexOf('up') == -1 );
    swapBlack  ( tag );
    return false;
  }
  else if ( checkArrowOrange( oppositeTag( tag ) ) )
  { // tag is orange for opposite tag
    changeCount( tag.indexOf('up') != -1 );
    swapBlack ( oppositeTag(tag) );
    return true;
  }
  // neither tag is orange
  return true;
}

function oppositeTag( tag )
{
  if( tag.indexOf('up') != -1)
    return 'downArrow';
  return 'upArrow';
}

function changeCount ( increase )
{
  var count = parseInt(document.getElementById('counter').innerHTML);
  if ( increase )
    count += 1;
  else
    count -= 1;
  document.getElementById('counter').innerHTML = count;
}

function swapOrange( tag )
{
  var img = document.getElementById( tag ).src;
  document.getElementById( tag ).src = img.replace('up','orangeArrow');
}

function swapBlack( tag )
{
  var img = document.getElementById( tag ).src;
  document.getElementById( tag ).src = img.replace('orangeArrow','up');
}

function checkArrowOrange( tag )
{  return document.getElementById( tag ).src.indexOf('up') == -1; }

function toggleVote( tag, songId )
{
  if ( ! checkVoteCodition( tag ))
    return

  changeCount( tag.indexOf('up') != -1 );
  swapOrange( tag );

  doCSRFstuff();
  // update the database
  var postdata = { song: songId, like: tag.indexOf('up') != -1 };
  $.post('/toggleVote/',postdata,function(data) {location.reload();});
}

function doCSRFstuff() {
  $('html').ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
              var cookieValue = null;
              if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                          var cookie = jQuery.trim(cookies[i]);
                          if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                      }
                }
              return cookieValue;
          }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          }
  });
}
// $(window).scroll(function () {
//     if ($(window).scrollTop() > 280) {
//         $('.search').css('top', $(window).scrollTop()- 290);
//     }}
// );
