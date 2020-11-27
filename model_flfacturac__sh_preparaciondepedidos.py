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

    def getForeignFields(self, template=None):
        return form.iface.getForeignFields(self, template)

    def field_grupoQueryColorRow(self):
        return form.iface.field_grupoQueryColorRow(self)

    def queryGrid_grupoPedidosCli(self, model):
        return form.iface.queryGrid_grupoPedidosCli(model)

    def fun_metadata(self):
        return form.iface.fun_metadata(self)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def procesaCodBarrasGrupo(self, oParam):
        return form.iface.procesaCodBarrasGrupo(self, oParam)

    def field_masterColorRow(self):
        return form.iface.field_masterColorRow(self)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def eliminarLineas(self, oParam):
        return form.iface.eliminarLineas(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def visualizarPedido(self, oParam):
        return form.iface.visualizarPedido(self, oParam)


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
