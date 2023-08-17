def is_admin(request):
    return {'is_admin': request.user.groups.filter(name='admin').exists()}

def is_owner(request):
    return {'is_owner': request.user.groups.filter(name='owner').exists()}

def is_karyawan(request):
    return {'is_karyawan': request.user.groups.filter(name='karyawan').exists()}

