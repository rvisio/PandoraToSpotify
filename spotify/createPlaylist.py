import spotipy
import spotipy.util as util 
import json
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

@app.route('/songPost', methods = ['POST', 'GET'])
def songPost():
	print request.json
	if request.method == 'POST':
		print request.json

		content = request.get_json(silent=True)
		
		artist = content['songInfo']['artist']
		title = content['songInfo']['song']

		add_track_to_playlist(artist,title)
		return app.response_class(request.json, content_type='application/json')
	else:
		print 'ERROR'
		print 'wasnt interpreted as post'
		return app.response_class(request.json, content_type='application/json')

@app.route('/song/<songData>')
@cross_origin()
def show_song(songData):
	print request.method
	print request.headers
	print 'entering show song'
	print songData
	songString = json.loads(songData)

	artist = songString['songInfo']['artist']
	title = songString['songInfo']['song']
	print artist,title
	add_track_to_playlist(artist, title)
	
	return app.response_class(songString['songInfo']['artist'], content_type='application/json')



def add_track_to_playlist(artist,songName):
	
	# Authenticate user
	#TODO
	 #need to get custom user input for username
	username = 'rob271992'

	# Client ID, secret key and redirect URI are set in system variables
	playlistName = 'Liked On Pandora'
	token = util.prompt_for_user_token(username, scope='playlist-modify-public')
	if token:
		sp = spotipy.Spotify(auth=token)
		sp.trace = False
	
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
		queryParam = ' '.join([artist,songName])
		print queryParam
		songResult = sp.search(q=queryParam, limit = 1)
		print songResult

		for i,t in enumerate(songResult['tracks']['items']):
			songId = [t['id']]
			print songId
		
		# Add song to liked on pandora playlist 	
		print 'adding the following song to the users playlist ', songId
		results = sp.user_playlist_add_tracks(username, playlistId, songId)
		
		
	else:
		print('cannot get token for user', username)
