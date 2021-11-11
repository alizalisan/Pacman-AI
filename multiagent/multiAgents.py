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


from typing import final
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

        "*** YOUR CODE HERE ***"

        # print("succ game state", str(successorGameState))
        # print("new pos", newPos)
        # print("new food", newFood.asList())
        # print("ghost states", newGhostStates)
        # print("scared time", newScaredTimes)

        finalScore = 0
        isNearer = 0

        #finding if distance to closest food is decreased
        distances = []
        currPos = currentGameState.getPacmanPosition()
        for food in newFood.asList():
            distances.append(manhattanDistance(food, currPos))
        if distances:
            currMinDist = min(distances)
        else:
            currMinDist = 0
        distances = []
        for food in newFood.asList():
            distances.append(manhattanDistance(food, newPos))
        if distances:
            newMinDist = min(distances)
        else:
            newMinDist = 0

        if currMinDist > newMinDist:
            isNearer = 1

        #see if the action gets pacman killed by a ghost or gets it too close
        for state in newGhostStates:
            distToGhost = manhattanDistance(newPos, state.getPosition())

        #do we get an increase in score
        scoreDiff = successorGameState.getScore() - currentGameState.getScore()

        if distToGhost <= 1:
            finalScore = finalScore - 90
        elif isNearer:
            finalScore = finalScore + 90
        elif scoreDiff > 0:
            finalScore = finalScore + 50
        else:
            finalScore = finalScore + 10
        
        return finalScore

        #return successorGameState.getScore()

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

        def maximizer(depth, state):
            legalMoves = state.getLegalActions(0)
            v = -999999
            #terminal condition
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            else:
                for move in legalMoves:
                    v = max(v, minimizer(depth, state.generateSuccessor(0, move), 1))
                return v

        def minimizer(depth, state, ghostIndex):
            legalMoves = state.getLegalActions(ghostIndex)
            #terminal condition
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            v = 999999
            if(ghostIndex < state.getNumAgents() - 1):
                for move in legalMoves:
                    v = min(v, minimizer(depth, state.generateSuccessor(ghostIndex, move), ghostIndex + 1))
                return v
            else:
                for move in legalMoves:
                    v = min(v, maximizer(depth + 1, state.generateSuccessor(ghostIndex, move)))
                return v

        #getting legal actions for Pacman
        nextStates = []
        legalMoves = gameState.getLegalActions(0)

        for move in legalMoves:
            nextStates.append(gameState.generateSuccessor(0, move))

        scores = []
        for state in nextStates:
            scores.append(minimizer(0, state, 1))

        #returning the move with maximum score
        return legalMoves[scores.index(max(scores))]

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def minimizer(state, ghostIndex, depth, alpha, beta):
            legalMoves = state.getLegalActions(ghostIndex)
            #terminal condition
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            v = 999999
            for move in legalMoves:
                succ = state.generateSuccessor(ghostIndex, move)

                if(ghostIndex < state.getNumAgents() - 1):
                    v = min(v, minimizer(succ, ghostIndex+1, depth, alpha, beta))
                else:
                    v = min(v, maximizer(succ, depth, alpha, beta))

                if v < alpha:
                    return v
                beta = min(beta, v)

            return v


        # agentIndex=0 for pacman
        def maximizer(state, depth, alpha, beta):
            legalMoves = state.getLegalActions(0)
            #terminal condition
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            v = -999999
            for move in legalMoves:
                succ = state.generateSuccessor(0, move)
                v = max(v, minimizer(succ, 1, depth+1, alpha, beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)

            return v

        legalMoves = gameState.getLegalActions(0)
        alpha = -999999
        beta = 999999
        #storing all the moves and their corresponding values in two lists
        Moves = []
        Values = []
        ghostIndex = 1
        for move in legalMoves:
            v = minimizer(gameState.generateSuccessor(0, move), ghostIndex, 1, alpha, beta)
            Moves.append(move)
            Values.append(v)

            if v > beta:
                return move
            alpha = max(v, alpha)

        #choosing the move with the max corresponding value
        maxValIndex = Values.index(max(Values))
        return Moves[maxValIndex]

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
        
        def maximizer(depth, state):
            legalMoves = state.getLegalActions(0)
            v = -999999
            #terminal condition
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            else:
                for move in legalMoves:
                    succ = state.generateSuccessor(0, move)
                    v = max(v, expectimax(depth + 1, succ, 1))
            return v


        def expectimax(depth, state, ghostIndex):
            legalMoves = state.getLegalActions(ghostIndex)
            #terminal check
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            v = 0
            for move in legalMoves:
                if(ghostIndex < state.getNumAgents() - 1):
                    succVal = expectimax(depth, state.generateSuccessor(ghostIndex, move), ghostIndex + 1)
                else:
                    succVal = maximizer(depth, state.generateSuccessor(ghostIndex, move))
                v = v + (succVal*(1/len(legalMoves))) #giving equal probability
            
            return v

        #getting legal actions for Pacman
        legalMoves = gameState.getLegalActions(0)
        Moves = []
        Values = []

        for move in legalMoves:
            Moves.append(move)
            Values.append(expectimax(1, gameState.generateSuccessor(0, move), 1))

        #choosing the move with the max corresponding value
        maxValIndex = Values.index(max(Values))
        return Moves[maxValIndex]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    currPos = currentGameState.getPacmanPosition()
    currFood = currentGameState.getFood()
    currGhostPositions = currentGameState.getGhostPositions()
    currGhostStates = currentGameState.getGhostStates()

    #calculating the distance to the closest food
    currMinDist = 0
    distances = []
    for food in currFood.asList():
        distances.append(util.manhattanDistance(currPos, food))
    if distances:
        currMinDist = min(distances)
    else:
        currMinDist = 1

    #calculating the total distance to all ghosts 
    ghostDistances = 1
    for ghost in currGhostPositions:
        distance = util.manhattanDistance(currPos, ghost)
        ghostDistances = ghostDistances + distance

    #calculating the total scared time left for all ghosts
    scaredTime = 0
    for ghost in currGhostStates:
        scaredTime = scaredTime + ghost.scaredTimer

    #calculating total number of capsules left
    newCapsule = currentGameState.getCapsules()
    numberOfCapsules = len(newCapsule)

    #combining all the above calculations for final score
    return currentGameState.getScore() + (1/currMinDist) - (1/ghostDistances) + numberOfCapsules + scaredTime

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
