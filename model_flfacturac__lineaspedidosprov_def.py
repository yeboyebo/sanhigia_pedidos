
# @class_declaration sanhigia_pedidos #
from YBUTILS.viewREST import  cacheController
from models.flfactalma.articulos import articulos
from models.flfacturac.pedidosprov import pedidosprov
from models.flfacturac import flfacturac_def
from models.flfacturac import pedidosprov as pedidosprov_def


class sanhigia_pedidos(flfacturac):

    def sanhigia_pedidos_fun_metadata(self, model):
        # porlotes = articulos.objects.filter(referencia__exact=model.referencia)
        porlotes = qsatype.FLUtil.sqlSelect("articulos", "porlotes", "referencia = '{}'".format(model.referencia.referencia))
        if not porlotes:
            return [{'colKey': 'shcantalbaran', 'colEditable': True}]
        else:
            return []

    def sanhigia_pedidos_fun_disStock(self, model):
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"stocks")
        q.setSelect(u"disponible")
        q.setFrom(u"stocks")
        # q.setWhere(u"referencia = UPPER('" + model.referencia.referencia.upper() + "') AND codalmacen = 'ALM'")
        q.setWhere(u"referencia = UPPER('{}') AND codalmacen = 'ALM'".format(model.referencia.referencia.upper()))
        if not q.exec_():
            return 0

        if q.next():
            return q.value(0)

    def sanhigia_pedidos_fun_referenciaprov(self, model):
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"articulosprov")
        q.setSelect(u"refproveedor")
        q.setFrom(u"articulosprov")
        # q.setWhere(u"referencia = UPPER('" + model.referencia.referencia.upper() + "') AND pordefecto = true")
        q.setWhere(u"referencia = UPPER('{}') AND pordefecto = true".format(model.referencia.referencia.upper()))
        if not q.exec_():
            return ""

        if q.next():
            return q.value(0)

    def sanhigia_pedidos_fun_codubicacion(self, model):
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"ubicacionesarticulo")
        q.setSelect(u"codubicacion")
        q.setFrom(u"ubicacionesarticulo")
        # q.setWhere(u"referencia = UPPER('" + model.referencia.referencia.upper() + "') AND pordefecto = true")
        q.setWhere(u"referencia = UPPER('{}') AND pordefecto = true".format(model.referencia.referencia.upper()))
        if not q.exec_():
            return ""

        if q.next():
            return q.value(0)

    def sanhigia_pedidos_getForeignFields(self, model, template):
        if template == "formRecord" or template == "grupopedidos":
            return [
                {'verbose_name': 'rowColor', 'func': 'field_colorRow'},
                {'verbose_name': 'metadata', 'func': 'fun_metadata'},
                {'verbose_name': 'disStock', 'func': 'fun_disStock'},
                {'verbose_name': 'codubicacion', 'func': 'fun_codubicacion'},
                {'verbose_name': 'referenciaprov', 'func': 'fun_referenciaprov'}
            ]
        return []

    def sanhigia_pedidos_modificarShcantidad(self, model, oParam):
        idLinea = model.pk
        shcantidad = oParam['shcantalbaran']
        curLP = qsatype.FLSqlCursor(u"lineaspedidosprov")
        curLP.select("idlinea = {}".format(idLinea))
        if not curLP.first():
            raise ValueError("Error no se encuentra la linea de pedido ")
            return False
        curLP.setModeAccess(curLP.Edit)
        curLP.refreshBuffer()
        curLP.setValueBuffer("shcantalbaran", shcantidad)
        if not curLP.commitBuffer():
            return False
        return True

    def sanhigia_pedidos_modificarUbicacion(self, model, oParam):
        curUA = qsatype.FLSqlCursor(u"ubicacionesarticulo")
        curUA.select("referencia = UPPER('{}') AND pordefecto = true".format(model.referencia.referencia.upper()))
        if not curUA.first():
            raise ValueError("Error no se encuentra la linea de pedido ")
            return False
        curUA.setModeAccess(curUA.Edit)
        curUA.refreshBuffer()
        curUA.setValueBuffer("codubicacion", oParam['codubicacion'])
        if not curUA.commitBuffer():
            return False
        return True

    def sanhigia_pedidos_dameTemplateMovilote(self, model):
        # porlotes = articulos.objects.filter(referencia__exact=model.referencia)
        porlotes = qsatype.FLUtil.sqlSelect("articulos", "porlotes", "referencia = '{}'".format(model.referencia.referencia))
        if porlotes:
            return '/facturacion/lineaspedidosprov/{}/cantidadapporlote'.format(model.pk)
        else:
            return '/facturacion/pedidosprov/{}'.format(model.idpedido.idpedido)
        return False

    def sanhigia_pedidos_cerrarLinea(self, model):
        idLinea = model.idlinea
        curLinea = qsatype.FLSqlCursor(u"lineaspedidosprov")
        curLinea.select("idlinea = {}".format(idLinea))
        if not curLinea.first():
            raise ValueError("Error no se encuentra la línea del pedido ")
            return False
        curLinea.setModeAccess(curLinea.Edit)
        curLinea.refreshBuffer()
        idPedido = curLinea.valueBuffer("idpedido")
        if curLinea.valueBuffer("cerradapda"):
            curLinea.setValueBuffer("cerradapda", False)
        else:
            curLinea.setValueBuffer("cerradapda", True)
        if not curLinea.commitBuffer():
            raise ValueError("Error al cerrar la línea")
            return False
        else:
            estado = flfacturac_def.iface.obtenerEstadoPDA(idPedido, "lineaspedidosprov")
            curPedido = qsatype.FLSqlCursor(u"pedidosprov")
            curPedido.select("idpedido = {}".format(idPedido))
            if not curPedido.first():
                raise ValueError("Error no se encuentra el pedido ")
                return False
            curPedido.setModeAccess(curPedido.Edit)
            curPedido.refreshBuffer()
            # curPedido.setValueBuffer("servido", estado)
            if estado == "Sí":
                curPedido.setValueBuffer("pda", "Preparado")
            else:
                curPedido.setValueBuffer("pda", "Pendiente")
            if not curPedido.commitBuffer():
                return False
        return True

    def sanhigia_pedidos_field_colorRow(self, model):
        total = model.totalenalbaran or 0
        shcant = model.shcantalbaran or 0
        cantidad = model.cantidad or 0
        if model.cerradapda:
            return "cPrimary"
        elif (total + shcant) == cantidad:
            return "cSuccess"
        elif model.cerradapda is True:
            return "cSuccess"
        elif (total + shcant) == cantidad and model.cerradapda is False:
            return None
        elif (total + shcant) > 0 and (total + shcant) < cantidad:
            return "cWarning"
        elif (total + shcant) > cantidad:
            return "cInfo"
        else:
            return None

    def sanhigia_pedidos_initValidation(self, name, data):
        response = True
        if name == "grupopedidos":
            # print(data)
            cacheController.setSessionVariable(ustr(u"grupoPedidos_", qsatype.FLUtil.nameUser()), data['params']['selecteds'])
            return response
        return response

    def sanhigia_pedidos_getFilters(self, model, name, template=None):
        filters = []
        if name == 'grupopedidos':
            pedidos = cacheController.getSessionVariable(ustr(u"grupoPedidos_", qsatype.FLUtil.nameUser()))
            return [{'criterio': 'idpedido__in', 'valor': pedidos.split(u",")}]
        return filters

    def sanhigia_pedidos_grupopedidosListoPDA(self, model, oParam):
        pedidos = cacheController.getSessionVariable(ustr(u"grupoPedidos_", qsatype.FLUtil.nameUser()))
        pedidos = pedidos.split(u",")
        curPedido = qsatype.FLSqlCursor(u"pedidosprov")
        codgrupo = qsatype.FLUtil.sqlSelect(u"pedidosprov", u"max(sh_codgrupopedido)", "1=1") or 0
        for p in pedidos:
            curPedido.select("idpedido = " + str(p))
            if not curPedido.first():
                raise ValueError("Error no se encuentra el pedido ")
                return False
            curPedido.setModeAccess(curPedido.Edit)
            curPedido.refreshBuffer()
            curPedido.setValueBuffer("pda", 'Listo PDA')
            curPedido.setValueBuffer("sh_codgrupopedido", codgrupo + 1)
            if not curPedido.commitBuffer():
                return False
        return True

    def sanhigia_pedidos_procesaCodBarrasGrupo(self, model, oParam):
        # print("Procesa codbarrasgrupo")
        arridPedido = "("
        pedidos = cacheController.getSessionVariable(ustr(u"grupoPedidos_", qsatype.FLUtil.nameUser()))
        oParam["selecteds"] = pedidos
        pedidos = pedidos.split(u",")
        for p in pedidos:
            arridPedido = arridPedido + "'" + str(p) + "',"
        arridPedido = arridPedido[:-1]
        arridPedido = arridPedido + ")"
        # pedido = pedidosprov.objects.filter(idpedido__exact=str(pedidos[0]))
        pedido = {}
        pedido["idpedido"] = pedidos[0]
        pedido["codalmacen"] = qsatype.FLUtil.sqlSelect("pedidosprov", "codalmacen", "idpedido = {}".format(pedido["idpedido"]))
        oParam['grupoPedidos'] = arridPedido
        # return pedidosprov_def.form.iface.procesaCodBarras(pedido[0], oParam)
        return pedidosprov_def.form.iface.procesaCodBarras(pedido, oParam)

    def sanhigia_pedidos_checkPDAButton(self, cursor):
        arrProveedores = cacheController.getSessionVariable(ustr(u"grupoPedidos_", qsatype.FLUtil.nameUser())).split(u",")
        for p in arrProveedores:
            np = qsatype.FLUtil.sqlSelect(u"pedidosprov", u"pda", ustr(u"idpedido = '", str(p), u"'"))
            if np != "Preparado":
                return "disabled"
        return "enabled"

    def sanhigia_pedidos_anadirLote(self, model, oParam):
        codalmacen = qsatype.FLUtil.sqlSelect(u"pedidosprov", u"codalmacen", "idpedido = {}".format(model.idpedido.idpedido))
        if "codlote" not in oParam:
            resul = {}
            query = qsatype.FLSqlQuery()
            query.setTablesList(u"lotes")
            query.setSelect(u"*")
            query.setFrom(u"lotes")
            query.setWhere("referencia = '{}' AND enalmacen > 0".format(model.referencia.referencia))

            if query.exec_():
                if query.size() >= 0:
                    opts = []
                    while query.next():
                        opt = {}
                        opt['key'] = query.value("codlote")
                        formatofecha = "%d/%m/%Y"
                        fecha = None
                        if query.value("caducidad"):
                            fecha = query.value("caducidad").strftime(formatofecha)
                        descLote = query.value("descripcion") or ""
                        opt['alias'] = query.value("codigo") + " - " + str(int(query.value("enalmacen"))) + " - " + str(fecha) + " - " + descLote
                        opts.append(opt)

                    response = {}
                    response['status'] = -1
                    response['data'] = {}
                    response['params'] = [
                        {
                            "tipo": 3,
                            "required": False,
                            "verbose_name": "Código Lote",
                            "null": True,
                            "key": "ncodlote",
                            # "clientBch": True,
                            "validaciones": None
                        },
                        {
                            "tipo": 26,
                            "required": False,
                            "verbose_name": "F. Caducidad",
                            "null": True,
                            "key": "caducidad",
                            "validaciones": None
                        },
                        {
                            "componente": "YBFieldDB",
                            "tipo": 90,
                            "verbose_name": "Opts",
                            "label": "Asignar lote",
                            "style": {"width": "700px"},
                            "key": "codlote",
                            "validaciones": None,
                            "null": True,
                            "opts": opts
                        }
                    ]
                    return response
                else:
                    resul['status'] = -3
                    resul['msg'] = "No existe stock para la referencia " + model.referencia.referencia + " en el almacén ", codalmacen
                    resul['param'] = idLinea
                    return resul
        else:
            if not oParam['codlote']:
                oParam['codlote'] = pedidosprov_def.form.iface.creaLote(oParam['ncodlote'], oParam['caducidad'], model.referencia.referencia)
            # qsatype.debug(model.idlinea, model.referencia, 1, codalmacen, oParam['codlote'])
            # print(pedidosprov_def.form.iface.insertarMovilote(model.idlinea, model.referencia.referencia, 1, codalmacen, oParam['codlote']))
            pedidosprov_def.form.iface.insertarMovilote(model.idlinea, model.referencia.referencia, 1, codalmacen, oParam['codlote'])
        return True

    def __init__(self, context=None):
        super(sanhigia_pedidos, self).__init__(context)

    def fun_metadata(self, model):
        return self.ctx.sanhigia_pedidos_fun_metadata(model)

    def fun_disStock(self, model):
        return self.ctx.sanhigia_pedidos_fun_disStock(model)

    def fun_codubicacion(self, model):
        return self.ctx.sanhigia_pedidos_fun_codubicacion(model)

    def fun_referenciaprov(self, model):
        return self.ctx.sanhigia_pedidos_fun_referenciaprov(model)

    def getForeignFields(self, model, template):
        return self.ctx.sanhigia_pedidos_getForeignFields(model, template)

    def modificarShcantidad(self, model, oParam):
        return self.ctx.sanhigia_pedidos_modificarShcantidad(model, oParam)

    def modificarUbicacion(self, model, oParam):
        return self.ctx.sanhigia_pedidos_modificarUbicacion(model, oParam)

    def dameTemplateMovilote(self, model):
        return self.ctx.sanhigia_pedidos_dameTemplateMovilote(model)

    def cerrarLinea(self, model):
        return self.ctx.sanhigia_pedidos_cerrarLinea(model)

    def field_colorRow(self, model):
        return self.ctx.sanhigia_pedidos_field_colorRow(model)

    def initValidation(self, name, data):
        return self.ctx.sanhigia_pedidos_initValidation(name, data)

    def getFilters(self, model, name, template=None):
        return self.ctx.sanhigia_pedidos_getFilters(model, name, template)

    def grupopedidosListoPDA(self, model, oParam):
        return self.ctx.sanhigia_pedidos_grupopedidosListoPDA(model, oParam)

    def procesaCodBarrasGrupo(self, model, oParam):
        return self.ctx.sanhigia_pedidos_procesaCodBarrasGrupo(model, oParam)

    def checkPDAButton(self, cursor):
        return self.ctx.sanhigia_pedidos_checkPDAButton(cursor)

    def anadirLote(self, model, oParam):
        return self.ctx.sanhigia_pedidos_anadirLote(model, oParam)

