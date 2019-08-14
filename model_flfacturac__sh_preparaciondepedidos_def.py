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
        desc = "codpreparaciondepedido"
        return desc

    def sanhigia_pedidos_dameTemplatePreparacion(self, model):
        url = '/facturacion/lineaspedidoscli/custom/grupopedidoscli?p_preparacion=' + model.codpreparaciondepedido
        return url

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.sanhigia_pedidos_getDesc()

    def dameTemplatePreparacion(self, model):
        return self.ctx.sanhigia_pedidos_dameTemplatePreparacion(model)


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
