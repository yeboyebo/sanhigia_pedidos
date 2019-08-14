# @class_declaration interna_sh_preparaciondepedidos #
import importlib

from YBUTILS.viewREST import helpers

from models.flfacturac import models as modelos


class interna_sh_preparaciondepedidos(modelos.mtd_sh_preparaciondepedidos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_pedidos_sh_preparaciondepedidos #
class sanhigia_pedidos_sh_preparaciondepedidos(interna_sh_preparaciondepedidos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getDesc():
        return form.iface.getDesc()

    @helpers.decoradores.accion()
    def dameTemplatePreparacion(self):
        return form.iface.dameTemplatePreparacion(self)


# @class_declaration sh_preparaciondepedidos #
class sh_preparaciondepedidos(sanhigia_pedidos_sh_preparaciondepedidos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfacturac.sh_preparaciondepedidos_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
