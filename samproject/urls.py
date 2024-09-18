"""
URL configuration for samproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import staticfiles
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from backend.views import home,list_videos, upload_image, process_image, list_images, list_results_images
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('upload_image/', upload_image, name='upload_image'),  # 添加上传图片的URL
    path('process_image/', process_image, name='process_image'),
    path('list_images/<path:image_path>', list_images, name='list_images'),
    path('list_results_images/', list_results_images, name='list_results_images'),
    path('list_videos/', list_videos, name='list_videos'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static('/static/images/', document_root=settings.RESULTS_ROOT)
    urlpatterns += static('/results/', document_root='/mnt/my_volume/Inpaint-Anything-main/samproject/results')
urlpatterns += staticfiles_urlpatterns()

