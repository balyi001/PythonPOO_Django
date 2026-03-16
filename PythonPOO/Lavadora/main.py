import pandas as pd
import random
import os
from datetime import datetime
from lavadora_estandar import LavadoraEstandar
from lavadora_inteligente import LavadoraInteligente

class SistemaLavaSmart:
    def __init__(self):
        self.historial_servicios = []

    def solicitar_dato(self, mensaje, tipo, validacion=None):
        while True:
            try:
                dato = input(f"{mensaje} (o escriba 'OFF' para cancelar): ")
                if dato.upper() == "OFF": return "CANCELAR"
                valor = tipo(dato)
                if validacion and not validacion(valor):
                    print("Dato fuera de los parametros establecidos.")
                    continue
                return valor
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nError: Entrada de datos invalida.")

    def ejecutar(self):
        try:
            print("\n" + "*"*36)
            print("   GESTION ADMINISTRATIVA LAVA SMART")
            print("*"*36)
            nombre_cli = input("Nombre del cliente: ")
            
            print("\nSeleccione modalidad:")
            print("1. Lavadora Estandar")
            print("2. Lavadora Inteligente (Sensores)")
            sel = self.solicitar_dato("Seleccion", int, lambda x: x in [1, 2])
            if sel == "CANCELAR": return

            if sel == 2:
                kilos = round(random.uniform(5, 40), 1)
                prenda = random.choice(["interior", "pijamas", "vestidos", "otra"])
                modo_texto = "Inteligente"
                print(f"\n[SENSORES]: Peso: {kilos}kg | Prenda: {prenda}")
            else:
                kilos = self.solicitar_dato("Peso (5-40)", float, lambda x: 5 <= x <= 40)
                if kilos == "CANCELAR": return
                opciones = {1: "interior", 2: "pijamas", 3: "vestidos", 4: "otra"}
                print("\nTipos de prenda:")
                for k, v in opciones.items(): print(f"{k}. {v}")
                idx = self.solicitar_dato("Opcion", int, lambda x: x in opciones)
                if idx == "CANCELAR": return
                prenda = opciones[idx]
                modo_texto = "Estandar"

            estrato = self.solicitar_dato("Estrato (2-5)", int, lambda x: 2 <= x <= 5)
            if estrato == "CANCELAR": return

            equipo = LavadoraEstandar(kilos, prenda, estrato) if sel == 1 else LavadoraInteligente(kilos, prenda, estrato)
            
            equipo.encender()
            if sel == 2: equipo.detectar_tipo_ropa()
            
            equipo._llenar()
            equipo.estregar()
            equipo.lavar()
            equipo.enjuagar()
            equipo.centrifugar()
            
            while True:
                sec = input("\n¿Ejecutar secado termico? (s/n): ").lower()
                if sec in ['s', 'si', 'n', 'no']: break
                print("Entrada no reconocida. Ingrese 's' o 'n'.")
            
            if sec in ['s', 'si']:
                equipo.secar()

            equipo.ciclo_terminado(nombre_cli, modo_texto)
            self.historial_servicios.append(equipo.obtener_datos_reporte(nombre_cli, modo_texto))
            
            if isinstance(equipo, LavadoraInteligente):
                equipo.conectar_wifi()

        except (KeyboardInterrupt, EOFError):
            print("\nOperacion interrumpida por el usuario.")

    def finalizar_jornada(self):
        # Procedimiento de persistencia de datos en directorio especifico
        if self.historial_servicios:
            try:
                # Definicion del nombre de la carpeta de destino
                nombre_dir = "Lavadora/Reportes_Servicio"
                
                # Creacion automatica del directorio si no existe en el sistema
                if not os.path.exists(nombre_dir):
                    os.makedirs(nombre_dir)
                    print(f"\n[SISTEMA]: Directorio '{nombre_dir}' creado exitosamente.")
                
                # Preparacion del DataFrame y generacion de nombre con estampa de tiempo
                df = pd.DataFrame(self.historial_servicios)
                stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_archivo = f"Reporte_{stamp}.xlsx"
                
                # Construccion de la ruta absoluta para el guardado
                ruta_final = os.path.join(nombre_dir, nombre_archivo)

                # Exportacion de datos utilizando el motor openpyxl
                df.to_excel(ruta_final, index=False, engine='openpyxl')
                print(f"\n[SISTEMA]: Registro de jornada exportado en: {ruta_final}")
                
            except Exception as e:
                print(f"\n[SISTEMA]: Fallo en la persistencia de datos: {e}")

if __name__ == "__main__":
    app = SistemaLavaSmart()
    while True:
        app.ejecutar()
        
        while True:
            try:
                continuar = input("\n¿Atender nuevo servicio? (s/n): ").lower()
                if continuar in ['s', 'si']:
                    break 
                elif continuar in ['n', 'no']:
                    app.finalizar_jornada()
                    print("Finalizando sesion administrativa.")
                    exit() 
                else:
                    print("Comando invalido. Use 's' para continuar o 'n' para finalizar.")
            except (KeyboardInterrupt, EOFError):
                print("\nUse 'n' para cerrar el programa de forma segura.")