
# @class_declaration sanhigia_pedidos #
from YBUTILS.viewREST import  cacheController

from models.flfactalma import flfactalma_def


class sanhigia_pedidos(flfactalma):

    def sanhigia_pedidos_getFilters(self, model, name, template=None):
        filters = []
        if name == 'soloAbiertas':
            visible = cacheController.getSessionVariable(ustr(u"visibeLRS_", qsatype.FLUtil.nameUser()))
            if visible is None:
                cacheController.setSessionVariable(ustr(u"visibeLRS_", qsatype.FLUtil.nameUser()), False)
            if visible:
                return [{'criterio': 'sh_estado__in', 'valor': ["Abierta", "Cerrada"]}]
            else:
                return [{'criterio': 'sh_estado__exact', 'valor': "Abierta"}]
        return filters

    def sanhigia_pedidos_getForeignFields(self, model, template=None):
        fields = []
        if template == 'formRecord':
            return [
                {'verbose_name': 'rowColor', 'func': 'field_colorRow'},
                {'verbose_name': 'metadata', 'func': 'fun_metadata'},
                {'verbose_name': 'referenciaprov', 'func': 'fun_referenciaprov'}
            ]
        return fields

    def sanhigia_pedidos_field_colorRow(self, model):
        if model.sh_estado == "Cerrada":
            return "cSuccess"
        elif model.cantidadini != model.cantidadfin:
            return "cPrimary"
        else:
            return "cWarning"
        return None

    def sanhigia_pedidos_fun_metadata(self, model):
        if model.sh_estado == "Cerrada":
            return [{'colKey': 'cantidadfin', 'colEditable': False}]
        else:
            return []

    def sanhigia_pedidos_cerrarLinea(self, model, cursor):
        estado = cursor.valueBuffer("sh_estado")
        if estado == "Abierta":
            # cursor.setValueBuffer("cantidadini", cursor.valueBuffer("cantidadfin"))
            cursor.setValueBuffer("sh_estado", "Cerrada")
        elif estado == "Cerrada":
            # cursor.setValueBuffer("cantidadfin", 0)
            cursor.setValueBuffer("sh_estado", "Abierta")
        if not cursor.commitBuffer():
            return False
        return True

    def sanhigia_pedidos_editarCantRegstock(self, model, oParam, cursor):
        estadoInventario = qsatype.FLUtil.sqlSelect(u"inventarios", u"sh_estado", "codinventario = '" + cursor.valueBuffer("codinventario") + "'")
        if cursor.valueBuffer("sh_estado") == "Abierta" and estadoInventario != "Cerrado":
            cursor.setActivatedCommitActions(False)
            cursor.setValueBuffer("cantidadfin", oParam['cantidadfin'])
            cursor.setValueBuffer("sh_estado", "Cerrada")
            if not cursor.commitBuffer():
                return False
        return True

    def sanhigia_pedidos_getCodBarrasProv(self, model, oParam, cursor):
        data = []
        # if len(oParam['val']) > 35:
        #     oParam['val'] = oParam['val'][:-32]
        if not oParam['val']:
            return data
        # qsatype.debug(ustr("codigobarrasposterior ", oParam['val']))
        datos = flfactalma_def.iface.datosLecturaCodBarras(oParam['val'])
        print("____", datos)
        referencia = qsatype.FLUtil.sqlSelect(u"articulosprov", u"referencia", ustr(u"codbarrasprov = '", datos["codbarras"], u"'"))
        print("______", referencia)
        if not referencia:
            return data
        print(cursor)
        print(oParam)
        print(model.__dict__)
        print(cursor.valueBuffer("codinventario"))
        where = u"codinventario = '" + cursor.valueBuffer("codinventario") + "' AND referencia = '" + referencia + "'"
        if datos["lote"]:
            where = where + " AND sh_codigolote = '" + datos["lote"] + "'"
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

    def sanhigia_pedidos_fun_referenciaprov(self, model):
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"articulosprov")
        q.setSelect(u"refproveedor")
        q.setFrom(u"articulosprov")
        q.setWhere(u"referencia = UPPER('" + model.referencia.referencia.upper() + "') AND pordefecto = true")
        if not q.exec_():
            return ""

        if q.next():
            return q.value(0)

    def __init__(self, context=None):
        super(sanhigia_pedidos, self).__init__(context)

    def getFilters(self, model, name, template=None):
        return self.ctx.sanhigia_pedidos_getFilters(model, name, template)

    def getForeignFields(self, model, template=None):
        return self.ctx.sanhigia_pedidos_getForeignFields(model, template)

    def field_colorRow(self, model):
        return self.ctx.sanhigia_pedidos_field_colorRow(model)

    def fun_metadata(self, model):
        return self.ctx.sanhigia_pedidos_fun_metadata(model)

    def cerrarLinea(self, model, cursor):
        return self.ctx.sanhigia_pedidos_cerrarLinea(model, cursor)

    def editarCantRegstock(self, model, oParam, cursor):
        return self.ctx.sanhigia_pedidos_editarCantRegstock(model, oParam, cursor)

    def getCodBarrasProv(self, model, oParam, cursor):
        return self.ctx.sanhigia_pedidos_getCodBarrasProv(model, oParam, cursor)

    def fun_referenciaprov(self, model):
        return self.ctx.sanhigia_pedidos_fun_referenciaprov(model)

