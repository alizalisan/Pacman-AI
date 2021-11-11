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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    #will have final path of direction for pacman
    path = []
    state1 =  problem.getStartState()
    #will hold nodes/coordinates that have been visited
    visitedNodes = []
    #will hold tuples of current state/coordinates and path/directions taken till that state by dfs
    stack = util.Stack()
    initialStateTuple = (state1, [])
    stack.push(initialStateTuple)

    while (not stack.isEmpty()):
        infoTuple = stack.pop()
        #current state popped from top of stack
        state = infoTuple[0]
        #directions taken till this state
        path = infoTuple[1]
        visitedNodes.append(state)
        if problem.isGoalState(state):
            break;
        else:
            for succ in problem.getSuccessors(state):
                if(succ[0] not in visitedNodes):
                    # print("Succ 0:", succ[0])
                    #state and direction for the current successor
                    State = succ[0]
                    Direction = succ[1]
                    #path till the successor which includes the previous recorded path
                    succPath = path + [Direction]
                    newTuple = (State, succPath)
                    stack.push(newTuple)        

    # print("Path:", path)
    # print("visitied:", visitedNodes)
    return path
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    #will have final path of directions for pacman
    path = []
    state =  problem.getStartState()
    #will hold nodes/coordinates that have been visited
    visitedNodes = []
    queue = util.Queue()
    initialStateTuple = (state, [])
    #will hold tuples of current state/coordinates and path/directions taken till that state by bfs
    queue.push(initialStateTuple)
    visitedNodes.append(state)

    while (not queue.isEmpty()):
        infoTuple = queue.pop()
        #current state popped from top of stack
        state = infoTuple[0]
        #directions taken till this state
        path = infoTuple[1]
        if problem.isGoalState(state):
                break;
        else:
            for succ in problem.getSuccessors(state):
                if(not succ[0] in visitedNodes):
                    #state and direction for the current successor
                    State = succ[0]
                    visitedNodes.append(State)
                    Direction = succ[1]
                    #path till the successor which includes the previous recorded path
                    succPath = path + [Direction]
                    newTuple = (State, succPath)
                    queue.push(newTuple) 

    return path
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    #will have final path of directions for pacman
    path = []
    state =  problem.getStartState()
    #will hold nodes/coordinates that have been visited
    visitedNodes = []
    priorQueue = util.PriorityQueue()
    initialStateTuple = (state, [])
    #will hold tuples of current state/coordinates and path/directions taken and priority is set to the of cost
    #of actions
    priorQueue.push(initialStateTuple, 0)

    while (not priorQueue.isEmpty()):
        infoTuple = priorQueue.pop()
        #current state popped from top of stack
        state = infoTuple[0]
        #directions taken till this state
        path = infoTuple[1]
        if problem.isGoalState(state):
            break;
        if state not in visitedNodes:
            visitedNodes.append(state) 
            for succ in problem.getSuccessors(state):
                if(not succ[0] in visitedNodes):
                    #state and direction for the current successor
                    State = succ[0]
                    Direction = succ[1]
                    #path till the successor which includes the previous recorded path
                    succPath = path + [Direction]
                    newTuple = (State, succPath)
                    priorQueue.push(newTuple, problem.getCostOfActions(succPath)) 

    return path
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
    #will have final path of directions for pacman
    path = []
    state =  problem.getStartState()
    #will hold nodes/coordinates that have been visited
    visitedNodes = []
    priorQueue = util.PriorityQueue()
    initialStateTuple = (state, [])
    #will hold tuples of current state/coordinates and path/directions taken and priority is set to the of cost
    #of actions
    priorQueue.push(initialStateTuple, 0)

    while (not priorQueue.isEmpty()):
        infoTuple = priorQueue.pop()
        #current state popped from top of stack
        state = infoTuple[0]
        #directions taken till this state
        path = infoTuple[1]
        if problem.isGoalState(state):
            break;
        if state not in visitedNodes:
            visitedNodes.append(state) 
            for succ in problem.getSuccessors(state):
                if(not succ[0] in visitedNodes):
                    #state and direction for the current successor
                    State = succ[0]
                    Direction = succ[1]
                    #path till the successor which includes the previous recorded path
                    succPath = path + [Direction]
                    newTuple = (State, succPath)
                    priorQueue.push(newTuple, problem.getCostOfActions(succPath)+heuristic(State, problem)) 

    return path

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
