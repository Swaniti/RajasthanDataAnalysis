from django.db import models
# Create your models here.
import csv

class Random(models.Model):	
	data = models.FileField(upload_to = './static')

class DataModel(models.Model):

	Policy_Year = models.CharField(max_length=20, db_column="Policy Year")

	TID_No = models.CharField(max_length=20, db_column="TID No")

	Patient_Name = models.CharField(max_length=150, db_column="Patient Name")

	Present_Pkg_Status = models.CharField(max_length=150, db_column="Present Pkg Status")

	Hosp_Name = models.CharField(max_length=150, db_column="Hosp Name")

	Adm_Date = models.CharField(max_length=150, db_column="Adm Date")

	Disch_Date = models.CharField(max_length=150, db_column="Disch Date")

	Pkg_Code = models.CharField(max_length=20, db_column="Pkg Code")

	Pkg_Name = models.CharField(max_length=500, db_column="Pkg Name")

	Pkg_Rate = models.CharField(max_length=10, db_column="Pkg Rate")

	Pkg_Cat = models.CharField(max_length=20, db_column="Pkg Cat")

	Dist_Name = models.CharField(max_length=20, db_column="Dist Name")

	Id_Type = models.CharField(max_length=20, db_column="Id Type")

	Identity_No = models.CharField(max_length=20, db_column="Identity No")

	Verified_Aadhar_No = models.CharField(max_length=20, db_column="Verified Aadhar No")

	Hospital_Type = models.CharField(max_length=25, db_column="Hospital Type")

	Hospital_Code = models.CharField(max_length=20, db_column="Hospital Code")

	Admission_Time = models.CharField(max_length=150, db_column="Admission Time")

	Discharge_Time = models.CharField(max_length=150, db_column="Discharge Time")

	Last_Mod_Date = models.CharField(max_length=150, db_column="Last Mod Date")

	Net_Paid_Amt = models.CharField(max_length=10, db_column="Net Paid Amt")


