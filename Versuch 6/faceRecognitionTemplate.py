from os.path import isdir,join,normpath
from os import listdir

from PIL import Image
from numpy import asfarray,dot,argmin,zeros, amax, transpose, apply_along_axis
from numpy import average,sort,argsort,trace
from numpy.linalg import svd,eigh
from numpy import concatenate, reshape
from math import sqrt

import tkFileDialog

def parseDirectory(directoryName,extension):
    '''This method returns a list of all filenames in the Directory directoryName. 
    For each file the complete absolute path is given in a normalized manner (with 
    double backslashes). Moreover only files with the specified extension are returned in 
    the list.
    '''
    if not isdir(directoryName): return
    imagefilenameslist=sorted([
        normpath(join(directoryName, fname))
        for fname in listdir(directoryName)
        if fname.lower().endswith('.'+extension)            
        ])
    return imagefilenameslist

#####################################################################################
# Implement required functions here
#
#
#

def generateListOfImgs(listOfTrainFiles):
    l = []
    for f in listOfTrainFiles:
        img = Image.open(f)
        img = img.convert("L")
        l.append(img)
    return l

def convertImgListToNumpyData(imgList):
    dataList = []
    for img in imgList:
        data = asfarray(img.getdata())
        dataMax = amax(data)
        dataList.append(data/dataMax)
    return asfarray(dataList)

def calculateEigenfaces(adjfaces):
    X = transpose(adjfaces)
    #CV = dot(X,adjfaces)

    #Calculate Eigenvalues and simplified Eigenvectors
    w,v = eigh(dot(adjfaces,X))

    #Multiply original matrix with simplified Eigenvectors to get real Eigenvectors
    v = dot(X,v)

    #Sort Eigenvalues to get indices for selection of relevant Eigenvectors
    idx = w.argsort()[::-1]

    #Order Eigenvalues by indices?
    w = w[idx]

    #Order Eigenvectors by indices
    v = v[:,idx]
    return v

def reshapeVectorToImage(x):
    global width,height
    print x.shape
    print width*height
    return x.reshape(height,width)

####################################################################################
#Start of main programm


#Choose Directory which contains all training images
TrainDir=tkFileDialog.askdirectory(title="Choose Directory of training images")
#Choose the file extension of the image files
Extension='png' 
#Choose the image which shall be recognized
#testImageDirAndFilename=tkFileDialog.askopenfilename(title="Choose Image to detect")
imgList = generateListOfImgs(parseDirectory(TrainDir,Extension))
width,height = imgList[0].size
####################################################################################
# Implement required functionality of the main programm here

a = convertImgListToNumpyData(imgList)
avg = average(a,axis=0)

NormedArrayOfFaces = a - avg

faces = calculateEigenfaces(NormedArrayOfFaces)
relevantFaces = faces[:,:6]

apply_along_axis(reshapeVectorToImage,axis=0,arr = relevantFaces)