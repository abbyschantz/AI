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
		(pacx, pacy) = newPos
		ghostNextDoor = False
		closestGhostDist = 9999999
		for ghostState in newGhostStates:
			(x,y) = ghostState.getPosition()
			currDistance = manhattanDistance(newPos, (x,y))
			if (abs(x - pacx) <= 4) and (abs(y - pacy) <= 4):
				ghostNextDoor = True
			if currDistance < closestGhostDist:
				closestGhostDist = currDistance

		#closest food record
		foodPathList = breadthFirstSearch(currentGameState)


		(foodx, foody) = 999999, 999999
		closestFoodDist = 999999
		listOfFood = newFood.asList()

		for (x,y) in listOfFood:
			manhattDistToCurr = manhattanDistance(newPos, (x,y))
			if manhattDistToCurr < closestFoodDist:
				(foodx, foody) = (x,y)
				closestFoodDist = manhattDistToCurr


		stateChange = successorGameState.getScore() - currentGameState.getScore()

		if ghostNextDoor:
			stateChange = stateChange - 500

		if action == 'Stop':
			stateChange = stateChange - 10
		#if (pacx == foodx) and ((foodx - pacx) =

		if newPos in foodPathList:
			#print 'oh captain'
			if len(foodPathList) <= 5:
				stateChange = stateChange + (10/closestFoodDist)
			else:
				stateChange = stateChange + 1
		else:
			#deviate from path, when ghost is within 5
			stateChange = stateChange - 20
			#print 'captain'

		#if ghost is scared and we're close enough, go towards the ghosts

		#return stateChange
		return 0

def breadthFirstSearch(gameState):
	"""Search the shallowest nodes in the search tree first."""
	"*** YOUR CODE HERE ***"
	queue = util.Queue()
	return generalizedSearch(gameState, queue)
	util.raiseNotDefined()

def generalizedSearch(gameState, dataStruc):
	closed = []
	wallsList = gameState.getWalls().asList()
	closed.extend(wallsList)

	startList = []
	startList.append(gameState.getPacmanPosition())
	dataStruc.push(startList)
	currFood = gameState.getFood()
	currFoodList = currFood.asList()

	while not dataStruc.isEmpty():
		"""[(currx, curry), (x1,y1), (x2, y2), ..., (xn, yn)]"""
		currAndActionsList = dataStruc.pop()
		#print currAndActionsList
		(currx, curry) = currAndActionsList[0]


		if (currx, curry) in currFoodList:
			path = currAndActionsList[1:len(currAndActionsList)]
			path.append((currx, curry))
			#print path[0]
			return path

		if not ((currx,curry) in closed):
			closed.append((currx, curry))

			succList = []
			#adds immediate points around current point
			if (currx + 1) < currFood.width:
				new = (currx+1, curry)
				succList.append(new)
			if (currx - 1) >= 0:
				new = (currx-1, curry)
				succList.append(new)
			if (curry + 1) < currFood.height:
				new = (currx, curry+1)
				succList.append(new)
			if (curry - 1) >= 0:
				new = (currx, curry-1)
				succList.append(new)

			for (xn, yn) in succList:

				newList = []
				newList.append((xn,yn))
				#print newList
				newList + currAndActionsList[1:len(currAndActionsList)]
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
		actionList = gameState.getLegalActions(0)
		(maxAction, maxScore) = (actionList[0], -9999999)

		agentNum = gameState.getNumAgents()
		for action in actionList:
			successor = gameState.generateSuccessor(0, action)
			succScore = self.valueFunc(successor, (1 % agentNum), currDepth - 1)
			if succScore > maxScore:
				(maxAction, maxScore) = (action, succScore)

		return maxAction


	def valueFunc(self, gameState, agentNumber, currDepth):
		#print self.depth, agentNumber, 'pizza'
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
			modAgent = (agentNumber+1) % gameState.getNumAgents()
			newScore = self.valueFunc(state, modAgent, currDepth - 1)
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
			modAgent =(agentNumber+1) % gameState.getNumAgents()
			newScore = self.valueFunc(state, modAgent, currDepth - 1)
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
