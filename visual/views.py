import io

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg

from .models import list

def list_view(request):
    lists = list.objects.all()
    return render(request, 'index.html',{"lists":lists})

def year_view(request):
    year1 = list.groupby('발생년')
    year2 = year1['발생년'].count()

    label=['2015','2016','2017','2018','2019']

    plt.pie(year2, label=label, autopct='%.1f%%', startangle=360, counterclock=False)

    plt.savefig('C:/djangowork1/accidentsite/static/img/year.png')


