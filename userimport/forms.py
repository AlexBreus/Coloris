#! -*- coding: utf-8 -*-
from django import forms
import pyexcel.ext.xls # pip install pyexcel-xls
import pyexcel.ext.xlsx # pip install pyexcel-xlsx

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField(
    	label=u'Загрузите файл Excel',
    	# allow_empty_file=True
    )

class UserForm(forms.Form):
	name = forms.CharField(max_length=30, label=u'Имя')
	patronymic = forms.CharField(max_length=30, label=u'Отчество')
	surname = forms.CharField(max_length=30, label=u'Фамилия')	
	birthday = forms.DateField(label=u'Дата рождения')
	email = forms.EmailField(max_length=70, label=u'Email')