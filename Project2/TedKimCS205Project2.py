from os import path
from array import *
from copy import deepcopy
import sys
#import numpy as np
import csv

#Global variables
colNum = 0 #Number of columns, total number of column features, value to be accessed for featureSearch function.
#The rows and columns for the dataset, used in featureSearch, cross validation, and for distance calculation (nearest neighbors distance)
row = []
columnFeature = []

"""
PSEUDOCODE BEING FOLLOWED:
function  feature_search_demo(data)
current_set_of_features = []; % Initialize an empty set
for i = 1 : size(data,2)-1
    disp(['On the ',num2str(i),'th level of the search tree'])
    feature_to_add_at_this_level = [];
    best_so_far_accuracy    = 0;
     for k = 1 : size(data,2)-1
       if isempty(intersect(current_set_of_features,k)) % Only consider adding, if not already added.
        disp(['--Considering adding the ', num2str(k),' feature'])
        accuracy = leave_one_out_cross_validation(data,current_set_of_features,k+1);
        if accuracy > best_so_far_accuracy
            best_so_far_accuracy = accuracy;
            feature_to_add_at_this_level = k;
        end
      end
     end
    current_set_of_features(i) =  feature_to_add_at_this_level;
    disp(['On level ', num2str(i),' i added feature ', num2str(feature_to_add_at_this_level), ' to current set'])
 end
end
"""
def featureSearch(colNum, row, columnFeature, userInput):
    algoName = "" #For the "Hello World introduction to the algorithm"
    action = "" #Depending on forward selection or backward elimination, we will either ADD or REMOVE a feature to our current set of features.
    #print(colNum)
    if userInput == '1': #If user picks forward selection
        algoName = "Forward Selection"
        currSetFeatures = []
    elif userInput == '2': #If user picks backward elimination.
        algoName = "Backward Elimination"
        #currSetFeatures = np.arange(1, colNum, 1) #https://numpy.org/doc/stable/reference/generated/numpy.arange.html using numpy library in order to create a currSetFeatures withe every feature

    print("Hello, world!! We have officially entered " + algoName + "!\n")
    accuracyArr = []
    featureOutput = []
    for i in range(1, colNum):
        if i % 10 == 1 and i != 11:
            print("On the " + str(i) + "st level of the search tree")
        elif i % 10 == 2:
            print("On the " + str(i) + "nd level of the search tree")
        elif i % 10 == 3:
            print("On the " + str(i) + "rd level of the search tree")
        else:
            print("On the " + str(i) + "th level of the search tree")
        featureToAddAtLevel = 0
        bestAcc = 0
        for k in range(1, colNum):
            initCopy = deepcopy(currSetFeatures) #https://docs.python.org/3/library/copy.html in order to create "levels" of the search tree, utilized deepcopy from Python's copy library.
            if userInput == '1':
                if k not in currSetFeatures:
                    if k % 10 == 1  and k != 11:
                        print("--Considering adding the " + str(k) + "st feature to this: " + str(initCopy))
                    elif k % 10 == 2:
                        print("--Considering adding the " + str(k) + "nd feature to this: " + str(initCopy))
                    elif k % 10 == 3:
                        print("--Considering adding the " + str(k) + "rd feature to this: " + str(initCopy))
                    else:
                        print("--Considering adding the " + str(k) + "th feature to this: " + str(initCopy))
                    accuracy = leaveOneOutCross(initCopy, k, row, columnFeature, userInput)
                    print("Accuracy: " + str(accuracy))
                    if accuracy > bestAcc:
                        bestAcc = accuracy
                        featureToAddAtLevel = k
            elif userInput == '2':
                if k in currSetFeatures:
                    if k % 10 == 1 and k != 11:
                        print("--Considering removing the " + str(k) + "st feature: " + str(initCopy))
                    elif k % 10 == 2:
                        print("--Considering removing the " + str(k) + "nd feature: " + str(initCopy))
                    elif k % 10 == 3:
                        print("--Considering removing the " + str(k) + "rd feature: " + str(initCopy))
                    else:
                        print("--Considering removing the " + str(k) + "th feature: " + str(initCopy))
                    accuracy = leaveOneOutCross(initCopy, k, row, columnFeature, userInput)
                    print("Accuracy: " + str(accuracy))
                    if accuracy > bestAcc:
                        bestAcc = accuracy
                        featureToAddAtLevel = k
        if userInput == '1':
            currSetFeatures.append(featureToAddAtLevel)
        elif userInput == '2':
            currSetFeatures = currSetFeatures[currSetFeatures != featureToAddAtLevel]
        accuracyArr.append(bestAcc)
        resultCopy = deepcopy(currSetFeatures) #We want to output the best features based on best accuracy.
        featureOutput.append(resultCopy)
        if userInput == '1':
            print("On level " + str(i) + " I added feature(s) " +
                  str(featureToAddAtLevel) + " to current set, accuracy is " + str(bestAcc) + "\n")
        elif userInput == '2':
            print("On level " + str(i) + " I removed feature " +
                  str(featureToAddAtLevel) + " from current set, accuracy is " + str(bestAcc) + "\n")
    maxPercent = max(accuracyArr)
    maxPercent = maxPercent * 100
    #https://www.w3schools.com/python/ref_list_index.asp to find the indexes that created the best accuracy
    print("Finished search!! The best feature subset is " + str(featureOutput[accuracyArr.index(max(accuracyArr))]) + ", which has an accuracy of " + str(maxPercent) + "%")

