def ColMap():
	# Black        0;30     Dark Gray     1;30
	# Red          0;31     Light Red     1;31
	# Green        0;32     Light Green   1;32
	# Brown/Orange 0;33     Yellow        1;33
	# Blue         0;34     Light Blue    1;34
	# Purple       0;35     Light Purple  1;35
	# Cyan         0;36     Light Cyan    1;36
	# Light Gray   0;37     White         1;37

	BLUE     ="\033[0;34m"
	LBLUE    ="\033[1;34m"
	RED      ="\033[0;31m"
	LRED     ="\033[1;31m"
	GREEN    ="\033[0;32m"
	LGREEN   ="\033[1;32m"
	YELLOW   ="\033[0;33m"
	LYELLOW  ="\033[1;33m"
	PURPLE   ="\033[0;35m"
	LPURPLE  ="\033[1;35m"
	CYAN     ="\033[0;36m"
	LCYAN    ="\033[1;36m"
	NC       ="\033[0m"

	#HEADER   ="\033[95m"
	#OKBLUE   =BLUE
	#OKGREEN  =GREEN
	WARNING  ="\033[93m"
	FAIL     =RED
	#ENDC     =NC

	BOLD     ="\033[1m"
	UNDERLINE="\033[4m"

	d = {
		"blue"     : BLUE,
		"lblue"    : LBLUE,
		"red"      : RED,
		"lred"     : LRED,
		"green"    : GREEN,
		"lgreen"   : LGREEN,
		"yellow"   : YELLOW,
		"lyellow"  : LYELLOW,
		"purple"   : PURPLE,
		"lpurple"  : LPURPLE,
		"cyan"     : CYAN,
		"lcyan"    : LCYAN,
		"nc"       : NC,
		#"header"   : HEADER,
		#"okblue"   : OKBLUE,
		#"okgreen"  : OKGREEN,
		"warning"  : WARNING,
		"fail"     : FAIL,
		#"endc"     : NC,
		"bold"     : BOLD,
		"underline": UNDERLINE
	}

	return d

def Col(colors, quieterror=False):
	assert isinstance(colors, str)
	assert isinstance(quieterror, bool)
	
	d = ColMap()
	keys = colors.lower().split()
	r = ""
	for i in keys:
		key = i.strip(',').strip()
		if key in d:
			r += d[key]
		elif not quieterror:
			raise ValueError("no such col='"+str(key)+"' (in parameter colors='"+str(colors)+"') in colormap")
		
	return r

def ColEnd():
	return Col("NC")
