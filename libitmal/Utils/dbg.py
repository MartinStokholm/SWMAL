import inspect
import traceback
from sys import stdout, stderr
from os import getcwd
import numpy

from colors import Col, ColEnd

__g_diagnostics_stderr = stdout

def DiagStdErr(f=None):
	global __g_diagnostics_stderr
	if f is not None:
		__g_diagnostics_stderr = f
	assert __g_diagnostics_stderr is not None
	return __g_diagnostics_stderr

class Diagnostics:
	__g_diagnostics_debug_verbose_level = 0 # NOTE: dunno how to make a static class var yet!

	@staticmethod
	def SetDebugVerboseLevel(n):
		assert isInt(n)
		assert isInt(Diagnostics.__g_diagnostics_debug_verbose_level)
		Diagnostics.__g_diagnostics_debug_verbose_level = n

	@staticmethod
	def DebugVerboseLevel():
		assert isInt(Diagnostics.__g_diagnostics_debug_verbose_level)
		return Diagnostics.__g_diagnostics_debug_verbose_level

	@staticmethod
	def _EPrint(msg):
		stdout.flush()
		print(str(msg), file=DiagStdErr())
		stderr.flush()

	@staticmethod
	def _CurrFun(offset=4, decorate=False):
		st = inspect.stack()
		assert len(st)>0
		n = offset
		if n>=len(st):
			Diagnostics._EPrint("warning in _CurrFun(n=" + str(n) + ": index out-of-range for stackframe len=" + str(len(st)) + ", using last frame")
			n=len(st)-1

		f=st[n][1]
		assert isinstance(f, str)
		if decorate:
			f += "@" + str(st[n][2])
			t = ""
			for i in st[n][4]:
				t += str(i).replace("\\t","").replace("\\n","").replace("\r","").strip()
			f = Col("LPURPLE") + t + ColEnd() + "  " + f
		return f

	@staticmethod
	def _TerminalMaxLen(defaultlen=215):
		try:
			try:
				import fcntl, termios, struct
			except ImportError:
				Diagnostics._EPrint("import error, missing modules 'fcntl, termios or struct' in _TerminalMaxLen(), defaulting to width=" + str(defaultlen))
				return defaultlen
					
			_th, tw, _hp, _wp = struct.unpack("HHHH", fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack("HHHH", 0, 0, 0, 0)))
			if tw<32:
				return 32
			return tw #, th
		
		except:
			Diagnostics._EPrint("exception in _TerminalMaxLen(), defaulting to width=" + str(defaultlen))
			return defaultlen

	@staticmethod
	def _Pad(t, l):
		n = Diagnostics._Len(t)
		while n<l:
			t += " "
			n += 1
		return t

	@staticmethod
	def _Len(t):
		col=False
		n = 0
		p = 0
		for i in t:
			if i=='\033':
				assert not col
				col=True
			elif col and i=='m':
				col=False
			elif not col:
				#if not str(i).isprintable():
				# print("warning found whitespace=" + str(ord(i)) + " in string '" + str(t) + "' pos=" + str(p))
				n += 1
				p += 1
		assert n<=len(t) and not col
		return n

	@staticmethod
	def _Trunc(t, maxtermlen):
		assert maxtermlen>=2
		col=False
		r=""
		n=0
		for i in t:
			r += i
			if i=='\033':
				assert not col
				col=True
			elif col and i=='m':
				col=False
			elif not col:
				n += 1

			if n+3>maxtermlen and not col:
				r += "."
				r += "."
				break

		assert Diagnostics._Len(r)<=maxtermlen and not col
		return r

	@staticmethod
	def Stacktrace(fullfilename=False, st=None, cut=-1):

		def _MkFile(f, fullfilename):
			if fullfilename:
				currdir =  str(getcwd()) + "/"
				n = f.find(currdir)
				if n>=0:
					f = f[len(currdir):]
			else:
				n=f.rfind('/')
				f=f if n<0 else f[n+1:]
			if len(f)>2 and f[0:2]=="./":
				f = f[2:]
			assert len(f) > 0
			return f

		def _MkSrc(stackframe, fullfilename):
			return "  " + Col('GREEN') + str(_MkFile(stackframe[1], fullfilename)) + Col('BLUE') + ":" + str(stackframe[2]) + ":" + ColEnd()

		def _MkModule(stackframe):
			return str(stackframe[3].strip()) + "(x)"

		def _Filter(l):
			t = ""
			for i in l:
				t += i.replace("\t","").replace("\n","")
			return "'" + t + "'"

		if st is None:
			st = inspect.stack()

		assert not st is None

		if len(st)<cut:
			cut = -1

		maxtermlen=Diagnostics._TerminalMaxLen()
		maxlen0 = -1
		maxlen1 = -1

		n = 0
		for stackframe in st:
			if n<cut:
				continue
			maxlen0 = max(maxlen0, Diagnostics._Len(_MkSrc(stackframe, fullfilename)))
			maxlen1 = max(maxlen1, Diagnostics._Len(_MkModule(stackframe)))

		t = []
		n = 0
		for stackframe in st:
			n += 1
			if n<cut:
				continue

			src = Diagnostics._Pad(_MkSrc(stackframe, fullfilename), maxlen0)
			msg = Diagnostics._Pad(str(src) + str(_MkModule(stackframe)), maxlen0+maxlen1+2)
			msg += Col('PURPLE') + str(_Filter(stackframe[4]))
			msg = Diagnostics._Trunc(msg, maxtermlen)

			t.append(msg + ColEnd())

		r = ""
		for i in reversed(t):
			r += str(i) + "\n"

		return r

	@staticmethod
	def __PrettyPrintTraceback(ex):
		try:
			r = Col('UNDERLINE, LYELLOW') + "STACKTRACE:" + ColEnd() + "\n"
			r += Diagnostics.Stacktrace(True)
			r += "\n" + Col('RED') + "EXCEPTION:\n  " + Col('UNDERLINE, LRED') + str(ex) + ColEnd()
			Diagnostics._EPrint(r)
			return r
		except Exception as e:
			WARN(e)
		try:
			tb = traceback.format_exc()
			return str(tb)
		except:
			WARN("cannot produce trace, and can not use fallback method")
			return "N/A"

	@staticmethod
	def PrettyPrintTraceback(_ex):
		def _Filter(text):
			try:
				#def Pad(text, n):
				#	while len(text)<n:
				#		text = text + " "
				#	return text
					#
				#def Trunc(text, maxlen=Diagnostics._TerminalMaxLen()):
				#	assert maxlen>2
				#	if len(text)>maxlen:
				#		return text[0:maxlen-2] + ".."
				#	return text

				def FiltPwd(filename):
					prefix = filename[0:8]
					#print("'" + str(prefix) + "'"")
					if prefix=='  File "':
						currdir = getcwd()
						n = len(currdir)
						#print("currdir=" + str(currdir) + ", filename=" + str(filename[0:n]))
						if filename[8:n+8] == currdir:
							return '  File "' + filename[n+8+1:]
					return filename

				maxtermlen=Diagnostics._TerminalMaxLen()
				maxlen = -1

				for n in range(2):
					r = Col('UNDERLINE, BOLD, RED') + "EXCEPTION OCCURED:" + ColEnd()
					s = text.split('\n')
					j = 0
					for i in s:
						t = ""
						if j==0:
							#t = "  " + str(i) + "\n"
							t = "\n"
						elif j+2==len(s):
							t = Col('LRED') + str(i) + ColEnd() + "\n"
						elif j+1==len(s):
							assert i==""
						elif i.find('File "')>=0:
							ii = i
							linetag = '", line '
							m = ii.find(linetag)
							if  m>=0:
								ii = FiltPwd(ii[0:m]) + Col('BLUE') + str(linetag) + ii[m+len(linetag):]
							t =  Col('CYAN') + str(ii) + ColEnd()
							if n==0:
								maxlen = len(t) if len(t)>maxlen else maxlen
							else:
								t = Diagnostics._Pad(t, maxlen)
						else:
							t = "  " + Col('PURPLE') + str(i) + ColEnd() + "\n"

						r += t
						j += 1

				rfilt = "\n"
				s =  r.split("\n")
				for i in s[0:-2]:
					rfilt += Diagnostics._Trunc(i, maxtermlen) + "\n"
				rfilt += "\n" + Diagnostics._Trunc(s[-2], maxtermlen) + "\n" + Diagnostics._Trunc(s[-1], maxtermlen)

				return rfilt
			except Exception as e:
				WARN(e)
				return text # fallback

		tb = traceback.format_exc() #print(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))
		msg = _Filter(tb)
		Diagnostics._EPrint(msg)
		return msg

	@staticmethod
	def Err(msg, printstack=True, willfail=True):
		Diagnostics._EPrint(Col('FAIL, BOLD, UNDERLINE') + "ERROR:" + ColEnd() + " " + Col('FAIL') + str(msg) + ColEnd())
		if printstack:
			Diagnostics._EPrint(Diagnostics.Stacktrace())
		if willfail:
			raise Exception(msg)

	@staticmethod
	def Warn(msg, printstack=False):
		Diagnostics._EPrint(Col('WARNING, BOLD, UNDERLINE') + "WARNING:" + ColEnd() + " " + Col('WARNING') + str(msg) + ColEnd())
		if printstack:
			Diagnostics._EPrint(Diagnostics.Stacktrace())

	@staticmethod
	def Dbg(msg, level, indent, printstack=False):
		if level<Diagnostics.__g_diagnostics_debug_verbose_level:
			Diagnostics._EPrint(Col('GREEN, BOLD') + "DBG:" + ColEnd() + " " + str(indent) + str(msg))
			if printstack:
				Diagnostics._EPrint(Diagnostics.Stacktrace())

	@staticmethod
	def Fun(msg, level, printstack=False, decorate=False):
		if level<2:
			Diagnostics._EPrint(Col('BLUE, BOLD') + "FUN:" + ColEnd() + " " + str(Diagnostics._CurrFun(decorate=True)) + str(msg))
			if printstack:
				Diagnostics._EPrint(Diagnostics.Stacktrace())

	@staticmethod
	def _isType(t, expected_type, report_errors=True):
		if _g_optimization_enabled:
			return True

		if isNone(t):
			ERR("got 'None' object, can not continue")
		if str(type(expected_type)) != "<class 'str'>":
			ERR("expected excepted type to be of str in Diagnostics._isType(), got '" + str(type(expected_type)) + "'")
		s = str(type(t))
		e = "<class '" + str(expected_type) + "'>"
		if s==e:
			return True
		if report_errors:
			msg = "N/A"
			try:
				msg = str(t)
			except:
				msg = "N/A"
			ERR("Diagnostics._isType(" + str(msg) + ", " + str(expected_type) + "), found type '" + str(s) + "' but expected '" + str(e) + "'")
		return False

	@staticmethod
	def isInstance(t, expected_type, report_errors=True):
		if _g_optimization_enabled:
			return True

		if isNone(t):
			ERR("got 'None' object, can not continue")

		if isinstance(t, expected_type):
			return True

		if report_errors:
			msg = "N/A"
			s   = "N/A"
			#e   = "N/A"
			try:
				msg = str(t)
				s = str(type(t))
				#e = str(type(expected_type))
			except:
				msg = "N/A"
			ERR("Diagnostics._isType(" + str(msg) + ", " + str(expected_type) + "), found type '" + str(s) + "' but expected '" + str(expected_type) + "'")

		return False

