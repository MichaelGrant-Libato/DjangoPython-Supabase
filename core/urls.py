from django.urls import path
from .views import upload_avatar

urlpatterns = [
    path("upload-avatar/", upload_avatar, name="upload_avatar"),
]
