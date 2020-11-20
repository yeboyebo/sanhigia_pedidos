
# @class_declaration sanhigia_pedidos #
from YBUTILS.viewREST import  cacheController
from models.flfactppal import flfactppal_def


class sanhigia_pedidos(flfactppal):

    def sanhigia_pedidos_getClientes(self, model, oParam):
        data = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"clientes")
        q.setSelect("nombre, codcliente")
        q.setFrom("clientes")
        q.setWhere("UPPER(nombre) LIKE '%" + oParam['val'].upper() + "%' OR UPPER(codcliente) LIKE '%" + oParam['val'].upper() + "%'")

        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 200:
            return []

        while q.next():
            data.append({"nombre": q.value(0), "codcliente": q.value(1)})

        return data

    def __init__(self, context=None):
        super(sanhigia_pedidos, self).__init__(context)

    def getClientes(self, model, oParam):
        return self.ctx.sanhigia_pedidos_getClientes(model, oParam)

