def readCSVNumber(filename):
  lines = open(filename, encoding='utf-8').read().strip().split('\n')
  return [[float(num) for num in line.split('\t')] for line in lines]