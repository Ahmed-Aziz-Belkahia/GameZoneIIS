from django.contrib import admin
from help_center.models import Notification, Question, Category, Answer
from import_export.admin import ImportExportModelAdmin



class QuestionAdmin(ImportExportModelAdmin):
	search_fields = ['title']
	list_editable = ['status']
	list_filter = ['status']
	list_display = ('title', 'status', 'user', 'answer_status')
	prepopulated_fields = {'slug':('title',)}

	def title(self):
		return self.title[0:10]

class CategoryAdmin(ImportExportModelAdmin):
	prepopulated_fields = {'slug':('title',)}
	list_display = ['title', 'active']

class AnswerAdmin(ImportExportModelAdmin):
	list_editable = ['active']
	list_filter = ['active']
	list_display = ['question', 'active',]
	
class NotiAdmin(ImportExportModelAdmin):
	list_display = ['user', 'question', 'answer','seen',]

# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Answer, AnswerAdmin)
# admin.site.register(Notification, NotiAdmin)