from temboo.Library.Facebook.Publishing import Post
from temboo.core.session import TembooSession
from models import Setting
from google.appengine.ext import db

class Facebook:

	def __init__(self):
		# Instantiate the Choreo, using a previously instantiated TembooSession object, eg:
		self.__session = TembooSession('dalen', 'myFirstApp', '9d8a70e0-eb35-4c38-b')
		self.__postChoreo = Post(self.__session)

		# Get an InputSet object for the choreo
		self.__postInputs = self.__postChoreo.new_input_set()

		# Get token from database
		q = db.Query(Setting)
		facebook_token = q.filter('k = ','facebook_token').get()

		# Set inputs
		self.__postInputs.set_ProfileID("32663722842")
		self.__postInputs.set_AccessToken(facebook_token.v)
		
	def postToFacebook(self,message):

		self.__postInputs.set_Message(message)

		# Execute choreo
		return self.__postChoreo.execute_with_results(self.__postInputs)