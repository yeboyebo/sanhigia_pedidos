
# @class_declaration sanhigia_pedidos #
from models.flfactalma import flfactalma_def


class sanhigia_pedidos(flfactalma):

    def sanhigia_pedidos_lecturaCodBar(self, model, oParam):
        if len(oParam['lectura']) > 35:
            oParam['lectura'] = oParam['lectura'][:-32]
        objcod = flfactalma_def.iface.datosLecturaCodBarras(oParam['lectura'], oParam['codproveedor'], model.referencia.referencia)
        response = {}
        response['status'] = 1
        response['data'] = {"codbar": objcod['codbarras'], "codproveedor": oParam['codproveedor']}
        return response

    def sanhigia_pedidos_asociarCodBarras(self, model, oParam):
        # print("asociar???")
        if len(oParam['codbar']) > 35:
            oParam['codbar'] = oParam['codbar'][:-32]
        response = flfactalma_def.iface.asociarCodBarras(model.referencia.referencia, oParam["codproveedor"], oParam["codbar"])
        return response

    def sanhigia_pedidos_dameCodBarras(self, model, oParam):
        response = {}
        codbarrasprov = flfactalma_def.iface.dameCodBarras(model.referencia.referencia, oParam["codproveedor"])
        response['status'] = 1
        response['data'] = {"codproveedor": oParam['codproveedor'], "codbar": codbarrasprov}
        return response

    def __init__(self, context=None):
        super(sanhigia_pedidos, self).__init__(context)

    def lecturaCodBar(self, model, oParam):
        return self.ctx.sanhigia_pedidos_lecturaCodBar(model, oParam)

    def asociarCodBarras(self, model, oParam):
        return self.ctx.sanhigia_pedidos_asociarCodBarras(model, oParam)

    def dameCodBarras(self, model, oParam):
        return self.ctx.sanhigia_pedidos_dameCodBarras(model, oParam)

