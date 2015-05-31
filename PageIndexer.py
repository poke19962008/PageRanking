__author__ = 'poke19962008'

from bs4 import BeautifulSoup
import re
import urllib2
import numpy
from urlparse import urljoin
import json
import PageRankCalculator as PGCalc

urlDict = {}            #urlDict[keyValue] = LinkObj
urlKeyValue = {}        #urlKeyValue[url] = value

class Link:

    def __init__(self, url, title, source, key):
        self.url = url
        self.source = source
        self.title = title
        self.key = key

    def setPageRank(self, rank):
        self.rank = rank

def getTitle(source):
    soup = BeautifulSoup(source)

    title_tag = soup.find('title')
    return title_tag.text.encode('utf-8')

def makeURLSet(fileName):
  f = open(fileName,'r')
  keyValue = 0

  for url in f.read().split('\n'):
      url_response = urllib2.urlopen(url)
      source = url_response.read()

      if url.rstrip("/") == url:
          if url != "" and not re.search("html$",url) and not re.search("htm$",url) and not re.search("css$",url):
            url =  url + "/"

      title = getTitle(source)

      LinkObj = Link(url, title, source, keyValue)
      urlDict[keyValue] = LinkObj
      urlKeyValue[url] = keyValue
      keyValue = keyValue + 1

      print(str(LinkObj.url) + " registered...")

def traverseURLset():                                               #ON THIS ONE
    metaGraph = numpy.zeros(shape = (len(urlDict), len(urlDict)))

    for key in urlDict.iterkeys():
        LinkObj = urlDict[key]

        soup = BeautifulSoup(LinkObj.source)
        anchors = soup.find_all('a')

        if anchors:
            for anchor in anchors:

                try:
                    hrefFound = anchor['href']
                except:
                    continue

                if re.search("mail", hrefFound):
                    continue

                if re.search("#", hrefFound):
                    hrefFound = hrefFound.split("#")[0]

                if hrefFound.rstrip("/") == hrefFound:
                     if hrefFound != "" and not re.search("html$",hrefFound) and not re.search("htm$",hrefFound) and not re.search("css$",hrefFound):
                         hrefFound =  hrefFound + "/"

                urlFound = urljoin(LinkObj.url, hrefFound)

                if urlFound in urlKeyValue:
                    row = urlKeyValue[LinkObj.url]
                    col = urlKeyValue[urlFound]

                    metaGraph[row][col] = 1
            print("Registered aTags for " + str(LinkObj.url))
        else:
            print("No anchor tags found for " + str(LinkObj.key))

    return metaGraph

def genTransProbMat(matrix):
  for row in range(0,len(matrix)):
    sum = 0
    for col in range(0,len(matrix)):
      sum = matrix[row][col] + sum
    for col in range(0,len(matrix)):
      if not sum:
        matrix[row][col] = 1/len(matrix)
      else:
        matrix[row][col] = matrix[row][col]/sum
  return matrix

def genSubGraph(metaGraph, dampFact):
    ''' subGraph = dampfact*[metaGraph] + (1/N)*(1-dampFactor).[unary Matrix of N]'''

    N = len(metaGraph)
    term1 = numpy.multiply(dampFact, metaGraph)
    term2 = numpy.multiply(float((1-dampFact)/N), numpy.ones((len(metaGraph), len(metaGraph))))

    return term1 + term2

def main():
    makeURLSet("WebsiteList.txt")
    print("File Scan Completed\n")

    metaGraph = traverseURLset()
    print("All Links Registered\n")

    transProbGraph = genTransProbMat(metaGraph)
    print("Generated Trans Probable Graph\n")

    print("\nGenerating sub Graph")
    dampFact = 0.85        #as per used by Google
    subGraph = genSubGraph(transProbGraph, dampFact)
    print("Generated Probability Graph\n")

    # subGraph = [[ 0.88,   0.03,   0.03,   0.03,   0.03 ],
    #             [ 0.455,  0.455 , 0.03,   0.03 ,  0.03 ],
    #             [ 0.455,  0.03,   0.455,  0.03 ,  0.03 ],
    #             [ 0.455,  0.03,   0.03,   0.455,  0.03 ],
    #             [ 0.455 , 0.03,   0.03,   0.03,   0.455]]

    PGVector = PGCalc.genPageRankVector(subGraph)
    print("Generated Page Rank Vector\n")

    RankList = {}
    for key in sorted(urlDict.iterkeys()):
        LinkObj = urlDict[key]
        LinkObj.setPageRank(PGVector[0][key])

        RankList[LinkObj.url] = LinkObj.rank

    file = open("RankList.json", "w")
    json.dump(RankList, file, indent=4)
    print("\n !!!! Process Completed Succesfully !!!!")

    print("\n\nMeta Graph --->")
    print(metaGraph)

    print("\ntrans Probability Graph ---->")
    print(transProbGraph)


    print("\nProbability Graph ---->")
    print(subGraph)

    print("\nRankList ---->")
    print(PGVector)

if __name__ == "__main__":
    main()