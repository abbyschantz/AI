# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.
 
      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """
 
 
    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.
 
        getAction chooses among the best options according to the evaluation function.
 
        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
 
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
 
        "Add more of your code here if you want to"
 
        return legalMoves[chosenIndex]
 
    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.
 
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
 
        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
 
        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newWalls = successorGameState.getWalls()
 
        "*** YOUR CODE HERE ***"
        """keeping this as an idea: if ghost distance is less than some arb.
        amount, turn around"""
        if successorGameState.isWin():
            return successorGameState.getScore()
 
        if successorGameState.isLose():
            return successorGameState.getScore()
 
        ghostPositionsList = successorGameState.getGhostPositions()
        foodList = newFood.asList()
        capsuleList = successorGameState.getCapsules()
        foodList.extend(capsuleList)
        foodPathList = self.breadthFirstSearch(successorGameState, foodList)
        ghostPathList = self.breadthFirstSearch(successorGameState, ghostPositionsList)
        stateChange = successorGameState.getScore() - currentGameState.getScore()
 
        if successorGameState.getPacmanPosition() in capsuleList:
            return stateChange + 50
 
        ghostNextDoor = False
        if len(ghostPathList) < 6:
            ghostNextDoor = True
 
        if ghostNextDoor:
            stateChange = stateChange - 250
 
        if newPos in foodPathList:
            #print 'oh captain'
            stateChange = stateChange + (10/len(foodPathList))
        else:
            #deviate from path, when ghost is within 5
            stateChange = stateChange - 20
 
        #if ghost is scared and we're close enough, go towards the ghosts
 
        #return stateChange
        return stateChange
 
    def breadthFirstSearch(self, gameState, goalList):
        """Search the shallowest nodes in the search tree first."""
        "*** YOUR CODE HERE ***"
        queue = util.Queue()
        return self.generalizedSearch(gameState, queue, goalList)
        util.raiseNotDefined()
 
    def generalizedSearch(self, gameState, dataStruc, goalList):
        goalSet = set(goalList)
 
        wallsMatr = gameState.getWalls()
        wallsList = wallsMatr.asList()
        closed = set(wallsList)
 
        startList = []
        startList.append(gameState.getPacmanPosition())
        dataStruc.push(startList)
 
 
        while not dataStruc.isEmpty():
            """currAndActions[(currx, curry), (x1,y1), (x2, y2), ..., (xn, yn)]"""
            currAndActions = dataStruc.pop()
 
            (currx, curry) = currAndActions.pop(0)
 
 
            if (currx, curry) in goalSet:
                currAndActions.append((currx, curry))
                print currAndActions
                return currAndActions
 
            if not ((currx,curry) in closed):
                closed.add((currx, curry))
 
                succList = []
                #adds immediate points around current point
                if (currx + 1) < wallsMatr.width and ((currx + 1), curry) not in closed:
                    new = (currx+1, curry)
                    succList.append(new)
                if (currx - 1) >= 0 and ((currx - 1), curry) not in closed:
                    new = (currx-1, curry)
                    succList.append(new)
                if (curry + 1) < wallsMatr.height and (currx, (curry + 1)) not in closed:
                    new = (currx, curry+1)
                    succList.append(new)
                if (curry - 1) >= 0 and (currx, (curry - 1)) not in closed:
                    new = (currx, curry-1)
                    succList.append(new)
 
                for (xn, yn) in succList:
                    newList = []
                    newList.append((xn,yn))
                    currAndActions.append((currx,curry))
                    newList.extend(currAndActions)
                    dataStruc.push(newList)
 
        util.raiseNotDefined()
	
def scoreEvaluationFunction(currentGameState):
	"""
	  This default evaluation function just returns the score of the state.
	  The score is the same one displayed in the Pacman GUI.

	  This evaluation function is meant for use with adversarial search agents
	  (not reflex agents).
	"""
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	  This class provides some common elements to all of your
	  multi-agent searchers.  Any methods defined here will be available
	  to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	  You *do not* need to make any changes here, but you can if you want to
	  add functionality to all your adversarial search agents.  Please do not
	  remove anything, however.

	  Note: this is an abstract class: one that should not be instantiated.  It's
	  only partially specified, and designed to be extended.  Agent (game.py)
	  is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent (question 2)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action from the current gameState using self.depth
		  and self.evaluationFunction.

		  Here are some method calls that might be useful when implementing minimax.

		  gameState.getLegalActions(agentIndex):
			Returns a list of legal actions for an agent
			agentIndex=0 means Pacman, ghosts are >= 1

		  gameState.generateSuccessor(agentIndex, action):
			Returns the successor game state after an agent takes an action

		  gameState.getNumAgents():
			Returns the total number of agents in the game

		  gameState.isWin():
			Returns whether or not the game state is a winning state

		  gameState.isLose():
			Returns whether or not the game state is a losing state
		"""
		"*** YOUR CODE HERE ***"
		direction = self.actionDecider(gameState, self.depth)
		return direction
		util.raiseNotDefined()

	def actionDecider(self, gameState, currDepth):
		if currDepth == 0:
			return Directions.STOP
		else:
			actionList = gameState.getLegalActions(0)
			(maxAction, maxScore) = (actionList[0], -9999999)

			agentNum = gameState.getNumAgents()
			for action in actionList:
				successor = gameState.generateSuccessor(0, action)
				succScore = self.valueFunc(successor, (1 % agentNum), currDepth)
				if succScore > maxScore:
					(maxAction, maxScore) = (action, succScore)

			return maxAction


	def valueFunc(self, gameState, agentNumber, currDepth):
		#print self.depth, agentNumber, 'pizza'
		if agentNumber >= gameState.getNumAgents():
			agentNumber = 0
			currDepth = currDepth - 1

		if gameState.isWin() or gameState.isLose() or (currDepth<=0):
			#print 'hamburger', self.depth
			return self.evaluationFunction(gameState)
		else:
			if agentNumber == 0:
				return self.maxValue(gameState, agentNumber, currDepth)
			else:
				return self.minValue(gameState, agentNumber, currDepth)
	#python passes by value for strings

	def maxValue(self, gameState, agentNumber, currDepth):
		score = -1*float("inf")
		legalActions = gameState.getLegalActions(agentNumber)
		successorStates = []
		for action in legalActions:
			successorStates.append(gameState.generateSuccessor(agentNumber, action))

		for state in successorStates:
			#score = max(score, self.valueFunc(state, (agentNumber+1) % gameState.getNumAgents))
			modAgent = (agentNumber+1)
			newScore = self.valueFunc(state, modAgent, currDepth)
			score = max(score, newScore)
		#print score, agentNumber, 'hotdog'
		return score

	def minValue(self, gameState, agentNumber, currDepth):
		score = float("inf")
		legalActions = gameState.getLegalActions(agentNumber)
		successorStates = []
		for action in legalActions:
			successorStates.append(gameState.generateSuccessor(agentNumber, action))

		for state in successorStates:
			#score = min(score, self.valueFunc(state, (agentNumber+1) % gameState.getNumAgents))
			modAgent =(agentNumber+1)
			newScore = self.valueFunc(state, modAgent, currDepth)
			score = min(score, newScore)
		#print score, agentNumber, 'chips'
		return score


