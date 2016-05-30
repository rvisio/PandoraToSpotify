var isPandora = false;

chrome.tabs.getSelected(null, function(tab) {
  var tabLink = tab.url;
  console.log("this should show");
  if(tabLink === "http://www.pandora.com/"){
    isPandora = true;
    addSongToPlaylist(isPandora);
  }
});

function addSongToPlaylist(check){
  var href = document.getElementsByClassName("artistSummary");
  alert(href.length);
}
