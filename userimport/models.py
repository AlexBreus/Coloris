from django.db import models

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=30)
	patronymic = models.CharField(max_length=30)
	surname = models.CharField(max_length=30)	
	birthday = models.DateField()
	email = models.EmailField(max_length=70, blank=True, null= True, unique= True)

	def __str__(self):
		return self.name

	class Meta:
		# db_table = 'Users'
		# verbose_name = 'Users'
		verbose_name_plural = 'Users'