from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
    def decorator(func):
        def wrap(request,*args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            request.is_admin = group == 'admin'
            request.is_karyawan = group == 'karyawan'
            request.is_owner = group == 'owner'

            if group in allowed_roles:
                return func(request, *args, **kwargs)
            else: 
                return HttpResponse('nda boleh kesini')

        return wrap
    return decorator