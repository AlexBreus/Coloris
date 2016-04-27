from django.shortcuts import render, render_to_response, redirect
from django.template.context_processors import csrf
from userimport.forms import UploadFileForm, UserForm
from django.template import RequestContext
import pyexcel.ext.xls
import pyexcel.ext.xlsx
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from userimport.models import User
import copy
from django.utils.datastructures import MultiValueDictKeyError

from django import template
register = template.Library()

@register.filter
def index(List, i):
    return List[int(i)]
    

def saveUser(fh, col_1, col_2, col_3, col_4, col_5):
	fh.save_to_database(
		model=User,
		mapdict={
			col_1: 'name',
			col_2: 'patronymic',
			col_3: 'surname',
			col_4: 'birthday',
			col_5: 'email'
		}
	)
	
	return redirect('/users/')


def upload(request):
	args = {}
	global fh
	if request.POST:
		if request.POST['step'] == '2':
			try:
				if request.POST['next'] == '3':
					return saveUser(fh, request.POST['col_1'], request.POST['col_2'], request.POST['col_3'], request.POST['col_4'], request.POST['col_5'])
			except MultiValueDictKeyError:
				form = UploadFileForm(request.POST, request.FILES)
				if form.is_valid():
					filehandle = request.FILES['file']
					fh = copy.deepcopy(request.FILES['file'])

					args['excel_arr'] = filehandle.get_array()
					args['db_column'] = [
						'Имя',
						'Отчество',
						'Фамилия',
						'Год рождения',
						'Email'
					]
	else:
		form = UploadFileForm()
		args['form'] = form

	return render_to_response('upload_form.html', args, context_instance=RequestContext(request))


def showusers(request):
	args = {}

	args['users'] = []
	users = User.objects.all()

	for user in users:
		args['users'].append({
			'name': user.name,
			'patronymic': user.patronymic,
			'surname': user.surname,
			'birthday': str(user.birthday),
			'email': user.email,
			'id': user.id,
		})

	return render_to_response('users_list.html', args, context_instance=RequestContext(request))


def deluser(request, user_id):
	user = User.objects.get(id=user_id)
	user.delete()

	return redirect('/users/')



def edituser(request, user_id):
	args = {}
	user = User.objects.get(id=user_id)
	args['form'] = UserForm()
	args['user'] = [user.id, user.name, user.patronymic, user.surname, user.birthday, user.email]

	if request.POST:
		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.id = User.objects.get(id=user_id)
			form.save()
			
	return render_to_response('user.html', args, context_instance=RequestContext(request))