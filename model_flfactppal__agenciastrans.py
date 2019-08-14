# @class_declaration interna_agenciastrans #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactppal import models as modelos


class interna_agenciastrans(modelos.mtd_agenciastrans, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_pedidos_agenciastrans #
class sanhigia_pedidos_agenciastrans(interna_agenciastrans, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration agenciastrans #
class agenciastrans(sanhigia_pedidos_agenciastrans, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactppal.agenciastrans_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
