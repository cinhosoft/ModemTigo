import serial
import time
import subprocess

def conexion_pppd(archivo_opciones, ind_abrir):
    comando_pppd = ""
    if(ind_abrir):
        comando_pppd = f"sudo pppd call {archivo_opciones}"
    else:
        comando_pppd = f"sudo poff {archivo_opciones}"

    try:
        subprocess.run(comando_pppd, shell=True, check=True)
        if(ind_abrir):
            print("Conexión establecida exitosamente.")
        else:
            print("Conexión cerrada exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al establecer la conexión PPP: {e}")

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

#for comando in comandos:
#    print("Enviando comando: " + comando.strip())
#    respuesta_modem = enviar_comando_at(puerto, comando)

# Ejemplo de uso
archivo_opciones_ppp = "gprs"  # Reemplaza con el nombre de tu archivo de opciones PPP
conexion_pppd(archivo_opciones_ppp, True) #Abrimos la conexion
##esto lo usamos para enviar el video
time.sleep(10) #dormimos 10 para ver que se activa la conexion
conexion_pppd(archivo_opciones_ppp, False) #Cerramos la conexion
time.sleep(5) #dormimos 5 para esperar que se libere el puerto
##Liberamos el puerto serie podemos enviar mensajes
#Vamos a enviar 1 mensaje
nCelular=1
celulares =[
    "+573246631576",
    "+573012608827" 
] 
comandos_sms = [
    'AT+CMGF=1', #configurar el modo de formato de mensaje (SMS) en un módem GSM (Global System for Mobile Communications). En particular, este comando establece el modo de formato de mensaje en modo texto.
    'AT+CSCS="GSM"', #activamos modo GSM
    'AT+CMGS="'+celulares[nCelular] +'"', #setteamos el numero de telefono
    'hola soy vigilant desde raspberry con python 14 noviembre 2023 12:23PM prueba mensaje a ' +celulares[nCelular]+' \032', #mensaje de prueba
]


for comando_sms in comandos_sms:
    print("Enviando comando: " + comando_sms.strip())
    respuesta_modem = enviar_comando_at(puerto, comando_sms)
