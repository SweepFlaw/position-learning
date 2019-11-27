from position_learning import getRecommendList, saveName, embedCSV
from sys import argv

if __name__ == "__main__":
  filename = argv[1]
  recommendList = getRecommendList(filename)
  for (lin, col) in recommendList:
    print(lin, ',', col)
