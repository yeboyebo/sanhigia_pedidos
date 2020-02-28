
# @class_declaration sanhigia_pedidos #
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_auth
from django.utils.decorators import method_decorator
import hashlib

from models.flfactppal.usuarios import usuarios


class sanhigia_pedidos(yblogin):

    @method_decorator(login_required(login_url='/login'))
    def sanhigia_pedidos_index(self, request):
        if request.GET:
            next_url = request.GET.get('next', None)
            if next_url:
                return HttpResponseRedirect(next_url)

        history = cacheController.addHistory(request, None, None)
        history = history["list"][history["pos"] - 1] if history["pos"] > 0 else history["list"][history["pos"]]
        usuario = request.user.username
        superuser = request.user.is_superuser

        dctMenu = templateCTX.cargaMenuJSON('portal/menu_portal.json')
        dctMenu = dctMenu["items"]
        miMenu = accessControl.accessControl.dameDashboard(request.user, dctMenu)

        return render(request, 'portal/index.html', {'aplic': 'portal', 'menuJson': miMenu, 'usuario': usuario, 'superuser': superuser, 'history': history})

    def sanhigia_pedidos_login(self, request, error=None):
        """ Peticion defecto"""
        if not error:
            error = ''
        return render(request, 'portal/login.html', {'error': error})

    # def sanhigia_pedidos_auth_login(self, request):

    #     _i = self.iface

    #     if request.method == 'POST':
    #         action = request.POST.get('action', None)
    #         username = request.POST.get('username', None).lower()

    #         if action == 'login':
    #             user = authenticate(username=username, password='Sh20Pda17')
    #             if user is not None:
    #                 login_auth(request, user)
    #                 accessControl.accessControl.registraAC()
    #             else:
    #                 return _i.login(request, 'Error de autentificación')
    #             return HttpResponseRedirect("/")
    #     return _i.login(request)

    def sanhigia_pedidos_auth_login(self, request):

        _i = self.iface

        if request.method == 'POST':
            action = request.POST.get('action', None)
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)

            if action == 'login':
                if username == "admin":
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login_auth(request, user)
                        accessControl.accessControl.registraAC()
                    else:
                        return _i.login(request, 'Error de autentificación')
                    return HttpResponseRedirect("/")
                try:
                    sisuser = User.objects.get(username=username)
                except Exception as e:
                    # Si no existe usuario en django lo creamos(Si existe el usuario en tabla usuarios)
                    try:
                        usuario = usuarios.objects.filter(idusuario__exact=username)
                        if len(usuario) == 0:
                            return _i.login(request, 'No existe el usuario')
                        user = User.objects.create_user(username=username, password="Sh20Pda17")
                        user.is_staff = False
                        user.groups.add(Group.objects.get(name='agentes'))
                        user.save()
                    except Exception as e:
                        print(e)
                usuario = usuarios.objects.get(idusuario=username)
                md5passwd = hashlib.md5(password.encode('utf-8')).hexdigest()
                print("falla por aqui??", usuario.password, md5passwd)
                if usuario.password != md5passwd:
                    print("si no")
                    return _i.login(request, 'Error de autentificación')
                user = authenticate(username=username, password="Sh20Pda17")
                if user is not None:
                    login_auth(request, user)
                    accessControl.accessControl.registraAC()
                else:
                    return _i.login(request, 'Error de autentificación')
                return HttpResponseRedirect("/")
        return _i.login(request)

    def sanhigia_pedidos_account_request(self, request):
        return HttpResponseRedirect("/")

    def __init__(self, context=None):
        super(sanhigia_pedidos, self).__init__(context)

    def index(self, request):
        return self.ctx.sanhigia_pedidos_index(request)

    def login(self, request, error=None):
        return self.ctx.sanhigia_pedidos_login(request, error)

    def auth_login(self, request):
        return self.ctx.sanhigia_pedidos_auth_login(request)

    def account_request(self, request):
        return self.ctx.sanhigia_pedidos_account_request(request)

