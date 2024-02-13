from django.contrib import admin


class CustomAppAdmin(admin.AdminSite):
    site_title = site_header = "LighTech"
    index_title = "Главная страница"


admin_site = CustomAppAdmin()
