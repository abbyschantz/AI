# mira.py
# -------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Mira implementation
import util
import copy
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"
        # cWeights = {}

        # for cVal in Cgrid:
        #     """need to copy weights over/keep track of for each cVal"""
        #     currWeights = copy.deepcopy(self.weights)
        #     print "pizza", currWeights
        #     print "pasta", self.weights
        #     print "training data", trainingData
        #     for iteration in range(self.max_iterations):
        #         for i in range(len(trainingData)):
        #             guessLabel = self.ourClassify(trainingData[i])

        #             if trainingLabels[i] is not guessLabel:
        #                 likelyTau = ((currWeights[guessLabel] - currWeights[trainingLabels[i]])*trainingData[i]+1.0)/(2.0*(trainingData[i]*trainingData[i]))
        #                 tau = min(cVal, likelyTau)
        #                 currWeights[trainingLabels[i]] = \
        #                     currWeights[trainingLabels[i]] + trainingData[i].divideAll(1.0/tau)
        #                 currWeights[guessLabels] = \
        #                     currWeights[guessLabel] - trainingData[i].divideAll(1.0/tau)

        #             #else do nothing
        #     cWeights[cVal] = currWeights

        # cWrong = {}
        # leastErrors = float("inf")
        # for cVal in Cgrid:
        #     cWrong[cVal] = 0
        #     for i in range(validationData):
        #         currLabel = self.ourClassify(validationData[i])
        #         if validationLabels[i] is not currLabel:
        #             cWrong[cVal] += 1
        #     if leastErrors > cWrong[cVal]:
        #         leastErrors = cVal

        # self.weights = cWeights[cVal]
        cWeights = {}
        cAccuracy = None
        allLabels = self.legalLabels
        
        for cVal in Cgrid:
            
            currWeights = copy.deepcopy(self.weights)
            for iteration in range(self.max_iterations):
                
                count = 0
                for i in range(len(trainingData)):

                    maxScore = None
                    maxY = None
                    for currLabel in allLabels:

                        currScore = trainingData[i] * currWeights[currLabel]

                        if maxScore is None or currScore > maxScore:
                            maxScore = currScore
                            maxY = currLabel

                    actualLabel = trainingLabels[count]

                    if maxY != actualLabel:

                        trainingPoint= trainingData[i].copy()
                        likelyTau = ((currWeights[maxY] - currWeights[actualLabel]) * trainingPoint + 1.0) / (2.0 * (trainingPoint*trainingPoint))
                        tau = min(cVal, likelyTau)
                        trainingPoint.divideAll(1.0/tau)

                        currWeights[actualLabel] = currWeights[actualLabel] + trainingPoint
                        currWeights[maxY] = currWeights[maxY] - trainingPoint
                    
                    count += 1

            actual = 0
            guessLabel = self.classify(validationData)
            count = 0

            for currLabel in guessLabel:
                if validationLabels[count] == currLabel:
                    actual += 1.0
                count += 1
            accuracy = actual / len(guessLabel)

            if accuracy > cAccuracy or cAccuracy is None:
                cAccuracy = accuracy
                cWeights = currWeights
        self.weights = cWeights

    def ourClassify(self, data):
        # returns the classified data point's guessed label given current weights
        maxVal, maxLabel = -1*float("inf"), None
        for l in self.legalLabels:
            if self.weights[l] * data > maxVal:
                maxVal, maxLabel = self.weights[l] * data, l

        return maxLabel

    def classify(self, data):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses
