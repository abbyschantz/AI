# search.py

# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import pacman
import pdb


class SearchProblem:
	"""
	This class outlines the structure of a search problem, but doesn't implement
	any of the methods (in object-oriented terminology: an abstract class).

	You do not need to change anything in this class, ever.
	"""

	def getStartState(self):
		"""
		Returns the start state for the search problem.
		"""
		util.raiseNotDefined()

	def isGoalState(self, state):
		"""
		  state: Search state

		Returns True if and only if the state is a valid goal state.
		"""
		util.raiseNotDefined()

	def getSuccessors(self, state):
		"""
		  state: Search state

		For a given state, this should return a list of triples, (successor,
		action, stepCost), where 'successor' is a successor to the current
		state, 'action' is the action required to get there, and 'stepCost' is
		the incremental cost of expanding to that successor.
		"""
		util.raiseNotDefined()

	def getCostOfActions(self, actions):
		"""
		 actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.
		The sequence must be composed of legal moves.
		"""
		util.raiseNotDefined()


def tinyMazeSearch(problem):
	"""
	Returns a sequence of moves that solves tinyMaze.  For any other maze, the
	sequence of moves will be incorrect, so only use this for tinyMaze.
	"""
	from game import Directions
	s = Directions.SOUTH
	w = Directions.WEST
	return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:

	print "Start:", problem.getStartState()
	print "Is the start a goal?", problem.isGoalState(problem.getStartState())
	print "Start's successors:", problem.getSuccessors(problem.getStartState())
	"""
	"*** YOUR CODE HERE ***"
	#working on the implementation of the actionlist; currently printing a list of actions that is incorrect
	stk = util.Stack()
	return generalizedSearch(problem, stk)
	util.raiseNotDefined()



def breadthFirstSearch(problem):
	"""Search the shallowest nodes in the search tree first."""
	"*** YOUR CODE HERE ***"
	queue = util.Queue()
	return generalizedSearch(problem, queue)
	util.raiseNotDefined()

def generalizedSearch(problem, dataStruc):
	closed = []

	startState = problem.getStartState()
	startList = []
	startList.append(startState)
	dataStruc.push(startList)

	while not dataStruc.isEmpty():
		"""[curr, action0, action1, action2,...., action n]"""
		currAndActionsList = dataStruc.pop()
		curr = currAndActionsList[0]
		if problem.isGoalState(curr):
			return currAndActionsList[1:len(currAndActionsList)]
		if not (curr in closed):
			closed.append(curr)
			succList = problem.getSuccessors(curr)
			for (successor, direction, cost) in succList:
				"""copy.copyOf(list)"""
				newList = []
				newList.append(successor)
				newList.extend(currAndActionsList[1:len(currAndActionsList)])
				newList.append(direction)
				dataStruc.push(newList)


	util.raiseNotDefined()

"""not perfect memory wise"""
class PQNode:
	def  __init__(self, state, action, cost):
		self.state = state
		self.action = action
		self.cost = cost

def uniformCostSearch(problem):
	"""Search the node of least total cost first."""
	"*** YOUR CODE HERE ***"

	#closed = set()
#
	#startState = problem.getStartState()
	#fringe = util.PriorityQueue()
	#fringe.push(PQNode(startState, [], 0),0)
#
	#while not fringe.isEmpty():
	#	node = fringe.pop()
	#	curr = node.state
	#	action = node.action
	#	cost = node.cost
		#currAction = action[0]
#
	#	if problem.isGoalState(curr):
	#		return action
	#	if not (curr in closed):
	#		closed.add(curr)
	#		succList = problem.getSuccessors(curr)
	#		for (successor, direction, currCost) in succList:
	#			fringe.push(PQNode(successor, action+[direction], cost+currCost), cost+currCost)
	#util.raiseNotDefined()

	closed = []

	startState = problem.getStartState()
	fringe = util.PriorityQueue()
	fringe.push(PQNode(startState, [], 0),0)

	while not fringe.isEmpty():
		node = fringe.pop()
		curr = node.state
		action = node.action
		cost = node.cost
		#currAction = action[0]

		if problem.isGoalState(curr):
			return action
		if not (curr in closed):
			closed.append(curr)
			succList = problem.getSuccessors(curr)
			for (successor, direction, currCost) in succList:
				fringe.push(PQNode(successor, action+[direction], cost+currCost), cost+currCost)
	util.raiseNotDefined()

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first."""
	"*** YOUR CODE HERE ***"

	closed = []

	startState = problem.getStartState()
	fringe = util.PriorityQueue()
	fringe.push(PQNode(startState, [], 0),0)

	while not fringe.isEmpty():
		node = fringe.pop()
		curr = node.state
		action = node.action
		cost = node.cost
		#currAction = action[0]

		if problem.isGoalState(curr):
			return action
		if not (curr in closed):
			closed.append(curr)
			succList = problem.getSuccessors(curr)
			for (successor, direction, currCost) in succList:
				estCost = heuristic(successor, problem)
				fringe.push(PQNode(successor, action+[direction], cost+currCost), estCost+cost+currCost)

	util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
