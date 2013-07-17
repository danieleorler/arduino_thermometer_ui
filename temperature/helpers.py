from google.appengine.api import urlfetch

def makeRequest(sensor,ts_from,ts_to):

	url = "http://sultry-ridge-5201.herokuapp.com/survey?device=viabasse&sensor={}&from={}&to={}"
	url = url.format(sensor,ts_from,ts_to)
	return urlfetch.fetch(url)