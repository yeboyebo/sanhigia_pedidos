
# @class_declaration sanhigia_pedidos_lineasregstocks #
class sanhigia_pedidos_lineasregstocks(flfactalma_lineasregstocks, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getFilters(self, name, template=None):
        return form.iface.getFilters(self, name, template)

    def getForeignFields(self, template=None):
        return form.iface.getForeignFields(self, template)

    def field_colorRow(cursor):
        return form.iface.field_colorRow(cursor)

    def fun_metadata(self):
        return form.iface.fun_metadata(self)

    @helpers.decoradores.accion(aqparam=["cursor"])
    def cerrarLinea(self, cursor):
        return form.iface.cerrarLinea(self, cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def editarCantRegstock(self, oParam, cursor):
        return form.iface.editarCantRegstock(self, oParam, cursor)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def getCodBarrasProv(self, oParam, cursor):
        return form.iface.getCodBarrasProv(self, oParam, cursor)

    def fun_referenciaprov(self):
        return form.iface.fun_referenciaprov(self)

