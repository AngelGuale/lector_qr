import RPi.GPIO as GPIO
import time
import subprocess
import re
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT) #good recognition #LED verde para informar de codigo valido
GPIO.setup(17, GPIO.OUT) #always on # LED AMARILLO, INFORMA QUE EL DISPOSITIVO ESTÁ FUNCIONANDO
GPIO.setup(15, GPIO.OUT) #bad recognition # LED ROJO, INFORMA UN CODIGO NO VALIDO

codigos_leidos=[]#ALMACENA LOS CODIGOS QUE YA HAN SIDO VALIDADOS
patron=re.compile('[0-9]{1,2}_[0-9]{2}_[0-9]{6,12}') # EXPRESION REGULAR QUE VALIDA LOS CODIGO
try:
	cmdping = "zbarcam --prescale=10x10 --nodisplay /dev/video0"  # LLAMADA A LA FUNCION ZBARCAM QUE DETECTA CODIGO QR
	p = subprocess.Popen(cmdping, shell=True, stdout=subprocess.PIPE)
	while True:
		GPIO.output(17, True)  # LED AMARILLO ON
		GPIO.output(18, False) # LED VERDE OFF
		GPIO.output(15, False) #LED ROJO OFF
		out = p.stdout.readline()
		print "Salida del comando ",out
		if out == '' and p.poll() != None:
			break # si la salida del comando zbar es nula, repite el lazo
		if out != '': #se procesa la salida
			try:
				out2=out.split(":") # se obtiene el dato leido
				print out2[1]
				if out2[1] not in codigos_leidos and patron.match(out2[1]): # se valida el dato leido
					print "aqui se debe prender la luz, todo ok"
					GPIO.output(18, True) #LED VERDE ON
					GPIO.output(17, False) #LED AMARILLO OFF
					codigos_leidos.append(out2[1])
				else:
					print "codigo repetido"
					print codigos_leidos
					GPIO.output(18, False) #LED VERDE OFF
					GPIO.output(17, False) #LED AMARILLO OFF
					GPIO.output(15, True) #LED ROJO ON
			except:
				GPIO.output(18, False) #LED VERDE OFF
				GPIO.output(17, False) #LED AMARILLO OFF
				GPIO.output(15, True) #LED ROJO ON
			time.sleep(1)    # TIEMPO DE ENCENDIDO DE LOS LEDS
except Exception as e:
	print e
finally:
	GPIO.cleanup() #LINEA PARA APAGAR TODOS LOS LED SI OCURRE ALGUNA INTERRUPCION DEL PROGRAMA
