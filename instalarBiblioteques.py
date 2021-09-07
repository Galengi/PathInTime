import sys
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'spade==3.2.0'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'numpy==1.21.1'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'selenium==3.141.0'])

