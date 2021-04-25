from django.db import models

# Create your models here.
    #def __str__(self):
     #   return self.nombre + ' ' + self.apellido

#cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)

#********** Desde Aqui ***********
class Cliente(models.Model):
    razonSocial = models.CharField(verbose_name="Apellidos y Nombres/Razón Social", max_length=100)
    select_tipoIdentificacion = [
        ("CEDULA", 'CEDULA'),
        ("RUC", 'RUC'),
        ("PASAPORTE", 'PASAPORTE'),
        ("IDENTIFICACION_EXTERIOR", 'IDENTIFICACION DEL EXTERIOR')
    ]
    tipoIdentificacion = models.CharField(verbose_name="Tipo Identificacón", max_length=50, choices= select_tipoIdentificacion, default="CEDULA",)
    identificacion = models.CharField(verbose_name="Identificacón", max_length=50, unique = True )
    select_tipoCliente = [
        ("CLIENTE", 'CLIENTE'),
        ("SUJETO_RETENIDO", 'SUJETO RETENIDO'),
        ("DESTINATARIO", 'DESTINATARIO'),
    ]
    tipoCliente = models.CharField(verbose_name="Tipo Cliente", max_length=50, choices= select_tipoCliente, default="CLIENTE",)
    direccion = models.TextField(verbose_name="Dirección")
    telefocnoConvencional =  models.CharField(verbose_name="Teléfono Convencional", max_length=50)
    extension = models.CharField(verbose_name="Extensión", max_length=50)
    telefonoCelular = models.CharField(verbose_name="Teléfono Celular", max_length=50)
    correoElectronico = models.EmailField(verbose_name="Correo Electronico", max_length=50)

    #def clean(self):
     #   try:
      #      if not self.instance.pk:
       #         raise forms.ValidationError("Cliente ya Existe")
        #except Cliente.DoesNotExist:
         #   pass
        #return self.cleaned_data

    def __str__(self):
        return self.razonSocial + ' ' + self.identificacion
    

