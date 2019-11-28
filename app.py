from position_learning import getRecommendList, saveName, embedCSV
from sys import argv

if __name__ == "__main__":
  filename = argv[1]
  if len(argv) > 2:
    modelType = argv[2]
  else:
    modelType = 'GRU'

  recommendList = getRecommendList(filename, modelType)
  for (lin, col) in recommendList:
    print(lin, col, sep=',', end='\n')
