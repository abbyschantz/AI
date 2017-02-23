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
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #loop through each iteration
        for i in range(self.iterations):
          #loop through each state in the states of that interaction
          for state in self.mdp.getStates():
            #initialize utility and rewards to 0
            utility = 0
            reward = 0
            #loop through each action of the possible actions for that state 
            for action in self.mdp.getPossibleActions(state):
              #set utility for this specific action to 0 
              currUtility = 0
              #loop through each of the state, prob pairs for the transition states
              for nextStateAndProb in self.mdp.getTransitionStatesAndProbs(state, action):
                nextState = nextStateAndProb[0]
                nextProb = nextStateAndProb[1]
                #get the reward for this current state
                currReward = self.mdp.getReward(state, action, nextState)
                #sum current utility with  the prob times the value of that state
                currUtility += nextProb*self.values[nextState]
              #if new utility is better, set that to utility and take its reward
              if currUtility >= utility:
                utility = currUtility
                reward = currReward
            #set value of the state to be the function (reward + (utility * gamma))
            self.values[state] = reward + utility*self.discount


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
        
        
        #initialze at 0
        value = 0
        #if self.mdp.isTerminal():
          #return getReward(state, action, state)

        #loop through the state and probability pairs for each transition state
        for nextStateAndProbs in self.mdp.getTransitionStatesAndProbs(state, action):
          currNextStateProb = nextStateAndProbs[1]
          currNextState = nextStateAndProbs[0]
          
          #currReward = self.mdp.getReward(state, action, currNextState)
          
          #currValue = self.values[currNextState] * currNextStateProb
          
          #set current value to be the prob times the value of the state 
          currValue = currNextStateProb * self.values[currNextState]
          #if this new value is greater than our old, set value to the new value
          if currValue >= value:
            value = currValue
        return value
        
        #gamma = self.discount



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

        #values (initialized) prints {'TERMINAL_STATE': 0} {(0, 0): 0, 'TERMINAL_STATE': 0}
        #values = self.values
        #return self.values
        #case for when a state has no available actions in an MDP 
        if len(self.mdp.getPossibleActions(state)) == 0:
          print "in base case, no possible actions"
          return None

        #initialize at 0 and None
        value = 0
        action = None

        #loop through each action of all possible actions for the given state
        for currAction in self.mdp.getPossibleActions(state):
          print "currAction is", currAction
          #set QValue using our computeQValueFromValues function
          QValue = self.computeQValueFromValues(state, currAction)
          print "QValue is", QValue
          #If that new value is greater than our previous value, 
          #we set value to this new value and action to that action
          if QValue >= value:
            value = QValue
            action = currAction
        print "best action is", action
        return action

        #util.raiseNotDefined()

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

