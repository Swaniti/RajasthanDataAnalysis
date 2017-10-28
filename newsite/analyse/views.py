from django.shortcuts import render
from .models import *

# Create your views here.
from django.http import HttpResponse

# data science libraries
from .functions import patient_traffic
import pandas as pd
data = pd.read_csv('/home/itachi/newsite/static/data.csv')


def index(request):
	if request.method == 'GET':
		return  render(request, 'analyse/index.html')
	else:
		maincate = request.POST.get("Maincategory", "")
		subcate1 = request.POST.get("subcategory1", "")
		subcate2 = request.POST.get("subcategory2", "")
		subcate3 = request.POST.get("subcategory3", "")
		var  = compute(maincate, subcate1)
		fig  = patient_traffic(data, subcate1)
		plots = [maincate, subcate1, subcate2, subcate3]
		return render(request, 'analyse/index.html', {"plots": plots, "fig": fig})

def compute(a,b):
	return a + b
