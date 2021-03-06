from google.appengine.ext import db

# Create your models here.
class Statistic(db.Model):
	day = db.DateProperty()
	k = db.StringProperty()
	v = db.FloatProperty()
	when = db.DateTimeProperty()
	sensor = db.StringProperty()
	type = db.StringProperty(required=True, choices=set(["daily", "monthly", "yearly"]))

class Setting(db.Model):
    k = db.StringProperty()
    v = db.StringProperty()