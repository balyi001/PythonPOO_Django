from lavadora_base import LavadoraBase

class LavadoraEstandar(LavadoraBase):
    # Clase especializada en el flujo de trabajo convencional
    def lavar(self):
        print("Ejecutando protocolo de lavado estandar...")