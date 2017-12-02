from django.shortcuts import render
from .models import *

# Create your views here.
from django.http import HttpResponse

# data science libraries
from .functions import analyser
import pandas as pd
import os

data = pd.read_csv('/home/ubuntu/RJ-anal/Django-app/newsite/static/data.csv')
pkg_list = sorted(list(data['Pkg Name'].unique()))
dist_list = sorted(list(data['Dist Name'].unique()))
renal_cardiac_disease = ['Nephroureterectomy for Transitional Cell Carcinoma of renal pelvis (one side)',
    'Laproscopic surgery for kidney & supra renal any type',
    'Splenorenal Anastomosis', 'Splenectomy - For -  Trauma',
    'Maintenance Hemodialysis (Mhd) (With Inj. Erythropoetine With Inj. Iron) –Per Dialysis.',
    'Brachiocephalic Av Fistula For Hemodialysis',
    'AV Shunt for dialysis', 'Aural polypectomy', 'Reimplanation  of Urethra', 'Refractory Cardiac Failure']
natal_disease = ['Special Pkg for Neo Natal Care (Babies admitted with mild-moderate respiratory distress, Infections/sepsis with no major complications, Prolonged/persistent jaundice, Assisted feeding for low birth weight - babies (<1800 gms), Neonatal seizures)',
    'Nephrectomy', 'neonatal jaundice #',
    'Basic Package for Neo -  Natal Care (Package for Babies admitted for short term care for conditions like: Transient tachypnoea of newborn, Mild birth asphyxia, Jaundice requiring phototherapy, Hemorrhagic disease of newborn, Large for date',
    'Advanced Pkg for - Neo Natal Care (Low birth weight babies <1500 gm and all babies admitted with complications like Meningitis, Severe respiratory distress - Shock, Coma, Convulsions or Encephalopathy, Jaundice requiring exchange transfusion, NEC)'
    ]

                             
def index(request):
	if request.method == 'GET':
		return  render(request, 'analyse/index.html', {"pkg_list": pkg_list, "dist_list": dist_list, "renal_cardiac_disease":renal_cardiac_disease, "natal_disease":natal_disease})
	else:
		maincate = request.POST.get("Maincategory", "")
		subcate1 = request.POST.get("subcategory1", "")
		subcate2 = request.POST.get("subcategory2", "")
		subcate3 = request.POST.get("subcategory3", "")
		subcate4 = request.POST.get("subcategory4", "")
		subcate5 = request.POST.get("subcategory5", "")
		subcate6 = request.POST.get("subcategory6", "")

		plot = analyser(data, maincate, subcate1, subcate3, subcate4, subcate5, subcate6)
		
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		STATIC_ROOT = os.path.join(BASE_DIR, 'static')
		img_path = os.path.join(STATIC_ROOT, 'analyse/images')

		plot.savefig(os.path.join( img_path, str(maincate)+str(subcate1)+str(subcate3)+str(subcate4)+str(subcate5)+str(subcate6)+str(".png")), bbox_inches = 'tight')

		path = os.path.join( 'analyse/images', str(maincate)+str(subcate1)+str(subcate3)+str(subcate4)+str(subcate5)+str(subcate6)+str(".png")) #'images/filename.png'

		return render(request, 'analyse/index.html', {"pkg_list": pkg_list, "dist_list": dist_list, "renal_cardiac_disease":renal_cardiac_disease, "natal_disease":natal_disease, "path": path})

def compute():
	return 'a + b'
