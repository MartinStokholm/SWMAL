#!/usr/bin/env python3

import subprocess 
#from Utils.dbg import ERR

#subprocess.run(["ls", "-l"])  # doesn't capture output
#CompletedProcess(args=['ls', '-l'], returncode=0)
#subprocess.run("exit 1", shell=True, check=True)

#def SysCallPrimitive(cmd, quiet=False, debug=False, checkretval=False):
#	try:
#		o = subprocess.getstatusoutput(cmd)
#		
#		retval = o[0]
#		output = o[1].split("\n")
#
#		assert isinstance(retval, int)
#		assert isinstance(output, list)
#		
#		for i in output:
#			assert isinstance(i, str)
#				
#		if not quiet:
#			print("> " + cmd + " => retval=" + str(retval))
#			for i in output:
#					assert isinstance(i, str)
#					print("  " + i)
#
#		if checkretval and retval!=0:
#			ERR(f"encountered retval!=0 in SysCallPrimitive(cmd='{cmd}', ..) {o[1]}")
#			
#		return output, retval
#	except Exception as e:
#		ERR(f"encountered unexpected exceptionion SysCallPrimitive(cmd='{cmd}', ..), exception='{e}'")
		
def Shell(cmd, quiet=False, verbose=True, shell=True):
	def TrimOutput(out):
		assert isinstance(out, str)
		n = len(out)
		if n>0 and out[:n-1]=='\n':
			return TrimOutput(out[0:n-1])
		else:
			return out
				
	assert isinstance(cmd, str)
	args = cmd.split(" ")
	if verbose:
		print(f"SHELL: {args}..")
		
	o = subprocess.run(args, capture_output=True, text=True, shell=shell)
	print(o)
	r = o.returncode
	stdout = TrimOutput(o.stdout)
	stderr = TrimOutput(o.stderr)

	assert isinstance(r, int)
	assert isinstance(stdout, str)
	assert isinstance(stderr, str)
	
	if not quiet:
		print(f"stdout: '{stdout}'")
		print(f"stderr: '{stderr}'")
	
	if verbose:
		print(f"SHELL: returncode={r}")

	return r, stdout, stderr

if __name__=='__main__':
	try:
		r = Shell("dir | grep dir", quiet=True, verbose=False)
		print(r[1])
		
		#SysCallPrimitive("ls -l | grep dir")
	except Exception as ex:
		#Diagnostics.PrettyPrintTraceback(ex)
		print("EXCEPTION: {ex}", file=std.err)
		exit(-1)
