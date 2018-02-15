from django.shortcuts import render
from .models import *
import csv
# Create your views here.
from django.http import HttpResponse

# data science libraries
from .functions import analyser
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
# with open('/home/itachi/newsite/static/data.csv') as f:
# 	reader = csv.reader(f)
# 	header = next(reader)
# 	next(reader)
# 	fiels_name = [f.db_column for f in DataModel._meta.get_fields()][1:]
# 	if fiels_name == header[:-5]:
# 		for row in reader:
# 			_, created = DataModel.objects.get_or_create(
# 				Policy_Year=row[0],
# 				TID_No=row[1],
# 				Patient_Name=row[2],
# 				Present_Pkg_Status=row[3],
# 				Hosp_Name=row[4],
# 				Adm_Date=row[5],
# 				Disch_Date=row[6],
# 				Pkg_Code=row[7],
# 				Pkg_Name=row[8],
# 				Pkg_Rate=row[9],
# 				Pkg_Cat=row[10],
# 				Dist_Name=row[11],
# 				Id_Type=row[12],
# 				Identity_No=row[13],
# 				Verified_Aadhar_No=row[14],
# 				Hospital_Type=row[15],
# 				Hospital_Code=row[16],
# 				Admission_Time=row[17],
# 				Discharge_Time=row[18],
# 				Last_Mod_Date=row[19],
# 				Net_Paid_Amt=row[20],
# 				)


qs = DataModel.objects.all()
df = pd.DataFrame(list(qs.values()))
df.drop('id', axis=1, inplace=True)
df.reset_index(drop=True,inplace=True)
df.columns=sorted([f.db_column for f in DataModel._meta.get_fields()][1:], key=str.lower)
df.loc[:,'year'] = df['TID No'].apply(lambda x: '20'+x[5:7])
df.loc[:,'month'] = df['TID No'].apply(lambda x: x[3:5])
df.loc[:,'day'] = df['TID No'].apply(lambda x: x[1:3])
df.loc[:,'Time'] = df[['year', 'month', 'day']].apply(lambda x: '-'.join(x), axis=1)
df.loc[:,'Time'] = df['Time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
df['year'] = df['year'].astype(int)
df['month'] = df['month'].astype(int)


#data = pd.read_csv('/home/itachi/newsite/static/data.csv')
pkg_list = sorted(list(df['Pkg Name'].unique()))
dist_list = sorted(list(df['Dist Name'].unique()))
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

		plot = analyser(df, maincate, subcate1, subcate3, subcate4, subcate5, subcate6)
		
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		STATIC_ROOT = os.path.join(BASE_DIR, 'static')
		img_path = os.path.join(STATIC_ROOT, 'analyse/images')

		plot.savefig(os.path.join( img_path, str(maincate)+str(".png")), bbox_inches = 'tight')
		plt.close('all')
		path = os.path.join( 'analyse/images', str(maincate)+str(".png")) #'images/filename.png'

		return render(request, 'analyse/index.html', {"pkg_list": pkg_list, "dist_list": dist_list, "renal_cardiac_disease":renal_cardiac_disease, "natal_disease":natal_disease, "path": path})

def compute():
	return 'a + b'