class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent with alpha-beta pruning (question 3)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"
		direction = self.actionDecider(gameState, self.depth)
		return direction
		util.raiseNotDefined()

	def actionDecider(self, gameState, currDepth):
		alpha = float("inf")
		beta = -1*float("inf")
		if currDepth == 0:
			return Directions.STOP
		else:
			actionList = gameState.getLegalActions(0)
			(maxAction, maxScore) = (actionList[0], -9999999)

			agentNum = gameState.getNumAgents()
			for action in actionList:
				successor = gameState.generateSuccessor(0, action)
				succScore = self.valueFunc(successor, (1 % agentNum), currDepth, alpha, beta)
				if succScore > maxScore:
					(maxAction, maxScore) = (action, succScore)

			return maxAction


	def valueFunc(self, gameState, agentNumber, currDepth, alpha, beta):
		#print self.depth, agentNumber, 'pizza'
		if agentNumber >= gameState.getNumAgents():
			agentNumber = 0
			currDepth = currDepth - 1

		if gameState.isWin() or gameState.isLose() or (currDepth<=0):
			#print 'hamburger', self.depth
			return self.evaluationFunction(gameState)
		else:
			if agentNumber == 0:
				return self.maxValue(gameState, agentNumber, currDepth, alpha, beta)
			else:
				return self.minValue(gameState, agentNumber, currDepth, alpha, beta)
	#python passes by value for strings

	def maxValue(self, gameState, agentNumber, currDepth, alpha, beta):
		score = -1*float("inf")
		legalActions = gameState.getLegalActions(agentNumber)
		successorStates = []
		for action in legalActions:
			successorStates.append(gameState.generateSuccessor(agentNumber, action))

		for state in successorStates:
			#score = max(score, self.valueFunc(state, (agentNumber+1) % gameState.getNumAgents))
			modAgent = (agentNumber+1)
			newScore = self.valueFunc(state, modAgent, currDepth, alpha, beta)
			score = max(score, newScore)
			if score > beta:
				return score
			alpha = max(alpha, score)
		#print score, agentNumber, 'hotdog'
		return score

	def minValue(self, gameState, agentNumber, currDepth, alpha, beta):
		score = float("inf")
		legalActions = gameState.getLegalActions(agentNumber)
		successorStates = []
		for action in legalActions:
			successorStates.append(gameState.generateSuccessor(agentNumber, action))

		for state in successorStates:
			#score = min(score, self.valueFunc(state, (agentNumber+1) % gameState.getNumAgents))
			modAgent =(agentNumber+1)
			newScore = self.valueFunc(state, modAgent, currDepth, alpha, beta)
			score = min(score, newScore)
			if score < alpha:
				return score
			beta = min(beta, score)
		#print score, agentNumber, 'chips'
		return score
		util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 4)
	"""

	def getAction(self, gameState):
		"""
		  Returns the expectimax action using self.depth and self.evaluationFunction

		  All ghosts should be modeled as choosing uniformly at random from their
		  legal moves.
		"""
		"*** YOUR CODE HERE ***"
		util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
	"""
	  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	  evaluation function (question 5).

	  DESCRIPTION: <write something here so we know what you did>
	"""
	"*** YOUR CODE HERE ***"
	util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
