# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration sanhigia_pedidos #
from YBLEGACY.constantes import *


class sanhigia_pedidos(interna):

    def sanhigia_pedidos_getDesc(self):
        return None

    def sanhigia_pedidos_getCodUbicacion(self, model, oParam):
        data = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"sh_ubicaciones")
        q.setSelect(u"codubicacion")
        q.setFrom(u"sh_ubicaciones")
        q.setWhere(u"codubicacion LIKE '%" + oParam['val'] + "%'")

        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 100:
            return []

        while q.next():
            data.append({"codubicacion": q.value(0), "ubicacionini": q.value(0), "ubicacionfin": q.value(0)})

        return data

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.sanhigia_pedidos_getDesc()

    def getCodUbicacion(self, model, oParam):
        return self.ctx.sanhigia_pedidos_getCodUbicacion(model, oParam)


# @class_declaration head #
class head(sanhigia_pedidos):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
