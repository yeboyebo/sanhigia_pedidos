
# @class_declaration sanhigia_pedidos #
from models.flfactalma.articulos import articulos
from models.flfacturac import flfacturac_def, pedidoscli
from YBUTILS.viewREST import cacheController
from models.flfactalma import flfactalma_def


class sanhigia_pedidos(flfacturac):

    def sanhigia_pedidos_initValidation(self, name, data):
        response = True
        if name == "grupopedidoscli":
            # print(data['params']['preparacion'])
            cacheController.setSessionVariable(ustr(u"grupoPedidoscli_", qsatype.FLUtil.nameUser()), data['params']['preparacion'])
            return response
        return response

    def sanhigia_pedidos_fun_metadata(self, model):
        porlotes = articulos.objects.filter(referencia__exact=model.referencia)
        if not porlotes[0].porlotes:
            return [{'colKey': 'shcantalbaran', 'colEditable': True}]
        else:
            return []

    def sanhigia_pedidos_fun_queryMetadata(self, model):
        porlotes = articulos.objects.filter(referencia__exact=model["lineaspedidoscli.referencia"])
        if not porlotes[0].porlotes:
            return [{'colKey': 'lineaspedidoscli.shcantalbaran', 'colEditable': True}]
        else:
            return []

    def sanhigia_pedidos_fun_disStock(self, model):
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"stocks")
        q.setSelect(u"cantidad")
        q.setFrom(u"stocks")
        q.setWhere(u"referencia = UPPER('" + model.referencia.upper() + "') AND codalmacen = 'ALM'")
        if not q.exec_():
            return 0

        if q.next():
            return q.value(0)

    def sanhigia_pedidos_fun_codubicacion(self, model):
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"ubicacionesarticulo")
        q.setSelect(u"codubicacion")
        q.setFrom(u"ubicacionesarticulo")
        q.setWhere(u"referencia = UPPER('" + model.referencia.upper() + "') AND pordefecto = true")
        if not q.exec_():
            return ""

        if q.next():
            return q.value(0)

    def sanhigia_pedidos_fun_referenciaprov(self, model):
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"articulosprov")
        q.setSelect(u"refproveedor")
        q.setFrom(u"articulosprov")
        q.setWhere(u"referencia = UPPER('" + model.referencia.upper() + "') AND pordefecto = true")
        if not q.exec_():
            return ""

        if q.next():
            return q.value(0)

    def sanhigia_pedidos_fun_Queryreferenciaprov(self, model):
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"articulosprov")
        q.setSelect(u"refproveedor")
        q.setFrom(u"articulosprov")
        q.setWhere(u"referencia = UPPER('" + model["lineaspedidoscli.referencia"].upper() + "') AND pordefecto = true")
        if not q.exec_():
            return ""

        if q.next():
            return q.value(0)

    def sanhigia_pedidos_fun_QuerypteServir(self, model):
        try:
            pteservir = int(model["lineaspedidoscli.cantidad"]) - int(model["lineaspedidoscli.totalenalbaran"])
        except Exception:
            pteservir = int(model.cantidad) - int(model.totalenalbaran)
        return pteservir

    def sanhigia_pedidos_fun_pteServir(self, model):
        pteservir = int(model.cantidad) - int(model.totalenalbaran)
        return pteservir

    def sanhigia_pedidos_fun_codpedido(self, model):
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"pedidoscli")
        q.setSelect(u"codigo")
        q.setFrom(u"pedidoscli")
        q.setWhere(u"idpedido = '" + str(model.idpedido) + "'")
        if not q.exec_():
            return ""

        if q.next():
            return q.value(0)

    def sanhigia_pedidos_getForeignFields(self, model, template):
        if template == "grupoPedidosCli":
            return [
                {'verbose_name': 'rowColor', 'func': 'field_grupoQueryColorRow'},
                {'verbose_name': 'metadata', 'func': 'fun_queryMetadata'},
                {'verbose_name': 'referenciaprov', 'func': 'fun_Queryreferenciaprov'},
                {'verbose_name': 'pteServir', 'func': 'fun_QuerypteServir'}
            ]
        elif template == 'formRecord':
            return [
                {'verbose_name': 'rowColor', 'func': 'field_colorRow'},
                {'verbose_name': 'metadata', 'func': 'fun_metadata'},
                {'verbose_name': 'disStock', 'func': 'fun_disStock'},
                {'verbose_name': 'codubicacion', 'func': 'fun_codubicacion'},
                {'verbose_name': 'referenciaprov', 'func': 'fun_referenciaprov'},
                {'verbose_name': 'pteServir', 'func': 'fun_pteServir'}
            ]
        elif template == 'grupopedidoscli':
            return [
                {'verbose_name': 'rowColor', 'func': 'field_grupoColorRow'},
                {'verbose_name': 'metadata', 'func': 'fun_metadata'},
                {'verbose_name': 'disStock', 'func': 'fun_disStock'},
                {'verbose_name': 'codubicacion', 'func': 'fun_codubicacion'},
                {'verbose_name': 'referenciaprov', 'func': 'fun_referenciaprov'},
                {'verbose_name': 'codpedido', 'func': 'fun_codpedido'},
                {'verbose_name': 'pteServir', 'func': 'fun_QuerypteServir'}
            ]
        return []

    def sanhigia_pedidos_modificarShcantidad(self, model, oParam):
        idLinea = model.pk
        shcantidad = oParam['shcantalbaran']
        curLP = qsatype.FLSqlCursor(u"lineaspedidoscli")
        curLP.select("idlinea = " + str(idLinea))
        if not curLP.first():
            raise ValueError("Error no se encuentra la linea de pedido ")
            return False
        curLP.setModeAccess(curLP.Edit)
        curLP.refreshBuffer()
        curLP.setValueBuffer("shcantalbaran", shcantidad)
        if not curLP.commitBuffer():
            return False
        return True


    def sanhigia_pedidos_modificarShcantidadQuery(self, model, oParam):
        idLinea = model.pk
        shcantidad = oParam['lineaspedidoscli.shcantalbaran']
        curLP = qsatype.FLSqlCursor(u"lineaspedidoscli")
        curLP.select("idlinea = " + str(idLinea))
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
        if "ubicacionesarticulo.codubicacion" in oParam:
            ubicacion = oParam['ubicacionesarticulo.codubicacion']
        else:
            ubicacion = oParam["codubicacion"]
        codubicacion = qsatype.FLUtil.sqlSelect(u"sh_ubicaciones", u"codubicacion", ustr(u"codubicacion = '", ubicacion, u"'"))
        if not codubicacion:
            resul = {}
            resul['status'] = -1
            resul['msg'] = "No se encuentra ubicacion: " + ubicacion
            return resul
        curUA = qsatype.FLSqlCursor(u"ubicacionesarticulo")
        curUA.select(u"referencia = UPPER('" + model.referencia.upper() + "') AND pordefecto = true")
        if not curUA.first():
            raise ValueError("Error no se encuentra la linea de pedido ")
            return False
        curUA.setModeAccess(curUA.Edit)
        curUA.refreshBuffer()
        curUA.setValueBuffer("codubicacion", ubicacion)
        if not curUA.commitBuffer():
            return False
        return True

    def sanhigia_pedidos_dameTemplateMovilote(self, model):
        porlotes = articulos.objects.filter(referencia__exact=model.referencia)
        if porlotes[0].porlotes:
            return '/facturacion/lineaspedidoscli/' + str(model.pk) + '/cantidadPorLote'
        return True

    def sanhigia_pedidos_dameTemplateMoviloteQuery(self, model):
        porlotes = articulos.objects.filter(referencia__exact=model.referencia)
        if porlotes[0].porlotes:
            return '/facturacion/lineaspedidoscli/' + str(model.pk) + '/cantidadPorLote'
        return True

    def sanhigia_pedidos_dameTemplatePedidoCli(self, model):
        # print(model.idpedido)
        # user = sh_trabajadores.objects.get(nombre__iexact=qsatype.FLUtil.nameUser())
        user = qsatype.FLUtil.sqlSelect(u"sh_trabajadores", u"codtrabajador", ustr(u"upper(nombre) = upper('", qsatype.FLUtil.nameUser(), u"')"))
        codtrabajador = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"codtrabajador", ustr(u"idpedido = '", model.idpedido, u"'"))
        if user != codtrabajador and codtrabajador:
            # resul = {}
            # resul['status'] = -1
            #nombre = qsatype.FLUtil.sqlSelect(u"sh_trabajadores", u"nombre", ustr(u"codtrabajador = '", codtrabajador, u"'"))
            if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"codtrabajador", user, ustr(u"idpedido = '", str(model.idpedido), "'")):
                return False
            #qsatype.FLUtil.execSql(ustr(u"UPDATE pedidoscli set codtrabajador = '", user, u"' WHERE idpedido = '", str(model.idpedido), "'"))
            print("trabajado cambiado")
            # print("______", nombre)
            # resul['msg'] = "El pedido esta asignado al usuario: " + nombre
            # return resul
        return '/facturacion/pedidoscli/' + str(model.idpedido)

    def sanhigia_pedidos_cerrarLinea(self, model):
        idLinea = model.pk
        curLinea = qsatype.FLSqlCursor(u"lineaspedidoscli")
        curLinea.select("idlinea = " + str(idLinea))
        if not curLinea.first():
            qsatype.debug("Error no se encuentra la línea del pedido")
            raise ValueError("Error no se encuentra la línea del pedido ")
            return False
        curLinea.setModeAccess(curLinea.Edit)
        curLinea.refreshBuffer()
        idPedido = curLinea.valueBuffer("idpedido")
        if curLinea.valueBuffer("cerradapda"):
            curLinea.setValueBuffer("cerradapda", False)
            # curLinea.setValueBuffer("cerrada", False)
        else:
            curLinea.setValueBuffer("cerradapda", True)
            # curLinea.setValueBuffer("cerrada", True)
        if not curLinea.commitBuffer():
            qsatype.debug("tiene esos caracteres extraños")
            raise ValueError("Error al cerrar la línea")
            return False
        else:
            estado = flfacturac_def.iface.obtenerEstadoPDA(idPedido, "lineaspedidoscli")
            curPedido = qsatype.FLSqlCursor(u"pedidoscli")
            curPedido.select("idpedido = " + str(idPedido))
            if not curPedido.first():
                qsatype.debug("Error no se encuentra el pedido")
                raise ValueError("Error no se encuentra el pedido ")
                return False
            curPedido.setModeAccess(curPedido.Edit)
            curPedido.refreshBuffer()
            # curPedido.setValueBuffer("servido", estado)
            if estado == "Sí":
                qsatype.debug("Si")
                curPedido.setValueBuffer("pda", "Preparado")
            else:
                qsatype.debug("No")
                curPedido.setValueBuffer("pda", "Pendiente")
            #     curPedido.setValueBuffer("editable", False)
            if not curPedido.commitBuffer():
                qsatype.debug("No commitBuffer")
                return False
        return True

    def sanhigia_pedidos_field_grupoQueryColorRow(self, model):
        pda = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"pda", ustr(u"idpedido = '", model["lineaspedidoscli.idpedido"], u"'"))
        total = model["lineaspedidoscli.totalenalbaran"] or 0
        shcant = model["lineaspedidoscli.shcantalbaran"] or 0
        cantidad = model["lineaspedidoscli.cantidad"] or 0
        if pda == "Preparado":
            return "cLink"
        # print(model.idpedido)
        if model["lineaspedidoscli.cerradapda"]:
            return "cPrimary"
        elif (total + shcant) == cantidad:
            return "cSuccess"
        # elif model["lineaspedidoscli.cerradapda"] is True:
        #     return "cSuccess"
        elif (total + shcant) == cantidad and model["lineaspedidoscli.cerradapda"] is False:
            return None
        elif (total + shcant) > 0 and (total + shcant) < cantidad:
            return "cWarning"
        elif (total + shcant) > cantidad:
            return "cInfo"
        else:
            return None

    def sanhigia_pedidos_field_grupoColorRow(self, model):
        pda = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"pda", ustr(u"idpedido = '", model.idpedido, u"'"))
        total = model.totalenalbaran or 0
        shcant = model.shcantalbaran or 0
        cantidad = model.cantidad or 0
        if pda == "Preparado":
            return "cLink"
        # print(model.idpedido)
        elif model.cerradapda:
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

    def sanhigia_pedidos_anadirLote(self, model, oParam):
        if "codlote" not in oParam:
            resul = {}
            query = qsatype.FLSqlQuery()
            query.setTablesList(u"lotes")
            query.setSelect(u"*")
            query.setFrom(u"lotes")
            query.setWhere(ustr(u"referencia = '", model.referencia, "' AND enalmacen > 0"))

            if query.exec_():
                if query.size() >= 1:
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
                            "componente": "YBFieldDB",
                            "tipo": 90,
                            "verbose_name": "Opts",
                            "label": "Asignar lote",
                            "style": {"width": "700px"},
                            "key": "codlote",
                            "validaciones": None,
                            "opts": opts
                        }
                    ]
                    return response
                else:
                    resul['status'] = -3
                    codalmacen = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"codalmacen", ustr(u"idpedido = '", model.idpedido, u"'"))
                    resul['msg'] = "No existe stock para la referencia " + model.referencia + " en el almacén ", codalmacen
                    # resul['param'] = idLinea
                    return resul
        else:
            codalmacen = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"codalmacen", ustr(u"idpedido = '", model.idpedido, u"'"))
            # qsatype.debug(model.idlinea, model.referencia, 1, codalmacen, oParam['codlote'])
            # codLote = qsatype.FLUtil.sqlSelect(u"lotes", u"codlote", ustr(u"codigo = '", oParam['codlote'], u"' AND referencia = '", model.referencia, "' AND enalmacen > 0 "))
            codLote = oParam['codlote']
            # print("_____codlote1____", codLote)
            pedidoscli.form.iface.insertarMovilote(model.idlinea, model.referencia, 1, codalmacen, codLote)
        return True

    def sanhigia_pedidos_getFilters(self, model, name, template=None):
        filters = []
        if name == 'grupopedidoscli':
            preparacion = cacheController.getSessionVariable(ustr(u"grupoPedidoscli_", qsatype.FLUtil.nameUser()))
            return [{'criterio': 'codpreparaciondepedido__exact', 'valor': preparacion}, {'criterio': 'sh_preparacion__exact', 'valor': "En Curso"}]
        return filters

    def sanhigia_pedidos_procesaCodBarrasGrupo(self, model, oParam):
        print("procesacodbarrasgrupo", oParam)
        cantidad = 1
        if "preparacion" not in oParam:
            preparacion = cacheController.getSessionVariable(ustr(u"grupoPedidoscli_", qsatype.FLUtil.nameUser()))
            oParam['preparacion'] = preparacion
        if "idlinea" in oParam and "codlote" in oParam:
            idPedido = qsatype.FLUtil.sqlSelect(u"lineaspedidoscli", u"idpedido", ustr(u"idlinea = '", oParam["idlinea"], u"'"))
            oParam["codalmacen"] = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"codalmacen", ustr(u"idpedido = '", idPedido, u"'"))
            # codLote = qsatype.FLUtil.sqlSelect(u"lotes", u"codlote", ustr(u"codigo = '", oParam['codlote'], u"' AND referencia = '", oParam['referencia'], "' AND enalmacen > 0 "))
            codLote = oParam["codlote"]
            # print("_____codlote2____", codLote)
            val = pedidoscli.form.iface.insertarMovilote(oParam['idlinea'], oParam['referencia'], cantidad, oParam["codalmacen"], codLote)
            if val['status'] == 0:
                return True
            return val
        else:
            # print(oParam)
            datos = flfactalma_def.iface.datosLecturaCodBarras(oParam['codbarras'])
            codBarras = datos['codbarras']
            # print(datos)
            # Ver si existe alguna referencia para ese codigo de barras
            referencia = qsatype.FLUtil.sqlSelect(u"articulosprov", u"referencia", ustr(u"codbarrasprov = '", codBarras, u"' AND referencia IN (select referencia from lineaspedidoscli where codpreparaciondepedido = '", oParam['preparacion'], "')"))
            if referencia:
                oParam["referencia"] = referencia
                oParam["idlinea"] = pedidoscli.form.iface.dameIdLinea(oParam)
                idPedido = qsatype.FLUtil.sqlSelect(u"lineaspedidoscli", u"idpedido", ustr(u"idlinea = '", oParam["idlinea"], u"'"))
                oParam["codalmacen"] = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"codalmacen", ustr(u"idpedido = '", idPedido, u"'"))
            else:
                resul = {}
                resul['status'] = -1
                resul['msg'] = "No se encuentra artículo con código: " + codBarras
                return resul
            # Analizar si el articulo va por lotes y si es asi comprobar si tenemos lote o necesitamos pedir
            porLotes = qsatype.FLUtil.sqlSelect(u"articulos", u"porlotes", ustr(u"referencia = '", referencia, u"'"))
            if not porLotes and "lote" in datos:
                datos['lote'] = None
            # print("referencia ", referencia, " oparam ", oParam, " datos ", datos)
            if not porLotes:
                # Actualizo línea
                shcantidad = qsatype.FLUtil.sqlSelect(u"lineaspedidoscli", u"shcantalbaran", ustr(u"idlinea = ", oParam["idlinea"])) or 0
                shcantidad = shcantidad + 1
                if not qsatype.FLUtil.sqlUpdate(u"lineaspedidoscli", u"shcantalbaran", shcantidad, ustr(u"idlinea = ", oParam["idlinea"])):
                    resul['status'] = -3
                    resul['msg'] = "Error al actualizar línea del pedido"
                    resul['param'] = idLinea
                    return resul
            else:
                if "lote" in datos and datos["lote"]:
                    codLote = qsatype.FLUtil.sqlSelect(u"lotes", u"codlote", ustr(u"codigo = '", datos["lote"], u"' AND referencia = '", oParam['referencia'], "'  AND enalmacen > 0 "))
                    # print("_____codlote3____", codLote)
                    val = pedidoscli.form.iface.insertarMovilote(oParam['idlinea'], oParam['referencia'], cantidad, oParam["codalmacen"], codLote)
                    if val['status'] == 0:
                        return True
                    return val
                else:
                    # No tengo codlote hay que pedirlo
                    val = pedidoscli.form.iface.analizaCodBarras(idPedido, oParam['codbarras'], cantidad, oParam["codalmacen"], oParam['idlinea'])
                    # print(ustr("analizado ", val))
                    return pedidoscli.form.iface.respuestaAnalizaCodBarras(None, oParam, val)
                # print("referencia ", referencia, " idlinea ", oParam["idlinea"], "porLotes ", porLotes, " codalmacen", oParam["codalmacen"])
        return True

    def sanhigia_pedidos_queryGrid_grupoPedidosCli(self):
        preparacion = cacheController.getSessionVariable(ustr(u"grupoPedidoscli_", qsatype.FLUtil.nameUser()))
        query = {}
        query["tablesList"] = ("lineaspedidoscli, ubicacionesarticulo, pedidoscli")
        query["select"] = ("lineaspedidoscli.idlinea, lineaspedidoscli.idpedido, lineaspedidoscli.shcantalbaran, lineaspedidoscli.cantidad, lineaspedidoscli.descripcion, lineaspedidoscli.referencia, lineaspedidoscli.totalenalbaran, lineaspedidoscli.cerradapda, stocks.disponible, stocks.cantidad, ubicacionesarticulo.codubicacion, pedidoscli.codigo")
        query["from"] = ("lineaspedidoscli INNER JOIN pedidoscli ON lineaspedidoscli.idpedido = pedidoscli.idpedido INNER JOIN ubicacionesarticulo ON lineaspedidoscli.referencia = ubicacionesarticulo.referencia INNER JOIN stocks on lineaspedidoscli.referencia = stocks.referencia AND pedidoscli.codalmacen = stocks.codalmacen")
        query["where"] = ("lineaspedidoscli.codpreparaciondepedido = '" + preparacion + "' AND lineaspedidoscli.sh_preparacion = 'En Curso'")
        query["orderby"] = " ubicacionesarticulo.codubicacion, lineaspedidoscli.referencia, lineaspedidoscli.idlinea"
        return query

    def sanhigia_pedidos_inventariar(self, model, oParam):
        ref = model.referencia
        if "referencia" in oParam and oParam["referencia"] != model.referencia:
            ref = oParam["referencia"]
        porLotes = qsatype.FLUtil.sqlSelect(u"articulos", u"porlotes", ustr(u"referencia = '", ref, u"'"))
        # print(porLotes)
        response = {}
        response['status'] = -1
        response['data'] = {"referencia": ref}
        response['params'] = []
        if "cantidadStock" not in oParam or ("cantidadStock" in oParam and not oParam["cantidadStock"]):
            response['params'].append({
                "tipo": 3,
                "required": False,
                "verbose_name": "Cantidad Final",
                "key": "cantidadStock",
                "validaciones": None
            })
        if porLotes:
            resul = {}
            today = str(qsatype.Date())[:10]
            query = qsatype.FLSqlQuery()
            query.setTablesList(u"lotes")
            query.setSelect(u"*")
            query.setFrom(u"lotes")
            where = ustr(u"referencia = '", ref, "' AND caducidad is not NULL AND descripcion is not Null AND caducidad > '", today, "'  AND enalmacen > 0 ORDER BY enalmacen DESC")
            if "vertodo" in oParam and oParam["vertodo"]:
                where = ustr(u"referencia = '", ref, "' AND caducidad is not NULL AND descripcion is not Null AND caducidad > '", today, "' ORDER BY enalmacen DESC")
            query.setWhere(where)

            if query.exec_():
                if query.size() >= 1:
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

                    response['params'].append({
                        "componente": "YBFieldDB",
                        "tipo": 90,
                        "verbose_name": "Opts",
                        "label": "Asignar lote",
                        "style": {"width": "700px"},
                        "key": "codlote",
                        "required": False,
                        "validaciones": None,
                        "opts": opts
                    })
                    response['params'].append({
                        "tipo": 18,
                        "required": False,
                        "verbose_name": "Ver todo",
                        "key": "vertodo",
                        "validaciones": None
                    })
                    response['params'].append({
                        "tipo": 3,
                        "required": False,
                        "visible": False,
                        "verbose_name": "Ref",
                        "key": "referencia",
                        "validaciones": None
                    })
                else:
                    resul['status'] = -3
                    codalmacen = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"codalmacen", ustr(u"idpedido = '", model.idpedido, u"'"))
                    resul['msg'] = "No existe stock para la referencia " + ref + " en el almacén ", codalmacen
                    # resul['param'] = idLinea
                    return resul
        if "cantidadStock" not in oParam or ("cantidadStock" in oParam and not oParam["cantidadStock"]):
            return response
        if "cantidadStock" in oParam and oParam["cantidadStock"] and ("codlote" in oParam and not oParam["codlote"]):
            return response
        else:
            # print(oParam)
            # Buscar inventario con observacion Recuento PDA + año, si no existe lo creamos
            codInventario = flfacturac_def.iface.dameInventarioRecuentoPDA()
            # print(codInventario)
            # Añadir linea de inventario con articulo + codlote si necesario
            # Cambiar stock
            curInventario = qsatype.FLSqlCursor(u"inventarios")
            curInventario.select("codinventario = '" + str(codInventario) + "'")
            if not curInventario.first():
                resul = {}
                resul['status'] = -1
                resul['msg'] = "Error no se encuentra inventario"
                return resul
            curInventario.setModeAccess(curInventario.Browse)
            curInventario.refreshBuffer()
            idStock = qsatype.FLUtil.sqlSelect(u"stocks", u"idstock", ustr(u"codalmacen = 'ALM' AND referencia = '", ref, u"'"))
            if porLotes:
                lineaLote = flfacturac_def.iface.generarLineaRegStockLote(curInventario, ref, oParam["codlote"], oParam['cantidadStock'])
                print("tengo linea lote no")
                if not lineaLote:
                    return False
            else:
                params = qsatype.Object()
                if not idStock:
                    oArticulo = qsatype.Object()
                    oArticulo[u"referencia"] = q.value(u"a.referencia")
                    idStock = qsatype.FactoriaModulos.get('flfactalma').iface.pub_crearStock(codAlmacen, oArticulo)
                params.curLineaRegStock = qsatype.FLSqlCursor(u"lineasregstocks")
                params.idStock = idStock
                params.cursor = curInventario
                params.codInventario = codInventario
                params.referencia = ref
                params.actionCommit = False
                params.cantidad = oParam["cantidadStock"]
                idLineaRegStock = flfacturac_def.iface.crearLineaRegStock(curInventario, params)
                if not idLineaRegStock:
                    return False
        return True

    def __init__(self, context=None):
        super(sanhigia_pedidos, self).__init__(context)

    def fun_metadata(self, model):
        return self.ctx.sanhigia_pedidos_fun_metadata(model)

    def fun_queryMetadata(self, model):
        return self.ctx.sanhigia_pedidos_fun_queryMetadata(model)

    def fun_disStock(self, model):
        return self.ctx.sanhigia_pedidos_fun_disStock(model)

    def fun_codubicacion(self, model):
        return self.ctx.sanhigia_pedidos_fun_codubicacion(model)

    def fun_referenciaprov(self, model):
        return self.ctx.sanhigia_pedidos_fun_referenciaprov(model)

    def fun_Queryreferenciaprov(self, model):
        return self.ctx.sanhigia_pedidos_fun_Queryreferenciaprov(model)

    def fun_codpedido(self, model):
        return self.ctx.sanhigia_pedidos_fun_codpedido(model)

    def getForeignFields(self, model, template):
        return self.ctx.sanhigia_pedidos_getForeignFields(model, template)

    def modificarShcantidad(self, model, oParam):
        return self.ctx.sanhigia_pedidos_modificarShcantidad(model, oParam)

    def modificarShcantidadQuery(self, model, oParam):
        return self.ctx.sanhigia_pedidos_modificarShcantidadQuery(model, oParam)

    def modificarUbicacion(self, model, oParam):
        return self.ctx.sanhigia_pedidos_modificarUbicacion(model, oParam)

    def anadirLote(self, model, oParam):
        return self.ctx.sanhigia_pedidos_anadirLote(model, oParam)

    def dameTemplateMovilote(self, model):
        return self.ctx.sanhigia_pedidos_dameTemplateMovilote(model)

    def dameTemplateMoviloteQuery(self, model):
        return self.ctx.sanhigia_pedidos_dameTemplateMoviloteQuery(model)

    def dameTemplatePedidoCli(self, model):
        return self.ctx.sanhigia_pedidos_dameTemplatePedidoCli(model)

    def cerrarLinea(self, model):
        return self.ctx.sanhigia_pedidos_cerrarLinea(model)

    def field_colorRow(self, model):
        return self.ctx.sanhigia_pedidos_field_colorRow(model)

    def field_grupoColorRow(self, model):
        return self.ctx.sanhigia_pedidos_field_grupoColorRow(model)

    def field_grupoQueryColorRow(self, model):
        return self.ctx.sanhigia_pedidos_field_grupoQueryColorRow(model)

    def fun_QuerypteServir(self, model):
        return self.ctx.sanhigia_pedidos_fun_QuerypteServir(model)

    def fun_pteServir(self, model):
        return self.ctx.sanhigia_pedidos_fun_pteServir(model)

    def getFilters(self, model, name, template=None):
        return self.ctx.sanhigia_pedidos_getFilters(model, name, template)

    def initValidation(self, name, data):
        return self.ctx.sanhigia_pedidos_initValidation(name, data)

    def procesaCodBarrasGrupo(self, model, oParam):
        return self.ctx.sanhigia_pedidos_procesaCodBarrasGrupo(model, oParam)

    def queryGrid_grupoPedidosCli(self):
        return self.ctx.sanhigia_pedidos_queryGrid_grupoPedidosCli()

    def inventariar(self, model, oParam):
        return self.ctx.sanhigia_pedidos_inventariar(model, oParam)

