
# @class_declaration sanhigia_pedidos #
from YBUTILS.viewREST import  cacheController
from models.flfactalma import flfactalma_def


class sanhigia_pedidos(flfactalma):

    def sanhigia_pedidos_initValidation(self, name, data=None):
        response = True
        print(data["DATA"]["codinventario"])
        cacheController.setSessionVariable(ustr(u"inventarios_", qsatype.FLUtil.nameUser()), data["DATA"]["codinventario"])
        return response

    def sanhigia_pedidos_getForeignFields(self, model, template=None):
        fields = []
        if template == 'formRecord':
            return [
                {'verbose_name': 'rowColor', 'func': 'field_colorRow'}
            ]
        return fields

    def sanhigia_pedidos_field_colorRow(self, model):
        if model.sh_estado == "Cerrado":
            return "cWarning"
        else:
            return None
        return None

    # def sanhigia_pedidos_getCodBarrasProv(self, model, oParam, cursor):
    #     data = []
    #     # print(cursor.valueBuffer("codinventario"))
    #     # if len(oParam['val']) > 35:
    #     #     oParam['val'] = oParam['val'][:-32]
    #     # qsatype.debug(ustr("codigobarrasposterior ", oParam['val']))
    #     datos = flfactalma_def.iface.datosLecturaCodBarras(oParam['val'])
    #     referencia = qsatype.FLUtil.sqlSelect(u"articulosprov", u"referencia", u"codbarrasprov = '{}".format(datos["codbarras"]))
    #     if referencia is None:
    #         resul['status'] = -3
    #         resul['msg'] = "No existe referencia con código de barras '{}'".format(datos["codbarras"])
    #         resul['param'] = idLinea
    #         return resul
    #     where = u"referencia = '" + referencia + "'"
    #     if datos["lote"]:
    #         where = where + " AND sh_codlote = '" + datos["lote"] + "'"
    #     where = where + " LIMIT 7"
    #     q = qsatype.FLSqlQuery()
    #     q.setTablesList(u"lineasregstocks")
    #     q.setSelect(u"id, referencia, sh_codigolote")
    #     q.setFrom(u"lineasregstocks")
    #     q.setWhere(where)

    #     if not q.exec_():
    #         print("Error inesperado")
    #         return []
    #     if q.size() > 100:
    #         print("sale por aqui")
    #         return []

    #     while q.next():
    #         data.append({"id": q.value(0), "descripcion": str(q.value(1)) + "_" + str(q.value(2))})

    #     return data

    def __init__(self, context=None):
        super(sanhigia_pedidos, self).__init__(context)

    def initValidation(self, name, data=None):
        return self.ctx.sanhigia_pedidos_initValidation(name, data)

    def getForeignFields(self, model, template=None):
        return self.ctx.sanhigia_pedidos_getForeignFields(model, template)

    def field_colorRow(self, model):
        return self.ctx.sanhigia_pedidos_field_colorRow(model)

    # def getCodBarrasProv(self, model, oParam, cursor):
    #     return self.ctx.sanhigia_pedidos_getCodBarrasProv(model, oParam, cursor)

