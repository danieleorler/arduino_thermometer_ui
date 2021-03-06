# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import Context, loader
import math, time
from django.conf import settings
from datetime import datetime,date,timedelta
from time import mktime
from models import Statistic
from models import Setting
from google.appengine.ext import db
from temperature.DataFetcher import DataFetcher
from temperature.StatisticManager import StatisticManager
from temperature.Facebook import Facebook
import logging

def index(request, sensor = "out"):

    ts_to = int(time.time())*1000;
    ts_from = ts_to - 7*24*60*60*1000;
    
    dataFetcher = DataFetcher()
    dataFetcher.compileUrl("viabasse",sensor,ts_from,ts_to)

    plots = []

    if dataFetcher.call() == 1 and dataFetcher.getStatusCode() == 200:
        
        data = dataFetcher.getJson()

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

def stats(request, sensor, type):

    sm = StatisticManager()
    indicators = None

    if(type == "daily"):
        indicators = sm.getLastDayIndicators(sensor)
        
    if(type == "monthly"):
        indicators = sm.getLastMonthIndicators(sensor)

    if(indicators != None):

        db.put(indicators["min"])
        db.put(indicators["max"])
        db.put(indicators["avg"])
        db.put(indicators["range"])

        logging.info("{} indicators -> min: {}, max: {}, avg: {}, range: {}".format(type,indicators["min"].v,indicators["max"].v,indicators["avg"].v,indicators["range"].v))

    else:
        print logging.info("Nothing to compute")

    return HttpResponse('OK', status=200)

def manualStats(request, sensor, type, date):

    day = datetime.strptime(date, '%Y-%m-%d').date()
    sm = StatisticManager()
    sm.setToday(day)

    indicators = None

    if(type == "daily"):
        indicators = sm.getLastDayIndicators(sensor)

    if(type == "monthly"):
        indicators = sm.getLastMonthIndicators(sensor)

    if(indicators != None):

        db.put(indicators["min"])
        db.put(indicators["max"])
        db.put(indicators["avg"])
        db.put(indicators["range"])

        logging.info("{} indicators -> min: {}, max: {}, avg: {}, range: {}".format(type,indicators["min"].v,indicators["max"].v,indicators["avg"].v,indicators["range"].v))

    else:
        print logging.info("Nothing to compute")

    return HttpResponse('OK', status=200)

def indicators(request, sensor, type):

    indicators = dict()

    q = db.Query(Statistic)

    if(type == "daily"):
        q.filter('day >', date.today()-timedelta(90)).filter('sensor = ',sensor).filter('type = ',type).order('day')

    if(type == "monthly"):
        q.filter('sensor = ',sensor).filter('type = ',type).order('day')
    
    for stat in q.run():
        if(not stat.day in indicators):
            indicators[stat.day] = {"day":"new Date({}, {}, {})".format(stat.day.year,stat.day.month-1,stat.day.day)}

        indicators[stat.day][stat.k] = stat.v


    context = Context({ 'table': indicators })
    template = loader.get_template('indicators_chart.html')
    return HttpResponse(template.render(context))

def publish(request):
    
    sensor = 'out'
    type = 'daily'

    max_value = 0
    min_value = 1000
    sum_value = 0
    cnt_value = 0

    q = db.Query(Statistic)
    q.filter('day >', date.today()-timedelta(6)).filter('sensor = ',sensor).filter('type = ',type).filter('k = ','min_temp').order('day')
    for stat in q.run():
        if(stat.v < min_value):
            min_value = stat.v

    q = db.Query(Statistic)
    q.filter('day >', date.today()-timedelta(6)).filter('sensor = ',sensor).filter('type = ',type).filter('k = ','max_temp').order('day')
    for stat in q.run():
        if(stat.v > max_value):
            max_value = stat.v

    q = db.Query(Statistic)
    q.filter('day >', date.today()-timedelta(6)).filter('sensor = ',sensor).filter('type = ',type).filter('k = ','avg_temp').order('day')
    for stat in q.run():
        cnt_value = cnt_value + 1
        sum_value = sum_value + stat.v
    avg_value = round(sum_value/cnt_value,2)
    rng_value = max_value - min_value

    message_template = "Last week temperatures:\n* min: {} C\n* max: {} C\n* avg: {} C\n* max - min: {} C\n\n http://arduinothermometer.appspot.com/"
    message = message_template.format(min_value,max_value,avg_value,rng_value)

    facebook = Facebook()
    result = facebook.postToFacebook(message)
    logging.info(result)
    return HttpResponse('OK', status=200)