def OptimizationOn():
	OO=True
	try:
		assert False
	except:
		OO=False
	if OO:
		WARN("OptimizationOn() => optimization=" + str(OO) )
	return OO

_g_optimization_enabled=OptimizationOn()

def PrettyPrintTracebackDiagnostics(ex):
	return Diagnostics.PrettyPrintTraceback(ex)

def DbgLevel():
	return Diagnostics.DebugVerboseLevel()

def SetDbgLevel(n):
	Diagnostics.SetDebugVerboseLevel(n)

_g_handler_err=None
_g_handler_warn=None

def SetHandlerErr(f):
	global _g_handler_err
	assert isFunction(f) or f is None
	r=_g_handler_err
	_g_handler_err=f
	return r

def SetHandlerWarn(f):
	global _g_handler_warn
	assert isFunction(f) or f is None
	r=_g_handler_warn
	_g_handler_warn=f
	return r

def ERR(msg):
	global _g_handler_err
	r=Diagnostics.Err(msg)
	if _g_handler_err is not None:
		assert isFunction(_g_handler_err)
		_g_handler_err(msg)
	return r

def WARN(msg):
	global _g_handler_warn
	r=Diagnostics.Warn(msg)
	if _g_handler_warn is not None:
		assert isFunction(_g_handler_warn)
		_g_handler_warn(msg)
	return r

