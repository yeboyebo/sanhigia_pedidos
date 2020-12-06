# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration sanhigia_pedidos #
from YBLEGACY.constantes import *
from YBUTILS.viewREST import cacheController
from models.flfactalma import flfactalma_def
from models.flfacturac import pedidoscli


class sanhigia_pedidos(interna):

    def sanhigia_pedidos_getDesc(self):
        desc = "codpreparaciondepedido"
        return desc

    def sanhigia_pedidos_initValidation(self, name, data=None):
        response = True
        cacheController.setSessionVariable(ustr(u"grupoPedidoscli_", qsatype.FLUtil.nameUser()), data["DATA"]["codpreparaciondepedido"])
        return response

    def sanhigia_pedidos_getForeignFields(self, model, template):
        if template == "master":
            return [
                {'verbose_name': 'rowColor', 'func': 'field_masterColorRow'}
            ]
        if template == "grupoPedidosCli":
            return [
                {'verbose_name': 'rowColor', 'func': 'field_grupoQueryColorRow'},
                {'verbose_name': 'metadata', 'func': 'fun_metadata'}
            ]
        return []

    def sanhigia_pedidos_field_masterColorRow(self, model):
        preparacion = model.codpreparaciondepedido
        tengolineas = qsatype.FLUtil.sqlSelect("lineaspedidoscli", "count(idlinea)", "codpreparaciondepedido = '{}' and sh_preparacion = 'En Curso' AND (shcantalbaran is null or shcantalbaran < cantidad)".format(preparacion))
        if tengolineas == 0:
            return "colorGris"
        return ""

    def sanhigia_pedidos_field_grupoQueryColorRow(self, model):
        pda = model["pedidoscli.pda"]
        total = model["lineaspedidoscli.totalenalbaran"] or 0
        shcant = model["lineaspedidoscli.shcantalbaran"] or 0
        cantidad = model["lineaspedidoscli.cantidad"] or 0
        cerradapda = model["lineaspedidoscli.cerradapda"] or False
        # if pda == "Preparado":
        #     return "cLink"
        # if cerradapda:
        #     return "cPrimary"
        # elif (total + shcant) == cantidad:
        #     return "cSuccess"
        # # elif model["lineaspedidoscli.cerradapda"] is True:
        # #     return "cSuccess"
        # elif (total + shcant) == cantidad and cerradapda is False:
        #     return None
        # elif shcant > 0 and (total + shcant) > 0 and (total + shcant) < cantidad:
        #     return "cWarning"
        # elif (total + shcant) > cantidad:
        #     return "cInfo"
        # else:
        #     return None
        if pda == "Preparado" and shcant <= (cantidad - total):
            return "cLink"
        elif shcant > (cantidad - total):
            return "cDanger"
        elif cerradapda:
            return "cWarning"
        elif shcant == (cantidad - total):
            return "cSuccess"
        elif shcant < (cantidad - total):
            return None
        else:
            return None

    def sanhigia_pedidos_queryGrid_grupoPedidosCli(self, model):
        preparacion = cacheController.getSessionVariable(ustr(u"grupoPedidoscli_", qsatype.FLUtil.nameUser()))
        query = {}
        query["tablesList"] = "lineaspedidoscli, ubicacionesarticulo, pedidoscli, articulosprov"
        query["select"] = "lineaspedidoscli.idlinea, lineaspedidoscli.idpedido, lineaspedidoscli.shcantalbaran, lineaspedidoscli.cantidad, lineaspedidoscli.descripcion, lineaspedidoscli.referencia, lineaspedidoscli.totalenalbaran, lineaspedidoscli.cerradapda, stocks.disponible, stocks.cantidad, ubicacionesarticulo.codubicacion, pedidoscli.codigo, articulosprov.refproveedor, lineaspedidoscli.cantidad - lineaspedidoscli.totalenalbaran, lineaspedidoscli.codpreparaciondepedido, pedidoscli.pda"
        query["from"] = "lineaspedidoscli INNER JOIN pedidoscli ON lineaspedidoscli.idpedido = pedidoscli.idpedido INNER JOIN ubicacionesarticulo ON lineaspedidoscli.referencia = ubicacionesarticulo.referencia INNER JOIN stocks on lineaspedidoscli.referencia = stocks.referencia AND pedidoscli.codalmacen = stocks.codalmacen LEFT OUTER JOIN articulosprov ON (lineaspedidoscli.referencia = articulosprov.referencia AND articulosprov.pordefecto)"
        query["where"] = "lineaspedidoscli.codpreparaciondepedido = '" + preparacion + "' AND lineaspedidoscli.sh_preparacion = 'En Curso'"
        # query["where"] = "lineaspedidoscli.codpreparaciondepedido = '" + preparacion + "'"
        query["orderby"] = "ubicacionesarticulo.codubicacion, lineaspedidoscli.referencia, lineaspedidoscli.idlinea"
        return query

    def sanhigia_pedidos_fun_metadata(self, model):
        porlotes = qsatype.FLUtil.sqlSelect("articulos", "porlotes", "referencia = '{}'".format(model["lineaspedidoscli.referencia"]))
        if not porlotes:
            return [{'colKey': 'lineaspedidoscli.shcantalbaran', 'colEditable': True}]
        else:
            return []

    def sanhigia_pedidos_procesaCodBarrasGrupo(self, model, oParam):
        cantidad = 1
        if "preparacion" not in oParam:
            preparacion = cacheController.getSessionVariable(ustr(u"grupoPedidoscli_", qsatype.FLUtil.nameUser()))
            oParam['preparacion'] = preparacion
        if "idlinea" in oParam and "codlote" in oParam:
            idPedido = qsatype.FLUtil.sqlSelect(u"lineaspedidoscli", u"idpedido", u"idlinea = {}".format(oParam["idlinea"]))
            oParam["codalmacen"] = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"codalmacen", u"idpedido = {}".format(idPedido))
            # codLote = qsatype.FLUtil.sqlSelect(u"lotes", u"codlote", ustr(u"codigo = '", oParam['codlote'], u"' AND referencia = '", oParam['referencia'], "' AND enalmacen > 0 "))
            codLote = oParam["codlote"]
            val = pedidoscli.form.iface.insertarMovilote(oParam['idlinea'], oParam['referencia'], cantidad, oParam["codalmacen"], codLote)
            if val['status'] == 0:
                return True
            return val
        else:
            datos = flfactalma_def.iface.datosLecturaCodBarras(oParam['codbarras'])
            codBarras = datos['codbarras']
            # Ver si existe alguna referencia para ese codigo de barras
            referencia = qsatype.FLUtil.sqlSelect(u"articulosprov", u"referencia", u"codbarrasprov = '{}' AND referencia IN (select referencia from lineaspedidoscli where codpreparaciondepedido = '{}')".format(codBarras, oParam['preparacion']))
            if referencia:
                oParam["referencia"] = referencia
                oParam["idlinea"] = pedidoscli.form.iface.dameIdLinea(oParam)
                if oParam["idlinea"] == -1:
                    resul = {}
                    resul['status'] = -1
                    resul['msg'] = "El estado de preparación del artículo con código de barras {} no está 'En curso'".format(codBarras)
                    return resul
                idPedido = qsatype.FLUtil.sqlSelect(u"lineaspedidoscli", u"idpedido", u"idlinea = {}".format(oParam["idlinea"]))
                oParam["codalmacen"] = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"codalmacen", u"idpedido = {}".format(idPedido))
            else:
                resul = {}
                resul['status'] = -1
                resul['msg'] = "No se encuentra artículo con código: " + codBarras
                return resul
            # Analizar si el articulo va por lotes y si es asi comprobar si tenemos lote o necesitamos pedir
            porLotes = qsatype.FLUtil.sqlSelect(u"articulos", u"porlotes", u"referencia = '{}'".format(referencia))
            if not porLotes and "lote" in datos:
                datos['lote'] = None
            if not porLotes:
                # Actualizo línea
                shcantidad = qsatype.FLUtil.sqlSelect(u"lineaspedidoscli", u"shcantalbaran", u"idlinea = {}".format(oParam["idlinea"])) or 0
                shcantidad = shcantidad + 1
                if not qsatype.FLUtil.sqlUpdate(u"lineaspedidoscli", u"shcantalbaran", shcantidad, u"idlinea = {}".format(oParam["idlinea"])):
                    resul['status'] = -3
                    resul['msg'] = "Error al actualizar línea del pedido"
                    resul['param'] = idLinea
                    return resul
            else:
                if "lote" in datos and datos["lote"]:
                    codLote = qsatype.FLUtil.sqlSelect(u"lotes", u"codlote", u"codigo = '{}' AND referencia = '{}'  AND enalmacen > 0 ".format(datos["lote"], oParam['referencia']))
                    # print("_____codlote3____", codLote)
                    val = pedidoscli.form.iface.insertarMovilote(oParam['idlinea'], oParam['referencia'], cantidad, oParam["codalmacen"], codLote)
                    if val['status'] == 0:
                        return True
                    return val
                else:
                    # No tengo codlote hay que pedirlo
                    val = pedidoscli.form.iface.analizaCodBarras(idPedido, oParam['codbarras'], cantidad, oParam["codalmacen"], oParam['idlinea'])
                    return pedidoscli.form.iface.respuestaAnalizaCodBarras(None, oParam, val)
        return True

    def sanhigia_pedidos_eliminarLineas(self, model, oParam):
        response = {}
        if "selecteds" not in oParam or not oParam['selecteds']:
            response['status'] = -1
            response['msg'] = "Debes seleccionar al menos una línea"
            return response
        curLineas = qsatype.FLSqlCursor(u"lineaspedidoscli")
        where = "idlinea IN ({})".format(oParam['selecteds'])
        curLineas.select(where)
        total_lineas = curLineas.size()
        while curLineas.next():
            curLineas.setModeAccess(curLineas.Edit)
            curLineas.refreshBuffer()
            curLineas.setValueBuffer("sh_estadopreparacion", "No")
            curLineas.setValueBuffer("sh_preparacion", "Pendiente")
            curLineas.setNull("codpreparaciondepedido")
            if not curLineas.commitBuffer():
                return False
        response['resul'] = 1
        response['msg'] = "Se ha(n) eliminado {0} línea(s) correctamente de la preparación".format(total_lineas)
        return response

    def sanhigia_pedidos_visualizarPedido(self, model, oParam):
        regimen_iva = qsatype.FLUtil.sqlSelect("pedidosprov INNER JOIN proveedores ON pedidosprov.codproveedor = proveedores.codproveedor", "proveedores.regimeniva", "idpedido = {}".format(model.idpedido))
        response = {}
        if regimen_iva == "UE":
            if "confirmacion" in oParam:
                response['url'] = "/facturacion/pedidosprov/{}".format(model.pk)
            else:
                response["status"] = 2
                response["title"] = "CMR Necesario"
                response["confirm"] = "Este pedido corresponde a un proveedor de la EU y necesita de un documento CMR. Comprueba que disponemos del documento y reclámalo si no es así."
                response["customButtons"] = [{"accion": "goto", "nombre": "Aceptar", "url": "/facturacion/pedidosprov/{}".format(model.pk)}]
        else:
            response["url"] = "/facturacion/pedidosprov/{}".format(model.pk)
        return response

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.sanhigia_pedidos_getDesc()

    def initValidation(self, name, data=None):
        return self.ctx.sanhigia_pedidos_initValidation(name, data)

    def getForeignFields(self, model, template):
        return self.ctx.sanhigia_pedidos_getForeignFields(model, template)

    def field_grupoQueryColorRow(self, model):
        return self.ctx.sanhigia_pedidos_field_grupoQueryColorRow(model)

    def queryGrid_grupoPedidosCli(self, model):
        return self.ctx.sanhigia_pedidos_queryGrid_grupoPedidosCli(model)

    def fun_metadata(self, model):
        return self.ctx.sanhigia_pedidos_fun_metadata(model)

    def procesaCodBarrasGrupo(self, model, oParam):
        return self.ctx.sanhigia_pedidos_procesaCodBarrasGrupo(model, oParam)

    def field_masterColorRow(self, model):
        return self.ctx.sanhigia_pedidos_field_masterColorRow(model)

    def eliminarLineas(self, model, oParam):
        return self.ctx.sanhigia_pedidos_eliminarLineas(model, oParam)

    def visualizarPedido(self, model, oParam):
        return self.ctx.sanhigia_pedidos_visualizarPedido(model, oParam)


# @class_declaration head #
class head(sanhigia_pedidos):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
