
# @class_declaration sanhigia_pedidos_lineaspedidoscli #
class sanhigia_pedidos_lineaspedidoscli(flfacturac_lineaspedidoscli, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def fun_metadata(self):
        return form.iface.fun_metadata(self)

    def fun_queryMetadata(self):
        return form.iface.fun_queryMetadata(self)

    def fun_disStock(self):
        return form.iface.fun_disStock(self)

    def fun_codubicacion(self):
        return form.iface.fun_codubicacion(self)

    def fun_referenciaprov(self):
        return form.iface.fun_referenciaprov(self)

    def fun_Queryreferenciaprov(self):
        return form.iface.fun_Queryreferenciaprov(self)

    def fun_codpedido(self):
        return form.iface.fun_codpedido(self)

    def fun_QuerypteServir(self):
        return form.iface.fun_QuerypteServir(self)

    def fun_pteServir(self):
        return form.iface.fun_pteServir(self)

    def initValidation(name, data):
        return form.iface.initValidation(name, data)

    def getForeignFields(self, template=None):
        return form.iface.getForeignFields(self, template)

    def getFilters(self, name, template=None):
        return form.iface.getFilters(self, name, template)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def modificarShcantidad(self, oParam):
        return form.iface.modificarShcantidad(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def modificarShcantidadQuery(self, oParam):
        return form.iface.modificarShcantidadQuery(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def modificarUbicacion(self, oParam):
        return form.iface.modificarUbicacion(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def anadirLote(self, oParam):
        return form.iface.anadirLote(self, oParam)

    @helpers.decoradores.accion(miparam=[])
    def dameTemplateMovilote(self):
        return form.iface.dameTemplateMovilote(self)

    @helpers.decoradores.accion(miparam=[])
    def dameTemplateMoviloteQuery(self):
        return form.iface.dameTemplateMoviloteQuery(self)

    @helpers.decoradores.accion(miparam=[])
    def cerrarLinea(self):
        return form.iface.cerrarLinea(self)

    def field_colorRow(self):
        return form.iface.field_colorRow(self)

    def field_grupoColorRow(self):
        return form.iface.field_grupoColorRow(self)

    def field_grupoQueryColorRow(self):
        return form.iface.field_grupoQueryColorRow(self)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def procesaCodBarrasGrupo(self, oParam):
        return form.iface.procesaCodBarrasGrupo(self, oParam)

    @helpers.decoradores.accion(miparam=[])
    def dameTemplatePedidoCli(self):
        return form.iface.dameTemplatePedidoCli(self)

    def queryGrid_grupoPedidosCli(algo):
        return form.iface.queryGrid_grupoPedidosCli()

    @helpers.decoradores.accion(aqparam=["oParam"])
    def inventariar(self, oParam):
        return form.iface.inventariar(self, oParam)

    @helpers.decoradores.accion(aqparam=[])
    def visualizarPedido(self):
        print("_______________________")
        return form.iface.visualizarPedido(self)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def completarLinea(self, oParam):
        return form.iface.completarLinea(self, oParam)

