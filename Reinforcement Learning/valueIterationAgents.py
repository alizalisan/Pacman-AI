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
        for x in range(self.iterations):
            counter = util.Counter()
            states = self.mdp.getStates()
            for state in states:
                if self.mdp.isTerminal(state):
                    counter[state] = 0
                else:
                    actions = self.mdp.getPossibleActions(state)
                    values = []
                    for action in actions:
                        values.append(self.computeQValueFromValues(state, action))
                    counter[state] = max(values)

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
        stateNProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        qVal = 0
        for nextState, prob in stateNProbs:
            reward = self.mdp.getReward(state, action, nextState)
            qVal = qVal + prob * (reward + self.discount * self.values[nextState])
        return qVal
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None

        actions = self.mdp.getPossibleActions(state)
        correspondingVals = []

        for action in actions:
            correspondingVals.append(self.computeQValueFromValues(state, action))

        maxAction = actions[0]
        maximum = -9999999
        for i in range(len(correspondingVals)):
            if correspondingVals[i] > maximum:
                maximum = correspondingVals[i]
                maxAction = actions[i]

        return maxAction
        util.raiseNotDefined()

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
        numOfStates = len(states)
        index = 0

        for iteration in range(self.iterations):
            state  = states[index]
            if self.mdp.isTerminal(state):
                pass
            else:
                actions = self.mdp.getPossibleActions(state)
                values = []
                for action in actions:
                    values.append(self.computeQValueFromValues(state,action))
                self.values[state] = max(values)
            index = index + 1
            if(index == numOfStates):
                index = 0

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
        predecessors = {} #set

        states = self.mdp.getStates()
        for state in states:
            if not self.mdp.isTerminal(state):
                actions = self.mdp.getPossibleActions(state)
                for action in actions:
                    stateNProbs = self.mdp.getTransitionStatesAndProbs(state, action)
                    for sp in stateNProbs:
                        if sp[0] not in predecessors:
                            predecessors[sp[0]] = {state}
                        else:
                            predecessors[sp[0]].add(state) #adding multiple values/predecessors to one key/state

        priorQueue = util.PriorityQueue()
        states = self.mdp.getStates()
        for state in states:
            if not self.mdp.isTerminal(state):
                val = self.values[state]
                actions = self.mdp.getPossibleActions(state)
                maximum = -999999
                for action in actions:
                    qVal = self.computeQValueFromValues(state,action)
                    if maximum < qVal:
                        maximum = qVal
                diff = abs(val - maximum)
                priorQueue.update(state, -diff)
        
        for i in range(0,self.iterations):
            if priorQueue.isEmpty():
                break
            s = priorQueue.pop()
            if not self.mdp.isTerminal(s):
                actions = self.mdp.getPossibleActions(s)
                maximum = -999999
                for action in actions:
                    qVal = self.computeQValueFromValues(s,action)
                    if maximum < qVal:
                        maximum = qVal
                self.values[s] = maximum

            for p in predecessors[s]:
                val = self.values[p]
                actions = self.mdp.getPossibleActions(p)
                maximum = -999999
                for action in actions:
                    qVal = self.computeQValueFromValues(p,action)
                    if maximum < qVal:
                        maximum = qVal
                diff = abs(val - maximum)
                if(diff > self.theta):
                    priorQueue.update(p, -diff)                   
                            

