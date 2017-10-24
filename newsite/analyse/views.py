from django.shortcuts import render
from .models import *

# Create your views here.
from django.http import HttpResponse


def index(request):
	if request.method == 'GET':
		return  render(request, 'analyse/index.html')
	else:
		maincate = request.POST.get("Maincategory", "")
		subcate1 = request.POST.get("subcategory1", "")
		subcate2 = request.POST.get("subcategory2", "")
		subcate3 = request.POST.get("subcategory3", "")
		var  = compute(maincate, subcate1)
		csv = Random.objects.all()
		plots = [maincate, subcate1, subcate2, subcate3, var]
		return render(request, 'analyse/index.html', {"plots": plots, "csv": csv})

def compute(a,b):
  return a + b




