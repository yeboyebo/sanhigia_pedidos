
# @class_declaration sanhigia_pedidos #


class sanhigia_pedidos(flfactalma):

    def sanhigia_pedidos_asociarCodBarras(self, referencia, codproveedor, codbar):
        curAP = qsatype.FLSqlCursor(u"articulosprov")
        curAP.select("referencia = '" + str(referencia) + "' AND codproveedor = '" + str(codproveedor) + "'")
        if not curAP.first():
            raise ValueError("Error no se encuentra larticulo")
            return False

        curAP.setModeAccess(curAP.Edit)
        curAP.refreshBuffer()

        curAP.setValueBuffer("codbarrasprov", codbar)
        if not curAP.commitBuffer():
            return False

        return True

    def sanhigia_pedidos_dameCodBarras(self, referencia, codproveedor):
        curAP = qsatype.FLSqlCursor(u"articulosprov")
        curAP.select("referencia = '" + str(referencia) + "' AND codproveedor = '" + str(codproveedor) + "'")
        if not curAP.first():
            raise ValueError("Error no se encuentra larticulo")
            return False

        codBarrasProv = ""
        if(curAP.valueBuffer(u"codbarrasprov")):
            codBarrasProv = curAP.valueBuffer(u"codbarrasprov")

        return codBarrasProv

    def sanhigia_pedidos_datosLoteProveedor(self, lectura, codproveedor, referencia):
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"articulosprov")
        q.setSelect(u"iniciolote, finlote,codbarrasprov")
        q.setFrom(u"articulosprov")
        q.setWhere(u"codproveedor = '" + codproveedor + "' AND referencia = '" + referencia + "'")
        if not q.exec_():
            # print("Error inesperado")
            return None

        if q.next():
            if q.value("iniciolote") and q.value("finlote"):
                iniciolote = int(q.value("iniciolote"))
                finlote = len(lectura) - int(q.value("finlote"))
                lote = lectura[iniciolote:][:-finlote]
                return lote
        return None

    def sanhigia_pedidos_dameProveedor(self, codbarras):
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"articulosprov")
        q.setSelect(u"codproveedor, referencia")
        q.setFrom(u"articulosprov")
        q.setWhere(u"codbarrasprov = '" + codbarras + "'")

        if not q.exec_():
            # print("Error inesperado")
            return None, None

        if q.size() > 1:
            # Si tenemos mas de un proveedor hay que buscar el de por defecto
            q2 = qsatype.FLSqlQuery()
            q2.setTablesList(u"articulosprov")
            q2.setSelect(u"codproveedor, referencia")
            q2.setFrom(u"articulosprov")
            q2.setWhere(u"codbarrasprov = '" + codbarras + "' AND pordefecto=true")

            if not q2.exec_():
                if q.next():
                    return q.value(0), q.value(1)

            if q2.exec_():
                if q.next():
                    return q.value(0), q.value(1)

        if q.next():
            return q.value(0), q.value(1)

        return None, None

    def sanhigia_pedidos_dameReferenciaProveedor(self, codproveedor, codbarras):
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"articulosprov")
        q.setSelect(u"referencia")
        q.setFrom(u"articulosprov")
        q.setWhere(u"codproveedor = '" + codproveedor + "' AND codbarrasprov = '" + codbarras + "'")
        if not q.exec_():
            # print("Error inesperado")
            return None

        if q.next():
            return q.value(0)
        return None

    def sanhigia_pedidos_datosLecturaCodBarras(self, lectura=None, codproveedor=None, referencia=None):
        if not lectura or lectura == u"":
            return u""
        datos = None
        datos = {"codbarras": False, "lote": False}
        qsatype.debug("**" + lectura)
        crt = lectura.find("#")
        if crt > 0:
            datos['codbarras'] = lectura[:crt]
            # Para quitar #
            crt = crt + 1
            derecha = lectura[crt:]
            crtl = derecha.find("#")
            if crtl > 0:
                datos['lote'] = derecha[:crtl]
                qsatype.debug("1Tipo: ")
                qsatype.debug(datos)
                return datos
            else:
                datos['lote'] = derecha
                qsatype.debug("2Tipo: ")
                qsatype.debug(datos)
                return datos
        if len(lectura) == 12 and lectura[4] == u"\t":
            a = lectura.split(u"\t")
            datos['codbarras'] = a[0]
            datos['lote'] = a[1]
        elif len(lectura) <= 14:
            datos['codbarras'] = lectura
        # meisinger
        elif lectura.startswith('+E0HM'):
            derecha = lectura[5:]
            crt = derecha.find('9/$$8')
            if crt > 0:
                datos['codbarras'] = derecha[:crt]
                izquierda = lectura[:-1]
                datos['lote'] = izquierda[-6:]
            else:
                crt = derecha.find('1/$')
                datos['codbarras'] = derecha[:crt]
                izquierda = lectura[:-5]
                datos['lote'] = izquierda[-6:]
            qsatype.debug("3Tipo")
            qsatype.debug(datos)
            return datos
        else:
            if lectura.startswith('01') or lectura.startswith('02'):
                derecha = lectura[2:]
                datos['codbarras'] = derecha[:14]
                sincodbarras = derecha[14:]
                # Aesculap
                if sincodbarras.startswith('17') and sincodbarras[8] == '1' and sincodbarras[9] == '0':
                    # 010403865301991517241209104511266114
                    # 0114560146927560172208001017g59
                    derecha = derecha[16:]
                    datos['caducidad'] = derecha[:6]
                    lote = derecha[6:]
                    datos['lote'] = lote
                elif sincodbarras.startswith('11') and sincodbarras[8] == '1' and sincodbarras[9] == '7':
                    # 0108809490620277111805281723052710240811042100000274
                    derecha = lectura[26:]
                    datos['caducidad'] = derecha[:6]
                    derecha = derecha[8:]
                    datos['lote'] = derecha[:8]
                elif sincodbarras.startswith('91') and sincodbarras[8] == '1' and sincodbarras[9] == '0':
                    # 01805003882000489108D05s101802012240630 BIOPLANT
                    derecha = lectura[26:]
                    datos['lote'] = derecha[:5]
                    caducidad = derecha[7:]
                    datos['caducidad'] = caducidad
                elif sincodbarras.startswith('10'):
                    # 0104038653021093104510975730
                    lote = sincodbarras[2:]
                    datos['lote'] = lote
                else:
                    derecha = lectura[26:]
                    if len(derecha) == 7:
                        datos['lote'] = derecha[-7:]
                    else:
                        if len(lectura) > 35:
                            datos['lote'] = derecha[:6]
                            datos['caducidad'] = lectura[18:][:4]
                        else:
                            datos['lote'] = derecha[:9]
            elif lectura.startswith('(01)') or lectura.startswith('(02)'):
                derecha = lectura[4:]
                crt = derecha.find('(17)')
                datos['codbarras'] = derecha[:crt]
                crl = derecha.find('(10)') + 4
                derecha = derecha[crl:]
                datos['lote'] = derecha
            else:
                datos['codbarras'] = lectura
        qsatype.debug(datos)
        return datos

    def __init__(self, context=None):
        super(sanhigia_pedidos, self).__init__(context)

    def asociarCodBarras(self, referencia, codproveedor, codbar):
        return self.ctx.sanhigia_pedidos_asociarCodBarras(referencia, codproveedor, codbar)

    def dameCodBarras(self, referencia, codproveedor):
        return self.ctx.sanhigia_pedidos_dameCodBarras(referencia, codproveedor)

    def datosLoteProveedor(self, lectura, codproveedor, referencia):
        return self.ctx.sanhigia_pedidos_datosLoteProveedor(lectura, codproveedor, referencia)

    def dameProveedor(self, codbarras):
        return self.ctx.sanhigia_pedidos_dameProveedor(codbarras)

    def dameReferenciaProveedor(self, codproveedor, codbarras):
        return self.ctx.sanhigia_pedidos_dameReferenciaProveedor(codproveedor, codbarras)

    def datosLecturaCodBarras(self, lectura=None, codproveedor=None, referencia=None):
        return self.ctx.sanhigia_pedidos_datosLecturaCodBarras(lectura, codproveedor, referencia)

