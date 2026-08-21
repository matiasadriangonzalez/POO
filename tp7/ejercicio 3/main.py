from correo_local_oca import CorreoLocalOCA
from correo_internacional_fedex import CorreoInternacionalFedEx
from correo_regional_andreani import CorreoRegionalAndreani
from iexportable import IExportable

if __name__ == "__main__":
    oca = CorreoLocalOCA()
    fedex = CorreoInternacionalFedEx()
    andreani = CorreoRegionalAndreani()

    print(oca.calcular_costo(10))
    print(fedex.calcular_costo(10))
    print(fedex.rastrear_paquete_satelital())
    print(fedex.generar_reporte_aduana())
    print(andreani.rastrear_paquete_satelital())

    empresas = [oca, fedex, andreani]
    for empresa in empresas:
        if isinstance(empresa, IExportable):
            print(f"{empresa.__class__.__name__} puede exportar")
        else:
            print(f"{empresa.__class__.__name__} NO puede exportar")