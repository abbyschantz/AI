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
        currPos = currentGameState.getPacmanPosition()

        stateChange = successorGameState.getScore() - currentGameState.getScore()

        "*** YOUR CODE HERE ***"
        if successorGameState.isWin() or successorGameState.isLose():
            return successorGameState.getScore()

        foodList = newFood.asList()
        capsuleList = currentGameState.getCapsules()
        foodList.extend(capsuleList)
        ghostPositionsList = successorGameState.getGhostPositions()

        ghostNextDoor = False
        for ghostPos in ghostPositionsList:
            if manhattanDistance(newPos, ghostPos) <= 2:
                ghostNextDoor = True

        if ghostNextDoor:
            stateChange = stateChange - 250

        (closestFood, closestDist) = ((0,0), float('inf'))
        for foodPos in foodList:
            currDist = manhattanDistance(currPos, foodPos)
            if currDist < closestDist:
                (closestFood, closestDist) = (foodPos, currDist)
        newDist = manhattanDistance(newPos, closestFood)

        if successorGameState.getPacmanPosition() in capsuleList:
            return stateChange + 50

        if closestDist > newDist :
            stateChange = stateChange + (10/closestDist)
        else:
            stateChange = stateChange - 20

        if action == Directions.STOP:
            stateChange = stateChange - 10
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
		action = self.actionDecider(gameState, self.depth)
		return action
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
		if agentNumber >= gameState.getNumAgents():
			agentNumber = 0
			currDepth = currDepth - 1

		if gameState.isWin() or gameState.isLose() or (currDepth<=0):
			return self.evaluationFunction(gameState)
		else:
			if agentNumber == 0:
				return self.maxValue(gameState, agentNumber, currDepth)
			else:
				return self.minValue(gameState, agentNumber, currDepth)

	def maxValue(self, gameState, agentNumber, currDepth):
		score = -1*float("inf")
		legalActions = gameState.getLegalActions(agentNumber)
		successorStates = []
		for action in legalActions:
			successorStates.append(gameState.generateSuccessor(agentNumber, action))

		for state in successorStates:
			modAgent = (agentNumber+1)
			newScore = self.valueFunc(state, modAgent, currDepth)
			score = max(score, newScore)
		return score

	def minValue(self, gameState, agentNumber, currDepth):
		score = float("inf")
		legalActions = gameState.getLegalActions(agentNumber)
		successorStates = []
		for action in legalActions:
			successorStates.append(gameState.generateSuccessor(agentNumber, action))

		for state in successorStates:
			modAgent =(agentNumber+1)
			newScore = self.valueFunc(state, modAgent, currDepth)
			score = min(score, newScore)
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

		alpha = -1*float("inf")
		beta = float("inf")
		action = self.valueFunc(gameState, 0, -1, alpha, beta)[1]
		return action


	def valueFunc(self, gameState, agentNumber, currDepth, alpha, beta):
		if agentNumber == 0:
			currDepth = currDepth + 1

		if gameState.isWin() or gameState.isLose() or (currDepth>=self.depth):
			return (self.evaluationFunction(gameState), Directions.STOP)
		else:
			if agentNumber == 0:
				return self.maxValue(gameState, agentNumber, currDepth, alpha, beta)
			else:
				return self.minValue(gameState, agentNumber, currDepth, alpha, beta)

	def maxValue(self, gameState, agentNumber, currDepth, alpha, beta):
		score = -1*float("inf")
		bestAction = Directions.STOP
		for action in gameState.getLegalActions(agentNumber):
			state = gameState.generateSuccessor(agentNumber, action)
			modAgent = (agentNumber+1) % gameState.getNumAgents()
			newScore = max(score, self.valueFunc(state, modAgent, currDepth, alpha, beta)[0])
			if newScore > score:
				bestAction = action
			score = newScore
			if newScore > beta:
				return (newScore, bestAction)
			alpha = max(alpha, newScore)
		return (newScore, bestAction)

	def minValue(self, gameState, agentNumber, currDepth, alpha, beta):
		score = float("inf")
		bestAction = Directions.STOP
		for action in gameState.getLegalActions(agentNumber):
			state = gameState.generateSuccessor(agentNumber, action)
			modAgent =(agentNumber+1) % gameState.getNumAgents()
			newScore = min(score, self.valueFunc(state, modAgent, currDepth, alpha, beta)[0])
			if newScore < score:
				bestAction = action
			score = newScore
			if newScore < alpha:
				return (newScore, bestAction)
			beta = min(beta, newScore)
		return (newScore, bestAction)


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
		action = self.actionDecider(gameState, self.depth)
		return action
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
		if agentNumber >= gameState.getNumAgents():
			agentNumber = 0
			currDepth = currDepth - 1

		if gameState.isWin() or gameState.isLose() or (currDepth<=0):
			return self.evaluationFunction(gameState)
		else:
			if agentNumber == 0:
				return self.maxValue(gameState, agentNumber, currDepth)
			else:
				return self.expValue(gameState, agentNumber, currDepth)

	def maxValue(self, gameState, agentNumber, currDepth):
		score = -1*float("inf")
		legalActions = gameState.getLegalActions(agentNumber)
		successorStates = []
		for action in legalActions:
			successorStates.append(gameState.generateSuccessor(agentNumber, action))
		for state in successorStates:
			modAgent = (agentNumber+1)
			newScore = self.valueFunc(state, modAgent, currDepth)
			score = max(score, newScore)
		return score

	def expValue(self, gameState, agentNumber, currDepth):
		score = 0
		legalActions = gameState.getLegalActions(agentNumber)
		successorStates = []
		for action in legalActions:
			successorStates.append(gameState.generateSuccessor(agentNumber, action))
		successorStatesLength = len(successorStates)
		for state in successorStates:
			modAgent =(agentNumber+1)
			newScore = self.valueFunc(state, modAgent, currDepth)
			score += newScore
		score = score/successorStatesLength
		return score

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Rewards getting closer to using reciprocal to nearest food dot using bfs length of path.
	  Punishes for getting within 2 of ghost if scaredTimes less than or equal to 5
	  Punishes for staying in area with 3 walls around it when the scaredTime on the ghost isn't "fresh" (so it doesn't get stuck with only one way out)
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isLose() or currentGameState.isWin():
        return currentGameState.getScore()

    stateScore = currentGameState.getScore()

    walls = currentGameState.getWalls()
    wallsList = walls.asList()
    currPos = currentGameState.getPacmanPosition()
    (currX, currY) = currPos
    currCapsules = currentGameState.getCapsules()
    currFood = currentGameState.getFood()
    foodList = currFood.asList()
    foodList.extend(currCapsules)
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPositionsList = currentGameState.getGhostPositions()

    (foodLoc, nearManhFoodDist) = ((0,0), float('inf'))

    ghostDist = breadthFirstDepthLimitedSearch(currentGameState, ghostPositionsList)

    if ghostDist <= 2 and scaredTimes[0] < 5:
        stateScore = stateScore - 250

    foodPathList = breadthFirstSearch(currentGameState, foodList)
    stateScore = stateScore + 20/len(foodPathList)
    wallsCount = 0
    wallsTestList = [(currX+1, currY), (currX-1, currY), (currX, currY+1), (currX, currY-1)]
    for wallTest in wallsTestList:
        if wallTest in wallsList:
            wallsCount = wallsCount + 1

    if wallsCount == 3 and scaredTimes[0] <= 35 and scaredTimes[0] >= 0:
        stateScore = stateScore - 2

    return stateScore
    util.raiseNotDefined()