#distance function to help calculate accuracy using k-fold cross validation
#https://machinelearningmastery.com/implement-resampling-methods-scratch-python/ helped me grow in my understanding of what I needed to do.
def calculateDistance(current, a, b, columnFeature):
    distCalculated = 0.0
    for i in range(len(current)):
        row1 = float(columnFeature[current[i] - 1][b])
        row2 = float(columnFeature[current[i] - 1][a])
        distCalculated = distCalculated + ((row1 - row2)*(row1 - row2))
    return distCalculated

#Pseudocode from Project 2 Briefing lecture slides referenced
def leaveOneOutCross(initCopy, k, row, columnFeature, userInput):
    num = 0 #Integer variable to help calculate accuracy
    if userInput == '1': #If user chose Forward Selection
        initCopy.append(k)
    elif userInput == '2': #If user chose Backward Elimination
        # https://stackoverflow.com/questions/25004347/remove-list-element-without-mutation/25004389
        initCopy = initCopy[initCopy != k]
    else:
        print("")
    for i in range(len(row)):
        nearestNeighborDistance = sys.maxsize #https://docs.python.org/3/library/sys.html
        nearestNeighborLocation = sys.maxsize
        for j in range(len(row)):
            if not i == j:
                distance = calculateDistance(initCopy, i, j, columnFeature)
                if distance < nearestNeighborDistance:
                    nearestNeighborDistance = distance
                    nearestNeighborLocation = j
        if row[i] == row[nearestNeighborLocation]:
            num = num + 1
    #print("Object " + str(i) + " is class " + str(row[i]))
    #print("The nearest neighbor is " + str(nearestNeighborLocation) + " which is in class " + str(nearestNeighborDistance))
    accuracy = num / len(row)
    return accuracy

def main():
    global colNum
    global row
    global columnFeature
    userInput = "" #The user will be inputting 1, or 2, depending on their algorithm choice
    #print(sys.version)
    print("Welcome to Ted Kim's Feature Selection Algorithm!")
    fileInput = input("Type in the name of the file to test: ") #user has to input a correct file to run algorithm on
    # https://docs.python.org/3/library/os.path.html, using Python OS.path library to check if a file exists, if it does not exist, the user is re-prompted until a correct file is typed in.
    while not path.exists(fileInput):
        print("CRINGE!! THAT FILE ISN'T REAL.")
        fileInput = input("Type in the name of the file to test:")
    #w3schools.com/python/python_file_open.asp Referenced for opening the file
    f = open(fileInput, 'r')
    # https://docs.python.org/3/library/csv.html
    read = csv.reader(f, delimiter=' ', skipinitialspace=True)
    nr = next(read)  # https://www.w3schools.com/python/ref_func_next.asp
    colNum = len(nr)
    f.close()
    f2 = open(fileInput, 'r')
    rl = f2.readlines()  # https://www.w3schools.com/python/ref_file_readlines.asp
    #https://stackoverflow.com/questions/6696027/how-to-split-elements-of-a-list
    for i in rl:
        x = i.split()[0] #Splitting every single element in the dataset and then appending each indvidual element
        row.append(x)
    #arr = np.arange(1,colNum,1)
    #print(arr)
    print("\n")
    print("Wow! Thanks for inputting the file name: " +
          fileInput + "! Let's do something with it!\n")

    dup = []
    a = 0
    print("This dataset has " + str(colNum - 1) + " features (not including the class attribute, with " + str(len(row)) + " instances.")
    accuracyInit = leaveOneOutCross(dup, 0, row, columnFeature, 0)
    print("Running nearest neighbor with all " + str(colNum - 1) + " features, using \"leave one out\" evaluation, I get an accuracy of " + str(accuracyInit * 100) + "%.\n")

    #https://stackoverflow.com/questions/6696027/how-to-split-elements-of-a-list
    for i in range(1, colNum):
        f3 = open(fileInput,'r')
        rl2 = f3.readlines()
        outputArr = []
        for j in rl:
            y = j.split()[i]
            #print(y)
            outputArr.append(y)
        columnFeature.append(outputArr)
        f3.close()


    while userInput != '1' and userInput != '2': #User is asked to choose either 1 or 2 as correct inputs, for one of the two provided algorithms.
        print("Type the number of the algorithm you want to run.")
        print("1) Forward Selection")
        print("2) Backward Elimination")
        userInput = input()
        if userInput == '1':
            print("This is going to do forward selection.")
            featureSearch(colNum, row, columnFeature, userInput) #featureSearch function will begin performing forward selection
        elif userInput == '2':
            print("This is going to do backward elimination.")
            featureSearch(colNum, row, columnFeature, userInput) #featureSearch function will begin performing backward elimination
        else:
            print("BOO!! Let's try typing in a REAL algorithm!")


main()
