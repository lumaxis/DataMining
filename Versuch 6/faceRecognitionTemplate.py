from os.path import isdir,join,normpath
from os import listdir

from PIL import Image
from numpy import asfarray,dot,argmin,zeros, amax, transpose, apply_along_axis,flipud
from numpy import average,sort,argsort,trace
from numpy.linalg import svd,eigh,norm
from numpy import concatenate, reshape
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys
import Tkinter

import tkFileDialog

K = 6

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

def convertImgToNumpyData(img):
    data = asfarray(img.getdata())
    dataMax = amax(data)
    return asfarray(data/dataMax)

def convertImagesToNumpyData(trainingImages):
    dataList = []
    for img in trainingImages:
        data = asfarray(img.getdata())
        #data = data.reshape(1, width*height)
        dataMax = amax(data)
        dataList.append(data/dataMax)
    return flipud(asfarray(dataList))

def calculateEigenfaces(adjfaces):
    X = transpose(adjfaces)

    #Calculate Eigenvalues and simplified Eigenvectors
    w,v = eigh(dot(adjfaces,X))

    #Multiply original matrix with simplified Eigenvectors to get real Eigenvectors
    v = dot(X,v)

    #Sort Eigenvalues to get indices for selection of relevant Eigenvectors
    index = w.argsort()[::-1]

    #Order Eigenvalues by indices and return them
    w = w[index]
    v = v[:,index]
    return v

def calculateEigenspace(NormedArrayOfFaces):
    pointsInEigenspace = []
    for img in NormedArrayOfFaces:
        pointsInEigenspace.append(projectImageToEigenspace(img,Usub))
    return pointsInEigenspace

"""
Calculates the corresponding point of img in space
"""
def projectImageToEigenspace(img,space):
    pointInEigenspace = zeros(shape=(K))
    for i in range(K):
        pointInEigenspace[i] = dot(transpose(space[:,i:i+1]),img)
    return pointInEigenspace

####################################################################################
#Start of main programm


#Choose Directory which contains all training images
dialog = Tkinter.Tk()
TrainDir=tkFileDialog.askdirectory(title="Choose Directory of training images")
#Choose the file extension of the image files
Extension='png' 
#Choose the image which shall be recognized
testImageDirAndFilename=tkFileDialog.askopenfilename(title="Choose Image to detect")
dialog.destroy()
trainingImages = generateListOfImgs(parseDirectory(TrainDir,Extension))
width,height = trainingImages[0].size
####################################################################################
# Implement required functionality of the main programm here

a = convertImagesToNumpyData(trainingImages)
avg = average(a,axis=0)

NormedArrayOfFaces = a - avg

# faces formes our Eigenspace
faces = calculateEigenfaces(NormedArrayOfFaces)

# select K most relevant faces
Usub = faces[:,:K]

# display relevant faces
display = zeros(shape=(height,0))
for i in range(K):
    display = concatenate((display,Usub[:,i:i+1].reshape(height,width)), axis=1)
plt.imshow(display,cmap = cm.Greys_r)

# calculate point in Eigenspace for every image
Eigenspace = calculateEigenspace(NormedArrayOfFaces)

testImage = (Image.open(testImageDirAndFilename)).convert('L')

#testImage = testImage.convert('L')

testImageAsNumpy = convertImgToNumpyData(testImage)

#substract average
normedTestFace = testImageAsNumpy - avg

print 'Calculate Eigenspace'
testfaceCoordinates = projectImageToEigenspace(normedTestFace,Usub)

print 'Calculate distanceances'
distance = sys.float_info.max
closestMatchIndex = 0
for index, face in enumerate(Eigenspace):
    newdistance = norm(testfaceCoordinates-face)
    print newdistance
    if distance > newdistance:
        closestMatchIndex = index
        distance = newdistance
            
print 'Start ploting'
resultFig = plt.figure()
resultFig.suptitle("Euclidean distanceance %.3f" % (distance))

ax = resultFig.add_subplot(1,2,1)
ax.yaxis.set_visible(False)
ax.xaxis.set_visible(False)
ax.imshow(testImage, cmap=plt.cm.gray)

ax2 = resultFig.add_subplot(1,2,2)
ax2.yaxis.set_visible(False)
ax2.xaxis.set_visible(False)
ax2.imshow(trainingImages[closestMatchIndex], cmap=plt.cm.gray)

print 'Show plot'
plt.show()