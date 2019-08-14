# @class_declaration interna_movilote #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactalma import models as modelos


class interna_movilote(modelos.mtd_movilote, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_pedidos_movilote #
class sanhigia_pedidos_movilote(interna_movilote, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getForeignFields(self, template=None):
        return form.iface.getForeignFields(self, template)

    def field_codigolote(self):
        return form.iface.field_codigolote(self)

    def field_caducidadlote(self):
        return form.iface.field_caducidadlote(self)

    def field_cantidadmlote(self):
        return form.iface.field_cantidadmlote(self)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def cambiarCantidad(self, oParam, cursor):
        return form.iface.cambiarCantidad(self, oParam, cursor)


# @class_declaration movilote #
class movilote(sanhigia_pedidos_movilote, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactalma.movilote_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
