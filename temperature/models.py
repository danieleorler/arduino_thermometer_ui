from google.appengine.ext import db

# Create your models here.
class Statistic(db.Model):
	day = db.DateProperty()
	k = db.StringProperty()
	v = db.FloatProperty()
	when = db.DateTimeProperty()
	sensor = db.StringProperty()