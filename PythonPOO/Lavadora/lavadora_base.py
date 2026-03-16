import time
import os
from datetime import datetime
import winsound

class LavadoraBase:
    def __init__(self, kilos, tipo_ropa, estrato):
        # Atributos protegidos para asegurar el encapsulamiento de datos
        self._kilos = kilos                 
        self._tipo_ropa = tipo_ropa.lower() 
        self.__estado = "apagada"           
        self._tiempo_lavado = 30            
        self._precio_kilo = 10000           
        self._iva = 0.19                    
        self._potencia_kw = 1.5             
        self._estrato = estrato             
        
        # Variables de instancia para el almacenamiento de resultados financieros
        self.costo_base = 0
        self.costo_aumentado = 0
        self.costo_iva = 0
        self.energia_total = 0

    def _play_audio(self, nombre_archivo, asincrono=True):
        # Gestion de reproduccion de audio con manejo de excepciones
        try:
            ruta_carpeta = os.path.dirname(__file__)
            ruta_audio = os.path.join(ruta_carpeta, "Sound", nombre_archivo)
            modo = winsound.SND_FILENAME | winsound.SND_NODEFAULT
            if asincrono:
                modo |= winsound.SND_ASYNC
            winsound.PlaySound(ruta_audio, modo)
        except Exception:
            pass

    def _detener_audio(self):
        # Interrupcion inmediata de cualquier flujo de audio activo
        winsound.PlaySound(None, winsound.SND_PURGE)

    def _barra_progreso(self, proceso, segundos, con_sonido=None):
        # Sincronizacion de animacion visual y audio mediante hilos de ejecucion
        if con_sonido:
            self._play_audio(con_sonido)
        
        print(f"\n{proceso}:")
        bar_size = 20
        for i in range(bar_size + 1):
            porcentaje = (i * 100) // bar_size
            relleno = "#" * i
            espacios = "-" * (bar_size - i)
            # Retorno de carro (\r) para actualizacion dinamica de la terminal
            print(f"\r[{relleno}{espacios}] {porcentaje}%", end="")
            time.sleep(segundos / bar_size)
        
        print(" [COMPLETADO]")
        # Garantiza que el sonido cese exactamente al finalizar la barra
        if con_sonido:
            self._detener_audio()

    def encender(self):
        self.__estado = "encendida"
        print("\n--- INICIALIZANDO HARDWARE LAVA SMART ---")
        self._play_audio("encendido.wav", asincrono=False) 

    def _llenar(self):
        self._barra_progreso("Proceso de llenado", 4, "llenado.wav")

    def estregar(self):
        self._barra_progreso("Proceso de estregado", 5, "lavado.wav")

    def enjuagar(self):
        self._barra_progreso("Proceso de enjuague", 4, "enjuague.wav")

    def centrifugar(self):
        self._barra_progreso("Proceso de centrifugado", 4, "centrifugar.wav")

    def secar(self):
        self._barra_progreso("Proceso de secado termico", 6, "secado.wav")

    def lavar(self):
        pass

    def _calcular_costos(self):
        self.costo_base = self._kilos * self._precio_kilo
        prendas_especiales = ["interior", "pijamas", "vestidos"]
        if self._tipo_ropa in prendas_especiales:
            self.costo_aumentado = self.costo_base * 1.05
        else:
            self.costo_aumentado = self.costo_base
        self.costo_iva = self.costo_aumentado * 1.19

    def _calcular_consumo_energia(self):
        kwh_operacion = self._potencia_kw * (self._tiempo_lavado / 60)
        tarifas = {2: 867.8, 3: 737.6, 4: 867.8, 5: 1041.0}
        tarifa_estrato = tarifas.get(self._estrato, 800)
        self.energia_total = kwh_operacion * tarifa_estrato
        # Notificacion auditiva previa a la generacion del reporte
        self._play_audio("final.wav", asincrono=False)

    def obtener_datos_reporte(self, nombre_cliente, modo):
        return {
            "Fecha_Hora": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "Cliente": nombre_cliente,
            "Modo": modo,
            "Carga_KG": self._kilos,
            "Tipo_Ropa": self._tipo_ropa,
            "Total_Pago": round(self.costo_iva, 2),
            "Consumo_Energia": round(self.energia_total, 2)
        }

    def ciclo_terminado(self, nombre_cliente, modo):
        self._calcular_costos()
        self._calcular_consumo_energia()
        
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("\n" + "="*40)
        print("       REPORTE TECNICO DE SERVICIO")
        print("="*40)
        print(f"Fecha/Hora:    {ahora}")
        print(f"Cliente:       {nombre_cliente}")
        print(f"Modalidad:     {modo}")
        print(f"Peso Carga:    {self._kilos} KG")
        print(f"Tipo Ropa:     {self._tipo_ropa.capitalize()}")
        print(f"Consumo Elec:  ${self.energia_total:,.2f}")
        print("-" * 40)
        print(f"TOTAL A PAGAR: ${self.costo_iva:,.2f}")
        print("="*40)