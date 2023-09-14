#!/usr/bin/env python3

def Versions():
	def PrintVer(libname, version):
		print(f"{str(libname) + ' version:':28s} {version}")

	def TryImport(libname):
		import importlib
		import sys
		try:
			lib = importlib.import_module(libname)
			PrintVer(libname, f"{lib.__version__}")
		except ModuleNotFoundError:
			print(f"WARNING: could not find library '{libname}' in path", file=sys.stderr)

	import sys
	PrintVer("Python", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

	TryImport("numpy")
	TryImport("sklearn")
	TryImport("keras")
	TryImport("tensorflow")
	TryImport("tensorflow.keras")
	TryImport("cv2")
	TryImport("pytorch")

def TestAll():
	print("Test versions..")
	Versions()
	print("ALL OK")

if __name__ == '__main__':
	TestAll()