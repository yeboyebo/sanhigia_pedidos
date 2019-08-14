# @class_declaration interna_ubicacionesarticulo #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactalma import models as modelos


class interna_ubicacionesarticulo(modelos.mtd_ubicacionesarticulo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_pedidos_ubicacionesarticulo #
class sanhigia_pedidos_ubicacionesarticulo(interna_ubicacionesarticulo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration ubicacionesarticulo #
class ubicacionesarticulo(sanhigia_pedidos_ubicacionesarticulo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactalma.ubicacionesarticulo_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
