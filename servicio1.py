import RPi.GPIO as GPIO
import time
import subprocess
import re
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT) #good recognition
GPIO.setup(17, GPIO.OUT) #always on
GPIO.setup(15, GPIO.OUT) #bad recognition

codigos_leidos=[]
patron=re.compile('[0-9]{2}_[0-9]{2}_[0-9]{6}')
try:
	cmdping = "zbarcam --prescale=10x10 --nodisplay /dev/video0"
	p = subprocess.Popen(cmdping, shell=True, stdout=subprocess.PIPE)
	while True:
		GPIO.output(17, True)
		GPIO.output(18, False)
		GPIO.output(15, False)
		out = p.stdout.readline()
		print "esta es ",out
		#if out == '' and p.poll() != None:
		if out == '' and p.poll() != None:
			break
		if out != '':
			#sys.stdout.write(out)
			#sys.stdout.flush()
			try:
				out2=out.split(":")
				print out2[1]
				if out2[1] not in codigos_leidos and patron.match(out2[1]):
					print "aqui se debe prender la luz, todo ok"
					GPIO.output(18, True)
					GPIO.output(17, False)
					codigos_leidos.append(out2[1])
				else:
					print "codigo repetido"
					print codigos_leidos
					GPIO.output(18, False)
					GPIO.output(17, False)
					GPIO.output(15, True)
			except:
				#print out
				GPIO.output(18, False)
				GPIO.output(17, False)
				GPIO.output(15, True)
				#pass
			time.sleep(1)
except Exception as e:
	print e
finally:
	GPIO.cleanup()