class DetalleAdicional(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=50)
    valor = models.DecimalField(verbose_name="Valor", max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.nombre + ' ' + str(self.valor)


class Impuesto(models.Model):
    baseImponible = models.DecimalField(verbose_name="Base Imponible", max_digits=10, decimal_places=2)
    codigo = models.CharField(verbose_name="Código Impuesto", max_length=50)
    codigoPorcentaje = models.CharField(verbose_name="Código Porcentaje", max_length=50)
    tarifa = models.DecimalField(verbose_name="Tarifa", max_digits=10, decimal_places=2)
    valor = models.DecimalField(verbose_name="Valor", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.codigo + ' ' +str(self.valor)


class DetalleFactura(models.Model):
    cantidad = models.IntegerField(verbose_name="Cantidad")
    codigoAuxiliar = models.CharField(verbose_name="Código Auxiliar", max_length=50)
    codigoPrincipal = models.CharField(verbose_name="Código Principal", max_length=50)
    descripcion = models.TextField(verbose_name="Descripción", max_length=50)
    descuento = models.DecimalField(verbose_name="Descuento", max_digits=10, decimal_places=2)
    detalleAdicional = models.ForeignKey(DetalleAdicional, verbose_name="Detalle Adicional", related_name='Campo_Adicional', on_delete=models.CASCADE) #DetalleAdicional --- Relacion de UNO a MUCHOS
    impuestos = models.ForeignKey(DetalleAdicional, verbose_name="Impuesto", on_delete=models.CASCADE) #Impuesto --- Relacion de UNO a MUCHOS
    precioTotalSinImpuesto = models.DecimalField(verbose_name="Precio Total Impuesto", max_digits=10, decimal_places=2)
    precioUnitario = models.DecimalField(verbose_name="Precio Unitario", max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.cantidad) + ' ' + self.descripcion + ' ' + str(self.precioUnitario) + ' ' + str(self.precioTotalSinImpuesto)



class CampoAdicional(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=50)
    valor = models.DecimalField(verbose_name="Valor", max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.nombre + ' ' + str(self.valor)


class DetalleGuiaRemision(models.Model):
    cantidad = models.DecimalField(verbose_name="Cantidad", max_digits = 10, decimal_places = 2)
    codigoAdicional = models.CharField(verbose_name="Código Adicional", max_length=50)
    codigoInterno = models.CharField(verbose_name="Código Interno", max_length=50)
    detallesAdicionales = models.OneToOneField(DetalleAdicional, verbose_name="Detalles Adicionales", on_delete=models.CASCADE) #DetalleAdicional --- Relacion UNO a UNO
    
    def __str__(self):
        return str(self.cantidad) + ' ' + self.codigoAdicional + ' ' + self.descripcion

class Destinatario(models.Model):
    codDocSustento = models.CharField(verbose_name="Código Documento Sustento", max_length=50)
    codEstabDestino = models.CharField(verbose_name="Código Estado Destino", max_length=50)
    detalles = models.OneToOneField(DetalleGuiaRemision, verbose_name="Detalles", on_delete=models.CASCADE) #DetalleGuiaRemision --- Relacion UNO a UNO
    dirDestinatario = models.TextField(verbose_name="Dirección Destinatario")
    docAduaneroUnico = models.CharField(verbose_name="Documento Aduanero Unico", max_length=50)
    fechaEmisionDocSustento = models.DateField(verbose_name="Fecha Emision Documento Sustento ")
    identificacionDestinatario = models.CharField(verbose_name="Identificación Destinatario", max_length=50)
    motivoTraslado = models.TextField(verbose_name="Motivo Traslado")
    numAutDocSustento = models.IntegerField(verbose_name="Número Aut. Doc. Sustento")
    numDocSustento = models.IntegerField(verbose_name="Número Documento Sustento")
    razonSocialDestinatario = models.CharField(verbose_name="Razón Social Destinatario", max_length=50)
    ruta = models.CharField(verbose_name="Ruta", max_length=50)

    def __str__(self):
        return self.identificacionDestinatario + ' ' + self.codDocSustento  + ' ' +  self.codEstabDestino


class TotalImpuesto(models.Model):
    baseImponible = models.DecimalField(verbose_name="Base Imponible", max_digits = 10, decimal_places = 2)
    codigo = models.CharField(verbose_name="Código", max_length=50)
    codigoPorcentaje = models.CharField(verbose_name="Código Porcentaje", max_length=50)
    descuentoAdicional = models.DecimalField(verbose_name="Descuento Adicional", max_digits = 10, decimal_places = 2)
    tarifa = models.DecimalField(verbose_name="Tarifa", max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.codigo + ' '+ self.codigoPorcentaje +' '+str(self.baseImponible)

class Pagos(models.Model):
    select_formaPago = [
        ("SIN_UTILIZACION_FINANCIERA", '01-SIN UTILIZACIÓN DEL SISTEMA FINANCIERO'),
        ("COMPESACION_DEUDAS", '15-COMPESACIÓN DE DEUDAS'),
        ("TARJETA_DEBIDO", '16-TARJETA DE DEBITO'),
        ("DINERO_ELECTRONICO", '17-DINERO ELECTRONICO'),
        ("TARJETA_PREPAGO", '18-TARJETA PREPAGO'),
        ("TARJETA_CREDITO", '19-TARJETA DE CREDITO'),
        ("OTROS", '20-OTROS CON UTILIZACIÓN DEL SISTEMA FINANCIERO'),
        ("ENDOSO_TITULOS", '21-ENDOSO DE TITULOS'),
    ]
    formaPago = models.CharField(verbose_name="Forma de Pago", max_length=50, choices= select_formaPago, default="SIN_UTILIZACION_FINANCIERA",)
    total = models.DecimalField(verbose_name="Total", max_digits = 5, decimal_places = 2)
    plazo = models.CharField(verbose_name="Plazo", max_length=50)
    select_unidadTiempo = [
        ("NINGUNA", 'Ninguna'),
        ("DIAS", 'Días'),
        ("MESES", 'Meses'),
        ("AÑOS", 'Años'),
    ]
    unidadTiempo = models.CharField(verbose_name="Unidad Tiempo", max_length=50, choices = select_unidadTiempo, default="NINGUNA")

    def __str__(self):
        return self.formaPago + ' '+self.total

class ConfigCorreo(models.Model):
    correoAsunto = models.CharField(verbose_name="Correo Asunto", max_length=50)
    correoHost = models.CharField(verbose_name="Correo Host", max_length=50)
    correoPass = models.CharField(verbose_name="Correo Password", max_length=50)
    correoPort = models.CharField(verbose_name="Correo Port", max_length=50)
    correoRemitente = models.CharField(verbose_name="Correo Remitente", max_length=50)
    sslHabilitado = models.BooleanField(verbose_name="SSL Habilitado", default=False)

    def __str__(self):
        return self.correoAsunto + ' ' + self.correoRemitente + ' ' + self.correoHost

class ConfigAplicacion(models.Model):
    dirAutorizados = models.CharField(verbose_name="Dirección Autorizados", max_length=100)
    dirFirma = models.CharField(verbose_name="Dirección Firma", max_length=100)
    dirLogo = models.CharField(verbose_name="Dirección Logo", max_length=100)
    passFirma = models.CharField(verbose_name="Password", max_length=50)

    def __str__(self):
        return self.dirAutorizados + ' '+ self.dirFirma

class DetalleProforma(models.Model):
    codigo = models.CharField(verbose_name="Código", max_length=50)
    descripcion = models.TextField(verbose_name="Descripción")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    precioUnitario = models.DecimalField(verbose_name="Precio Unitario", max_digits = 10, decimal_places = 2)
    descuento = models.DecimalField(verbose_name="Descuento", max_digits = 10, decimal_places = 2)
    precioTotalSinImpuesto = models.DecimalField(verbose_name="Precio Total Sin Impuesto", max_digits = 5, decimal_places = 2)

    def __str__(self):
        return self.codigo + ' '+descripcion + ' '+ str(self.cantidad) + ' ' + str(self.precioTotalSinImpuesto)

def asignarLogo():
    configuracion=ConfigAplicacion.objects.all().get()
    print('este valor se imprime', configuracion)
    valor=configuracion.dirLogo
    return valor

class Proforma(models.Model):
    configCorreo = models.OneToOneField(ConfigCorreo, verbose_name="Configuración Correo", on_delete=models.CASCADE) #ConfigCorreo --- UNO a UNO 
    dirLogo = models.CharField(verbose_name="Dirección Logo", max_length=100, default=asignarLogo)
    dirProformas = models.CharField(verbose_name="Dirección Proformas", max_length=100)
    tipoEmision = models.CharField(verbose_name="Tipo Emision", max_length=100)
    razonSocial = models.CharField(verbose_name="Razón Social", max_length=100)
    nombreComercial = models.CharField(verbose_name="Nombre Comercial", max_length=100)
    ruc = models.CharField(verbose_name="RUC", max_length=13)
    numero = models.IntegerField(verbose_name="Número")
    dirMatriz = models.CharField(verbose_name="Dirección Matriz", max_length=100)
    dirEstablecimiento = models.CharField(verbose_name="Dirección Establecimiento", max_length=50)
    fechaEmision = models.DateField(verbose_name="Fecha Emisión")
    razonSocialComprador = models.CharField(verbose_name="Razon Social Comprador", max_length=100)
    identificacionComprador = models.CharField(verbose_name="Identificación Comprador", max_length=50)
    direccionComprador = models.TextField(verbose_name="Dirección Comprador", max_length=100)
    subTotal12 = models.DecimalField(verbose_name="SUB Total 12%", max_digits = 10, decimal_places = 2)
    subTotal0 = models.DecimalField(verbose_name="SUB Total", max_digits = 10, decimal_places = 2)
    subTotalSinImpuesto = models.DecimalField(verbose_name="SUB Total Sin Impuesto", max_digits = 10, decimal_places = 2)
    iva = models.DecimalField(verbose_name="IVA", max_digits = 10, decimal_places = 2)
    totalDescuento = models.DecimalField(verbose_name="Total Descuento", max_digits = 10, decimal_places = 2)
    importeTotal = models.DecimalField(verbose_name="Importe Total", max_digits = 10, decimal_places = 2)
    detalles = models.ForeignKey(DetalleProforma, verbose_name="Detalles", on_delete=models.CASCADE) #DetalleProforma --- Relacion UNO a MUCHOS
    infoAdicional = models.OneToOneField(CampoAdicional, verbose_name="Campo Adicional", on_delete=models.CASCADE) #CampoAdicional --- Relacion UNO a UNO

    def __str__(self):
        return self.ruc + ' ' + self.tipoEmision + ' ' +str(self.importeTotal)

    

class ComprobanteGeneral(models.Model):
    cliente = models.OneToOneField(CampoAdicional, verbose_name="Cliente", on_delete=models.CASCADE)
    ambiente = models.CharField(verbose_name="Ambiente", max_length=100)
    claveAcc = models.CharField(verbose_name="Clave Acc", max_length=50)
    codDoc = models.CharField(verbose_name="Código Documento", max_length=50)
    configAplicacion = models.OneToOneField(ConfigCorreo, verbose_name="Configuración Aplicación", on_delete=models.CASCADE) #ConfigCorreo --- UNO a UNO 
    configCorreo = models.OneToOneField(ConfigAplicacion, verbose_name="Configuración Correo", on_delete=models.CASCADE) #ConfigAplicacion --- UNO a UNO 
    contribuyenteEspecial = models.CharField(verbose_name="Contribuyente Especial", max_length=100)
    dirEstablecimiento = models.CharField(verbose_name="Direeción Establecimiento", max_length=100)
    dirMatriz = models.CharField(verbose_name="Dirección Matriz", max_length=100)
    establecimiento = models.CharField(verbose_name="Establecimeinto", max_length=100)
    fechaEmision = models.DateField(verbose_name="Fecha Emisión")
    nombreComercial = models.CharField(verbose_name="Nombre Comercial", max_length=100)
    obligadoContabilidad = models.CharField(verbose_name="Obligado a LLevar Contabilidad", max_length=100)
    ptoEmision = models.CharField(verbose_name="pto Emisión", max_length=100)
    razonSocial = models.CharField(verbose_name="Razón Social", max_length=100)
    ruc = models.CharField(verbose_name="RUC", max_length=13)
    secuencial = models.CharField(verbose_name="Secuencial", max_length=100)
    tipoDoc = models.CharField(verbose_name="Tipo Documento", max_length=50)
    tipoEmision = models.CharField(verbose_name="Tipo Emisión", max_length=50)

    def __str__(self):
        return self.ambiente + ' ' + self.ruc + ' '+ self.tipoEmision

class GuiaRemision(ComprobanteGeneral):
    destinatarios = models.OneToOneField(Destinatario, verbose_name="Destinatarios", on_delete=models.CASCADE) #Destinatario --- Relacion UNO a UNO
    dirPartida = models.TextField(verbose_name="Direccion Partida") 
    fechaFinTransporte = models.DateField(verbose_name="Fecha Fin Transporte")
    fechaIniTransporte = models.DateField(verbose_name="Fecha Inicio Transporte", max_length=50)
    infoAdicional = models.OneToOneField(CampoAdicional, verbose_name="Campo Adicional", on_delete=models.CASCADE) #CampoAdicional --- Relacion UNO a UNO
    placa = models.CharField(verbose_name="Placa", max_length=10)
    razonSocialTransportista = models.CharField(verbose_name="Razón Social Transportista", max_length=50)
    rise = models.CharField(verbose_name="RISE", max_length=50)
    rucTransportista = models.CharField(verbose_name="RUC Transportista", max_length=50)
    tipoIdentificacionTransportista = models.CharField(verbose_name="Tipo Identificación Trnasportista", max_length=50)

    def __str__(self):
        return self.placa + ' '+self.rise +' ' +self.rucTransportista

class Factura(ComprobanteGeneral):
    detalles = models.ForeignKey(DetalleFactura, verbose_name="Detalles", on_delete=models.CASCADE) #DetalleFactura --- Relacion de UNO a MUCHOS
    guiaRemision = models.OneToOneField(GuiaRemision, verbose_name="Guía Remisión", on_delete=models.CASCADE) #GuiaRemision --- Relacion de UNO a UNO
    identificacionComprador = models.CharField(verbose_name="Identificación del Comprador", max_length=100)
    importeTotal = models.DecimalField(verbose_name="Importe Total", max_digits = 10, decimal_places = 2)
    infoAdicional = models.OneToOneField(CampoAdicional, verbose_name="Campo Adicional", related_name='campoAdicional', on_delete=models.CASCADE) #CampoAdicional --- Relacion UNO a UNO
    moneda = models.DecimalField(verbose_name="Moneda", max_digits = 10, decimal_places = 2)
    propina = models.DecimalField(verbose_name="Propina", max_digits = 10, decimal_places = 2)
    razonSocialComprador = models.CharField(verbose_name="Razón social Comprador", max_length=100)
    tipoIdentificacionComprador = models.CharField(verbose_name="Tipo Identificación Comprador", max_length=50)
    totalConImpuesto = models.OneToOneField(TotalImpuesto, verbose_name="Total con Impuesto", on_delete=models.CASCADE) #TotalImpuesto --- Relacion UNO a UNO
    totalDescuento = models.DecimalField(verbose_name="Total Descuento", max_digits = 10, decimal_places = 2)
    totalSinImpuestos = models.DecimalField(verbose_name="Total Sin Impuesto", max_digits = 10, decimal_places = 2)
    pagos = models.ForeignKey(Pagos, verbose_name="Pagos", on_delete=models.CASCADE) #Pagos --- Relacion de UNO a MUCHOS
    direccionComprador = models.TextField(verbose_name="Dirección Comprador")

    def __str__(self):
        return self.identificacionComprador + ' '+ str(self.importeTotal) + ' '+ str(self.totalConImpuesto)+' '+str(self.totalSinImpuestos)




class LiquidacionCompra(ComprobanteGeneral):
    detalles = models.ForeignKey(DetalleProforma, verbose_name="Detalles", on_delete=models.CASCADE) #DetalleProforma --- Relacion UNO a MUCHOS
    direccionProveedor = models.CharField(verbose_name="Dirección Proveedor", max_length=100)
    identificacionProveedor = models.CharField(verbose_name="Identificación Proveedor", max_length=50)
    importeTotal = models.DecimalField(verbose_name="Importe Total", max_digits = 10, decimal_places = 2)
    infoAdicional = models.OneToOneField(CampoAdicional, verbose_name="Campo Adicional", on_delete=models.CASCADE) #CampoAdicional --- Relacion UNO a UNO
    moneda = models.DecimalField(verbose_name="Moneda", max_digits = 10, decimal_places = 2)
    razonSocialProveedor = models.CharField(verbose_name="Razón Social Proveedor", max_length=100)
    tipoIdentificacionProveedor = models.CharField(verbose_name="Tipo de identificación Proveedor", max_length=100)
    totalConImpuesto = models.OneToOneField(TotalImpuesto, verbose_name="Total Con Impuesto", on_delete=models.CASCADE) #TotalImpuesto --- Relacion UNO a UNO
    totalDescuento = models.DecimalField(verbose_name="Total con Descuento", max_digits = 10, decimal_places = 2)
    totalSinImpuestos = models.DecimalField(verbose_name="Total sin Impuesto", max_digits = 10, decimal_places = 2)
    pagos = models.ForeignKey(Pagos, verbose_name="Pagos", on_delete=models.CASCADE) #Pagos --- Relacion de UNO a MUCHOS

    def __str__(self):
        return self.importeTotal + ' '+str(self.importeTotal) + ' '+str(self.totalConImpuesto) + ' '+ str(self.totalSinImpuestos)
    

class DetalleLiquidacionCompra(models.Model):
    cantidad = models.IntegerField(verbose_name="Cantidad")
    codigoAuxiliar = models.CharField(verbose_name="Código Auxiliar", max_length=50)
    codigoPrincipal = models.CharField(verbose_name="Código Principal", max_length=50)
    descripcion = models.TextField(verbose_name="Descripción")
    descuento = models.DecimalField(verbose_name="Descuento", max_digits = 10, decimal_places = 2)
    detalleAdicional = models.ForeignKey(DetalleAdicional, verbose_name="Detalle Adicional", on_delete=models.CASCADE) #DetalleAdicional --- Relacion de UNO a MUCHOS
    impuestos = models.ForeignKey(Impuesto, verbose_name="Impuesto", on_delete=models.CASCADE) #Impuesto --- Relacion de UNO a MUCHOS
    precioTotalSinImpuesto = models.DecimalField(verbose_name="Precio total Sin Impuesto", max_digits = 10, decimal_places = 2)
    precioUnitario = models.DecimalField(verbose_name="Precio Unitario", max_digits = 10, decimal_places = 2)

    def __str__(self):
        return str(self.cantidad) + ' '+self.codigoAuxiliar + ' '+ self.precioTotalSinImpuesto +' '+self.precioUnitario


class ImpuestoComprobanteRetencion(models.Model):
    baseImponible = models.DecimalField(verbose_name="Base Imponible", max_digits = 10, decimal_places = 2)
    codDocSustento = models.CharField(verbose_name="Código Doc. sustento", max_length=50)
    codigo = models.CharField(verbose_name="Código", max_length=50)
    codigoRetencion = models.CharField(verbose_name="Código Retención", max_length=50)
    fechaEmisionDocSustento = models.DateField(verbose_name="Fecha Emisión Doc. Sustento")
    numDocSustento = models.IntegerField(verbose_name="Número Doc. Sustento")
    porcentajeRetener = models.IntegerField(verbose_name="Porcentaje Retener")
    valorRetenido = models.DecimalField(verbose_name="Valor Retenido", max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.codigo + ' '+ str(self.porcentajeRetener) + ' ' + str(self.valorRetenido)


class ComprobanteRetencion(ComprobanteGeneral):
    identificacionSujetoRetenido = models.CharField(verbose_name="Identificación Sujeto Retenido", max_length=100)
    impuestos = models.ForeignKey(ImpuestoComprobanteRetencion, verbose_name="Impuestos", on_delete=models.CASCADE)#ImpuestoComprobanteRetencion --- Relacion de UNO a MUCHOS
    infoAdicional = models.OneToOneField(CampoAdicional, verbose_name="Campo Adicional", on_delete=models.CASCADE) #CampoAdicional --- Relacion UNO a UNO
    periodoFiscal = models.CharField(verbose_name="Periodo Fiscal", max_length=100)
    razonSocialSujetoRetenido = models.CharField(verbose_name="Razón Social Sujeto Retenido", max_length=100)
    tipoIdentificacionSujetoRetenido = models.CharField(verbose_name="Tipo Idrntificación Sujeto Retenido", max_length=50)

    def __str__(self):
        return self.identificacionSujetoRetenido + ' ' + self.periodoFiscal + ' ' + self.tipoIdentificacionSujetoRetenido 

class Motivo(models.Model):
    razon = models.CharField(verbose_name="Razón", max_length=100)
    valor = models.DecimalField(verbose_name="Valor", max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.razon + ' ' + str(self.valor)


class NotaDebito(ComprobanteGeneral):
    codDocModificado = models.CharField(verbose_name="Cod. Documento Modificado", max_length=50)
    fechaEmisionDocSustento = models.DateField(verbose_name="Fecha Emisión Doc. Sustento")
    identificacionComprador = models.CharField(verbose_name="Identificación Comprador", max_length=50)
    impuestos = models.ForeignKey(Impuesto, verbose_name="Impuesto", on_delete=models.CASCADE) #Impuesto --- Relacion UNO a MUCHOS
    infoAdicional = models.OneToOneField(CampoAdicional, verbose_name="Campo Adicional", on_delete=models.CASCADE) #CampoAdicional --- Relacion UNO a UNO
    motivos = models.OneToOneField(Motivo, verbose_name="Motivos", on_delete=models.CASCADE)#Motivo --- Relacion UNO a UNO
    numDocModificado = models.IntegerField(verbose_name="Número Doc. Modificado")
    razonSocialComprador = models.CharField(verbose_name="Razón Social Comprado", max_length=100)
    rise = models.CharField(verbose_name="RISE", max_length=50)
    tipoIdentificacionComprador = models.CharField(verbose_name="Tipo Identificación Comprador", max_length=50)
    totalSinImpuestos = models.DecimalField(verbose_name="Total Identificación Comprador", max_digits = 10, decimal_places = 2)
    valorTotal = models.DecimalField(verbose_name="Valor Total", max_digits = 10, decimal_places = 2)
    pagos = models.ForeignKey(Pagos, verbose_name="Pagos", on_delete=models.CASCADE)#Pagos --- Relacion de UNO a MUCHOS

    def __str__(self):
        return self.identificacionComprador + ' '+ self.rise + ' ' + str(self.valorTotal)

class DetalleNotaCredito(models.Model):
    cantidad = models.IntegerField(verbose_name="Cantidad")
    codigoAdicional = models.CharField(verbose_name="Código Adicional", max_length=50)
    codigoInterno = models.CharField(verbose_name="Código Interno", max_length=50)
    descripcion = models.TextField(verbose_name="Descripción")
    descuento = models.DecimalField(verbose_name="Descuento", max_digits = 10, decimal_places = 2)
    detallesAdicionales = models.ForeignKey(DetalleAdicional, verbose_name="Detalle Adicional", on_delete=models.CASCADE) #DetalleAdicional --- Relacion de UNO a MUCHOS
    impuestos = models.ForeignKey(Impuesto, verbose_name="Impuesto", on_delete=models.CASCADE)#Impuesto --- Relacion de UNO a MUCHOS
    precioTotalSinImpuesto = models.DecimalField(verbose_name="Precio Total Sin Impuesto", max_digits = 10, decimal_places = 2)
    precioUnitario = models.DecimalField(verbose_name="Precio Unitario", max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.cantidad +' '+ str(self.codigoAdicional) + ' ' + str(self.precioTotalSinImpuesto)

class NotaCredito(ComprobanteGeneral):
    codDocModificado = models.CharField(verbose_name="Código Doc. Modificado", max_length=50)
    detalles = models.ForeignKey(DetalleNotaCredito, verbose_name="Detalles", on_delete=models.CASCADE) #DetalleNotaCredito --- Relacion de UNO a MUCHOS
    fechaEmisionDocSustento = models.DateField(verbose_name="Fecha Emisión Doc. Sustento")
    identificacionComprador = models.CharField(verbose_name="Identificación Comprador", max_length=50)
    infoAdicional = models.OneToOneField(CampoAdicional, verbose_name="Campo Adicional", on_delete=models.CASCADE) #CampoAdicional --- Relacion UNO a UNO
    moneda = models.DecimalField(verbose_name="Moneda", max_digits = 10, decimal_places = 2)
    motivo = models.CharField(verbose_name="Motivo", max_length=100) 
    numDocModificado = models.IntegerField(verbose_name="Número Doc. Modificado")
    razonSocialComprador = models.CharField(verbose_name="Razón Social Comprador", max_length=100)
    rise = models.CharField(verbose_name="RISE", max_length=50)
    tipoIdentificacionComprador = models.CharField(verbose_name="Tipo Identificación Comprador", max_length=50)
    totalConImpuesto = models.OneToOneField(TotalImpuesto, verbose_name="Total Con Impuesto", on_delete=models.CASCADE) #TotalImpuesto --- Relacion UNO a UNO
    totalSinImpuestos = models.DecimalField(verbose_name="Total Sin Impuesto", max_digits = 10, decimal_places = 2)
    valorModificacion = models.DecimalField(verbose_name="Valor Modificación", max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.rise + ' ' + str(self.totalSinImpuestos) + ' ' +str(self.valorModificacion)


class ComprobantePendiente(models.Model):
    ambiente = models.CharField(verbose_name="Ambiente", max_length=100)
    codDoc = models.CharField(verbose_name="Código Documento", max_length=50)
    configAplicacion = models.OneToOneField(ConfigAplicacion, verbose_name="Configuración Aplicación", on_delete=models.CASCADE) #ConfigAplicacion --- UNO a UNO
    configCorreo = models.OneToOneField(ConfigCorreo, verbose_name="Configuración Correo", on_delete=models.CASCADE) #ConfigCorreo --- UNO a UNO
    establecimiento = models.CharField(verbose_name="Establecimiento", max_length=100)
    fechaEmision = models.DateField(verbose_name="Fecha Emisión")
    ptoEmision = models.CharField(verbose_name="Pto. Emisión", max_length=100)
    ruc = models.CharField(verbose_name="RUC", max_length=50)
    secuencial = models.CharField(verbose_name="Secuencial", max_length=100)
    tipoEmision = models.CharField(verbose_name="Tipo Emisión", max_length=100)
    clavAcc = models.CharField(verbose_name="Clave Acc", max_length=50)

    def __str__(self):
        return self.ambiente + ' ' + self.codDoc + ' ' + self.ruc

class procesarComprobantePendiente(models.Model):

    comprobantePendiente = models.OneToOneField(ComprobantePendiente, verbose_name="Comprobante Pendiente", on_delete=models.CASCADE) #ComprobantePendiente --- UNO a UNO

    def __str__(self):
        return self.comprobantePendiente