def DBG(msg, level=0, indent=" "):
	return Diagnostics.Dbg(msg, level, indent)

def FUN(msg="", level=1):
	return Diagnostics.Fun(msg, level, decorate=True)

def StatusMessage(r):
	isInt(r)
	if r==0:
		return "[  " + Col('GREEN') + "OK" + ColEnd() + "  ]"
	elif r<0:
		return "[" + Col('LRED')  + "FAILED" + ColEnd() + "]"
	elif r>0:
		return "[ " + Col('YELLOW') + "WARN" + ColEnd() + " ]"
	else:
		assert False

def isNone(t):
	return not t is not None
def isBool(t):
	return Diagnostics.isInstance(t, bool)
def isInt(t, expected_min=None):
	return Diagnostics.isInstance(t, int) and (isNone(expected_min) or t>=expected_min)
def isNatural(t):
	return isInt(t, 0)
def isPositive(t):
	return isInt(t, 1)
def isFloat(t):
	return Diagnostics.isInstance(t, float)
def isStr(t, checknonempty=True):
	return Diagnostics.isInstance(t, str)   and (not checknonempty or len(t)>0)
def isTuple(t, expected_len=-1):
	return Diagnostics.isInstance(t, tuple) and (expected_len<0 or expected_len==len(t))
def isList(t, expected_len=-1):
	return Diagnostics.isInstance(t, list)  and (expected_len<0 or expected_len==len(t))
