
# @class_declaration sanhigia_pedidos_inventarios #
class sanhigia_pedidos_inventarios(flfactalma_inventarios, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def initValidation(name, data=None):
        return form.iface.initValidation(name, data)

    def getForeignFields(self, template=None):
        return form.iface.getForeignFields(self, template)

    def field_colorRow(cursor):
        return form.iface.field_colorRow(cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def visibility(self, oParam):
        return form.iface.visibility(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def getCodBarrasProv(self, oParam, cursor):
        return form.iface.getCodBarrasProv(self, oParam, cursor)

