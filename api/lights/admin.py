from django.contrib import admin

from lights.models import get_register_eligible_models

for model in get_register_eligible_models():
    admin.site.register(model)