def isDict(t, expected_len=-1):
	return Diagnostics.isInstance(t, dict)  and (expected_len<0 or expected_len==len(t))
def isNumpyNdarray(t, expected_ndim=-1, expected_shape=None):
	return Diagnostics.isInstance(t, numpy.ndarray) and (expected_ndim<0 or expected_ndim==t.ndim) and expected_shape in (None, t.shape)
def isNp(t, expected_ndim=-1, expected_shape=None):
	return isNumpyNdarray(t, expected_ndim, expected_shape)
#def isImg(t, expected_ndim=3, expected_shape=None):
#	return isNumpyNdarray(t, expected_ndim, expected_shape)
def isLabel(t, selfcheck=True):
	return Diagnostics._isType(t, "Utils.labelfuns.Label")  #and (not selfcheck or t.isOk())
def isLabels(t, selfcheck=True, expected_len=-1):
	return Diagnostics._isType(t, "Utils.labelfuns.Labels") and (not selfcheck or t.isOk()) and (expected_len<0 or expected_len==len(t))
def isFilter(t, selfcheck=True):
	return Diagnostics._isType(t, "Utils.labelfuns.Filter") and (not selfcheck or t.isOk())
def isFunction(t):
	return hasattr(t, "__call__") # or callable(obj)

def isType(t, expected_type):
	assert isStr(expected_type)
	return Diagnostics._isType(t, expected_type)
	
	
def Bool(t):
	assert isBool(t)
	return t
def Int(t, expected_min=None):
	assert isInt(t, expected_min)
	return t
def Natural(t):
	assert isNatural(t)
	return t
def Str(t, checknonempty=True):
	assert isStr(t, checknonempty)
	return t
def Float(t):
	assert isFloat(t)
	return t
def List(t, expected_len=-1):
	assert isList(t, expected_len)
	return t