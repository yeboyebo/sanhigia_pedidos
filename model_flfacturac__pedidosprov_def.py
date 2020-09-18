
# @class_declaration sanhigia_pedidos #
from models.flfacturac.lineaspedidosprov import lineaspedidosprov
from models.flfactppal.sh_trabajadores import sh_trabajadores
from models.flfactalma.articulosprov import articulosprov
from models.flfactalma import flfactalma_def
import requests


class sanhigia_pedidos(flfacturac):

    def sanhigia_pedidos_procesaCodBarras(self, model, oParam):
        print(oParam)
        # Suma 1
        cantidad = 1
        # qsatype.debug(ustr("lencodbarras ", len(oParam['codbarras'])))
        # qsatype.debug(ustr("codigobarrasprevio ", oParam['codbarras']))
        # oParam['codbarras'] = re.sub(r"/(\\x00)/g", " ", oParam['codbarras'])
        # oParam['codbarras'] = re.sub(r"/(\^@)/g", " ", oParam['codbarras'])
        # if len(oParam['codbarras']) > 35:
        #     oParam['codbarras'] = oParam['codbarras'][:-32]
        qsatype.debug(ustr("codigobarrasposterior ", oParam['codbarras']))
        if "grupoPedidos" in oParam:
            idPedido = oParam['grupoPedidos']
            codAlmacen = model["codalmacen"]
        else:
            idPedido = "({})".format(model.pk)
            codAlmacen = model.codalmacen.codalmacen
        if "referencia" in oParam:
            oParam['idlinea'] = self.iface.dameIdLinea(model, oParam)
            if not oParam['idlinea']:
                return False

        # Ya no va a venir idlinea en oparam lo voy a meter yo, buscando lineas de model.pk que tengan esa referencia
        # Si tengo idlinea y codlote puedo asignar procesar el codigo de barras
        if "idlinea" in oParam and "codlote" in oParam:
            if "ncodlote" in oParam and oParam["ncodlote"]:
                lote = self.iface.creaLote(oParam["ncodlote"], oParam["caducidad"], oParam['referencia'])
                if("status" in lote):
                    return lote
                val = self.iface.insertarMovilote(oParam['idlinea'], oParam['referencia'], cantidad, codAlmacen, lote)
                if val['status'] == 0:
                    return True
                return val
            val = self.iface.insertarMovilote(oParam['idlinea'], oParam['referencia'], cantidad, codAlmacen, oParam['codlote'])
            if val['status'] == 0:
                return True
            return val
        # Si tengo idlinea y nuevo codlote puedo asignar procesar el codigo de barras
        if "idlinea" in oParam and "ncodlote" in oParam:
            lote = self.iface.creaLote(oParam["ncodlote"], oParam["caducidad"], oParam['referencia'])
            val = self.iface.insertarMovilote(oParam['idlinea'], oParam['referencia'], cantidad, codAlmacen, lote)
            if val['status'] == 0:
                return True
            return val

        # Si idlinea y codproveedor en oParam tengo todo lo necesario para asignar un codigo de barras
        if "idlinea" in oParam and "codproveedor" in oParam:
            # linea = lineaspedidosprov.objects.get(pk=oParam['idlinea'])
            referencia = qsatype.FLUtil.sqlSelect("lineaspedidosprov", "referencia", "idlinea = {}".format(oParam['idlinea']))
            objcod = flfactalma_def.iface.datosLecturaCodBarras(oParam['codbarras'], oParam["codproveedor"], referencia)
            asociado = flfactalma_def.iface.asociarCodBarras(referencia, oParam["codproveedor"], objcod['codbarras'])
            if asociado and not objcod['lote']:
                val = self.iface.analizaCodBarras(idPedido, oParam['codbarras'], cantidad, codAlmacen, oParam['idlinea'])
                return self.iface.respuestaAnalizaCodBarras(model, oParam, val)
                return val
            else:
                val = self.iface.analizaCodBarrasLote(referencia, objcod['codbarras'], objcod, cantidad, oParam['idlinea'], codAlmacen)
                return self.iface.respuestaAnalizaCodBarras(model, oParam, val)
                return val

        # Si idlinea en oParam significa que me estan enviando un codigo de barras para asociar a un articulo de la linea
        if "idlinea" in oParam and "codproveedor" not in oParam:
            # linea = lineaspedidosprov.objects.get(pk=oParam['idlinea'])
            # proveedor = articulosprov.objects.filter(referencia__exact=linea.referencia)
            referencia = qsatype.FLUtil.sqlSelect("lineaspedidosprov", "referencia", "idlinea = {}".format(oParam['idlinea']))
            codproveedor = qsatype.FLUtil.sqlSelect("articulosprov", "codproveedor", "referencia = '{}'".format(referencia))
            if codproveedor:
                # print("tengo ilinea y no proveedor pero ", proveedor[0].codproveedor, " ", linea.referencia, " ", oParam['codbarras'])
                objcod = flfactalma_def.iface.datosLecturaCodBarras(oParam['codbarras'], codproveedor, referencia)
                asociado = flfactalma_def.iface.asociarCodBarras(referencia, codproveedor, objcod['codbarras'])
                if asociado and not objcod['lote']:
                    val = self.iface.analizaCodBarras(idPedido, oParam['codbarras'], cantidad, codAlmacen, oParam['idlinea'])
                    return self.iface.respuestaAnalizaCodBarras(model, oParam, val)
                    return val
                else:
                    val = self.iface.analizaCodBarrasLote(referencia, objcod['codbarras'], objcod, cantidad, oParam['idlinea'], codAlmacen)
                    return self.iface.respuestaAnalizaCodBarras(model, oParam, val)
                    # return val
            else:
                response = {}
                response['status'] = -1
                response['data'] = {"codbarras": oParam['codbarras'], "cantidad": cantidad, "idlinea": oParam["idlinea"], "referencia": referencia}
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
            val = self.iface.analizaCodBarras(idPedido, oParam['codbarras'], cantidad, codAlmacen, None)
            return self.iface.respuestaAnalizaCodBarras(model, oParam, val)

        return True

    def sanhigia_pedidos_dameIdLinea(self, model, oParam):
        # idPedido = "('" + str(model.pk) + "')"
        if "grupoPedidos" in oParam:
            idPedido = oParam['grupoPedidos']
        else:
            idPedido = "({})".format(model.idpedido)
        query = qsatype.FLSqlQuery()
        query.setTablesList(u"lineaspedidosprov")
        query.setSelect(u"idlinea, referencia, cantidad, shcantalbaran")
        query.setFrom(u"lineaspedidosprov")
        query.setWhere(u"referencia = '{}'  AND idpedido IN {}".format(oParam['referencia'], idPedido))

        if query.exec_():
            if query.size() > 1:
                while query.next():
                    shcantalbaran = query.value(3) or 0
                    if int(query.value(2)) > int(shcantalbaran):
                        return query.value(0)
            if query.size() == 1:
                if query.next():
                    return query.value(0)
            return query.value(0)
        return False

    def sanhigia_pedidos_respuestaAnalizaCodBarras(self, model, oParam, val):
        # Si se produce un error que no permite modificar el pedido
        # Suma 1
        cantidad = 1
        if val['status'] == -3 or val['status'] == -2:
            return val

        # -1 Si el codigo de barras no pertenece a nigun articulo y algun articulo del pedido no tienen codigo de barras
        if val['status'] == -1:
            opts = []
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

        # Va por lotes y tengo que pedir que se cree uno
        if val['status'] == 3:
            response = {}
            response['status'] = -1
            response['data'] = {
                "codbarras": oParam['codbarras'],
                "cantidad": cantidad,
                "idlinea": oParam['idlinea'],
                "referencia": oParam['referencia']
            }
            response['params'] = [
                {
                    "tipo": 3,
                    "required": False,
                    "verbose_name": "Código Lote",
                    "visible": True,
                    "key": "ncodlote",
                    # "clientBch": True,
                    "validaciones": None
                },
                {
                    "tipo": 26,
                    "required": False,
                    "verbose_name": "F. Caducidad",
                    "visible": True,
                    "key": "caducidad",
                    "validaciones": None
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

        # va por lotes y no tengo codlote
        if val['status'] == 2:
            opts = []
            query = val['param']['query']
            ncodlote = None
            if "ncodlote" in val['param']:
                ncodlote = val['param']['ncodlote']
            # print(val)
            # opt = {}
            # opt['key'] = "ncodlote"
            # opt['alias'] = "Nuevo Lote"
            # opts.append(opt)
            while query.next():
                opt = {}
                opt['key'] = query.value("codlote")
                formatofecha = "%d/%m/%Y"
                if query.value("caducidad"):
                    fecha = query.value("caducidad").strftime(formatofecha)
                else:
                    fecha = None
                # opt['alias'] = query.value("codigo") + " - " + str(int(query.value("enalmacen"))) + " - " + str(fecha) + " - " + query.value("descripcion")
                opt['alias'] = "{} - {} - {} - {}".format(query.value("codigo"), query.value("enalmacen"), fecha, query.value("descripcion"))
                opts.append(opt)
            response = {}
            response['status'] = -1

            response['data'] = {
                "codbarras": oParam['codbarras'],
                "cantidad": cantidad,
                "idlinea": val['param']['idlinea'],
                "referencia": val['param']['referencia'],
                "ncodlote": ncodlote
            }

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
        curPedido = qsatype.FLSqlCursor(u"pedidosprov")
        curPedido.select("idpedido = {}".format(model.idpedido))
        if not curPedido.first():
            raise ValueError("Error no se encuentra el pedido ")
            return False
        curPedido.setModeAccess(curPedido.Edit)
        curPedido.refreshBuffer()
        curPedido.setValueBuffer("pda", 'Listo PDA')
        codtrabajador = qsatype.FLUtil.sqlSelect("sh_trabajadores", "codtrabajador", "idusuario = '{}'".format(qsatype.FLUtil.nameUser()))
        if codtrabajador and codtrabajador != "":
            curPedido.setValueBuffer("codtrabajador", codtrabajador)
        if not curPedido.commitBuffer():
            return False
        if not qsatype.FLUtil.sqlUpdate(u"lineaspedidosprov", "sh_codtrabarecep", codtrabajador, "idpedido = {} AND sh_codtrabarecep IS NULL AND shcantalbaran > 0".format(model.idpedido)):
            raise ValueError("Error al actualizar el trabajador de las líneas")
            return False
        return True

    def sanhigia_pedidos_generarAlbaranProv(self, model, oParam):
        response = {}
        idpedido = model.idpedido
        pedidopreparado = qsatype.FLUtil.sqlSelect("lineaspedidosprov", "COUNT(idlinea)", "idpedido = {}  AND shcantalbaran > 0 AND cantidad > totalenalbaran ".format(idpedido))
        if not pedidopreparado or pedidopreparado < 1:
            resul = {}
            resul['status'] = 1
            resul['msg'] = "Para generar albarán primero debe preparar las lineás"
            return resul
        codtrabajador = qsatype.FLUtil.sqlSelect("pedidosprov", "codtrabajador", "idpedido = {} ".format(idpedido))
        if not codtrabajador or codtrabajador == "":
            resul = {}
            resul['status'] = 1
            resul['msg'] = "No esta informado el campo trabajador.Para informarlo usa el bóton 'Listo PDA'"
            return resul
        try:
            # Llamadas locales
            # res = requests.post("http://127.0.0.1:8005/api/pedidosproveedor/{0}/llama_generar_albaran".format(idpedido))
            res = requests.post("http://172.65.0.1:8005/api/pedidosproveedor/{0}/llama_generar_albaran".format(idpedido))
            if res.status_code != 200:
                response['status'] = -1
                response['msg'] = "Error al generar albáran.<br>Código error: {1} {2}".format(res.status_code, res.reason)
                return response
        except Exception:
            response['status'] = -1
            response['msg'] = "Error al generar albáran.<br>Error de conexión con el servidor"
            return response
        idalbaran = res.json()
        if not idalbaran:
            response['status'] = -1
            response['msg'] = "Error al generar albáran."
            return response
        codigo = qsatype.FLUtil.sqlSelect("albaranesprov", "codigo", "idalbaran = {}  ".format(idalbaran))
        response['resul'] = 1
        response['msg'] = "Se ha generado correctamente el albáran {}".format(codigo)
        return response

    def sanhigia_pedidos_getForeignFields(self, model, template):
        return [
            {'verbose_name': 'rowColor', 'func': 'field_colorRow'}
        ]

    def sanhigia_pedidos_creaLote(self, codigo, caducidad, referencia):
        codLote = qsatype.FLUtil.sqlSelect(u"lotes", u"codlote", u"codigo = '{0}' AND referencia = '{1}' AND caducidad = '{2}'".format(codigo, referencia, caducidad))
        if not codLote:
            query = qsatype.FLSqlQuery()
            query.setTablesList(u"articulos")
            query.setSelect(u"descripcion")
            query.setFrom(u"articulos")
            query.setWhere("referencia = '{}'".format(referencia))

            if query.exec_():
                if query.next():
                    descripcion = query.value(0)
                else:
                    return False
            else:
                return False

            if not caducidad:
                resul = {}
                resul['status'] = -3
                resul['msg'] = "F.Caducidad obligatoria"
                resul['resul'] = False
                return resul

            curLote = qsatype.FLSqlCursor(u"lotes")
            curLote.setModeAccess(curLote.Insert)
            curLote.refreshBuffer()
            curLote.setValueBuffer("codigo", codigo)
            curLote.setValueBuffer("caducidad", caducidad)
            curLote.setValueBuffer("descripcion", descripcion)
            curLote.setValueBuffer("referencia", referencia)
            curLote.setValueBuffer("enalmacen", 0)
            curLote.setValueBuffer(u"codlote", qsatype.FLUtil.nextCounter(u"codlote", curLote))
            if curLote.commitBuffer():
                return curLote.valueBuffer("codlote")
            return False
        else:
            return codLote

    def sanhigia_pedidos_insertarMovilote(self, idLinea, referencia, cantidad, codAlmacen, codLote):
        resul = {}
        # lo que tenemos es el codigo de lotes pero lo que se inserta es el campo codlote de lotes, vamos a buscar el primer codlote de la tabla lotes que tenga como codigo el lote que hemos ledio y que tenga stock
        # codLote = qsatype.FLUtil.sqlSelect(u"lotes", u"codlote", ustr(u"codigo = '", codigo, u"' AND enalmacen > 0 "))
        if codLote == u"" or not codLote:
            resul['status'] = -3
            resul['msg'] = "No existe ningún lote con stock para este pedido"
            resul['param'] = idLinea
            resul['resul'] = False
            return resul

        idStock = qsatype.FLUtil.sqlSelect(u"stocks", u"idstock", u"referencia = '{}' AND codalmacen = '{}'".format(referencia, codAlmacen))

        if idStock == u"" or not idStock:
            resul['status'] = -3
            resul['msg'] = "No existe stock para la referencia {} en el almacén {}.".format(referencia, codAlmacen)
            resul['param'] = idLinea
            resul['resul'] = False
            return resul

        hoy = qsatype.Date()
        idmovilote = qsatype.FLUtil.sqlSelect(u"movilote", u"id", u"idlineapp = '{}' AND fecha = '{}' AND codlote = '{}' AND idlineaap is null".format(idLinea, hoy, codLote))
        if idmovilote:
            curMovilote = qsatype.FLSqlCursor(u"movilote")
            curMovilote.select("id = '{}'".format(idmovilote))
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
            curMovilote.setValueBuffer("tipo", "Entrada")
            curMovilote.setValueBuffer("codlote", codLote)
            curMovilote.setValueBuffer("docorigen", "PP")
            curMovilote.setValueBuffer("fecha", hoy)
            curMovilote.setValueBuffer("idlineapp", idLinea)

            if not curMovilote.commitBuffer():
                resul['status'] = -3
                resul['msg'] = "Error al crear movimiento de lote"
                resul['param'] = idLinea
                resul['resul'] = False
                return resul

        resul['status'] = 0
        resul['msg'] = "OK"
        resul['param'] = idLinea
        resul['resul'] = True
        return resul

    def sanhigia_pedidos_analizaCodBarras(self, idPedido, barcode, cantidad, codAlmacen, idlineapedido):
        '''
        1. Comprobar si el barcode existe en alguna liea del pedido.
            1.1. No existe --> Devuelvo Error.
        2. Si existe.
            2.1. El barcode NO es cuadrado
                2.1.1. El barcode no va por lotes --> Actualizo cantidad de la l?ea. Devuelvo true.
                2.1.2. El barcode va por lotes --> Devuelvo que va por lotes para mostrar formulario que elije lotes y debo de hacer otra llamada que inserte el lote y actualice cantidad
            2.2. El barcode SI es cuadrado --> Tengo lote --> Inserto l?ea en movilote y devuelvo true.

        '''

        referencia = ""
        idLinea = idlineapedido
        resul = {}
        # datos = qsatype.FactoriaModulos.get('formRecordarticulosprov').iface.datosLecturaCodBarras(barcode)
        datos = flfactalma_def.iface.datosLecturaCodBarras(barcode)

        codBarras = datos['codbarras']

        # Ver si existe alguna referencia para ese c?igo de barras
        referencia = qsatype.FLUtil.sqlSelect(u"articulosprov", u"referencia", "codbarrasprov = '{}'".format(codBarras))
        # Si no existe referencia compruebo si las lineas tienen codbarras
        if referencia == u"" or not referencia:
            # if "lote" in datos and not datos["lote"]:
            query = qsatype.FLSqlQuery()
            query.setTablesList(u"articulosprov,lineaspedidosprov")
            query.setSelect(u"DISTINCT(articulosprov.referencia), lineaspedidosprov.descripcion")
            # query.setSelect(u"articulosprov.referencia, lineaspedidosprov.idlinea, lineaspedidosprov.descripcion")
            query.setFrom(u"articulosprov inner join lineaspedidosprov on articulosprov.referencia = lineaspedidosprov.referencia")
            # query.setWhere(ustr(u"articulosprov.codbarrasprov is null AND lineaspedidosprov.idpedido = ", idPedido))
            query.setWhere(u"lineaspedidosprov.idpedido IN {}".format(idPedido))

            if query.exec_():
                if query.size() >= 1:
                    resul['status'] = -1
                    resul['msg'] = "¿Asociar codigo de barras a pedido?"
                    resul['param'] = query
                    return resul
                else:
                    resul['status'] = -2
                    resul['msg'] = "No existe la referencia en el pedido"
                    resul['param'] = referencia
                    return resul
            else:
                return False

        # Ver si existe m? de una referencia para el c?igo de barras pero filtramos ya por el pedido
        numReg = qsatype.FLUtil.sqlSelect(u"articulosprov inner join lineaspedidosprov on articulosprov.referencia = lineaspedidosprov.referencia ", u"count(distinct(articulosprov.referencia))", u"articulosprov.codbarrasprov = '{}' AND lineaspedidosprov.idpedido IN {} GROUP BY articulosprov.referencia".format(codBarras, idPedido))
        if not numReg:
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
            query = qsatype.FLSqlQuery()
            query.setTablesList(u"lineaspedidosprov")
            query.setSelect(u"idlinea, referencia, cantidad")
            query.setFrom(u"lineaspedidosprov")
            query.setWhere(u"referencia = '{}' AND idpedido IN {}".format(referencia, idPedido))

            if query.exec_():
                if query.size() > 1:
                    while query.next():
                        if int(query.value(2)) == int(cantidad):
                            referencia = query.value(1)
                            idLinea = query.value(0)
                    if not idLinea:
                        referencia = query.value(1)
                        idLinea = query.value(0)
                if query.size() == 1:
                    if query.next():
                        referencia = query.value(1)
                        idLinea = query.value(0)
            else:
                resul['status'] = -3
                resul['msg'] = "Error inesperado"
                resul['resul'] = False
                return resul
        # 2.Existe
        # 2.1 no es cuadrado
        if datos['lote'] == u"" or not datos['lote']:
            porLotes = qsatype.FLUtil.sqlSelect(u"articulos", u"porlotes", "referencia = '{}'".format(referencia))
            if not porLotes:
                # 2.1.1 actualizo línea
                # print("_____idlinea____", idLinea)
                shcantidad = qsatype.FLUtil.sqlSelect(u"lineaspedidosprov", u"shcantalbaran", "idlinea = {}".format(idLinea)) or 0
                shcantidad = shcantidad + 1
                if not qsatype.FLUtil.sqlUpdate(u"lineaspedidosprov", u"shcantalbaran", shcantidad, u"idlinea = {}".format(idLinea)):
                    resul['status'] = -3
                    resul['msg'] = "Error al actualizar línea del pedido"
                    resul['param'] = idLinea
                    resul['resul'] = False
                    return resul
            else:
                # 2.1.2 Va por lotes
                resul['status'] = -3
                resul['msg'] = "Error inesperado"
                query = qsatype.FLSqlQuery()
                query.setTablesList(u"lotes")
                query.setSelect(u"*")
                query.setFrom(u"lotes")
                query.setWhere("referencia = '{}' AND enalmacen > 0".format(referencia))

                if query.exec_():
                    if query.size() >= 1:
                        resul = {}
                        resul['status'] = 2
                        resul['msg'] = "¿Asociar codigo de barras a pedido?"
                        oParam = {}
                        oParam['referencia'] = referencia
                        oParam['descripcion'] = qsatype.FLUtil.sqlSelect(u"articulos", u"descripcion", "referencia = '{}'".format(referencia))
                        oParam['idlinea'] = idLinea
                        oParam['query'] = query
                        resul['param'] = oParam
                        return resul
                    else:
                        resul = {}
                        resul['status'] = 2
                        resul['msg'] = "¿Asociar codigo de barras a pedido?"
                        oParam = {}
                        oParam['referencia'] = referencia
                        oParam['descripcion'] = qsatype.FLUtil.sqlSelect(u"articulos", u"descripcion", "referencia = '{}'".format(referencia))
                        oParam['idlinea'] = idLinea
                        oParam['query'] = query
                        resul['param'] = oParam
                        return resul

                return resul
        else:
            # 2.2 El barcode es cuadrado
            codigo = datos['lote']
            if "caducidad" in datos:
                caducidad = datos["caducidad"]
            else:
                caducidad = None
            # lo que tenemos es el codigo de lotes pero lo que se inserta es el campo codlote de lotes, vamos a buscar el primer codlote de la tabla lotes que tenga como codigo el lote que hemos ledio y que tenga stock
            codLote = qsatype.FLUtil.sqlSelect(u"lotes", u"codlote", "codigo = '{}' AND referencia = '{}'".format(codigo, referencia))
            if not codLote:
                query = qsatype.FLSqlQuery()
                query.setTablesList(u"lotes")
                query.setSelect(u"*")
                query.setFrom(u"lotes")
                query.setWhere("referencia = '{}' AND enalmacen > 0".format(referencia))

                # if query.exec_():
                #     if query.size() >= 1:
                resul = {}
                resul['status'] = 2
                resul['msg'] = "¿Asociar codigo de barras a pedido?"
                oParam = {}
                oParam['referencia'] = referencia
                oParam['descripcion'] = qsatype.FLUtil.sqlSelect(u"articulos", u"descripcion", "referencia = '{}'".format(referencia))
                oParam['idlinea'] = idLinea
                oParam['query'] = query
                oParam['ncodlote'] = codigo
                resul['param'] = oParam
                oParam["caducidad"] = caducidad
                return resul
                #     else:
                #         resul['status'] = -3
                #         resul['msg'] = "No existe stock para la referencia ", referencia, " en el almacén ", codAlmacen
                #         resul['param'] = idLinea
                #         return resul
                # print("______1_______")
                # resul['status'] = -3
                # resul['msg'] = "No existe ningún lote con stock para este pedido"
                # resul['param'] = idLinea
                # return resul

            # idStock = qsatype.FLUtil.sqlSelect(u"stocks", u"idstock", ustr(u"referencia = '", referencia, u"' AND codalmacen = '", codAlmacen, u"'"))
            idStock = qsatype.FLUtil.sqlSelect(u"stocks", u"idstock", "referencia = '{}' AND codalmacen = '{}'".format(referencia, codAlmacen))
            if idStock == u"" or not idStock:
                resul['status'] = -1
                resul['msg'] = "No existe stock para la referencia {} en el almacén {}.".format(referencia, codAlmacen)
                resul['param'] = idLinea
                resul['resul'] = False
                return resul
            hoy = qsatype.Date()
            idmovilote = qsatype.FLUtil.sqlSelect(u"movilote", u"id", u"idlineapp = '{}' AND fecha = '{}' AND codlote = '{}' AND idlineaap is null".format(idLinea, hoy, codLote))
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
                curMovilote.setValueBuffer("tipo", "Entrada")
                curMovilote.setValueBuffer("codlote", codLote)
                curMovilote.setValueBuffer("docorigen", "PP")
                curMovilote.setValueBuffer("fecha", hoy)
                curMovilote.setValueBuffer("idlineapp", idLinea)

                if not curMovilote.commitBuffer():
                    resul['status'] = -3
                    resul['msg'] = "Error al crear movimiento de lote"
                    resul['param'] = idLinea
                    resul['resul'] = False
                    return resul

        resul['status'] = 0
        resul['msg'] = "OK"
        resul['param'] = idLinea
        return resul

    def sanhigia_pedidos_analizaCodBarrasLote(self, referencia, barcode, objarticulo, cantidad, idLinea, codAlmacen):
        # 2.2 El barcode es cuadrado
        # print("___analizarcodbarraslote____")
        resul = {}
        codigo = objarticulo["lote"]
        if "caducidad" in objarticulo:
            caducidad = objarticulo["caducidad"]
        else:
            caducidad = None
        # codigo = lote
        # lo que tenemos es el codigo de lotes pero lo que se inserta es el campo codlote de lotes, vamos a buscar el primer codlote de la tabla lotes que tenga como codigo el lote que hemos ledio y que tenga stock
        codLote = qsatype.FLUtil.sqlSelect(u"lotes", u"codlote", "codigo = '{}' AND enalmacen > 0 AND referencia ='{}'".format(codigo, referencia))
        # print("________________________", codLote)
        if codLote == u"" or not codLote:
            query = qsatype.FLSqlQuery()
            query.setTablesList(u"lotes")
            query.setSelect(u"*")
            query.setFrom(u"lotes")
            query.setWhere("referencia = '{}' AND enalmacen > 0".format(referencia))

            resul = {}
            resul['status'] = 2
            resul['msg'] = "¿Asociar codigo de barras a pedido?"
            oParam = {}
            oParam['referencia'] = referencia
            oParam['descripcion'] = qsatype.FLUtil.sqlSelect(u"articulos", u"descripcion", "referencia = '{}'".format(referencia))
            oParam['idlinea'] = idLinea
            oParam['query'] = query
            oParam['ncodlote'] = codigo
            oParam['caducidad'] = caducidad
            resul['param'] = oParam
            return resul

        idStock = qsatype.FLUtil.sqlSelect(u"stocks", u"idstock", "referencia = '{}' AND codalmacen = '{}'".format(referencia, codAlmacen))
        if idStock == u"" or not idStock:
            resul['status'] = -1
            resul['msg'] = "No existe stock para la referencia ", referencia, " en el almacén ", codAlmacen
            resul['param'] = idLinea
            return resul

        hoy = qsatype.Date()
        idmovilote = qsatype.FLUtil.sqlSelect(u"movilote", u"id", u"idlineapp = '{}' AND fecha = '{}' AND codlote = '{}' AND idlineaap is null".format(idLinea, hoy, codLote))
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
            curMovilote.setValueBuffer("tipo", "Entrada")
            curMovilote.setValueBuffer("codlote", codLote)
            curMovilote.setValueBuffer("docorigen", "PP")
            curMovilote.setValueBuffer("fecha", hoy)
            curMovilote.setValueBuffer("idlineapp", idLinea)

            if not curMovilote.commitBuffer():
                resul['status'] = -1
                resul['msg'] = "Error al crear movimiento de lote"
                resul['param'] = idLinea
                resul['resul'] = False
                return resul

        resul['status'] = 0
        resul['msg'] = "OK"
        resul['param'] = idLinea
        return resul
        return None

    def sanhigia_pedidos_agruparPedidos(self, model, oParam):
        # print("agruparPedidos___pedidosprov: ", oParam)
        response = {}
        if "selecteds" not in oParam or not oParam['selecteds']:
            response['status'] = -1
            response['msg'] = "Debes seleccionar al menos un pedido"
            return response
        arrProveedores = oParam['selecteds'].split(u",")
        fp = qsatype.FLUtil.sqlSelect(u"pedidosprov", u"codproveedor", "idpedido = {}".format(arrProveedores[0]))
        fa = qsatype.FLUtil.sqlSelect(u"pedidosprov", u"codalmacen", "idpedido = {}".format(arrProveedores[0]))
        for p in arrProveedores:
            np = qsatype.FLUtil.sqlSelect(u"pedidosprov", u"codproveedor", "idpedido = {}".format(p))
            na = qsatype.FLUtil.sqlSelect(u"pedidosprov", u"codalmacen", "idpedido = {}".format(p))
            if fp != np:
                response['status'] = -1
                response['msg'] = "Los proveedores no coinciden"
                return response
            if fa != na:
                response['status'] = -1
                response['msg'] = "Los almacenes no coinciden"
                return response
        response['status'] = 1
        response['url'] = "/facturacion/lineaspedidosprov/custom/grupopedidos?p_selecteds={}".format(oParam['selecteds'])
        return response

    def sanhigia_pedidos_dameTemplateMasterPedidosprov(self, model):
        return '/facturacion/pedidosprov/master'

    def __init__(self, context=None):
        super(sanhigia_pedidos, self).__init__(context)

    def sanhigia_pedidos_field_colorRow(self, model):
        estado = model.pda
        if estado == "Listo PDA":
            return "cSuccess"
        else:
            return None

    def procesaCodBarras(self, model, oParam):
        return self.ctx.sanhigia_pedidos_procesaCodBarras(model, oParam)

    def dameIdLinea(self, model, oParam):
        return self.ctx.sanhigia_pedidos_dameIdLinea(model, oParam)

    def respuestaAnalizaCodBarras(self, model, oParam, val):
        return self.ctx.sanhigia_pedidos_respuestaAnalizaCodBarras(model, oParam, val)

    def pedidoListoPDA(self, model, oParam):
        return self.ctx.sanhigia_pedidos_pedidoListoPDA(model, oParam)

    def getForeignFields(self, model, template):
        return self.ctx.sanhigia_pedidos_getForeignFields(model, template)

    def insertarMovilote(self, idLinea, referencia, cantidad, codAlmacen, codLote):
        return self.ctx.sanhigia_pedidos_insertarMovilote(idLinea, referencia, cantidad, codAlmacen, codLote)

    def creaLote(self, codigo, caducidad, referencia):
        return self.ctx.sanhigia_pedidos_creaLote(codigo, caducidad, referencia)

    def analizaCodBarras(self, idPedido, barcode, cantidad, codAlmacen, idlineapedido):
        return self.ctx.sanhigia_pedidos_analizaCodBarras(idPedido, barcode, cantidad, codAlmacen, idlineapedido)

    def analizaCodBarrasLote(self, referencia, barcode, codigo, cantidad, idLinea, codAlmacen):
        return self.ctx.sanhigia_pedidos_analizaCodBarrasLote(referencia, barcode, codigo, cantidad, idLinea, codAlmacen)

    def agruparPedidos(self, model, oParam):
        return self.ctx.sanhigia_pedidos_agruparPedidos(model, oParam)

    def field_colorRow(self, model):
        return self.ctx.sanhigia_pedidos_field_colorRow(model)

    def dameTemplateMasterPedidosprov(self, model):
        return self.ctx.sanhigia_pedidos_dameTemplateMasterPedidosprov(model)

    def generarAlbaranProv(self, model, oParam):
        return self.ctx.sanhigia_pedidos_generarAlbaranProv(model, oParam)

