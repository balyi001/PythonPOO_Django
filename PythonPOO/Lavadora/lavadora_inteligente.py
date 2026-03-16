from lavadora_base import LavadoraBase

class LavadoraInteligente(LavadoraBase):
    # Clase con implementacion de hardware simulado y conectividad
    def __init__(self, kilos, tipo_ropa, estrato):
        super().__init__(kilos, tipo_ropa, estrato)
        self._wifi = True
        self._sensores = True

    def detectar_tipo_ropa(self):
        # Simulacion de telemetria mediante sensores de tejido
        print(f"Sensores: Identificando densidad textil de {self._tipo_ropa}...")

    def conectar_wifi(self):
        # Procedimiento de enlace de datos con la red local
        print("Conexion WiFi: Sincronizando datos con el servidor central.")

    def lavar(self):
        # Implementacion del principio de Polimorfismo para lavado optimizado
        print("Ejecutando protocolo inteligente con ahorro de agua...")