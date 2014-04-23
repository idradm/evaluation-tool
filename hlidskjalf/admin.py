from django.contrib import admin
from hlidskjalf.models import DataItem, DataSet, Item, Result, Type, Run, ResultItem

# Register your models here.
admin.site.register(DataItem)
admin.site.register(DataSet)
admin.site.register(Item)
admin.site.register(Result)
admin.site.register(Type)
admin.site.register(Run)
admin.site.register(ResultItem)
