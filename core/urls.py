
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='api/', permanent=False)),
    path('api/', include('accounts.urls')),
    #path("drugs/", include('drugs.urls'))
]
