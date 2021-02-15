# @class_declaration interna_eventos #
import importlib

from YBUTILS.viewREST import helpers

from models.flfacturac import models as modelos


class interna_eventos(modelos.mtd_eventos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_pedidos_eventos #
class sanhigia_pedidos_eventos(interna_eventos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration eventos #
class eventos(sanhigia_pedidos_eventos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfacturac.eventos_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
