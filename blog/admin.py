from django.contrib import admin
from blog.models import Post, Comment, Category
from import_export.admin import ImportExportModelAdmin



class ArticleAdmin(ImportExportModelAdmin):
	search_fields = ['title']
	list_editable = ['status', 'category']
	list_filter = ('category', 'status')
	list_display = ('title', 'status', 'category', 'user', 'featured', 'trending')

	def title(self):
		return self.title[0:10]

class CategoryAdmin(ImportExportModelAdmin):
	prepopulated_fields = {'slug':('title',)}
	list_display = ('title', 'active')

class CommentAdmin(ImportExportModelAdmin):
	search_fields = ['comment']
	list_editable = ('active',)
	list_filter = ('active',)
	list_display = ('post', 'active')


admin.site.register(Post, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)