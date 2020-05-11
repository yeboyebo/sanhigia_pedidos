
# @class_declaration sanhigia_pedidos_pedidoscli #
class sanhigia_pedidos_pedidoscli(flfacturac_pedidoscli, helpers.MixinConAcciones):
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

    def getFilters(self, name, template=None):
        return form.iface.getFilters(self, name, template)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def pedidoListoPDA(self, oParam):
        return form.iface.pedidoListoPDA(self, oParam)

    def initValidation(name, data):
        return form.iface.initValidation(name, data)

    def field_trabajador(self):
        return form.iface.field_trabajador(self)

    def field_colorRow(self):
        return form.iface.field_colorRow(self)

    def field_descPreparacion(self):
        return form.iface.field_descPreparacion(self)

    def getForeignFields(self, template=None):
        return form.iface.getForeignFields(self, template)

    def insertarMovilote(self, idLinea, referencia, cantidad, codAlmacen, codLote):
        return form.iface.insertarMovilote(idLinea, referencia, cantidad, codAlmacen, codLote)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def agruparPedidos(self, oParam):
        return form.iface.agruparPedidos(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def agruparpedidosstock(self, oParam):
        return form.iface.agruparpedidosstock(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def quitarTrabajador(self, oParam):
        return form.iface.quitarTrabajador(self, oParam)

    @helpers.decoradores.accion(aqparam=[])
    def visualizarPedido(self):
        return form.iface.visualizarPedido(self)

