from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
    def decorator(func):
        def wrap(request,*args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            request.is_admin = group == 'Admin'
            request.is_pegawai = group == 'Pegawai'
            

            if group in allowed_roles:
                return func(request, *args, **kwargs)
            else: 
                return HttpResponse('nda boleh kesini')
            # group_name = request.user.groups.values_list('name',flat = True)[0]
            # if group_name in allowed_roles:
            #     return func(request,*args, **kwargs)
            # else :
            #     raise PermissionDenied
        return wrap
    return decorator