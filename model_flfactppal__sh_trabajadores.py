# @class_declaration interna_sh_trabajadores #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactppal import models as modelos


class interna_sh_trabajadores(modelos.mtd_sh_trabajadores, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_pedidos_sh_trabajadores #
class sanhigia_pedidos_sh_trabajadores(interna_sh_trabajadores, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sh_trabajadores #
class sh_trabajadores(sanhigia_pedidos_sh_trabajadores, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactppal.sh_trabajadores_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
