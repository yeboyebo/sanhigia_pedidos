# @class_declaration interna_lotes #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactalma import models as modelos


class interna_lotes(modelos.mtd_lotes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_pedidos_lotes #
class sanhigia_pedidos_lotes(interna_lotes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration lotes #
class lotes(sanhigia_pedidos_lotes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactalma.lotes_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
