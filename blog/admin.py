from django.contrib import admin

# Register your models here.
from blog.models import Post, Category


class PostAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass

# Register the models now


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)

# The reason I am not adding the comments to the admin site is
# becasue it is not necessary to create or edit comments myself.
# But if I want to add a way to moderate the comments and make sure
# they aren't out of control I can easily do so by doing the exact same
# thing as above
