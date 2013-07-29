from google.appengine.api import urlfetch
import json

class DataFetcher:
	__urlPattern = "http://sultry-ridge-5201.herokuapp.com/survey?device={}&sensor={}&from={}&to={}"


	def __init__(self):
		self.__url = ""
		self.__statusCode = -1
		self.__content = None
		self.__contentJson = None
		urlfetch.set_default_fetch_deadline(10)

	def compileUrl(self,device,sensor,ts_from,ts_to):
		self.__url = self.__urlPattern.format(device,sensor,ts_from,ts_to)

	def call(self):
		if(self.__url.__len__() > 0):
			result = urlfetch.fetch(self.__url)
			self.__statusCode = result.status_code
			
			if(self.__statusCode == 200):
				self.__content = result.content
				self.__contentJson = json.loads(self.__content)
				return 1
			else:
				return 0
		else:
			return 0

	def getStatusCode(self):
		return self.__statusCode

	def getCompiledUrl(self):
		return self.__url

	def getJson(self):
		return self.__contentJson