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

	def getLastDayIndicators(self,sensor):
		if(self.__today == None):
			self.setToday(date.today())

		yesterday = self.__today-timedelta(1)
		tmp_ts_from = int(mktime(yesterday.timetuple()))
		tmp_ts_to = tmp_ts_from + 24*60*60
		ts_from = tmp_ts_from * 1000 + settings.TMZDIFF
		ts_to = tmp_ts_to * 1000 + settings.TMZDIFF

		return self.computeIndicators("daily",sensor,yesterday,ts_from,ts_to)

	def getLastMonthIndicators(self,sensor):
		import calendar

		if(self.__today == None):
			self.setToday(date.today())
		yesterday = self.__today-timedelta(1)
		
		month = yesterday.month
		year = yesterday.year

		first_day_of_month = datetime.strptime("{}-{}-{}".format(year,month,"01"), '%Y-%m-%d').date()
		last_day_of_month = datetime.strptime("{}-{}-{}".format(year,month,calendar.monthrange(year,month)[1]), '%Y-%m-%d').date()

		tmp_ts_from = int(mktime(first_day_of_month.timetuple()))
		tmp_ts_to = int(mktime(last_day_of_month.timetuple()))
		ts_from = tmp_ts_from * 1000 + settings.TMZDIFF
		ts_to = tmp_ts_to * 1000 + settings.TMZDIFF

		return self.computeIndicators("monthly",sensor,first_day_of_month,ts_from,ts_to)


	def computeIndicators(self,indicator_type,sensor,day_of_computation,ts_from,ts_to):
		self.__dataFetcher.compileUrl("viabasse",sensor,ts_from,ts_to)

		if self.__dataFetcher.call() == 1 and self.__dataFetcher.getStatusCode() == 200:

			data = self.__dataFetcher.getJson()

			min_value = Statistic(day=day_of_computation,k="min_temp",v=10000.0,sensor=sensor,type=indicator_type)
			max_value = Statistic(day=day_of_computation,k="max_temp",v=-10000.0,sensor=sensor,type=indicator_type)
			sum_value = 0
			count_value = 0

			for line in data:

				if line["temperature"] < min_value.v:
					min_value.v = float(line["temperature"])
					min_value.when = datetime.fromtimestamp((int(line["timestamp"])/1000))
				if line["temperature"] > max_value.v:
					max_value.v = float(line["temperature"])
					max_value.when = datetime.fromtimestamp((int(line["timestamp"])/1000))

				sum_value = sum_value + line["temperature"]
				count_value = count_value + 1

			avg_value = Statistic(day=day_of_computation,k="avg_temp",v=round(sum_value/count_value,2),sensor=sensor,type=indicator_type)
			range_value = Statistic(day=day_of_computation,k="range_temp",v=max_value.v-min_value.v,sensor=sensor,type=indicator_type)
			return {'min':min_value,'max':max_value,'avg':avg_value,'range':range_value}
		else:
			return None