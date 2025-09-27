import io, uuid, mimetypes
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import AvatarUploadForm
from .supabase_client import supabase

@login_required
def upload_avatar(request):
    ctx = {"form": AvatarUploadForm()}
    if request.method == "POST":
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["image"]       # InMemoryUploadedFile
            file_bytes = file.read()                # bytes to send
            ext = (file.name.split(".")[-1] or "bin").lower()
            # Example path: <user_id>/<random>.ext
            path = f"{request.user.id}/{uuid.uuid4().hex}.{ext}"

            # Guess content-type for Supabase
            content_type = mimetypes.guess_type(file.name)[0] or "application/octet-stream"

            # Upload to bucket 'avatars'
            storage = supabase.storage.from_("avatars")
            # v2 client supports passing bytes + path:
            res = storage.upload(path=path, file=file_bytes, file_options={"content-type": content_type})
            # If your client version uses the older signature, try: storage.upload(path, file_bytes)

            # If bucket is public:
            public = storage.get_public_url(path)
            # Some clients return dict; normalize:
            public_url = public.get("publicUrl") if isinstance(public, dict) else public

            # If bucket is private, create a short-lived signed URL (e.g., 10 minutes):
            signed = storage.create_signed_url(path, 600)
            signed_url = (signed.get("signedURL") or signed.get("signedUrl")) if isinstance(signed, dict) else signed

            ctx.update({"public_url": public_url, "signed_url": signed_url})
        else:
            ctx["form"] = form
    return render(request, "upload_avatar.html", ctx)
