
# @class_declaration sanhigia_pedidos_lineaspedidosprov #
class sanhigia_pedidos_lineaspedidosprov(flfacturac_lineaspedidosprov, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def fun_metadata(self):
        return form.iface.fun_metadata(self)

    def fun_disStock(self):
        return form.iface.fun_disStock(self)

    def fun_codubicacion(self):
        return form.iface.fun_codubicacion(self)

    def fun_referenciaprov(self):
        return form.iface.fun_referenciaprov(self)

    def getFilters(self, name, template=None):
        return form.iface.getFilters(self, name, template)

    def getForeignFields(self, template=None):
        return form.iface.getForeignFields(self, template)

    def initValidation(name, data):
        return form.iface.initValidation(name, data)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def modificarShcantidad(self, oParam):
        return form.iface.modificarShcantidad(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def modificarUbicacion(self, oParam):
        return form.iface.modificarUbicacion(self, oParam)

    @helpers.decoradores.accion(miparam=[])
    def dameTemplateMovilote(self):
        return form.iface.dameTemplateMovilote(self)

    @helpers.decoradores.accion(miparam=[])
    def cerrarLinea(self):
        return form.iface.cerrarLinea(self)

    def field_colorRow(self):
        return form.iface.field_colorRow(self)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def grupopedidosListoPDA(self, oParam):
        return form.iface.grupopedidosListoPDA(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def procesaCodBarrasGrupo(self, oParam):
        return form.iface.procesaCodBarrasGrupo(self, oParam)

    def checkPDAButton(cursor):
        return form.iface.checkPDAButton(cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def anadirLote(self, oParam):
        return form.iface.anadirLote(self, oParam)

