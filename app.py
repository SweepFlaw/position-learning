from position_learning import getRecommendList, saveName, embedCSV

if __name__ == "__main__":
  filename = '/newdisk/autofix/deeplearning/data/code.cpp'
  recommendList = getRecommendList(filename)
  print(recommendList)
