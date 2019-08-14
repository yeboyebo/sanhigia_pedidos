
# @class_declaration sanhigia_pedidos #
from models.flfacturac.lineaspedidoscli import lineaspedidoscli
from models.flfactppal.sh_trabajadores import sh_trabajadores
from models.flfactalma.articulosprov import articulosprov
from models.flfactalma import flfactalma_def


class sanhigia_pedidos(flfacturac):

    def sanhigia_pedidos_procesaCodBarras(self, model, oParam):
        # print("proceso")
        # print(oParam)
        # Suma 1
        cantidad = 1
        qsatype.debug(oParam)
        # if str(oParam['codbarras']).endsith("\x00"):
        #     qsatype.debug("tiene esos caracteres extraños")
        qsatype.debug(ustr("lencodbarras ", len(oParam['codbarras'])))
        qsatype.debug(ustr("codigobarrasprevio ", oParam['codbarras']))
        # oParam['codbarras'] = re.sub(r"/(\\x00)/g", " ", oParam['codbarras'])
        # oParam['codbarras'] = re.sub(r"/(\^@)/g", " ", oParam['codbarras'])
        if len(oParam['codbarras']) > 35:
            oParam['codbarras'] = oParam['codbarras'][:-32]
        qsatype.debug(ustr("codigobarrasposterior ", oParam['codbarras']))

        if "referencia" in oParam:
            oParam['idpedido'] = model.pk
            oParam['idlinea'] = self.iface.dameIdLinea(oParam)
            if not oParam['idlinea']:
                return False
        # Ya no va a venir idlinea en oparam lo voy a meter yo, buscando lineas de model.pk que tengan esa referencia
        # Si tengo idlinea y codlote puedo asignar procesar el codigo de barras
        if "idlinea" in oParam and "codlote" in oParam:
            val = self.iface.insertarMovilote(oParam['idlinea'], oParam['referencia'], cantidad, model.codalmacen, oParam['codlote'])
            if val['status'] == 0:
                return True
            return val
        # Si idlinea y codproveedor en oParam tengo todo lo necesario para asignar un codigo de barras
        if "idlinea" in oParam and "codproveedor" in oParam:
            print("viene por aqui 1")
            linea = lineaspedidoscli.objects.get(pk=oParam['idlinea'])
            objcod = flfactalma_def.iface.datosLecturaCodBarras(oParam['codbarras'], oParam["codproveedor"], linea.referencia)
            porLotes = qsatype.FLUtil.sqlSelect(u"articulos", u"porlotes", ustr(u"referencia = '", linea.referencia, u"'"))
            if not porLotes and "lote" in objcod:
                objcod['lote'] = None
            asociado = flfactalma_def.iface.asociarCodBarras(linea.referencia, oParam["codproveedor"], objcod['codbarras'])
            if asociado and not objcod['lote']:
                val = self.iface.analizaCodBarras(model.pk, oParam['codbarras'], cantidad, model.codalmacen, oParam['idlinea'])
                qsatype.debug(ustr("analizado ", val))
                return self.iface.respuestaAnalizaCodBarras(model, oParam, val)
                return val
            else:
                val = self.iface.analizaCodBarrasLote(linea.referencia, objcod['codbarras'], objcod['lote'], cantidad, linea.idlinea, model.codalmacen)
                qsatype.debug(ustr("analizado ", val))
                return self.iface.respuestaAnalizaCodBarras(model, oParam, val)
                return val

        # Si idlinea en oParam significa que me estan enviando un codigo de barras para asociar a un articulo de la linea
        if "idlinea" in oParam and "codproveedor" not in oParam:
            print("viene por aqui 2")
            linea = lineaspedidoscli.objects.get(pk=oParam['idlinea'])
            proveedor = articulosprov.objects.filter(referencia__exact=linea.referencia)
            if len(proveedor) == 1:
                # print("tengo idlinea y no proveedor pero ", proveedor[0].codproveedor, " ", linea.referencia, " ", oParam['codbarras'])
                objcod = flfactalma_def.iface.datosLecturaCodBarras(oParam['codbarras'], proveedor[0].codproveedor, linea.referencia)
                porLotes = qsatype.FLUtil.sqlSelect(u"articulos", u"porlotes", ustr(u"referencia = '", linea.referencia, u"'"))
                if not porLotes and "lote" in objcod:
                    objcod['lote'] = None
                asociado = flfactalma_def.iface.asociarCodBarras(linea.referencia, proveedor[0].codproveedor, objcod['codbarras'])
                if asociado and not objcod['lote']:
                    val = self.iface.analizaCodBarras(model.pk, oParam['codbarras'], cantidad, model.codalmacen, oParam['idlinea'])
                    qsatype.debug(ustr("analizado ", val))
                    return self.iface.respuestaAnalizaCodBarras(model, oParam, val)
                    return val
                else:
                    val = self.iface.analizaCodBarrasLote(linea.referencia, objcod['codbarras'], objcod['lote'], cantidad, linea.idlinea, model.codalmacen)
                    qsatype.debug(ustr("analizado ", val))
                    return self.iface.respuestaAnalizaCodBarras(model, oParam, val)
                    return val
            else:
                response = {}
                response['status'] = -1
                response['data'] = {"codbarras": oParam['codbarras'], "cantidad": cantidad, "idlinea": oParam["idlinea"], "referencia": linea.referencia}
                response['params'] = [
                    {
                        "componente": "YBFieldDB",
                        "prefix": "otros",
                        "desc_name": "Proveedor",
                        "verbose_name": "Proveedor",
                        "tipo": 5,
                        "rel": "articulosprov",
                        "aplic": "almacen",
                        "filtro": {"referencia": None},
                        "key": "codproveedor",
                        "desc": "nombre",
                        "showpk": False
                    },
                    {
                        "tipo": 37,
                        "required": True,
                        "verbose_name": "codbarras",
                        "visible": False,
                        "key": "codbarras",
                        "validaciones": None
                    },
                    {
                        "tipo": 3,
                        "required": False,
                        "verbose_name": "cantidad",
                        "key": "cantidad",
                        "visible": False,
                        "validaciones": None
                    },
                    {
                        "tipo": 3,
                        "required": False,
                        "verbose_name": "idlinea",
                        "key": "idlinea",
                        "visible": False,
                        "validaciones": None
                    }
                ]
                return response
            return False

        # Solo viene codigo de barras y cantidad
        else:
            val = self.iface.analizaCodBarras(model.pk, oParam['codbarras'], cantidad, model.codalmacen, None)
            qsatype.debug(ustr("analizado ", val))
            # print(val)
            return self.iface.respuestaAnalizaCodBarras(model, oParam, val)

        return True

    def sanhigia_pedidos_dameIdLinea(self, oParam):
        if "idpedido" in oParam:
            where = ustr(u"referencia = '", oParam['referencia'], "' AND idpedido = '", oParam['idpedido'], "'")
        elif "preparacion" in oParam:
            where = ustr(u"referencia = '", oParam['referencia'], "' AND codpreparaciondepedido = '", oParam['preparacion'], "' AND sh_preparacion = 'En Curso'")
        else:
            return False
        query = qsatype.FLSqlQuery()
        query.setTablesList(u"lineaspedidoscli")
        query.setSelect(u"idlinea, referencia, cantidad, shcantalbaran, totalenalbaran")
        query.setFrom(u"lineaspedidoscli")
        query.setWhere(where)
        idLinea = False
        if query.exec_():
            if query.size() > 1:
                while query.next():
                    total = int(query.value('totalenalbaran') or 0)
                    if int(query.value('cantidad')) != int(query.value('shcantalbaran') or 0) + int(total):
                        idLinea = query.value(0)
            if query.size() == 1:
                if query.next():
                    idLinea = query.value(0)
            if not idLinea:
                idLinea = query.value(0)
        return idLinea

    def sanhigia_pedidos_respuestaAnalizaCodBarras(self, model, oParam, val):
        # Si se produce un error que no permite modificar el pedido
        # Suma 1
        cantidad = 1
        if val['status'] == -3:
            return val

        # -1 Si el codigo de barras no pertenece a nigun articulo y algun articulo del pedido no tienen codigo de barras
        if val['status'] == -1:
            opts = []
            print("________________")
            print(val)
            query = val['param']
            while query.next():
                opt = {}
                opt['key'] = query.value(0)
                opt['alias'] = query.value(0) + " - " + query.value(1)
                opts.append(opt)
            response = {}
            response['status'] = -1
            response['data'] = {"codbarras": oParam['codbarras'], "cantidad": cantidad}
            response['params'] = [
                {
                    "componente": "YBFieldDB",
                    "tipo": 90,
                    "verbose_name": "Opts",
                    "label": "Asignar el Código de Barras a un articulo",
                    "style": {"width": "700px"},
                    "key": "referencia",
                    "validaciones": None,
                    "opts": opts
                },
                {
                    "tipo": 37,
                    "required": True,
                    "verbose_name": "codbarras",
                    "visible": False,
                    "key": "codbarras",
                    "validaciones": None
                },
                {
                    "tipo": 3,
                    "required": False,
                    "verbose_name": "cantidad",
                    "key": "cantidad",
                    "visible": False,
                    "validaciones": None
                }
            ]
            return response

        # va por lotes y no tengo codlote
        if val['status'] == 2:
            opts = []
            query = val['param']['query']
            while query.next():
                opt = {}
                opt['key'] = query.value("codlote")
                formatofecha = "%d/%m/%Y"
                fecha = query.value("caducidad").strftime(formatofecha)
                descLote = query.value("descripcion") or ""
                opt['alias'] = query.value("codigo") + " - " + str(int(query.value("enalmacen"))) + " - " + str(fecha) + " - " + descLote
                opts.append(opt)
            response = {}
            response['status'] = -1

            response['data'] = {
                "codbarras": oParam['codbarras'],
                "cantidad": cantidad,
                "idlinea": val['param']['idlinea'],
                "referencia": val['param']['referencia']
            }

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
                },
                {
                    "tipo": 37,
                    "required": True,
                    "verbose_name": "codbarras",
                    "visible": False,
                    "key": "codbarras",
                    "validaciones": None
                },
                {
                    "tipo": 3,
                    "required": False,
                    "verbose_name": "cantidad",
                    "key": "cantidad",
                    "visible": False,
                    "validaciones": None
                },
                {
                    "tipo": 3,
                    "required": False,
                    "verbose_name": "idlinea",
                    "key": "idlinea",
                    "visible": False,
                    "validaciones": None
                },
                {
                    "tipo": 3,
                    "required": False,
                    "verbose_name": "referencia",
                    "key": "referencia",
                    "visible": False,
                    "validaciones": None
                }
            ]
            return response
        return True

    def sanhigia_pedidos_pedidoListoPDA(self, model, oParam):
        if "pesobultos" not in oParam:
            valor = parseFloat(qsatype.FLUtil.sqlSelect(u"articulos a INNER JOIN lineaspedidoscli l ON a.referencia = l.referencia ", u"SUM(a.peso*l.shcantalbaran)", ustr(u"l.idpedido = ", model.idpedido), u"articulos,lineaspedidoscli"))
            valor = qsatype.FLUtil.roundFieldValue(valor, u"albaranescli", u"peso")
            if valor < 1:
                valor = 1
            response = {}
            response['status'] = -1

            response['data'] = {
                "pesobultos": valor
            }

            response['params'] = [
                {
                    "tipo": 16,
                    "required": True,
                    "verbose_name": "Nº de Bultos",
                    "key": "canbultos",
                    "null": True,
                    "validaciones": None
                },
                {
                    "tipo": 16,
                    "required": True,
                    "verbose_name": "Peso Bultos",
                    "key": "pesobultos",
                    "null": True,
                    "visible": True,
                    "validaciones": None
                }
            ]
            return response
        elif "codagencia" not in oParam:
            print(model)
            print(model.codpais)
            print(model.idprovincia)
            print(oParam['pesobultos'])
            print(oParam['canbultos'])
            print(model.total)
            valor = parseFloat(qsatype.FLUtil.sqlSelect(u"lineaspedidoscli", u"SUM((pvptotal / cantidad) * shcantalbaran)", ustr(u"idpedido = ", model.idpedido , " AND shcantalbaran > 0"), u"lineaspedidoscli"))
            print("importe ", valor)
            codAgencia = qsatype.FLUtil.sqlSelect(u"reglas_tarifa", u"codagencia", ustr(u"codpais = '", model.codpais, u"' AND provincias like '%''", model.idprovincia ,"''%' AND (", oParam['pesobultos'] ," >= pesodesde and (", oParam['pesobultos'] ," <= pesohasta or pesohasta IS NULL)) AND (", oParam['canbultos'] ," >= bultosdesde and (", oParam['canbultos'] ," <= bultoshasta or bultoshasta IS NULL)) AND (", valor ," >= importedesde and (", valor ," <= importehasta or importehasta IS NULL)) ORDER BY orden ASC"))

            print("codagencia: ", codAgencia)
            if not codAgencia or codAgencia == None:
                response = {}
                response['status'] = -1

                response['data'] = {
                    "pesobultos": oParam['pesobultos'],
                    "canbultos": oParam['canbultos']
                }

                response['params'] = [
                    {
                        "tipo": 16,
                        "required": True,
                        "verbose_name": "Nº de Bultos",
                        "key": "canbultos",
                        "null": True,
                        "validaciones": None,
                        "visible": False
                    },
                    {
                        "tipo": 16,
                        "required": True,
                        "verbose_name": "Peso Bultos",
                        "key": "pesobultos",
                        "null": True,
                        "visible": False,
                        "validaciones": None
                    },
                    {
                        "tipo": 56,
                        "componente": "YBFieldDB",
                        "prefix": "otros",
                        "rel": "agenciastrans",
                        "aplic": "pedidoscli",
                        "key": "codagencia",
                        "desc": "codagencia",
                        "verbose_name": "Agencia",
                        "null": True
                    }
                ]
                return response
            else:
                tarifaDefecto = ""
                q = qsatype.FLSqlQuery()
                q.setTablesList(u"productosagtrans")
                q.setSelect(u"codproductoagt, descripcion")
                q.setFrom(u"productosagtrans")
                q.setWhere(ustr(u"codagencia = '", codAgencia, "'"))
                if not q.exec_():
                    return False

                obj = {}
                while q.next():
                    obj[q.value("descripcion")] = q.value("codproductoagt")

                tarifaDefecto = qsatype.FLUtil.sqlSelect(u"agenciastrans", u"codproductoagtdefecto", ustr(u"codagencia = '", codAgencia ,"'"))
                codzona = qsatype.FLUtil.sqlSelect("provincias","codigo",ustr(u"idprovincia = '", model.idprovincia ,"'"))
                if codzona == "07" and codAgencia == "CEX":
                    tarifaDefecto = "82"
                response = {}
                response['status'] = -1

                response['data'] = {
                    "pesobultos": oParam['pesobultos'],
                    "canbultos": oParam['canbultos'],
                    "codagencia": codAgencia,
                    "Tarifa": tarifaDefecto
                }

                response['params'] = [
                    {
                        "tipo": 16,
                        "required": True,
                        "verbose_name": "Nº de Bultos",
                        "key": "canbultos",
                        "null": True,
                        "validaciones": None,
                        "visible": False
                    },
                    {
                        "tipo": 16,
                        "required": True,
                        "verbose_name": "Peso Bultos",
                        "key": "pesobultos",
                        "null": True,
                        "visible": False,
                        "validaciones": None
                    },
                    {
                        "tipo": 56,
                        "componente": "YBFieldDB",
                        "prefix": "otros",
                        "rel": "agenciastrans",
                        "aplic": "pedidoscli",
                        "key": "codagencia",
                        "desc": "codagencia",
                        "verbose_name": "Agencia",
                        "null": True
                    },
                    {
                        "tipo": 5,
                        "componente": "YBFieldDB",
                        "prefix": "tarifa",
                        "label": "Tarifa",
                        "key": "Tarifa",
                        "verbose_name": "Tarifa",
                        "clientoptionslist": obj
                    }
                ]
                return response
        elif "Tarifa" not in oParam:
            print("_______________1_______________")
            tarifaDefecto = ""
            q = qsatype.FLSqlQuery()
            q.setTablesList(u"productosagtrans")
            q.setSelect(u"codproductoagt, descripcion")
            q.setFrom(u"productosagtrans")
            q.setWhere(ustr(u"codagencia = '", oParam['codagencia'], "'"))
            if not q.exec_():
                return False

            obj = {}
            while q.next():
                obj[q.value("descripcion")] = q.value("codproductoagt")

            tarifaDefecto = qsatype.FLUtil.sqlSelect(u"agenciastrans", u"codproductoagtdefecto", ustr(u"codagencia = '", oParam['codagencia'] ,"'"))
            codzona = qsatype.FLUtil.sqlSelect("provincias","codigo",ustr(u"idprovincia = '", model.idprovincia ,"'"))
            if codzona == "07" and oParam['codagencia'] == "CEX":
                tarifaDefecto = "82";
            response = {}
            response['status'] = -1

            response['data'] = {
                "pesobultos": oParam['pesobultos'],
                "canbultos": oParam['canbultos'],
                "codagencia": oParam['codagencia'],
                "Tarifa": tarifaDefecto
            }
            response['params'] = [
                {
                    "tipo": 16,
                    "required": True,
                    "verbose_name": "Nº de Bultos",
                    "key": "canbultos",
                    "null": True,
                    "validaciones": None,
                    "visible": False
                },
                {
                    "tipo": 16,
                    "required": True,
                    "verbose_name": "Peso Bultos",
                    "key": "pesobultos",
                    "null": True,
                    "visible": False,
                    "validaciones": None
                },
                {
                    "tipo": 56,
                    "componente": "YBFieldDB",
                    "prefix": "otros",
                    "rel": "agenciastrans",
                    "aplic": "pedidoscli",
                    "key": "codagencia",
                    "desc": "codagencia",
                    "verbose_name": "Agencia",
                    "null": True,
                    "visible": False
                },
                {
                    "tipo": 5,
                    "componente": "YBFieldDB",
                    "prefix": "tarifa",
                    "label": "Tarifa",
                    "key": "Tarifa",
                    "verbose_name": "Tarifa",
                    "clientoptionslist": obj
                }
            ]
            return response
        else:
            print("____________2_______________")
            if(oParam['codagencia'] != qsatype.FLUtil.sqlSelect(u"productosagtrans", u"codagencia", ustr(u"codproductoagt = '", oParam['Tarifa'],"'"))):
                codTarifa = qsatype.FLUtil.sqlSelect(u"agenciastrans", u"codproductoagtdefecto", ustr(u"codagencia = '", oParam['codagencia'],"'"))
                codzona = qsatype.FLUtil.sqlSelect("provincias","codigo",ustr(u"idprovincia = '", model.idprovincia ,"'"))
                if codzona == "07" and oParam['codagencia'] == "CEX":
                    codTarifa = "82";
                q = qsatype.FLSqlQuery()
                q.setTablesList(u"productosagtrans")
                q.setSelect(u"codproductoagt, descripcion")
                q.setFrom(u"productosagtrans")
                q.setWhere(ustr(u"codagencia = '", oParam['codagencia'], "'"))
                if not q.exec_():
                    return False

                obj = {}
                while q.next():
                    obj[q.value("descripcion")] = q.value("codproductoagt")
                response = {}
                response['status'] = -1

                response['data'] = {
                    "pesobultos": oParam['pesobultos'],
                    "canbultos": oParam['canbultos'],
                    "codagencia": oParam['codagencia'],
                    "Tarifa": codTarifa
                }
                response['title'] = "Ha cambiado la agencia, seleccione una tarifa:"
                response['params'] = [
                    {
                        "tipo": 16,
                        "required": True,
                        "verbose_name": "Nº de Bultos",
                        "key": "canbultos",
                        "null": True,
                        "validaciones": None,
                        "visible": False
                    },
                    {
                        "tipo": 16,
                        "required": True,
                        "verbose_name": "Peso Bultos",
                        "key": "pesobultos",
                        "null": True,
                        "visible": False,
                        "validaciones": None
                    },
                    {
                        "tipo": 56,
                        "componente": "YBFieldDB",
                        "prefix": "otros",
                        "rel": "agenciastrans",
                        "aplic": "pedidoscli",
                        "key": "codagencia",
                        "desc": "codagencia",
                        "verbose_name": "Agencia",
                        "null": True,
                        "visible": False
                    },
                    {
                        "tipo": 5,
                        "componente": "YBFieldDB",
                        "prefix": "tarifa",
                        "label": "Tarifa",
                        "key": "Tarifa",
                        "verbose_name": "Tarifa",
                        "clientoptionslist": obj
                    }
                ]
                return response
            curPedido = qsatype.FLSqlCursor(u"pedidoscli")
            curPedido.select("idpedido = " + str(model.idpedido))
            if not curPedido.first():
                raise ValueError("Error no se encuentra el pedido ")
                return False
            curPedido.setModeAccess(curPedido.Edit)
            curPedido.refreshBuffer()
            curPedido.setValueBuffer("pda", 'Listo PDA')
            if "canbultos" in oParam and "pesobultos" in oParam:
                curPedido.setValueBuffer("canbultos", oParam['canbultos'])
                curPedido.setValueBuffer("pesobultos", oParam['pesobultos'])
            if "codagencia" in oParam:
                curPedido.setValueBuffer("codagencia", oParam['codagencia'])
            if "Tarifa" in oParam:
                curPedido.setValueBuffer("codproductoagt", oParam['Tarifa'])
            if not curPedido.commitBuffer():
                return False
            if not qsatype.FLUtil.execSql(ustr(u"UPDATE lineaspedidoscli set sh_preparacion = 'Pendiente' WHERE idpedido = '", str(model.idpedido), "'")):
                return False
            return True

    def sanhigia_pedidos_initValidation(self, name, data):
        response = True
        if name == 'formRecord':
            codtrabajador = qsatype.FLUtil.sqlSelect("sh_trabajadores", "codtrabajador", "nombre = '{}'".format(qsatype.FLUtil.nameUser()))
            # user = sh_trabajadores.objects.get(nombre__iexact=qsatype.FLUtil.nameUser())
            if not data['DATA']['codtrabajador']:
                response = self.iface.asignarTrabajador(data['DATA']['idpedido'], codtrabajador)
            else:
                if data['DATA']['codtrabajador'] == codtrabajador:
                    return True
                else:
                    return False
        return response

    def sanhigia_pedidos_field_trabajador(self, model):
        nombre = ""
        if(model.codtrabajador):
            nombre = qsatype.FLUtil.sqlSelect("sh_trabajadores", "nombre", "codtrabajador = '{}'".format(qsatype.FLUtil.nameUser()))
            # user = sh_trabajadores.objects.get(codtrabajador__iexact=model.codtrabajador)
            # nombre = user.nombre
        return nombre

    def sanhigia_pedidos_field_descPreparacion(self, model):
        descPreparacion = ""
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"lineaspedidoscli, pedidoscli, sh_preparaciondepedidos")
        q.setSelect(u"pr.descripcion")
        q.setFrom(u"pedidoscli p INNER JOIN lineaspedidoscli l ON p.idpedido = l.idpedido INNER JOIN sh_preparaciondepedidos pr ON l.codpreparaciondepedido = pr.codpreparaciondepedido")
        q.setWhere(ustr(u"p.idpedido = ", model.idpedido, " GROUP BY pr.descripcion, p.idpedido"))
        if not q.exec_():
            return descPreparacion
        if q.size() > 100:
            return descPreparacion

        while q.next():
            if q.value(0):
                descPreparacion += " " + q.value("pr.descripcion")
        return descPreparacion

    def sanhigia_pedidos_field_colorRow(self, model):
        estado = model.pda
        trabajador = model.codtrabajador
        if estado == "Listo PDA":
            return "cSuccess"
        elif estado == "Albaranado":
            return "cDanger"
        elif trabajador:
            return "cWarning"
        else:
            return None

    def sanhigia_pedidos_getForeignFields(self, model, template):
        return [
            {'verbose_name': 'Trabajador', 'func': 'field_trabajador'},
            {'verbose_name': 'Desc. preparación', 'func': 'field_descPreparacion'},
            {'verbose_name': 'rowColor', 'func': 'field_colorRow'}
        ]

    def sanhigia_pedidos_asignarTrabajador(self, idpedido, codtrabajador):
        curPedido = qsatype.FLSqlCursor(u"pedidoscli")
        curPedido.select("idpedido = " + str(idpedido))
        if not curPedido.first():
            raise ValueError("Error no se encuentra el pedido ")
            return False
        curPedido.setModeAccess(curPedido.Edit)
        curPedido.refreshBuffer()
        curPedido.setValueBuffer("codtrabajador", codtrabajador)
        if not curPedido.commitBuffer():
            return False
        return True

    def sanhigia_pedidos_insertarMovilote(self, idLinea, referencia, cantidad, codAlmacen, codLote):
        resul = {}
        print("idLinea", idLinea, "referencia", referencia, "cantidad", cantidad, "codAlmacen", codAlmacen, "codLote", codLote)
        # lo que tenemos es el codigo de lotes pero lo que se inserta es el campo codlote de lotes, vamos a buscar el primer codlote de la tabla lotes que tenga como codigo el lote que hemos ledio y que tenga stock
        # codLote = qsatype.FLUtil.sqlSelect(u"lotes", u"codlote", ustr(u"codigo = '", codigo, u"' AND enalmacen > 0 "))
        if codLote == u"" or not codLote:
            resul['status'] = -3
            resul['msg'] = "No existe ningún lote con stock para este pedido"
            resul['param'] = idLinea
            return resul

        idStock = qsatype.FLUtil.sqlSelect(u"stocks", u"idstock", ustr(u"referencia = '", referencia, u"' AND codalmacen = '", codAlmacen, u"'"))
        if idStock == u"" or not idStock:
            resul['status'] = -3
            resul['msg'] = "No existe stock para la referencia ", referencia, " en el almacén ", codAlmacen
            resul['param'] = idLinea
            return resul

        cantidad = cantidad * -1
        hoy = qsatype.Date()
        idmovilote = qsatype.FLUtil.sqlSelect(u"movilote", u"id", ustr(u"idlineapc = '", idLinea, u"' AND fecha = '", hoy, u"' AND codlote = '" + codLote + "' AND idlineaac is null"))
        print("______________", idmovilote)
        if idmovilote:
            print("por aqui")
            curMovilote = qsatype.FLSqlCursor(u"movilote")
            curMovilote.select("id = '" + str(idmovilote) + "'")
            if not curMovilote.first():
                resul['status'] = -3
                resul['msg'] = "Error al crear movimiento de lote"
                resul['param'] = idLinea
                return resul
            curMovilote.setModeAccess(curMovilote.Edit)
            curMovilote.refreshBuffer()
            curMovilote.setValueBuffer("cantidad", curMovilote.valueBuffer("cantidad") + cantidad)
            if not curMovilote.commitBuffer():
                resul['status'] = -3
                resul['msg'] = "Error al crear movimiento de lote"
                resul['param'] = idLinea
                return resul
        else:
            print("no por aqui", cantidad, idStock, codLote, idLinea)
            curMovilote = qsatype.FLSqlCursor(u"movilote")
            curMovilote.setModeAccess(curMovilote.Insert)
            curMovilote.refreshBuffer()
            curMovilote.setValueBuffer("cantidad", cantidad)
            curMovilote.setValueBuffer("idstock", idStock)
            curMovilote.setValueBuffer("tipo", "Salida")
            curMovilote.setValueBuffer("codlote", codLote)
            curMovilote.setValueBuffer("docorigen", "PC")
            curMovilote.setValueBuffer("fecha", hoy)
            curMovilote.setValueBuffer("idlineapc", idLinea)
            print("vamos a commit", curMovilote.valueBuffer("codlote"))
            if not curMovilote.commitBuffer():
                resul['status'] = -3
                resul['msg'] = "Error al crear movimiento de lote"
                resul['param'] = idLinea
                return resul

        resul['status'] = 0
        resul['msg'] = "OK"
        resul['param'] = idLinea
        resul['resul'] = True
        return resul

    def sanhigia_pedidos_analizaCodBarras(self, idPedido, barcode, cantidad, codAlmacen, idlineapedido):
        '''
        1. Comprobar si el barcode existe en alguna l?ea del pedido.
            1.1. No existe --> Devuelvo Error.
        2. Si existe.
            2.1. El barcode NO es cuadrado
                2.1.1. El barcode no va por lotes --> Actualizo cantidad de la l?ea. Devuelvo true.
                2.1.2. El barcode va por lotes --> Devuelvo que va por lotes para mostrar formulario que elije lotes y debo de hacer otra llamada que inserte el lote y actualice cantidad
            2.2. El barcode SI es cuadrado --> Tengo lote --> Inserto l?ea en movilote y devuelvo true.

        '''
        print("analizacodbarras", idlineapedido)
        print("_______________________________________________")
        referencia = ""
        idLinea = idlineapedido
        resul = {}
        # datos = qsatype.FactoriaModulos.get('formRecordarticulosprov').iface.datosLecturaCodBarras(barcode)
        datos = flfactalma_def.iface.datosLecturaCodBarras(barcode)
        qsatype.debug(datos)
        codBarras = datos['codbarras']

        # Ver si existe alguna referencia para ese c?igo de barras
        referencia = qsatype.FLUtil.sqlSelect(u"articulosprov", u"referencia", ustr(u"codbarrasprov = '", codBarras, u"' AND referencia IN (select referencia from lineaspedidoscli where idpedido = '", idPedido, "')"))
        if referencia:
            porLotes = qsatype.FLUtil.sqlSelect(u"articulos", u"porlotes", ustr(u"referencia = '", referencia, u"'"))
            if not porLotes and "lote" in datos:
                datos['lote'] = None
        # Si no existe referencia compruebo si las lineas tienen codbarras
        if referencia == u"" or not referencia:
            query = qsatype.FLSqlQuery()
            query.setTablesList(u"articulosprov,lineaspedidoscli")
            query.setSelect(u"DISTINCT(articulosprov.referencia), lineaspedidoscli.descripcion")
            # query.setSelect(u"articulosprov.referencia, lineaspedidoscli.idlinea, lineaspedidoscli.descripcion")
            query.setFrom(u"articulosprov inner join lineaspedidoscli on articulosprov.referencia = lineaspedidoscli.referencia")
            # query.setWhere(ustr(u"articulosprov.codbarrasprov is null AND lineaspedidoscli.idpedido = ", idPedido))
            query.setWhere(ustr(u"lineaspedidoscli.idpedido = ", idPedido))

            if query.exec_():
                if query.size() >= 1:
                    resul['status'] = -1
                    resul['msg'] = "?Asociar codigo de barras a pedido?"
                    resul['param'] = query
                    return resul
                else:
                    resul['status'] = -2
                    resul['msg'] = "No existe la referencia en el pedido"
                    resul['param'] = referencia
                    return resul

        # Ver si existe m? de una referencia para el c?igo de barras pero filtramos ya por el pedido
        numReg = qsatype.FLUtil.sqlSelect(u"articulosprov inner join lineaspedidoscli on articulosprov.referencia = lineaspedidoscli.referencia ", u"count(distinct(articulosprov.referencia))", ustr(u"articulosprov.codbarrasprov = '", codBarras, u"' AND lineaspedidoscli.idpedido = ", idPedido, u" group by articulosprov.referencia"))
        if not numReg:
            query = qsatype.FLSqlQuery()
            query.setTablesList(u"articulosprov,lineaspedidoscli")
            query.setSelect(u"DISTINCT(articulosprov.referencia), lineaspedidoscli.descripcion")
            # query.setSelect(u"articulosprov.referencia, lineaspedidoscli.idlinea, lineaspedidoscli.descripcion")
            query.setFrom(u"articulosprov inner join lineaspedidoscli on articulosprov.referencia = lineaspedidoscli.referencia")
            # query.setWhere(ustr(u"articulosprov.codbarrasprov is null AND lineaspedidoscli.idpedido = ", idPedido))
            query.setWhere(ustr(u"lineaspedidoscli.idpedido = ", idPedido))

            if query.exec_():
                if query.size() >= 1:
                    resul['status'] = -1
                    resul['msg'] = "?Asociar codigo de barras a pedido?"
                    resul['param'] = query
                    return resul
                else:
                    resul['status'] = -2
                    resul['msg'] = "No existe la referencia en el pedido"
                    resul['param'] = referencia
                    return resul

        if numReg > 1:
            resul['status'] = -3
            resul['msg'] = "Hay más de una referencia para el código de barras"
            resul['param'] = codBarras
            return resul
        # si existe solo una referencia para el c?igo de barras que exista en el pedido , cogeremos esa
        if not idlineapedido:
            print("no entra aqui?????")
            query = qsatype.FLSqlQuery()
            query.setTablesList(u"lineaspedidoscli")
            query.setSelect(u"idlinea, referencia, cantidad, shcantalbaran")
            query.setFrom(u"lineaspedidoscli")
            query.setWhere(ustr(u"referencia = '", referencia, "' AND idpedido = '", idPedido, "'"))

            if query.exec_():
                if query.size() > 1:
                    while query.next():
                        # print(" linea ", query.value(0), " cantidad ", int(query.value(2)), " oparam ", query.value(3), " son iguales", int(query.value(2)) == int(query.value(3) or 0))
                        if int(query.value(2)) != int(query.value(3) or 0):
                            referencia = query.value(1)
                            idLinea = query.value(0)
                    if not idLinea:
                        print("aqui al menos")
                        referencia = query.value(1)
                        idLinea = query.value(0)
                if query.size() == 1:
                    if query.next():
                        referencia = query.value(1)
                        idLinea = query.value(0)
            else:
                resul['status'] = -3
                resul['msg'] = "Error inesperado"
                return resul
            print("?????????????", idLinea)

            # query = qsatype.FLSqlQuery()
            # query.setTablesList(u"articulosprov,lineaspedidoscli")
            # query.setSelect(u"articulosprov.referencia,lineaspedidoscli.idlinea")
            # query.setFrom(u"articulosprov inner join lineaspedidoscli on articulosprov.referencia = lineaspedidoscli.referencia")
            # query.setWhere(ustr(u"articulosprov.codbarrasprov = '", codBarras, u"' AND lineaspedidoscli.idpedido = ", idPedido))

            # if query.exec_():
            #     if query.next():
            #         referencia = query.value(0)
            #         idLinea = query.value(1)
            #     else:
            #         resul['status'] = -1
            #         resul['msg'] = "No existe la referencia en el pedido"
            #         resul['param'] = referencia
            #         return resul
            # else:
            #     resul['status'] = -3
            #     resul['msg'] = "Error inesperado"
            #     return resul
        # 2.Existe
        # 2.1 no es cuadrado
        if datos['lote'] == u"" or not datos['lote']:
            porLotes = qsatype.FLUtil.sqlSelect(u"articulos", u"porlotes", ustr(u"referencia = '", referencia, u"'"))
            if not porLotes:
                # 2.1.1 actualizo línea
                shcantidad = qsatype.FLUtil.sqlSelect(u"lineaspedidoscli", u"shcantalbaran", ustr(u"idlinea = ", idLinea)) or 0
                shcantidad = shcantidad + 1
                if not qsatype.FLUtil.sqlUpdate(u"lineaspedidoscli", u"shcantalbaran", shcantidad, ustr(u"idlinea = ", idLinea)):
                    resul['status'] = -3
                    resul['msg'] = "Error al actualizar línea del pedido"
                    resul['param'] = idLinea
                    return resul
            else:
                # 2.1.2 Va por lotes
                resul['status'] = -3
                resul['msg'] = "Error inesperado"
                query = qsatype.FLSqlQuery()
                query.setTablesList(u"lotes")
                query.setSelect(u"*")
                query.setFrom(u"lotes")
                query.setWhere(ustr(u"referencia = '", referencia, "' AND enalmacen > 0"))

                if query.exec_():
                    # TODO
                    if query.size() == 1:
                        if query.next():
                            idStock = qsatype.FLUtil.sqlSelect(u"stocks", u"idstock", ustr(u"referencia = '", referencia, u"' AND codalmacen = '", codAlmacen, u"'"))
                            print("aqui tengo que hacer el movimiento", query.value(0))
                            codLote = query.value("codlote")
                            # codLote = qsatype.FLUtil.sqlSelect(u"lotes", u"codlote", ustr(u"codigo = '", query.value(0), u"'"))
                            hoy = qsatype.Date()
                            idmovilote = qsatype.FLUtil.sqlSelect(u"movilote", u"id", ustr(u"idlineapc = '", idLinea, u"' AND fecha = '", hoy, u"' AND codlote = '" + codLote + "' AND idlineaac is null"))
                            cantidad = cantidad * -1
                            if idmovilote:
                                curMovilote = qsatype.FLSqlCursor(u"movilote")
                                curMovilote.select("id = '" + str(idmovilote) + "'")
                                if not curMovilote.first():
                                    resul['status'] = -3
                                    resul['msg'] = "Error al crear movimiento de lote"
                                    resul['param'] = idLinea
                                    return resul
                                curMovilote.setModeAccess(curMovilote.Edit)
                                curMovilote.refreshBuffer()
                                curMovilote.setValueBuffer("cantidad", curMovilote.valueBuffer("cantidad") + cantidad)
                                if not curMovilote.commitBuffer():
                                    resul['status'] = -3
                                    resul['msg'] = "Error al crear movimiento de lote"
                                    resul['param'] = idLinea
                                    return resul

                                resul['status'] = 0
                                resul['msg'] = "OK"
                                resul['param'] = idLinea
                                return resul
                            else:
                                curMovilote = qsatype.FLSqlCursor(u"movilote")
                                curMovilote.setModeAccess(curMovilote.Insert)
                                curMovilote.refreshBuffer()
                                curMovilote.setValueBuffer("cantidad", cantidad)
                                curMovilote.setValueBuffer("idstock", idStock)
                                curMovilote.setValueBuffer("tipo", "Salida")
                                curMovilote.setValueBuffer("codlote", codLote)
                                curMovilote.setValueBuffer("docorigen", "PC")
                                curMovilote.setValueBuffer("fecha", hoy)
                                curMovilote.setValueBuffer("idlineapc", idLinea)

                                if not curMovilote.commitBuffer():
                                    resul['status'] = -1
                                    resul['msg'] = "Error al crear movimiento de lote"
                                    resul['param'] = idLinea
                                    return resul
                                resul['status'] = 0
                                resul['msg'] = "OK"
                                resul['param'] = idLinea
                                return resul
                        else:
                            return False
                    if query.size() > 1:
                        resul = {}
                        resul['status'] = 2
                        resul['msg'] = "¿Asociar codigo de barras a pedido?"
                        oParam = {}
                        oParam['referencia'] = referencia
                        oParam['descripcion'] = qsatype.FLUtil.sqlSelect(u"articulos", u"descripcion", ustr(u"referencia = '", referencia, u"'"))
                        oParam['idlinea'] = idLinea
                        oParam['query'] = query
                        resul['param'] = oParam
                        return resul
                    else:
                        resul['status'] = -3
                        resul['msg'] = "No existe stock para la referencia ", referencia, " en el almacén ", codAlmacen
                        resul['param'] = idLinea
                        return resul

                return resul
        else:
            # 2.2 El barcode es cuadrado
            codigo = datos['lote']
            print("por aqui ????_______________")
            # lo que tenemos es el codigo de lotes pero lo que se inserta es el campo codlote de lotes, vamos a buscar el primer codlote de la tabla lotes que tenga como codigo el lote que hemos ledio y que tenga stock
            codLote = qsatype.FLUtil.sqlSelect(u"lotes", u"codlote", ustr(u"codigo = '", codigo, u"' and referencia = '" + referencia + "'"))
            if not codLote:
                query = qsatype.FLSqlQuery()
                query.setTablesList(u"lotes")
                query.setSelect(u"*")
                query.setFrom(u"lotes")
                query.setWhere(ustr(u"referencia = '", referencia, "' AND enalmacen > 0"))

                if query.exec_():
                    if query.size() >= 1:
                        resul = {}
                        resul['status'] = 2
                        resul['msg'] = "¿Asociar codigo de barras a pedido?"
                        oParam = {}
                        oParam['referencia'] = referencia
                        oParam['descripcion'] = qsatype.FLUtil.sqlSelect(u"articulos", u"descripcion", ustr(u"referencia = '", referencia, u"'"))
                        oParam['idlinea'] = idLinea
                        oParam['query'] = query
                        resul['param'] = oParam
                        return resul
                    else:
                        resul['status'] = -3
                        resul['msg'] = "No existe stock para la referencia ", referencia, " en el almacén ", codAlmacen
                        resul['param'] = idLinea
                        return resul
                resul['status'] = -3
                resul['msg'] = "No existe ningún lote con stock para este pedido"
                resul['param'] = idLinea
                return resul
            codLote = qsatype.FLUtil.sqlSelect(u"lotes", u"codlote", ustr(u"codigo = '", codigo, u"' AND enalmacen > 0  and referencia = '" + referencia + "'"))
            if codLote == u"" or not codLote:
                resul['status'] = -3
                resul['msg'] = "No hay stock para este lote "
                resul['param'] = idLinea
                return resul

            idStock = qsatype.FLUtil.sqlSelect(u"stocks", u"idstock", ustr(u"referencia = '", referencia, u"' AND codalmacen = '", codAlmacen, u"'"))
            if idStock == u"" or not idStock:
                resul['status'] = -1
                resul['msg'] = "No existe stock para la referencia ", referencia, " en el almacén ", codAlmacen
                resul['param'] = idLinea
                return resul

            hoy = qsatype.Date()
            idmovilote = qsatype.FLUtil.sqlSelect(u"movilote", u"id", ustr(u"idlineapc = '", idLinea, u"' AND fecha = '", hoy, u"' AND codlote = '" + codLote + "' AND idlineaac is null"))
            cantidad = cantidad * -1
            print(idStock, "idmovilote", idmovilote, "codlote", codLote)
            if idmovilote:
                curMovilote = qsatype.FLSqlCursor(u"movilote")
                curMovilote.select("id = '" + str(idmovilote) + "'")
                if not curMovilote.first():
                    resul['status'] = -3
                    resul['msg'] = "Error al crear movimiento de lote"
                    resul['param'] = idLinea
                    return resul
                curMovilote.setModeAccess(curMovilote.Edit)
                curMovilote.refreshBuffer()
                curMovilote.setValueBuffer("cantidad", curMovilote.valueBuffer("cantidad") + cantidad)
                if not curMovilote.commitBuffer():
                    resul['status'] = -3
                    resul['msg'] = "Error al crear movimiento de lote"
                    resul['param'] = idLinea
                    return resul
            else:
                curMovilote = qsatype.FLSqlCursor(u"movilote")
                curMovilote.setModeAccess(curMovilote.Insert)
                curMovilote.refreshBuffer()
                curMovilote.setValueBuffer("cantidad", cantidad)
                curMovilote.setValueBuffer("idstock", idStock)
                curMovilote.setValueBuffer("tipo", "Salida")
                curMovilote.setValueBuffer("codlote", codLote)
                curMovilote.setValueBuffer("docorigen", "PC")
                curMovilote.setValueBuffer("fecha", hoy)
                curMovilote.setValueBuffer("idlineapc", idLinea)

                if not curMovilote.commitBuffer():
                    resul['status'] = -1
                    resul['msg'] = "Error al crear movimiento de lote"
                    resul['param'] = idLinea
                    return resul

        resul['status'] = 0
        resul['msg'] = "OK"
        resul['param'] = idLinea
        return resul

    def sanhigia_pedidos_analizaCodBarrasLote(self, referencia, barcode, codigo, cantidad, idLinea, codAlmacen):
        # 2.2 El barcode es cuadrado
        resul = {}
        # codigo = lote
        # lo que tenemos es el codigo de lotes pero lo que se inserta es el campo codlote de lotes, vamos a buscar el primer codlote de la tabla lotes que tenga como codigo el lote que hemos ledio y que tenga stock
        print("analiza codbarraslote", referencia)
        codLote = qsatype.FLUtil.sqlSelect(u"lotes", u"codlote", ustr(u"codigo = '", codigo, u"' AND enalmacen > 0 AND referencia ='", referencia, "'"))
        if codLote == u"" or not codLote:
            resul['status'] = -3
            resul['msg'] = "No existe ningún lote con stock para este pedido"
            resul['param'] = idLinea
            return resul

        idStock = qsatype.FLUtil.sqlSelect(u"stocks", u"idstock", ustr(u"referencia = '", referencia, u"' AND codalmacen = '", codAlmacen, u"'"))
        if idStock == u"" or not idStock:
            resul['status'] = -1
            resul['msg'] = "No existe stock para la referencia ", referencia, " en el almacén ", codAlmacen
            resul['param'] = idLinea
            return resul

        hoy = qsatype.Date()
        idmovilote = qsatype.FLUtil.sqlSelect(u"movilote", u"id", ustr(u"idlineapc = '", idLinea, u"' AND fecha = '", hoy, u"' AND codlote = '" + codLote + "' AND idlineaac is null"))
        if idmovilote:
            curMovilote = qsatype.FLSqlCursor(u"movilote")
            curMovilote.select("id = '" + str(idmovilote) + "'")
            if not curMovilote.first():
                resul['status'] = -3
                resul['msg'] = "Error al crear movimiento de lote"
                resul['param'] = idLinea
                return resul
            curMovilote.setModeAccess(curMovilote.Edit)
            curMovilote.refreshBuffer()
            curMovilote.setValueBuffer("cantidad", curMovilote.valueBuffer("cantidad") + cantidad)
            if not curMovilote.commitBuffer():
                resul['status'] = -3
                resul['msg'] = "Error al crear movimiento de lote"
                resul['param'] = idLinea
                return resul
        else:
            cantidad = cantidad * -1
            curMovilote = qsatype.FLSqlCursor(u"movilote")
            curMovilote.setModeAccess(curMovilote.Insert)
            curMovilote.refreshBuffer()
            curMovilote.setValueBuffer("cantidad", cantidad)
            curMovilote.setValueBuffer("idstock", idStock)
            curMovilote.setValueBuffer("tipo", "Salida")
            curMovilote.setValueBuffer("codlote", codLote)
            curMovilote.setValueBuffer("docorigen", "PC")
            curMovilote.setValueBuffer("fecha", hoy)
            curMovilote.setValueBuffer("idlineapc", idLinea)

            if not curMovilote.commitBuffer():
                resul['status'] = -1
                resul['msg'] = "Error al crear movimiento de lote"
                resul['param'] = idLinea
                return resul

        resul['status'] = 0
        resul['msg'] = "OK"
        resul['param'] = idLinea
        return resul
        return None

    def sanhigia_pedidos_getFilters(self, model, name, template=None):
        filters = []
        if name == 'nocompletados':

            return [{'criterio': 'codagente__in', 'valor': [agente[0].codagente]}]
        return filters

    def sanhigia_pedidos_agruparPedidos(self, model, oParam):
        # print(oParam)
        response = {}
        if ("selecteds" not in oParam or not oParam['selecteds']) and "data" not in oParam:
            response['status'] = -1
            response['msg'] = "Debes seleccionar pedido Desde y Hasta"
            return response
        if "data" not in oParam:
            response['status'] = -1
            response['data'] = {"selecteds": oParam['selecteds']}
            response['params'] = [
                {
                    "componente": "YBFieldDB",
                    "prefix": "otros",
                    "key": "ubicacionini",
                    "desc": "codubicacion",
                    "disabled_name": "Ubicacion Inicial",
                    "auto_name": "Ubicacion Inicial",
                    "tipo": "56",
                    "rel": "sh_ubicaciones",
                    "function": "getCodUbicacion",
                    "className": "relatedField",
                    "to_field": "codubicacion"
                },
                {
                    "componente": "YBFieldDB",
                    "prefix": "otros",
                    "key": "ubicacionfin",
                    "desc": "codubicacion",
                    "disabled_name": "Ubicacion Final",
                    "auto_name": "Ubicacion Final",
                    "tipo": "56",
                    "rel": "sh_ubicaciones",
                    "function": "getCodUbicacion",
                    "className": "relatedField",
                    "to_field": "codubicacion"
                },
                {
                    "tipo": 3,
                    "required": False,
                    "verbose_name": "Descripción",
                    "key": "descripcion",
                    "visible": True,
                    "validaciones": None,
                    "style": {
                        "width": "100%"
                    }
                }
            ]
            return response
        response = {}
        arrPedidoscli = oParam["data"]['selecteds'].split(u",")
        # if len(arrPedidoscli) != 2:
        #     response['status'] = -1
        #     response['msg'] = "Debes seleccionar solo pedido Desde y Hasta"
        #     return response
        if len(arrPedidoscli) == 0:
            response['status'] = -1
            response['msg'] = "Debes seleccionar al menos un pedido"
            return response

        print("_____generarpreparacion____")
        preparacion = self.sanhigia_pedidos_generaPreparaciondepedidos(model, oParam["data"])
        print(preparacion)
        if not preparacion:
            response['status'] = -1
            response['msg'] = "Error al generar la agrupación"
            return response

        if "preparacion" not in preparacion:
            return preparacion

        response['status'] = 1
        response['url'] = "/facturacion/lineaspedidoscli/custom/grupopedidoscli?p_preparacion=" + preparacion["preparacion"]
        return response

    def sanhigia_pedidos_generaPreparaciondepedidos(self, model, oParam):
        print(oParam)
        resul = {}
        ubicacionini = oParam["ubicacionini"]
        ubicacionfin = oParam["ubicacionfin"]
        # print(ubicacionfin, ubicacionini)
        # arrPedidoscli = oParam['selecteds'].split(u",")
        pedidoscli = "'" + "','".join(oParam['selecteds'].split(",")) + "'"
        # pedidoinicial = arrPedidoscli[0]
        # pedidofinal = arrPedidoscli[1]
        # if int(arrPedidoscli[0] < arrPedidoscli[1]):
        #     pedidoinicial = arrPedidoscli[1]
        #     pedidofinal = arrPedidoscli[0]
        # TODO query ver numero de lineas si > 100 o < 1 avisar
        # numLineas = qsatype.FLUtil.execSql(ustr(u"select l.idlinea from  WHERE ")
        query = qsatype.FLSqlQuery()
        query.setTablesList(u"pedidoscli, lineaspedidoscli, ubicacionesarticulo")
        query.setSelect(u"l.idlinea")
        query.setFrom(u"pedidoscli p INNER JOIN lineaspedidoscli l on l.idpedido = p.idpedido LEFT JOIN ubicacionesarticulo u ON l.referencia = u.referencia  ")
        query.setWhere(ustr(u"p.servido not like 'Sí' AND p.pda IN ('Pendiente', 'Listo PDA', 'Preparado') AND p.idpedido IN (", pedidoscli, ") AND u.codubicacion >= '", str(ubicacionini), "' AND u.codubicacion <= '", str(ubicacionfin), "' AND(l.sh_preparacion is null OR l.sh_preparacion NOT LIKE 'En Curso')"))
        if query.exec_():
            if query.size() >= 1:
                print("hay mas de uno", query.size())
                curPreparaciondepedidos = qsatype.FLSqlCursor(u"sh_preparaciondepedidos")
                codpreparacion = qsatype.FLUtil.nextCounter(u"codpreparaciondepedido", curPreparaciondepedidos)
                print("______", codpreparacion)
                if not qsatype.FLUtil.execSql(ustr(u"UPDATE lineaspedidoscli set sh_preparacion = 'En Curso', codpreparaciondepedido='", str(codpreparacion), "' WHERE idlinea IN (select l.idlinea from pedidoscli p INNER JOIN lineaspedidoscli l on l.idpedido = p.idpedido LEFT JOIN ubicacionesarticulo u ON l.referencia = u.referencia   WHERE p.servido not like 'Sí' AND p.pda IN ('Pendiente', 'Listo PDA', 'Preparado') AND p.idpedido IN (", pedidoscli, ") AND u.codubicacion >= '", str(ubicacionini), "' AND u.codubicacion <= '", str(ubicacionfin), "' AND(l.sh_preparacion is null OR l.sh_preparacion NOT LIKE 'En Curso'))")):
                    return False
                curPreparaciondepedidos.setModeAccess(curPreparaciondepedidos.Insert)
                curPreparaciondepedidos.refreshBuffer()
                curPreparaciondepedidos.setValueBuffer(u"codpreparaciondepedido", codpreparacion)
                curPreparaciondepedidos.setValueBuffer(u"descripcion", oParam["descripcion"])
                curPreparaciondepedidos.setValueBuffer(u"fecha", qsatype.Date())
                curPreparaciondepedidos.setValueBuffer(u"ubicacionini", oParam["ubicacionini"])
                curPreparaciondepedidos.setValueBuffer(u"ubicacionfin", oParam["ubicacionfin"])
                # curPreparaciondepedidos.setValueBuffer(u"desdehasta", oParam["selecteds"])
                if not curPreparaciondepedidos.commitBuffer():
                    return False
                resul["status"] = 1
                resul["preparacion"] = codpreparacion
                return resul
            else:
                print("no se encuentra")
                resul['status'] = -2
                resul['msg'] = "No se encuentran elementos que cumplan los requisitos"
                return resul
                # return False
        else:
            print("algo fallo")
            resul['status'] = -2
            resul['msg'] = "No se encuentran elementos que cumplan los requisitos"
            return resul
        return True

    # def sanhigia_pedidos_generaPreparaciondepedidos(self, model, oParam):
    #     print(oParam)
    #     resul = {}
    #     ubicacionini = oParam["ubicacionini"]
    #     ubicacionfin = oParam["ubicacionfin"]
    #     # print(ubicacionfin, ubicacionini)
    #     arrPedidoscli = oParam['selecteds'].split(u",")
    #     pedidoinicial = arrPedidoscli[0]
    #     pedidofinal = arrPedidoscli[1]
    #     if int(arrPedidoscli[0] < arrPedidoscli[1]):
    #         pedidoinicial = arrPedidoscli[1]
    #         pedidofinal = arrPedidoscli[0]
    #     # TODO query ver numero de lineas si > 100 o < 1 avisar
    #     # numLineas = qsatype.FLUtil.execSql(ustr(u"select l.idlinea from  WHERE ")
    #     query = qsatype.FLSqlQuery()
    #     query.setTablesList(u"pedidoscli, lineaspedidoscli, ubicacionesarticulo")
    #     query.setSelect(u"l.idlinea")
    #     query.setFrom(u"pedidoscli p INNER JOIN lineaspedidoscli l on l.idpedido = p.idpedido LEFT JOIN ubicacionesarticulo u ON l.referencia = u.referencia  ")
    #     query.setWhere(ustr(u"p.servido not like 'Sí' AND p.pda IN ('Pendiente', 'Listo PDA', 'Preparado') AND p.idpedido <= '", str(pedidoinicial), "' AND p.idpedido >= '", str(pedidofinal), "' AND u.codubicacion >= '", str(ubicacionini), "' AND u.codubicacion <= '", str(ubicacionfin), "' AND(l.sh_preparacion is null OR l.sh_preparacion NOT LIKE 'En Curso')"))
    #     if query.exec_():
    #         if query.size() >= 1:
    #             print("hay mas de uno", query.size())
    #             curPreparaciondepedidos = qsatype.FLSqlCursor(u"sh_preparaciondepedidos")
    #             codpreparacion = qsatype.FLUtil.nextCounter(u"codpreparaciondepedido", curPreparaciondepedidos)
    #             print("______", codpreparacion)
    #             if not qsatype.FLUtil.execSql(ustr(u"UPDATE lineaspedidoscli set sh_preparacion = 'En Curso', codpreparaciondepedido='", str(codpreparacion), "' WHERE idlinea IN (select l.idlinea from pedidoscli p INNER JOIN lineaspedidoscli l on l.idpedido = p.idpedido LEFT JOIN ubicacionesarticulo u ON l.referencia = u.referencia   WHERE p.servido not like 'Sí' AND p.pda IN ('Pendiente', 'Listo PDA', 'Preparado') AND p.idpedido <= '", str(pedidoinicial), "' AND p.idpedido >= '", str(pedidofinal), "' AND u.codubicacion >= '", str(ubicacionini), "' AND u.codubicacion <= '", str(ubicacionfin), "' AND(l.sh_preparacion is null OR l.sh_preparacion NOT LIKE 'En Curso'))")):
    #                 return False
    #             curPreparaciondepedidos.setModeAccess(curPreparaciondepedidos.Insert)
    #             curPreparaciondepedidos.refreshBuffer()
    #             curPreparaciondepedidos.setValueBuffer(u"codpreparaciondepedido", codpreparacion)
    #             curPreparaciondepedidos.setValueBuffer(u"fecha", qsatype.Date())
    #             curPreparaciondepedidos.setValueBuffer(u"ubicacionini", oParam["ubicacionini"])
    #             curPreparaciondepedidos.setValueBuffer(u"ubicacionfin", oParam["ubicacionfin"])
    #             curPreparaciondepedidos.setValueBuffer(u"desdehasta", oParam["selecteds"])
    #             if not curPreparaciondepedidos.commitBuffer():
    #                 return False
    #             resul["status"] = 1
    #             resul["preparacion"] = codpreparacion
    #             return resul
    #         else:
    #             print("no se encuentra")
    #             resul['status'] = -2
    #             resul['msg'] = "No se encuentran elementos que cumplan los requisitos"
    #             return resul
    #             # return False
    #     else:
    #         print("algo fallo")
    #         resul['status'] = -2
    #         resul['msg'] = "No se encuentran elementos que cumplan los requisitos"
    #         return resul
    #     return True

    def sanhigia_pedidos_generaPreparaciondepedidosConStock(self, model, oParam):
        resul = {}
        ubicacionini = oParam["ubicacionini"]
        ubicacionfin = oParam["ubicacionfin"]
        # TODO query ver numero de lineas si > 100 o < 1 avisar
        # numLineas = qsatype.FLUtil.execSql(ustr(u"select l.idlinea from  WHERE ")
        query = qsatype.FLSqlQuery()
        query.setTablesList(u"pedidoscli,. lineaspedidoscli, ubicacionesarticulo")
        query.setSelect(u"l.idlinea")
        query.setFrom(u"pedidoscli p INNER JOIN lineaspedidoscli l on l.idpedido = p.idpedido LEFT JOIN ubicacionesarticulo u ON l.referencia = u.referencia LEFT JOIN stocks s ON l.referencia = s.referencia")
        query.setWhere(ustr(u"p.servido in ('No','Parcial') AND p.pda IN ('Pendiente', 'Listo PDA', 'Preparado', 'Parcial') AND u.codubicacion >= '", str(ubicacionini), "' AND u.codubicacion <= '", str(ubicacionfin), "' AND(l.sh_preparacion is null OR l.sh_preparacion NOT LIKE 'En Curso') AND l.totalenalbaran <> l.cantidad AND s.disponible > 0"))
        # query.setWhere(ustr(u"p.servido like 'Parcial' AND p.pda IN ('Pendiente', 'Listo PDA', 'Preparado', 'Parcial') AND u.codubicacion >= '", str(ubicacionini), "' AND u.codubicacion <= '", str(ubicacionfin), "' AND(l.sh_preparacion is null OR l.sh_preparacion NOT LIKE 'En Curso') AND l.totalenalbaran <> l.cantidad AND s.disponible > 0"))
        if query.exec_():
            if query.size() >= 1:
                print("hay mas de uno", query.size())
                curPreparaciondepedidos = qsatype.FLSqlCursor(u"sh_preparaciondepedidos")
                codpreparacion = qsatype.FLUtil.nextCounter(u"codpreparaciondepedido", curPreparaciondepedidos)
                print("______", codpreparacion)
                if not codpreparacion:
                    return False
                if not qsatype.FLUtil.execSql(ustr(u"UPDATE lineaspedidoscli set sh_preparacion = 'En Curso', codpreparaciondepedido='", str(codpreparacion), "' WHERE idlinea IN (select l.idlinea from pedidoscli p INNER JOIN lineaspedidoscli l on l.idpedido = p.idpedido LEFT JOIN ubicacionesarticulo u ON l.referencia = u.referencia  LEFT JOIN stocks s ON l.referencia = s.referencia WHERE p.servido in ('No',Parcial') AND p.pda IN ('Pendiente', 'Listo PDA', 'Preparado', 'Parcial') AND u.codubicacion >= '", str(ubicacionini), "' AND u.codubicacion <= '", str(ubicacionfin), "' AND(l.sh_preparacion is null OR l.sh_preparacion NOT LIKE 'En Curso')  AND l.totalenalbaran <> l.cantidad AND s.disponible > 0)")):
                    return False
                curPreparaciondepedidos.setModeAccess(curPreparaciondepedidos.Insert)
                curPreparaciondepedidos.refreshBuffer()
                curPreparaciondepedidos.setValueBuffer(u"codpreparaciondepedido", codpreparacion)
                curPreparaciondepedidos.setValueBuffer(u"descripcion", oParam["descripcion"])
                curPreparaciondepedidos.setValueBuffer(u"fecha", qsatype.Date())
                curPreparaciondepedidos.setValueBuffer(u"ubicacionini", oParam["ubicacionini"])
                curPreparaciondepedidos.setValueBuffer(u"ubicacionfin", oParam["ubicacionfin"])
                curPreparaciondepedidos.setValueBuffer(u"desdehasta", oParam["selecteds"])
                curPreparaciondepedidos.setValueBuffer(u"tipo", "Stock")
                if not curPreparaciondepedidos.commitBuffer():
                    return False
                resul["status"] = 1
                resul["preparacion"] = codpreparacion
                return resul
            else:
                print("no se encuentra")
                resul['status'] = -2
                resul['msg'] = "No se encuentran elementos que cumplan los requisitos"
                return resul
                # return False
        else:
            print("algo fallo")
            resul['status'] = -2
            resul['msg'] = "No se encuentran elementos que cumplan los requisitos"
            return resul
        return True

    def sanhigia_pedidos_agruparpedidosstock(self, model, oParam):
        response = {}
        print("agrupar_____", oParam)
        if "data" not in oParam:
            response['status'] = -1
            response['data'] = {"selecteds": ""}
            response['params'] = [
                {
                    "componente": "YBFieldDB",
                    "prefix": "otros",
                    "key": "ubicacionini",
                    "desc": "codubicacion",
                    "disabled_name": "Ubicacion Inicial",
                    "auto_name": "Ubicacion Inicial",
                    "tipo": "56",
                    "rel": "sh_ubicaciones",
                    "function": "getCodUbicacion",
                    "className": "relatedField",
                    "to_field": "codubicacion"
                },
                {
                    "componente": "YBFieldDB",
                    "prefix": "otros",
                    "key": "ubicacionfin",
                    "desc": "codubicacion",
                    "disabled_name": "Ubicacion Final",
                    "auto_name": "Ubicacion Final",
                    "tipo": "56",
                    "rel": "sh_ubicaciones",
                    "function": "getCodUbicacion",
                    "className": "relatedField",
                    "to_field": "codubicacion"
                },
                {
                    "tipo": 3,
                    "required": False,
                    "verbose_name": "Descripción",
                    "key": "descripcion",
                    "visible": True,
                    "validaciones": None,
                    "style": {
                        "width": "100%"
                    }
                }
            ]
            return response

        preparacion = self.sanhigia_pedidos_generaPreparaciondepedidosConStock(model, oParam["data"])
        print("_______", preparacion)
        if not preparacion:
            response['status'] = -1
            response['msg'] = "Error al generar la agrupación"
            return response

        if "preparacion" not in preparacion:
            return preparacion

        response['status'] = 1
        response['url'] = "/facturacion/lineaspedidoscli/custom/grupopedidoscli?p_preparacion=" + preparacion["preparacion"]
        return response

    def sanhigia_pedidos_quitarTrabajador(self, model, oParam):
        # print(oParam)
        response = {}
        if ("selecteds" not in oParam or not oParam['selecteds']) and "data" not in oParam:
            response['status'] = -1
            response['msg'] = "Debes seleccionar pedido Desde y Hasta"
            return response
        response = {}

        print("_____actualizarTrabajador____")
        preparacion = self.sanhigia_pedidos_actualizarTrabajador(model, oParam)
        print(preparacion)
        if not preparacion:
            response['status'] = -1
            response['msg'] = "Error al quitar el trabajador"
            return response

        return True

    def sanhigia_pedidos_actualizarTrabajador(self, model, oParam):
        print(oParam)
        pedidoscli = "'" + "','".join(oParam['selecteds'].split(",")) + "'"
        if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"codtrabajador", u"", ustr(u"servido not like 'Sí' AND pda IN ('Pendiente') AND idpedido IN (", pedidoscli, ")")):
            return False
        print("sale pro aqui????")
        return True

    def __init__(self, context=None):
        super(sanhigia_pedidos, self).__init__(context)

    def getFilters(self, model, name, template=None):
        return self.ctx.sanhigia_pedidos_getFilters(model, name, template)

    def procesaCodBarras(self, model, oParam):
        return self.ctx.sanhigia_pedidos_procesaCodBarras(model, oParam)

    def dameIdLinea(self, oParam):
        return self.ctx.sanhigia_pedidos_dameIdLinea(oParam)

    def respuestaAnalizaCodBarras(self, model, oParam, val):
        return self.ctx.sanhigia_pedidos_respuestaAnalizaCodBarras(model, oParam, val)

    def pedidoListoPDA(self, model, oParam):
        return self.ctx.sanhigia_pedidos_pedidoListoPDA(model, oParam)

    def initValidation(self, name, data):
        return self.ctx.sanhigia_pedidos_initValidation(name, data)

    def field_trabajador(self, model):
        return self.ctx.sanhigia_pedidos_field_trabajador(model)

    def field_colorRow(self, model):
        return self.ctx.sanhigia_pedidos_field_colorRow(model)

    def getForeignFields(self, model, template):
        return self.ctx.sanhigia_pedidos_getForeignFields(model, template)

    def asignarTrabajador(self, idpedido, codtrabajador):
        return self.ctx.sanhigia_pedidos_asignarTrabajador(idpedido, codtrabajador)

    def insertarMovilote(self, idLinea, referencia, cantidad, codAlmacen, codLote):
        return self.ctx.sanhigia_pedidos_insertarMovilote(idLinea, referencia, cantidad, codAlmacen, codLote)

    def analizaCodBarras(self, idPedido, barcode, cantidad, codAlmacen, idlineapedido):
        return self.ctx.sanhigia_pedidos_analizaCodBarras(idPedido, barcode, cantidad, codAlmacen, idlineapedido)

    def analizaCodBarrasLote(self, referencia, barcode, codigo, cantidad, idLinea, codAlmacen):
        return self.ctx.sanhigia_pedidos_analizaCodBarrasLote(referencia, barcode, codigo, cantidad, idLinea, codAlmacen)

    def agruparPedidos(self, model, oParam):
        return self.ctx.sanhigia_pedidos_agruparPedidos(model, oParam)

    def agruparpedidosstock(self, model, oParam):
        return self.ctx.sanhigia_pedidos_agruparpedidosstock(model, oParam)

    def quitarTrabajador(self, model, oParam):
        return self.ctx.sanhigia_pedidos_quitarTrabajador(model, oParam)

    def field_descPreparacion(self, model):
        return self.ctx.sanhigia_pedidos_field_descPreparacion(model)

    def actualizarTrabajador(self, model, oParam):
        return self.ctx.sanhigia_pedidos_actualizarTrabajador(model, oParam)

