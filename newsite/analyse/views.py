from django.shortcuts import render
from .models import *

# Create your views here.
from django.http import HttpResponse

# data science libraries
from .functions import analyser
import pandas as pd
import os

data = pd.read_csv('/home/itachi/newsite/static/data.csv')


def index(request):
	if request.method == 'GET':
		return  render(request, 'analyse/index.html')
	else:
		maincate = request.POST.get("Maincategory", "")
		subcate1 = request.POST.get("subcategory1", "")
		subcate2 = request.POST.get("subcategory2", "")
		subcate3 = request.POST.get("subcategory3", "")

		plot = analyser(data, maincate, subcate1, subcate3)
		
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		STATIC_ROOT = os.path.join(BASE_DIR, 'static')
		img_path = os.path.join(STATIC_ROOT, 'analyse/images')

		plot.savefig(os.path.join( img_path, str(maincate)+str(subcate1)+str(subcate3)+str(".png")), bbox_inches = 'tight')

		path = os.path.join( 'analyse/images', str(maincate)+str(subcate1)+str(subcate3)+str(".png")) #'images/filename.png'

		plots = [maincate, subcate1, subcate2, subcate3, path]

		return render(request, 'analyse/index.html', {"plots": plots, "path": path})

def compute():
	return 'a + b'
