from django.contrib import admin

from webapp.models import UserProfile, Auto, Order, Services, Mark, AutoModel, Reviews, ServiceCategory

admin.site.register(UserProfile)
admin.site.register(Mark)
admin.site.register(AutoModel)
admin.site.register(Auto)
admin.site.register(ServiceCategory)
admin.site.register(Services)
admin.site.register(Order)
admin.site.register(Reviews)
