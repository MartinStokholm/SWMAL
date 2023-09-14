#!/usr/bin/env python3
     
def RestartKernel() :
	try:
		from IPython.display import display_html
		display_html("<script>Jupyter.notebook.kernel.restart()</script>",raw=True)
	except:
		print("ERROR in RestartKernel()!")		

def ResetSeeds(seed=42):
	import numpy as np
	import tensorflow as tf
	import random as python_random
	
	from os import environ
	environ['PYTHONHASHSEED']=str(seed)
	
	np.random.seed(seed) 
	python_random.seed(seed)
	tf.random.set_seed(seed)

def DisableGPUs():
	import os
	os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
	#try:
	#	# Disable all GPUS
	#	tf.config.set_visible_devices([], 'GPU')
	#	visible_devices = tf.config.get_visible_devices()
	#	for device in visible_devices:
	#		assert device.device_type != 'GPU'
	#except:
	#	# Invalid device or cannot modify virtual devices once initialized.
	#	WARN("exception in DisableGPUs() ignored")

def ReEnableGPUs():
	# if DisableGPUs() was called, you can re-enable GPUS via this function
	import os
	os.environ["CUDA_VISIBLE_DEVICES"] = "" 

def StartupSequence_GPU(verbose=False):
	n = -1
	if verbose:
		print("StartupSequence_GPU()..")
	try:
		import tensorflow

		physical_devices = tensorflow.config.list_physical_devices('GPU')
		n = 0
		for i in range(len(physical_devices)):
			if verbose:
				print(f"  setting physical_devices[{i}] set_memory_growth=True..")
			tensorflow.config.experimental.set_memory_growth(physical_devices[i], True)
			n += 1
			
	except Exception as e:
		if (verbose):
			print(f"ERROR: something failed in StartupSequence_EnableGPU(), re-raising exception='{e}'\n")
		raise e
	
	assert n > -1, f"something went wrong in startup-sequence, n={n} should be > -1"	
	return n

########################################

def TestAll():
	print("(not tests yet)")
	print("ALL OK")

if __name__ == '__main__':
	TestAll()

#Versions()
#ResetSeeds()
#DisableGPUs()
#StartupSequence_GPU(verbose=False)