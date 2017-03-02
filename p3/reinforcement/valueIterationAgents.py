# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
		"""
				* Please read learningAgents.py before reading this.*

				A ValueIterationAgent takes a Markov decision process
				(see mdp.py) on initialization and runs value iteration
				for a given number of iterations using the supplied
				discount factor.
		"""
		def __init__(self, mdp, discount = 0.9, iterations = 100):
				"""
					Your value iteration agent should take an mdp on
					construction, run the indicated number of iterations
					and then act according to the resulting policy.

					Some useful mdp methods you will use:
							mdp.getStates()
							mdp.getPossibleActions(state)
							mdp.getTransitionStatesAndProbs(state, action)
							mdp.getReward(state, action, nextState)
							mdp.isTerminal(state)
				"""
				self.mdp = mdp
				self.discount = discount
				self.iterations = iterations
				self.values = util.Counter() # A Counter is a dict with default 0
				self.runValueIteration()

		def runValueIteration(self):
				"*** YOUR CODE HERE ***"
				for i in range(self.iterations):
					counter = util.Counter()

					for state in self.mdp.getStates():

						if self.mdp.isTerminal(state):
							continue

						maxValue = float("inf")*-1

						for action in self.mdp.getPossibleActions(state):
							
							currValue = 0

							for nextStateAndProb in self.mdp.getTransitionStatesAndProbs(state, action):
								nextState = nextStateAndProb[0]
								nextProb = nextStateAndProb[1]

								currReward = self.mdp.getReward(state, action, nextState)
								currUtility = nextProb*self.values[nextState]
								currValue += nextProb * (currReward + (self.discount * self.values[nextState]))

							if currValue > maxValue:
								maxValue = currValue

						counter[state] += maxValue

					self.values = counter



		def getValue(self, state):
				"""
					Return the value of the state (computed in __init__).
				"""
				return self.values[state]


		def computeQValueFromValues(self, state, action):
				"""
					Compute the Q-value of action in state from the
					value function stored in self.values.
				"""
				"*** YOUR CODE HERE ***"

				value = 0

				for nextStateAndProbs in self.mdp.getTransitionStatesAndProbs(state, action):
					currNextStateProb = nextStateAndProbs[1]
					currNextState = nextStateAndProbs[0]
					currReward = self.mdp.getReward(state, action, currNextState)
					currValue = currNextStateProb * (currReward + (self.discount * self.values[currNextState]))
					value += currValue
				return value


		def computeActionFromValues(self, state):
				"""
					The policy is the best action in the given state
					according to the values currently stored in self.values.

					You may break ties any way you see fit.  Note that if
					there are no legal actions, which is the case at the
					terminal state, you should return None.

					HINT: Use the util.Counter class in util.py,
					which is a dictionary with a default value of zero.
					Methods such as totalCount should simplify your code.
					However, be careful with argMax:
					the actual argmax you want may be a key not in the counter!
				"""
				"*** YOUR CODE HERE ***"

				if len(self.mdp.getPossibleActions(state)) == 0:
					return None

				value = -1*float("inf")
				action = None

				for currAction in self.mdp.getPossibleActions(state):

					QValue = self.computeQValueFromValues(state, currAction)

					if QValue >= value:
						value = QValue
						action = currAction

				return action

		def getPolicy(self, state):
				return self.computeActionFromValues(state)

		def getAction(self, state):
				"Returns the policy at the state (no exploration)."
				return self.computeActionFromValues(state)

		def getQValue(self, state, action):
				return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
		"""
				* Please read learningAgents.py before reading this.*

				An AsynchronousValueIterationAgent takes a Markov decision process
				(see mdp.py) on initialization and runs cyclic value iteration
				for a given number of iterations using the supplied
				discount factor.
		"""
		def __init__(self, mdp, discount = 0.9, iterations = 1000):
				"""
					Your cyclic value iteration agent should take an mdp on
					construction, run the indicated number of iterations,
					and then act according to the resulting policy. Each iteration
					updates the value of only one state, which cycles through
					the states list. If the chosen state is terminal, nothing
					happens in that iteration.

					Some useful mdp methods you will use:
							mdp.getStates()
							mdp.getPossibleActions(state)
							mdp.getTransitionStatesAndProbs(state, action)
							mdp.getReward(state)
							mdp.isTerminal(state)
				"""
				ValueIterationAgent.__init__(self, mdp, discount, iterations)

		def runValueIteration(self):
				"*** YOUR CODE HERE ***"
				states = self.mdp.getStates()
				statesLen = len(states)
				i = 0
				currStateIteration = 0
				for i in range(self.iterations):

					if currStateIteration >= statesLen:
						currStateIteration = 0

					currState = states[currStateIteration]
					currStateIteration += 1
					
					if self.mdp.isTerminal(currState):
						continue

					maxValue = float("-inf")

					for action in self.mdp.getPossibleActions(currState):
						currValue = 0
						for nextStateAndProb in self.mdp.getTransitionStatesAndProbs(currState, action):
							nextState = nextStateAndProb[0]
							nextProb = nextStateAndProb[1]
							#print "before self.values[currState] is ", self.values[currState]
							currReward = self.mdp.getReward(currState, action, nextState)
							currValue += nextProb * (currReward + (self.discount * self.values[nextState]))
							#if self.values[currState] < currValue:
								#self.values[currState] = currValue
						if currValue > maxValue:
							maxValue = currValue
					self.values[currState] = maxValue
							#print "after self.values[currState] is ", self.values[currState]



					

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
		"""
				* Please read learningAgents.py before reading this.*

				A PrioritizedSweepingValueIterationAgent takes a Markov decision process
				(see mdp.py) on initialization and runs prioritized sweeping value iteration
				for a given number of iterations using the supplied parameters.
		"""
		def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
				"""
					Your prioritized sweeping value iteration agent should take an mdp on
					construction, run the indicated number of iterations,
					and then act according to the resulting policy.
				"""
				self.theta = theta
				ValueIterationAgent.__init__(self, mdp, discount, iterations)

		def runValueIteration(self):
				"*** YOUR CODE HERE ***"
