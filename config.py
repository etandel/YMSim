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
		lines = f.readlines()
		configured = eval(lines[1])['configured']
		if configured == False:
			f.seek(0,0)
			f.write("#coding: UTF-8\n" + "{'configured': True}\n")
			f.write(import_string)
			for i in range(2,len(lines)):
				f.write(lines[i])
		f.close()
def config():
	import_string = "PROJECT_DIR = \"" + PROJECT_DIR + "\"\nfrom sys import path" + "\npath.append(PROJECT_DIR)\n"

#	create_header("TROLL.py", import_string)
	create_header("__main__.py", import_string)
	create_header("utils.py", import_string)
	create_header(os.path.join("physics","physics.py"), import_string)
	create_header(os.path.join("TrackCreator","tracks.py"), import_string)
	create_header(os.path.join("TrackCreator","TrackCreatorGUI.py"), import_string)
	create_header(os.path.join("gallery","land_vehicles.py"), import_string)

def delete_header(path_from_main):
	WRITE_STRING = "#coding: UTF-8\n" + "{'configured': False}\n"
	with open(os.path.join(PROJECT_DIR, path_from_main), "r+") as f:
		lines = f.readlines()
		configured = eval(lines[1])['configured']
	f.close()
	if configured == True:
		with open(os.path.join(PROJECT_DIR, path_from_main), "w") as f:
			f.write(WRITE_STRING)
			for i in range(5, len(lines)): #5 because it works
				f.write(lines[i])
		f.close()

def unconfig():	
#	delete_header("TROLL.py")
	delete_header("__main__.py")
	delete_header("utils.py")
	delete_header(os.path.join("physics","physics.py"))
	delete_header(os.path.join("TrackCreator","tracks.py"))
	delete_header(os.path.join("TrackCreator","TrackCreatorGUI.py"))
	delete_header(os.path.join("gallery","land_vehicles.py"))

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
