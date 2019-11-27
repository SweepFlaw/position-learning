from position_learning import getRecommendList, saveName, embedCSV
import os

if __name__ == "__main__":
  filename = os.path.dirname(os.path.realpath(__file__)) + '/data/code.cpp'
  recommendList = getRecommendList(filename)
  print(recommendList)
