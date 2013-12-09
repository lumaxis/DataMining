from os.path import isdir,join,normpath
from os import listdir

from PIL import Image
from numpy import asfarray,dot,argmin,zeros, amax, transpose, apply_along_axis
from numpy import average,sort,argsort,trace
from numpy.linalg import svd,eigh
from numpy import concatenate, reshape
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.cm as cm

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

    #Calculate Eigenvalues and simplified Eigenvectors
    w,v = eigh(dot(adjfaces,X))

    #Multiply original matrix with simplified Eigenvectors to get real Eigenvectors
    v = dot(X,v)

    #Sort Eigenvalues to get indices for selection of relevant Eigenvectors
    idx = w.argsort()[::-1]

    #Order Eigenvalues by indices and return them
    w = w[idx]
    v = v[:,idx]
    return v

"""
Calculates the corresponding point of img in space
"""
def projectImageToEigenspace(img,space):
    pointInEigenspace = zeros(shape=(6))
    for i in range(6):
        pointInEigenspace[i] = dot(transpose(space[:,i:i+1]),img)
    return pointInEigenspace

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

# faces formes our Eigenspace
faces = calculateEigenfaces(NormedArrayOfFaces)

# select 6 most relevant faces
relevantFaces = faces[:,:6]

# display relevant faces
display = zeros(shape=(height,0))
for i in range(6):
    display = concatenate((display,relevantFaces[:,i:i+1].reshape(height,width)), axis=1)
plt.imshow(display,cmap = cm.Greys_r)

# calculate point in Eigenspace for every image
pointsInEigenspace = []
for img in NormedArrayOfFaces:
    pointsInEigenspace.append(projectImageToEigenspace(img,faces))
    