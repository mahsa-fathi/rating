from django.contrib import admin
from social.models import Post, UserRating


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['id', 'created_at', 'updated_at', 'title', 'author']
    fields = ['title', 'content', 'author', 'rate', 'number_of_rates', 'created_at', 'updated_at']

    def get_readonly_fields(self, request, obj=None):
        return ['rate', 'number_of_rates', 'created_at', 'updated_at']

    @staticmethod
    def rate(obj):
        return obj.rate

    @staticmethod
    def number_of_rates(obj):
        return obj.number_of_rates


class UserRatingAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['id', 'created_at', 'updated_at', 'user', 'post', 'rate']
    fields = ['user', 'post', 'rate', 'created_at', 'updated_at']

    def get_readonly_fields(self, request, obj=None):
        return ['created_at', 'updated_at']


admin.site.register(Post, PostAdmin)
admin.site.register(UserRating, UserRatingAdmin)
