
# @class_declaration sanhigia_pedidos #
class sanhigia_pedidos(interna):

    def sanhigia_pedidos_afterCommit_lineaspedidoscli(self, curLinea=None):
        _i = self.iface
        if not qsatype.FactoriaModulos.get('flfacturac').iface.afterCommit_lineaspedidoscli(curLinea):
            return False
        if not _i.comprobarEstadoPedidoCli(curLinea):
            return False
        if not _i.comprobarEstadoPreparacionPedidoCli(curLinea):
            return False
        return True

    def sanhigia_pedidos_afterCommit_lineaspedidosprov(self, curLinea=None):
        _i = self.iface
        if not qsatype.FactoriaModulos.get('flfacturac').iface.afterCommit_lineaspedidosprov(curLinea):
            return False
        if not _i.comprobarEstadoPedidoProv(curLinea):
            return False
        return True

    def sanhigia_pedidos_obtenerEstadoPDA(self, idPedido, name):
        # _i = self.iface
        query = qsatype.FLSqlQuery()
        query.setTablesList(name)
        query.setSelect(u"cantidad, totalenalbaran, shcantalbaran, cerradapda")
        query.setFrom(name)
        query.setWhere(ustr(u"idpedido = ", idPedido))
        if not query.exec_():
            return False
        estado = u""
        totalServidas = 0
        parcial = False
        totalLineas = 0
        totalCerradas = 0
        cantidad = None
        cantidadServida = None
        cerrada = None
        while query.next():
            cantidad = parseFloat(query.value(u"cantidad"))
            if cantidad == 0:
                continue
            totalLineas += 1
            cantidadServida = parseFloat(query.value(u"totalenalbaran")) + parseFloat(query.value(u"shcantalbaran"))
            cerrada = query.value(u"cerradapda")
            if cerrada:
                totalCerradas += 1
            else:
                if cantidad <= cantidadServida:
                    totalServidas += 1
                else:
                    if cantidad > cantidadServida and cantidadServida != 0:
                        parcial = True
        if totalLineas == 0:
            return u"No"
        totalAServir = totalLineas - totalCerradas
        if parcial:
            estado = u"Parcial"
        else:
            if totalServidas == 0 and totalCerradas == 0:
                estado = u"No"
            else:
                if totalServidas >= totalAServir:
                    estado = u"Sí"
                else:
                    estado = u"Parcial"
        return estado

    def sanhigia_pedidos_comprobarEstadoPedidoCli(self, curLinea):
        _i = self.iface
        idPedido = curLinea.valueBuffer("idpedido")
        estado = _i.obtenerEstadoPDA(idPedido, "lineaspedidoscli")
        curPedido = qsatype.FLSqlCursor(u"pedidoscli")
        curPedido.select("idpedido = " + str(idPedido))
        if not curPedido.first():
            raise ValueError("Error no se encuentra el pedido ")
            return False
        curPedido.setModeAccess(curPedido.Edit)
        curPedido.refreshBuffer()
        if estado == "Sí":
            curPedido.setValueBuffer("pda", "Preparado")
        else:
            curPedido.setValueBuffer("pda", "Pendiente")
        # curPedido.setValueBuffer("editable", True)
        if not curPedido.commitBuffer():
            return False
        return True

    def sanhigia_pedidos_comprobarEstadoPreparacionPedidoCli(self, curLinea):
        _i = self.iface
        idPedido = curLinea.valueBuffer("idpedido")
        estado = _i.obtenerEstadoPreparacion(idPedido)
        curPedido = qsatype.FLSqlCursor(u"pedidoscli")
        curPedido.select("idpedido = " + str(idPedido))
        if not curPedido.first():
            raise ValueError("Error no se encuentra el pedido ")
            return False
        curPedido.setModeAccess(curPedido.Edit)
        curPedido.refreshBuffer()
        if estado == "Todo":
            curPedido.setValueBuffer("sh_estadopreparacion", "Todo")
        elif estado == "Parcial":
            curPedido.setValueBuffer("sh_estadopreparacion", "Parcial")
        else:
            curPedido.setValueBuffer("sh_estadopreparacion", "No")
        # curPedido.setValueBuffer("editable", True)
        if not curPedido.commitBuffer():
            return False
        return True

    def sanhigia_pedidos_obtenerEstadoPreparacion(self, idPedido):
        # _i = self.iface
        query = qsatype.FLSqlQuery()
        query.setTablesList("lineaspedidoscli")
        query.setSelect(u"cantidad, shcantalbaran, codpreparaciondepedido")
        query.setFrom("lineaspedidoscli")
        query.setWhere(ustr(u"idpedido = ", idPedido))
        if not query.exec_():
            return False
        estado = u""
        totalEnPreparacion = 0
        parcial = False
        totalLineas = 0
        totalSinPreparacion = 0
        cantidad = None
        cantidadEnv = None
        while query.next():
            cantidad = parseFloat(query.value(u"cantidad"))
            if cantidad == 0:
                continue
            totalLineas += 1
            cantidadEnv = parseFloat(query.value(u"shcantalbaran"))
            codpreparaciondepedido = query.value(u"codpreparaciondepedido")
            if codpreparaciondepedido is None:
                totalSinPreparacion += 1
            elif cantidad <= cantidadEnv:
                totalEnPreparacion += 1
            elif cantidad > cantidadEnv and cantidadEnv != 0:
                parcial = True
        if totalLineas == 0:
            return u"No"
        if parcial:
            estado = u"Parcial"
        elif totalLineas == 0 and totalEnPreparacion == 0:
            estado = u"No"
        elif totalEnPreparacion >= totalLineas:
            estado = u"Todo"
        else:
            estado = u"Parcial"
        return estado

    def sanhigia_pedidos_comprobarEstadoPedidoProv(self, curLinea):
        _i = self.iface
        idPedido = curLinea.valueBuffer("idpedido")
        estado = _i.obtenerEstadoPDA(idPedido, "lineaspedidosprov")
        curPedido = qsatype.FLSqlCursor(u"pedidosprov")
        curPedido.select("idpedido = " + str(idPedido))
        if not curPedido.first():
            raise ValueError("Error no se encuentra el pedido ")
            return False
        curPedido.setModeAccess(curPedido.Edit)
        curPedido.refreshBuffer()
        if estado == "Sí":
            curPedido.setValueBuffer("pda", "Preparado")
        else:
            curPedido.setValueBuffer("pda", "Pendiente")
        # curPedido.setValueBuffer("editable", False)
        # print(curPedido.valueBuffer("pda"))
        if not curPedido.commitBuffer():
            return False
        return True

    def sanhigia_pedidos_dameInventarioRecuentoPDA(self):
        observacion = "Recuento PDA " + str(qsatype.Date().getYear())
        codinventario = qsatype.FLUtil.sqlSelect(u"inventarios", u"codinventario", ustr(u"observaciones like '", observacion, u"'"))
        if not codinventario:
            today = str(qsatype.Date())
            fecha = str(today)[:10]
            hora = str(today)[-(8):]
            curInventario = qsatype.FLSqlCursor(u"inventarios")
            curInventario.setModeAccess(curInventario.Insert)
            curInventario.refreshBuffer()
            curInventario.setValueBuffer("fecha", fecha)
            curInventario.setValueBuffer("hora", hora)
            curInventario.setValueBuffer("sh_estado", "Cerrado")
            curInventario.setValueBuffer("observaciones", observacion)
            curInventario.setValueBuffer("codalmacen", "ALM")
            curInventario.setValueBuffer(u"codinventario", qsatype.FLUtil.nextCounter(u"codinventario", curInventario))
            if not curInventario.commitBuffer():
                resul = {}
                resul['status'] = -1
                resul['msg'] = "Error crear inventario"
                return resul
        return codinventario

    def __init__(self, context=None):
        super(sanhigia_pedidos, self).__init__(context)

    def afterCommit_lineaspedidoscli(self, curLinea=None):
        return self.ctx.sanhigia_pedidos_afterCommit_lineaspedidoscli(curLinea)

    def afterCommit_lineaspedidosprov(self, curLinea=None):
        return self.ctx.sanhigia_pedidos_afterCommit_lineaspedidosprov(curLinea)

    def comprobarEstadoPedidoCli(self, curLinea):
        return self.ctx.sanhigia_pedidos_comprobarEstadoPedidoCli(curLinea)

    def comprobarEstadoPreparacionPedidoCli(self, curLinea):
        return self.ctx.sanhigia_pedidos_comprobarEstadoPreparacionPedidoCli(curLinea)

    def comprobarEstadoPedidoProv(self, curLinea):
        return self.ctx.sanhigia_pedidos_comprobarEstadoPedidoProv(curLinea)

    def obtenerEstadoPDA(self, idPedido, name):
        return self.ctx.sanhigia_pedidos_obtenerEstadoPDA(idPedido, name)

    def obtenerEstadoPreparacion(self, idPedido):
        return self.ctx.sanhigia_pedidos_obtenerEstadoPreparacion(idPedido)

    def dameInventarioRecuentoPDA(self):
        return self.ctx.sanhigia_pedidos_dameInventarioRecuentoPDA()

    def generarLineaRegStockLote(self, curInventario, referencia, codlote, cantidad):
        print("generalinearegstoclote", referencia, codlote)
        idStock = None
        idStock = qsatype.FLUtil.sqlSelect(u"stocks", u"idstock", ustr(u"codalmacen = 'ALM' AND referencia = '", referencia, u"'"))
        if not idStock:
            oArticulo = qsatype.Object()
            oArticulo[u"referencia"] = referencia
            idStock = qsatype.FactoriaModulos.get('flfactalma').iface.pub_crearStock("ALM", oArticulo)
        q = qsatype.AQSqlQuery()
        q.setSelect(u"l.codigo, l.codlote, l.enalmacen")
        q.setFrom(u"lotes l")
        q.setWhere(ustr(u"l.codlote = '", codlote, "'"))
        if q.exec_():
            if q.next():
                oParam = qsatype.Object()
                oParam.curLineaRegStock = qsatype.FLSqlCursor(u"lineasregstocks")
                oParam.codLote = q.value(u"l.codlote")
                oParam.codigoLote = q.value(u"l.codigo")
                oParam.cantidadLote = q.value(u"l.enalmacen")
                oParam.idStock = idStock
                oParam.codInventario = curInventario.valueBuffer("codinventario")
                oParam.referencia = referencia
                oParam.actionCommit = False
                oParam.cantidad = cantidad
                idLineaRegStock = self.iface.crearLineaRegStock(curInventario, oParam)
                if not idLineaRegStock:
                    return False
                return idLineaRegStock
        else:
            print("algo fallo en query???")
        return False

    def crearLineaRegStock(self, cursor, oParam):
        cantidad = oParam["cantidad"]
        curLineaRegStock = oParam.curLineaRegStock
        curLineaRegStock.setActivatedCommitActions(oParam.actionCommit)
        curLineaRegStock.setModeAccess(curLineaRegStock.Insert)
        curLineaRegStock.refreshBuffer()
        curLineaRegStock.setValueBuffer(u"idusuario", qsatype.FLUtil.nameUser())
        curLineaRegStock.setValueBuffer(u"codinventario", oParam.codInventario)
        curLineaRegStock.setValueBuffer(u"idstock", oParam.idStock)
        curLineaRegStock.setValueBuffer(u"fecha", cursor.valueBuffer(u"fecha"))
        curLineaRegStock.setValueBuffer(u"hora", cursor.valueBuffer(u"hora"))
        if u"codLote" in oParam:
            cantidadIni = oParam.cantidadLote
            curLineaRegStock.setValueBuffer(u"sh_codlote", oParam.codLote)
            curLineaRegStock.setValueBuffer(u"sh_codigolote", oParam.codigoLote)
        else:
            cantidadIni = qsatype.FLUtil.sqlSelect(u"stocks", u"cantidad", ustr(u"idstock = ", oParam.idStock))
        curLineaRegStock.setValueBuffer(u"referencia", oParam.referencia)
        curLineaRegStock.setValueBuffer(u"cantidadini", cantidadIni)
        curLineaRegStock.setValueBuffer(u"cantidadfin", cantidad)
        curLineaRegStock.setValueBuffer(u"desarticulo", qsatype.FLUtil.sqlSelect(u"articulos", u"descripcion", ustr(u"referencia = '", oParam['referencia'], u"'")))
        curLineaRegStock.setValueBuffer(u"sh_estado", u"Cerrada")

        if not curLineaRegStock.commitBuffer():
            print("error commit regstock")
            return False
        if curLineaRegStock.valueBuffer(u"sh_codlote"):
            idmovilote = qsatype.FactoriaModulos.get('flfactalma').iface.controlRegStockLote(curLineaRegStock)
            if not idmovilote:
                return False
        else:
            curLineaRegStock.setValueBuffer(u"sh_estado", u"Inventariada")
            if not qsatype.FactoriaModulos.get('flfactalma').iface.controlRegStock(curLineaRegStock):
                return False
        return curLineaRegStock.valueBuffer(u"id")