def breadthFirstSearch(gameState, goalList):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    return generalizedSearch(gameState, queue, goalList)
    util.raiseNotDefined()

def generalizedSearch(gameState, dataStruc, goalList):
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

def breadthFirstDepthLimitedSearch(gameState, goalList):
    queue = util.Queue()
    return generalizedDepthLimitedSearch(gameState, queue, goalList)
    util.raiseNotDefined()

def generalizedDepthLimitedSearch(gameState, dataStruc, goalList):
    goalSet = set(goalList)

    wallsMatr = gameState.getWalls()
    wallsList = wallsMatr.asList()
    closed = set(wallsList)

    startList = []
    startList.append(gameState.getPacmanPosition())
    dataStruc.push((startList, 0))


    while not dataStruc.isEmpty():
        """currAndActions[(currx, curry), (x1,y1), (x2, y2), ..., (xn, yn)]"""
        (currAndActions, currDepth) = dataStruc.pop()
        (currx, curry) = currAndActions.pop(0)

        #when ghost isn't within 2 actions
        if currDepth >= 3:
            return 99999

        if (currx, curry) in goalSet:
            currAndActions.append((currx, curry))
            return currDepth

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
                dataStruc.push((newList, currDepth + 1))

# Abbreviation
better = betterEvaluationFunction
