from __future__ import division
import numpy

  
def cmpMatrix(mat1,mat2):
  for row in range(0,len(mat1)):
    for col in range(0,len(mat1)):
      if(mat1[row][col] != mat2[row][col]):
        return 1
        
  return 0
  
def genPageRankVector(matrix):
  x = numpy.zeros(shape=(1,len(matrix)))
  rows,cols = x.shape
  for row in range(0,rows):
    for col in range(0,cols):
      x[row][col] = 1/len(matrix)
  
  i = 0
  oldMatrix = x
  newMatrix = numpy.dot(x,matrix)
  
  while cmpMatrix(oldMatrix,newMatrix):
    oldMatrix = newMatrix
    newMatrix = numpy.dot(oldMatrix,matrix)
    i = i+1

  print("working")
  return newMatrix 