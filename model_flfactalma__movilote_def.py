# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration sanhigia_pedidos #
from YBLEGACY.constantes import *


class sanhigia_pedidos(interna):

    def sanhigia_pedidos_pedidos_getDesc(self):
        return None

    def sanhigia_pedidos_getForeignFields(self, model, template):
        return [
            {'verbose_name': 'codigolote', 'func': 'field_codigolote'},
            {'verbose_name': 'caducidadlote', 'func': 'field_caducidadlote'},
            {'verbose_name': 'cantidadmlote', 'func': 'field_cantidadmlote'}
        ]

    def sanhigia_pedidos_field_cantidadmlote(self, model):
        cantmlote = model.cantidad * -1
        return cantmlote

    def sanhigia_pedidos_field_codigolote(self, model):
        lote = lotes.objects.filter(codlote__exact=model.codlote)
        codigo = lote[0].codigo
        return codigo

    def sanhigia_pedidos_field_caducidadlote(self, model):
        lote = lotes.objects.filter(codlote__exact=model.codlote)
        formatofecha = "%d/%m/%Y"
        try:
            caducidad = lote[0].caducidad.strftime(formatofecha)
        except Exception:
            caducidad = None
        return caducidad

    def sanhigia_pedidos_cambiarCantidad(self, model, oParam, cursor):
        print(oParam)
        if ("cantidadmlote" in oParam and oParam["cantidadmlote"] == '0') or ("cantidad" in oParam and oParam["cantidad"] == '0'):
            resul = {}
            resul['status'] = -1
            resul['msg'] = "No pueden generarse movimientos nulos"
            return resul
        if cursor.valueBuffer("docorigen") == "PP":
            cantidad = oParam["cantidad"]
        elif cursor.valueBuffer("docorigen") == "PC":
            cantidad = int(oParam["cantidadmlote"]) * -1
        cursor.setValueBuffer("cantidad", cantidad)
        if not cursor.commitBuffer():
            return False
        return True

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.sanhigia_pedidos_getDesc()

    def getForeignFields(self, model, template):
        return self.ctx.sanhigia_pedidos_getForeignFields(model, template)

    def field_codigolote(self, model):
        return self.ctx.sanhigia_pedidos_field_codigolote(model)

    def field_caducidadlote(self, model):
        return self.ctx.sanhigia_pedidos_field_caducidadlote(model)

    def field_cantidadmlote(self, model):
        return self.ctx.sanhigia_pedidos_field_cantidadmlote(model)

    def cambiarCantidad(self, model, oParam, cursor):
        return self.ctx.sanhigia_pedidos_cambiarCantidad(model, oParam, cursor)


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
