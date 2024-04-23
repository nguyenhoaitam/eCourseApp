from django.contrib import admin
from django.utils.html import mark_safe
from courses.models import Course, Category, Lesson, Comment, Tag, Like
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
import cloudinary


class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = '__all__'


class MyCourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_date', 'updated_date', 'active']
    search_fields = ['id', 'name']
    list_filter = ['created_date', 'name']
    readonly_fields = ['my_image']
    form = CourseForm

    def my_image(self, course):
        if course.image:
            if type(course.image) is cloudinary.CloudinaryResource:
                return mark_safe(f"<img width='300' src='{course.image.url}' />")
            return mark_safe(f"<img width='300' src='/static/{course.image.name}' />")

    class Media:
        css = {
            'all': ['/static/css/style.css']
        }


admin.site.register(Category)
admin.site.register(Course, MyCourseAdmin)
admin.site.register(Lesson)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Like)
