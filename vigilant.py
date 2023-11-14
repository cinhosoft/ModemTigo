import serial
import time

def enviar_comando_at(puerto_serie, comando):
    try:
        # Abrir la conexión con el puerto serie
        with serial.Serial(puerto_serie, baudrate=115200, timeout=2.0) as ser:
            print(f"Conexión con el puerto serie ({puerto_serie}) exitosa.")
            
            #Agregamos retorno de carro y nueva linea al comando
            
            #Codificamos el comando a utf-8
            comando +='\r\n'
            comando_utf= comando.encode(encoding='utf-8', errors = 'strict')
            # Envía el comando AT al módem
            ser.write(comando_utf)
            print(f"Enviando comando AT: {comando_utf}")

            # Espera para dar tiempo al módem para procesar el comando y enviar la respuesta
            time.sleep(1)

            # Lee la respuesta del módem
            respuesta = ser.read(1024).decode()
            print(f"Respuesta del módem: {respuesta}")

            return respuesta

    except serial.SerialException as e:
        print(f"Error de puerto serie: {str(e)}")
        return None

puerto = '/dev/ttyUSB0'
# Comandos AT para la activación de la conexión PPP
comandos = [
    'ATZ',        # Restablecer el módem
    'AT+CGDCONT=1,\"IP\",\"internet.comcel.com.co\"',  # Configurar APN
    'ATD*99#',    # Iniciar la conexión PPP
    # Agrega comandos adicionales si es necesario para la autenticación
    # Ejemplo: "AT+CGAUTH=1,1,\"TuNombreDeUsuario\",\"TuContraseña\"\r"
]

for comando in comandos:
    print("Enviando comando: " + comando.strip())
    respuesta_modem = enviar_comando_at(puerto, comando)
