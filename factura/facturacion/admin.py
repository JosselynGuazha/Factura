from django.contrib import admin
from .models import Cliente, DetalleAdicional, Impuesto, DetalleFactura, CampoAdicional, DetalleGuiaRemision, Destinatario, GuiaRemision
from .models import TotalImpuesto, Pagos, ConfigCorreo, ConfigAplicacion, DetalleProforma, Factura, Proforma, ComprobanteGeneral
from .models import LiquidacionCompra, DetalleLiquidacionCompra, ImpuestoComprobanteRetencion, ComprobanteRetencion, Motivo, NotaDebito
from .models import DetalleNotaCredito, NotaCredito, ComprobantePendiente, procesarComprobantePendiente
# Register your models here.


class FacturaAdmin(admin.ModelAdmin):
    list_display = ('identificacionComprador', 'moneda')
    search_fields = ('identificacionComprador', 'moneda')

admin.site.register(Cliente)
admin.site.register(DetalleAdicional)
admin.site.register(Impuesto)
admin.site.register(DetalleFactura)
admin.site.register(CampoAdicional)
admin.site.register(DetalleGuiaRemision)
admin.site.register(Destinatario)
admin.site.register(GuiaRemision)
admin.site.register(TotalImpuesto)
admin.site.register(Pagos)
admin.site.register(ConfigCorreo)
admin.site.register(ConfigAplicacion)
admin.site.register(DetalleProforma)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(Proforma)
admin.site.register(ComprobanteGeneral)
admin.site.register(LiquidacionCompra)
admin.site.register(DetalleLiquidacionCompra)
admin.site.register(ImpuestoComprobanteRetencion)
admin.site.register(ComprobanteRetencion)
admin.site.register(Motivo)
admin.site.register(NotaDebito)
admin.site.register(DetalleNotaCredito)
admin.site.register(NotaCredito)
admin.site.register(ComprobantePendiente)
admin.site.register(procesarComprobantePendiente)