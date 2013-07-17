from temperature.DataFetcher import DataFetcher
from django.conf import settings
from models import Statistic
from datetime import datetime,date,timedelta
from time import mktime

class StatisticManager:

	def __init__(self):
		self.__dataFetcher = DataFetcher()
		self.__today = None

	def setToday(self,today):
		self.__today = today

	def getYesterdaysIndicators(self,sensor):
		if(self.__today == None):
			self.setToday(date.today())

		yesterday = self.__today-timedelta(1)
		tmp_ts_from = int(mktime(yesterday.timetuple()))
		tmp_ts_to = tmp_ts_from + 24*60*60
		ts_from = tmp_ts_from * 1000
		ts_to = tmp_ts_to * 1000

		self.__dataFetcher.compileUrl("viabasse",sensor,ts_from,ts_to)

		if self.__dataFetcher.call() == 1 and self.__dataFetcher.getStatusCode() == 200:

			data = self.__dataFetcher.getJson()

			min_value = Statistic(day=self.__today,k="min_temp",v=10000.0,sensor=sensor,type="daily")
			max_value = Statistic(day=self.__today,k="max_temp",v=-10000.0,sensor=sensor,type="daily")
			sum_value = 0
			count_value = 0

			for line in data:

				if line["temperature"] < min_value.v:
					min_value.v = float(line["temperature"])
					min_value.when = datetime.fromtimestamp((int(line["timestamp"])/1000)+settings.TMZDIFF)
				if line["temperature"] > max_value.v:
					max_value.v = float(line["temperature"])
					max_value.when = datetime.fromtimestamp((int(line["timestamp"])/1000)+settings.TMZDIFF)

				sum_value = sum_value + line["temperature"]
				count_value = count_value + 1

			avg_value = Statistic(day=self.__today,k="avg_temp",v=round(sum_value/count_value,2),sensor=sensor,type="daily")

			return {'min':min_value,'max':max_value,'avg':avg_value}
		else:
			return None