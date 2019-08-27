
# @class_declaration sanhigia_pedidos #
from YBUTILS.viewREST import  cacheController
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

    def sanhigia_pedidos_getRerenciasInventario(self, model, oParam, cursor):
        data = []
        codinventario = cacheController.getSessionVariable(ustr(u"inventarios_", qsatype.FLUtil.nameUser()))
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"articulos, lineasregstocks")
        q.setSelect(u"distinct(a.referencia),a.descripcion")
        q.setFrom(u"articulos a INNER JOIN lineasregstocks l ON a.referencia = l.referencia")
        q.setWhere(u"l.codinventario = '{0}' AND (UPPER(a.referencia) LIKE '%{1}%' OR UPPER(a.descripcion) LIKE '%{1}%')".format(codinventario, oParam['val'].upper()))
        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 200:
            return []
        while q.next():
            descripcion = str(q.value(0)) + "  " + q.value(1)
            data.append({"descripcion": descripcion, "referencia": q.value(0)})
        return data

    def __init__(self, context=None):
        super(sanhigia_pedidos, self).__init__(context)

    def lecturaCodBar(self, model, oParam):
        return self.ctx.sanhigia_pedidos_lecturaCodBar(model, oParam)

    def asociarCodBarras(self, model, oParam):
        return self.ctx.sanhigia_pedidos_asociarCodBarras(model, oParam)

    def dameCodBarras(self, model, oParam):
        return self.ctx.sanhigia_pedidos_dameCodBarras(model, oParam)

    def getRerenciasInventario(self, model, oParam, cursor):
        return self.ctx.sanhigia_pedidos_getRerenciasInventario(model, oParam, cursor)

