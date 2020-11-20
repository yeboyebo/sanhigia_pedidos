
# @class_declaration sanhigia_pedidos_articulos #
class sanhigia_pedidos_articulos(flfactalma_articulos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam"])
    def lecturaCodBar(self, oParam):
        return form.iface.lecturaCodBar(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def asociarCodBarras(self, oParam):
        return form.iface.asociarCodBarras(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def dameCodBarras(self, oParam):
        return form.iface.dameCodBarras(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def getRerenciasInventario(self, oParam, cursor):
        return form.iface.getRerenciasInventario(self, oParam, cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getReferencia(self, oParam):
        return form.iface.getReferencia(self, oParam)

