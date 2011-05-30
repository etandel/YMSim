import sys
from re import match
import os

###########==Begin definitions==##########



def get_yesorno(question):
	cont = match("(y|n)", raw_input(question).lower())
	while not cont:
		print("Invalid input. 'y' or 'n' only.")
		cont = match("(y|n)", raw_input(question).lower())
	cont = cont.group(1)
	if cont == 'n':
		return False
	else:
		return True


def create_header(path_from_main, import_string):
	with open(os.path.join(PROJECT_DIR, path_from_main), "r+") as f:
		configured = eval(f.readline())["configured"]
		if configured == False:
			lines = f.readlines()
			f.flush()
			f.seek(0,0)
			f.write("{'configured': True}\n")
			f.write(import_string)
			f.writelines(lines)
		f.close()
def config():
	import_string = "PROJECT_DIR = \"" + PROJECT_DIR + "\"\nfrom sys import path" + "\npath.append(PROJECT_DIR)\n"

	create_header("__main__.py", import_string)
	create_header("utils.py", import_string)
	create_header(os.path.join("physics","physics.py"), import_string)
	create_header(os.path.join("gallery","tracks.py"), import_string)
	create_header(os.path.join("gallery","land_vehicles.py"), import_string)
	create_header(os.path.join("GUI","YMCreator.py"), import_string)

def delete_header(path_from_main):
	with open(os.path.join(PROJECT_DIR, path_from_main), "r+") as f:
		configured = eval(f.readline())["configured"]
		f.flush()
		if configured == True:
			lines = f.readlines()
			f.flush()
			f.seek(0,0)
			f.write("{'configured': False}\n")
			diff = -1
			for i in range(0,4):
				diff += len(lines[i])
			overwriter = ' '*diff
			for i in range(3, len(lines)):
				f.write(lines[i])
			f.write(overwriter)
		f.close()

def unconfig():	
	delete_header("__main__.py")
	delete_header("utils.py")
	delete_header(os.path.join("physics","physics.py"))
	delete_header(os.path.join("gallery","tracks.py"))
	delete_header(os.path.join("gallery","land_vehicles.py"))
	delete_header(os.path.join("GUI","YMCreator.py"))

arg_list = {
	"conf": config,
	"config": config,
	"configure": config,
	"unconf": unconfig,
	"unconfig": unconfig,
	"unconfigure": unconfig,
}
def parse_args():
	if len(sys.argv) > 1:
		for arg in sys.argv[1:]:
			if arg in arg_list:
				arg_list[arg]()
				break
			else:
				print("Wrong argument.")


###########==Begin real stuff==##########

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

print("This the project directory:\n" + PROJECT_DIR + "\n")
if not get_yesorno("Do you want to continue (y/n)? "):
	sys.exit(0)

parse_args()
