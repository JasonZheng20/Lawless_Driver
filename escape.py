import time
from subprocess import call
for i in range(10):
	call(["clear"])
	print(str(i))
	time.sleep(1)