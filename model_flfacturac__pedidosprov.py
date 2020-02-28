
# @class_declaration sanhigia_pedidos_pedidosprov #
class sanhigia_pedidos_pedidosprov(flfacturac_pedidosprov, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam"])
    def procesaCodBarras(self, oParam):
        return form.iface.procesaCodBarras(self, oParam)

    def dameIdLinea(self, oParam):
        return form.iface.dameIdLinea(self, oParam)

    def respuestaAnalizaCodBarras(self, oParam, val):
        return form.iface.respuestaAnalizaCodBarras(self, oParam, val)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def pedidoListoPDA(self, oParam):
        return form.iface.pedidoListoPDA(self, oParam)

    def getForeignFields(self, template=None):
        return form.iface.getForeignFields(self, template)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def agruparPedidos(self, oParam):
        return form.iface.agruparPedidos(self, oParam)

    def field_colorRow(self):
        return form.iface.field_colorRow(self)

    @helpers.decoradores.accion(miparam=[])
    def dameTemplateMasterPedidosprov(self):
        return form.iface.dameTemplateMasterPedidosprov(self)

