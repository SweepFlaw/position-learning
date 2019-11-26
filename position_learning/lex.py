import subprocess
import os

lexerName = os.path.dirname(os.path.realpath(__file__)) + '/lx_cpp2csv'
saveName = os.path.dirname(os.path.realpath(__file__)) + '/lexResult'


def lexCode(filename):
  subprocess.run([lexerName, filename, saveName])