from django.http import HttpResponse
from django.template import Context, loader
import json, math, time
from django.conf import settings
from datetime import datetime,date,timedelta
from time import mktime
from models import Statistic
from google.appengine.ext import db
from temperature.helpers import makeRequest

def index(request, sensor = "out"):

    ts_to = int(time.time())*1000;
    ts_from = ts_to - 7*24*60*60*1000;    
    result = makeRequest(sensor,ts_from,ts_to)

    plots = []

    if result.status_code == 200:
        
        json_data = result.content
        data = json.loads(json_data)

        template = loader.get_template('temperatures_table.html')

        for line in data:
            true_timestamp = (int(line["timestamp"])/1000)+settings.TMZDIFF
            
            line["date"] = datetime.fromtimestamp(true_timestamp).strftime("%d/%m/%Y %H:%M:%S")
            
            d = datetime.fromtimestamp(true_timestamp)
            js_date = "new Date({}, {}, {}, {}, {}, {})".format(d.year,d.month-1,d.day,d.strftime("%H"),d.strftime("%M"),d.strftime("%S"))
            plot_line = { 'x' : js_date, 'y' : line["temperature"] }
            plots.append(plot_line)

        context = Context({ 'data': data[::-1], 'last': data[-1], 'plots': plots })
        return HttpResponse(template.render(context))

    return HttpResponse("Error")

def stats(request, sensor):

    yesterday = date.today()-timedelta(1)
    tmp_ts_from = int(mktime(yesterday.timetuple()))
    print tmp_ts_from
    tmp_ts_to = tmp_ts_from + 24*60*60
    ts_from = tmp_ts_from * 1000
    ts_to = tmp_ts_to * 1000

    result = makeRequest(
        sensor,
        ts_from,
        ts_to
        )

    if result.status_code == 200:

        data = json.loads(result.content)

        min_value = Statistic(day=datetime.fromtimestamp(tmp_ts_from).date(),k="min_temp",v=10000.0,sensor=sensor)
        max_value = Statistic(day=datetime.fromtimestamp(tmp_ts_from).date(),k="max_temp",v=-10000.0,sensor=sensor)
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

        avg_value = Statistic(day=datetime.fromtimestamp(tmp_ts_from).date(),k="avg_temp",v=round(sum_value/count_value,2),sensor=sensor)

    db.put(min_value)
    db.put(max_value)
    db.put(avg_value)

    return HttpResponse("min: {}, max: {}, avg: {}".format(min_value.v,max_value.v,avg_value.v))
