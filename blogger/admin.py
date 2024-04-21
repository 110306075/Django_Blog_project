from django.contrib import admin
from .models import post, Author, Tag, Comment
# Register your models here. to the /admin interface


class PostAdmin(admin.ModelAdmin):
    list_filter=(('author','tags','date'))
    list_display=('title','date','author')
    prepopulated_fields={'slug':('title',)}

class AuthorAdmin(admin.ModelAdmin):
    list_filter=(('last_name',))
    list_display=('first_name','last_name','email')

class TagAdmin(admin.ModelAdmin):
    list_filter=(('captions',))
    list_display=('captions',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','date')

admin.site.register(post,PostAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Comment,CommentAdmin)

