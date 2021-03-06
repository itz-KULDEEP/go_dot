
import os
import sys


def is_active():
	return True

def get_name():
	return "OSX"

def can_build():

	if (sys.platform == "darwin" or os.environ.has_key("OSXCROSS_ROOT")):
		return True


	return False

def get_opts():

	return [
	    ('force_64_bits','Force 64 bits binary','no'),
	    ('osxcross_sdk','OSXCross SDK version','darwin14'),

	 ]

def get_flags():

	return [
	('legacygl', 'yes'),
	('builtin_zlib', 'no'),
	('freetype','builtin'), #use builtin freetype
	('glew', 'yes'),
	]



def configure(env):

	env.Append(CPPPATH=['#platform/osx'])

	if (env["bits"]=="default"):
	    env["bits"]="32"

	if (env["target"]=="release"):

		env.Append(CCFLAGS=['-O2','-ffast-math','-fomit-frame-pointer','-ftree-vectorize','-msse2'])

	elif (env["target"]=="release_debug"):

		env.Append(CCFLAGS=['-O2','-DDEBUG_ENABLED'])

	elif (env["target"]=="debug"):

		env.Append(CCFLAGS=['-g3', '-Wall','-DDEBUG_ENABLED','-DDEBUG_MEMORY_ENABLED'])


	if (env["freetype"]!="no"):
		env.Append(CCFLAGS=['-DFREETYPE_ENABLED'])
		env.Append(CPPPATH=['#tools/freetype'])
		env.Append(CPPPATH=['#tools/freetype/freetype/include'])



	if (not os.environ.has_key("OSXCROSS_ROOT")):
		#regular native build
		if (env["bits"]=="64"):
		    env.Append(CCFLAGS=['-arch', 'x86_64'])
		    env.Append(LINKFLAGS=['-arch', 'x86_64'])
		elif (env["bits"]=="32"):
		    env.Append(CCFLAGS=['-arch', 'i386'])
		    env.Append(LINKFLAGS=['-arch', 'i386'])
		else:
		    env.Append(CCFLAGS=['-arch', 'i386', '-arch', 'x86_64'])
		    env.Append(LINKFLAGS=['-arch', 'i386', '-arch', 'x86_64'])
	else:
		#osxcross build
		root=os.environ.get("OSXCROSS_ROOT",0)
		if env["bits"]=="64":
			basecmd=root+"/target/bin/x86_64-apple-"+env["osxcross_sdk"]+"-"
		else:
			basecmd=root+"/target/bin/i386-apple-"+env["osxcross_sdk"]+"-"


		env['CC'] = basecmd+"cc"
		env['CXX'] = basecmd+"c++"
		env['AR'] = basecmd+"ar"
		env['RANLIB'] = basecmd+"ranlib"
		env['AS'] = basecmd+"as"


#	env.Append(CPPPATH=['#platform/osx/include/freetype2', '#platform/osx/include'])
#	env.Append(LIBPATH=['#platform/osx/lib'])


	env.Append(CPPFLAGS=["-DAPPLE_STYLE_KEYS"])
	env.Append(CPPFLAGS=['-DUNIX_ENABLED','-DGLES2_ENABLED','-DOSX_ENABLED'])
	env.Append(LIBS=['pthread'])
	#env.Append(CPPFLAGS=['-F/Developer/SDKs/MacOSX10.4u.sdk/System/Library/Frameworks', '-isysroot', '/Developer/SDKs/MacOSX10.4u.sdk', '-mmacosx-version-min=10.4'])
	#env.Append(LINKFLAGS=['-mmacosx-version-min=10.4', '-isysroot', '/Developer/SDKs/MacOSX10.4u.sdk', '-Wl,-syslibroot,/Developer/SDKs/MacOSX10.4u.sdk'])
	env.Append(LINKFLAGS=['-framework', 'Cocoa', '-framework', 'Carbon', '-framework', 'OpenGL', '-framework', 'AGL', '-framework', 'AudioUnit','-lz'])

	if (env["CXX"]=="clang++"):
		env.Append(CPPFLAGS=['-DTYPED_METHOD_BIND'])
		env["CC"]="clang"
		env["LD"]="clang++"
		if (env["colored"]=="yes"):
			if sys.stdout.isatty():
				env.Append(CPPFLAGS=["-fcolor-diagnostics"])

	import methods

	env.Append( BUILDERS = { 'GLSL120' : env.Builder(action = methods.build_legacygl_headers, suffix = 'glsl.h',src_suffix = '.glsl') } )
	env.Append( BUILDERS = { 'GLSL' : env.Builder(action = methods.build_glsl_headers, suffix = 'glsl.h',src_suffix = '.glsl') } )
	env.Append( BUILDERS = { 'GLSL120GLES' : env.Builder(action = methods.build_gles2_headers, suffix = 'glsl.h',src_suffix = '.glsl') } )
	#env.Append( BUILDERS = { 'HLSL9' : env.Builder(action = methods.build_hlsl_dx9_headers, suffix = 'hlsl.h',src_suffix = '.hlsl') } )

	env["x86_opt_gcc"]=True
