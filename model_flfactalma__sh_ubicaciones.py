# @class_declaration interna_sh_ubicaciones #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactalma import models as modelos


class interna_sh_ubicaciones(modelos.mtd_sh_ubicaciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_pedidos_sh_ubicaciones #
class sanhigia_pedidos_sh_ubicaciones(interna_sh_ubicaciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getDesc():
        return form.iface.getDesc()

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getCodUbicacion(self, oParam):
        return form.iface.getCodUbicacion(self, oParam)


# @class_declaration sh_ubicaciones #
class sh_ubicaciones(sanhigia_pedidos_sh_ubicaciones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactalma.sh_ubicaciones_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
