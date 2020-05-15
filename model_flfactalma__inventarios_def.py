
# @class_declaration sanhigia_pedidos #
from YBUTILS.viewREST import  cacheController
from models.flfactalma import flfactalma_def
import requests


class sanhigia_pedidos(flfactalma):

    def sanhigia_pedidos_initValidation(self, name, data=None):
        response = True
        # print(data["DATA"]["codinventario"])
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

    def sanhigia_pedidos_cerrarAbrirInventario(self, model, oParam):
        response = {}
        # Hasta que no se revisa el comportamiento de reiniciar el docker la funcionalidad estará en mantenimiento - 27-04-2020
        # response['status'] = -1
        # response['msg'] = "La funcionalidad de Abrir/Cerrar Inventario está en mantenimiento"
        # return response

        if "selecteds" not in oParam or not oParam['selecteds']:
            response['status'] = -1
            response['msg'] = "Debes seleccionar al menos un inventario"
            return response
        arrInventarios = oParam['selecteds'].split(u",")
        if len(arrInventarios) != 1:
            response['status'] = -1
            response['msg'] = "Debes seleccionar sólo un inventario"
            return response
        estado = qsatype.FLUtil.sqlSelect("inventarios", "sh_estado", "codinventario = '{}'".format(arrInventarios[0]))
        if estado == "Cerrado":
            msgError = "Abrir"
            msgInfo = "abierto"
        else:
            msgError = "Cerrar"
            msgInfo = "cerrado"
        try:
            # Llamadas locales
            # res = requests.post("http://127.0.0.1:8005/api/inventariosapi/{0}/llama_abrircerrar_inventario".format(arrInventarios[0]))
            res = requests.post("http://172.65.0.1:8005/api/inventariosapi/{0}/llama_abrircerrar_inventario".format(arrInventarios[0]))
            if res.status_code != 200:
                response['status'] = -1
                response['msg'] = "Error al {0} el inventario.<br>Código error: {1} {2}".format(msgError, res.status_code, res.reason)
                return response
        except Exception as exc:
            print(exc)
            response['status'] = -1
            response['msg'] = "Error al {} el inventario.<br>Error de conexión con el servidor".format(msgError)
            return response
        response['resul'] = 1
        response['msg'] = "Se ha {0} correctamente el inventario '{1}'".format(msgInfo, arrInventarios[0])
        return response

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

    def cerrarAbrirInventario(self, model, oParam):
        return self.ctx.sanhigia_pedidos_cerrarAbrirInventario(model, oParam)

