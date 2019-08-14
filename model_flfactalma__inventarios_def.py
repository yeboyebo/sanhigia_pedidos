
# @class_declaration sanhigia_pedidos #
from YBUTILS.viewREST import  cacheController
from models.flfactalma import flfactalma_def


class sanhigia_pedidos(flfactalma):

    def sanhigia_pedidos_initValidation(self, name, data=None):
        response = True
        visible = cacheController.getSessionVariable(ustr(u"visibeLRS_", qsatype.FLUtil.nameUser()))
        if visible is None:
            cacheController.setSessionVariable(ustr(u"visibeLRS_", qsatype.FLUtil.nameUser()), False)
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

    def sanhigia_pedidos_visibility(self, model, oParam):
        visible = cacheController.getSessionVariable(ustr(u"visibeLRS_", qsatype.FLUtil.nameUser()))
        if not visible:
            cacheController.setSessionVariable(ustr(u"visibeLRS_", qsatype.FLUtil.nameUser()), True)
        elif visible:
            cacheController.setSessionVariable(ustr(u"visibeLRS_", qsatype.FLUtil.nameUser()), False)
        return True

    def sanhigia_pedidos_getCodBarrasProv(self, model, oParam, cursor):
        data = []
        # print(cursor.valueBuffer("codinventario"))
        # if len(oParam['val']) > 35:
        #     oParam['val'] = oParam['val'][:-32]
        # qsatype.debug(ustr("codigobarrasposterior ", oParam['val']))
        datos = flfactalma_def.iface.datosLecturaCodBarras(oParam['val'])
        print(datos)
        referencia = qsatype.FLUtil.sqlSelect(u"articulosprov", u"referencia", ustr(u"codbarrasprov = '", datos["codbarras"], u"'"))
        where = u"referencia = '" + referencia + "'"
        if datos["lote"]:
            where = where + " AND sh_codlote = '" + datos["lote"] + "'"
        where = where + " LIMIT 7"
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"lineasregstocks")
        q.setSelect(u"id, referencia, sh_codigolote")
        q.setFrom(u"lineasregstocks")
        q.setWhere(where)

        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 100:
            print("sale por aqui")
            return []

        while q.next():
            data.append({"id": q.value(0), "descripcion": str(q.value(1)) + "_" + str(q.value(2))})

        return data

    def __init__(self, context=None):
        super(sanhigia_pedidos, self).__init__(context)

    def initValidation(self, name, data=None):
        return self.ctx.sanhigia_pedidos_initValidation(name, data=None)

    def getForeignFields(self, model, template=None):
        return self.ctx.sanhigia_pedidos_getForeignFields(model, template)

    def field_colorRow(self, model):
        return self.ctx.sanhigia_pedidos_field_colorRow(model)

    def visibility(self, model, oParam):
        return self.ctx.sanhigia_pedidos_visibility(model, oParam)

    def getCodBarrasProv(self, model, oParam, cursor):
        return self.ctx.sanhigia_pedidos_getCodBarrasProv(model, oParam, cursor)

