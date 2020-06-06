import os
import sys
import runpy

def main():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	sys.path.append(BASE_DIR)
	runpy.run_module('TkPy3')

if __name__ == "__main__":
	main()
