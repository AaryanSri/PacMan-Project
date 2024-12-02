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
from game import Directions
from typing import List

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




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
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
    stack = util.Stack()               
    stack.push(problem.getStartState())


    # keep track of visited here
    path=[] 
    visited = set() 

    tempPath=util.Stack()           
    curr = stack.pop()


    while curr and not problem.isGoalState(curr):
        if curr not in visited:
            visited.add(curr)
            children = problem.getSuccessors(curr)

            for next,direction, cost in children:
                stack.push(next)
                direction = [direction]  # convert
                temp = []
                temp += path + direction

                tempPath.push(temp)

        curr = stack.pop()
        path = tempPath.pop()

    return path

   # util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    queue = util.Queue()
    queue.push(problem.getStartState())


    path = []
    visited = set()
    tempPath = []
    prev = util.Queue()
    curr = queue.pop()

    if problem.isGoalState(curr):
        return path

    while curr and not problem.isGoalState(curr):
        if curr not in visited:
            children = problem.getSuccessors(curr)

            for next, direction, cost in children:
                queue.push(next)
                temp2 = []
                direction = [direction]
                tempPath = path + direction
                prev.push(tempPath)

            visited.add(curr)
        curr = queue.pop()
        path = prev.pop()

    return path


def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
   # path = []
   # visited = set()
   # curr = problem.getStartState()
    #queue = util.PriorityQueue()

    path = []
    visited = set()
    queue = util.PriorityQueue()
    curr = problem.getStartState()
    if (problem.isGoalState(curr)):
        return path
    
    temp = []
    tempPath = util.PriorityQueue()
    queue.push(curr, 0)

    curr = queue.pop()
    while curr and not problem.isGoalState(curr):

        if curr not in visited:
            children = problem.getSuccessors(curr)
            visited.add(curr)

            for next, direction, cost in children:
                direction = [direction]
                temp = path + direction
                # calculate cost of path so far
                cost = problem.getCostOfActions(temp)
                if (next not in visited):

                    queue.push(next, cost)
                    tempPath.push(temp, cost)
                        
        curr = queue.pop()
        path = tempPath.pop()
    return path
    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    queue = util.PriorityQueue()
    path = {}
    curr = problem.getStartState()

    if (problem.isGoalState(curr)):
        return path
    recentCost = {}
    recentCost[curr] = 0
    path[curr] = []

    queue.push(curr, 0)
    curr = queue.pop()
    while curr and not problem.isGoalState(curr): 

        children = problem.getSuccessors(curr)
        for child, direction,cost in children:
            # recalculate
            newCost = recentCost[curr] + cost
            if child not in recentCost or newCost < recentCost[child]:
                recentCost[child] = newCost
                newCost2 = newCost + heuristic(child, problem)
                queue.push(child, newCost2)
                direction = [direction]
                path[child] = path[curr] + direction
        curr = queue.pop()

    return path[curr]  

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
