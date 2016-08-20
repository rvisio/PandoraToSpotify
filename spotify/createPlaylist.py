import spotipy
import spotipy.util as util 
import json
from flask import Flask

app = Flask(__name__)
@app.route('/song/<songData>')
def show_song(songData):
	print songData
	songString = json.loads(songData)
	print songString
	print songString['songInfo']['artist']

	artist = songString['songInfo']['artist']
	title = songString['songInfo']['song']

	add_track_to_playlist(artist, title)
	return app.response_class(songString['songInfo']['artist'], content_type='application/json')



def add_track_to_playlist(artist,songName):
	
	# Authenticate user
	#TODO
	# need to get custom user input for username
	username = 'rob271992'

	# Client ID, secret key and redirect URI are set in system variables
	playlistName = 'Liked On Pandora'
	token = util.prompt_for_user_token(username, scope='playlist-modify-public')
	if token:
		sp = spotipy.Spotify(auth=token)
		sp.trace = True
	
		# Check if user has playlist, create if not 
		playlists = sp.user_playlists(username)
	
		playlist_list = []
		for p in playlists['items']:
			playlist_list.append(p['name'])

		if playlistName not in playlist_list:
			print('playlist not in current users playlists')
			sp.user_playlist_create(username, playlistName)
		
		#TODO
		# better way of doing this, shouldnt need to query for all playlists again
		playlists = sp.user_playlists(username)

		# Get playlistID for liked on pandora
		for playlist in playlists['items']:
			if playlist['name'] == 'Liked On Pandora':
				playlistId =  playlist['id']
		
		#TODO
		# Get user input for song to add to playlist  
		songResult = sp.search(q='tycho a walk', limit = 1)

		for i,t in enumerate(songResult['tracks']['items']):
			songId = [t['id']]
		
		# Add song to liked on pandora playlist 	
		results = sp.user_playlist_add_tracks(username, playlistId, songId)
		print results
		
		
	else:
		print('cannot get token for user', username)
