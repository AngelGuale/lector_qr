import RPi.GPIO as GPIO
import time
import subprocess
import re
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
try:
	cmdping = "zbarcam --prescale=10x10 --nodisplay /dev/video0"
	p = subprocess.Popen(cmdping, shell=True, stderr=subprocess.PIPE)
	while True:
		GPIO.output(17, True)
		GPIO.output(18, False)
		out = p.stderr.read(1)
		if out == '' and p.poll() != None:
			break
		if out != '':
			#sys.stdout.write(out)
			#sys.stdout.flush()
			try:
				#out2=out.split(":")
				#print out2[1]
				pass
			except:
				print out
			print "aqui se debe prender la luz"
			GPIO.output(18, True)
			GPIO.output(17, False)
			time.sleep(1)
except Exception as e:
	print e
finally:
	GPIO.cleanup()
