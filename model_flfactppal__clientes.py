
# @class_declaration sanhigia_pedidos_clientes #
class sanhigia_pedidos_clientes(flfactppal_clientes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getClientes(self, oParam):
        return form.iface.getClientes(self, oParam)

