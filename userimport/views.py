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
	args['title'] = u'Импорт пользователей'
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
	args['title'] = u'Пользователи'
	args['users'] = []
	users = User.objects.all()

	for user in users:
		args['users'].append({
			'id': user.id,
			'name': user.name,
			'patronymic': user.patronymic,
			'surname': user.surname,
			'birthday': str(user.birthday),
			'email': user.email,
		})

	return render_to_response('users_list.html', args, context_instance=RequestContext(request))


def deluser(request, user_id):
	user = User.objects.get(id=user_id)
	user.delete()

	return redirect('/users/')

def edituser(request, user_id):
	args = {}
	user = User.objects.get(id=user_id)
	args['title'] = u'Редактирование пользователя: ' + user.name
	user.birthday = str(user.birthday)
	
	if request.POST:
		print(request.POST)
		user.name = request.POST['name']
		user.patronymic = request.POST['patronymic']
		user.surname = request.POST['surname']
		user.birthday = request.POST['birthday']
		user.email = request.POST['email']
		user.save()

		if request.POST['btn'] == 'save':
			return redirect('/users/')

	args['user'] = user
			
	return render_to_response('user.html', args, context_instance=RequestContext(request))