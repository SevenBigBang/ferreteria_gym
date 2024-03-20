from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ferreteria.views import ProductoListView
from .views import inicio,registro,logout_view 
from .views import generate_pdf_report
from .views import generate_excel_report
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', inicio, name='inicio'),
    path('productos/', ProductoListView.as_view(), name='productos'),
    path('generate-pdf-report/', generate_pdf_report, name='generate_pdf_report'),
    path('login/',LoginView.as_view(template_name='sitio/login.html'),name='login'),#new
    path('logout/', logout_view, name='logout'), #new
    path('registro/', registro, name='registro'), #new
    path('generate-excel-report/', generate_excel_report, name='generate_excel_report'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
