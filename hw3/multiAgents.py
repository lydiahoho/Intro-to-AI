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
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex): //(pacman,ghosr1,ghost2)
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action): 
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        """
        1. call minimax function 
        2. depth: the current depth of the tree 
           agentIndex: index of the current agent     
        3. Roll over agent index and increase current depth if all agents have finished 
        4. Return the value of evaluationFunction if max depth is reached
        5. If it is max (pacman) turn:
            Get the maximun score of successor
            Increase agent_index by 1 as it will be next player's (ghost) turn 
            Pass the new game state generated by pacman's action
            Update the best score and action
        6. If it is min (ghost) turn:
            Get the minimun score of successor
            Increase agent_index by 1 as it will be next player's (ghost or pacman) turn 
            Pass the new game state generated by ghost's action
            Update the best score and action
        7. If it is a leaf state with no successor states, return the value of evaluationFunction  
        8. Return the best_action and best_score
        9. getAction function retuen the action
        """
        action, score = self.minimax(0, 0, gameState)
        return action
    def minimax(self, depth, agentIndex, gameState):
        if agentIndex>= gameState.getNumAgents():
            agentIndex=0
            depth+=1
        if(depth==self.depth):
            return None,self.evaluationFunction(gameState)
        
        best_action, best_score = None, None
        actions= gameState.getLegalActions(agentIndex)
        if agentIndex==0:
            for action in actions:
                next= gameState.getNextState(agentIndex, action)
                _,score=self.minimax(depth, agentIndex+1, next)
                if best_score==None or score>best_score :
                    best_score=score
                    best_action=action
        else:
            for action in actions:
                next= gameState.getNextState(agentIndex, action)
                _,score=self.minimax(depth, agentIndex+1, next)
                if best_score==None or score<best_score :
                    best_score=score
                    best_action=action 
        if best_score is None:
            return  None,self.evaluationFunction(gameState)          
        return best_action, best_score
    
        raise NotImplementedError("To be implemented")
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        """
        1. Same as minimax
        2. Add alpha and beta
            alpha: The best choice (highest-value) we have found so far along the path of Maximizer.
                   The initial value of alpha is -inf.
            beta: The best choice (lowest-value) we have found along the path of Minimizer. 
                  The initial value of beta is inf.
        3. Prune the tree if alpha is greater than beta
        """
        action, score = self.AlphaBeta(0, 0, gameState, -float('inf'), float('inf'))
        return action
    def AlphaBeta(self, depth, agentIndex, gameState, alpha, beta):
        if agentIndex>= gameState.getNumAgents():
            agentIndex=0
            depth+=1
        if(depth==self.depth):
            return None,self.evaluationFunction(gameState)
        
        best_action, best_score = None, None
        actions= gameState.getLegalActions(agentIndex)
        if agentIndex==0:
            for action in actions:
                next= gameState.getNextState(agentIndex, action)
                _,score=self.AlphaBeta(depth, agentIndex+1, next, alpha, beta)
                if best_score==None or score>best_score :
                    best_score=score
                    best_action=action
                if score>alpha:
                    alpha=score
                if alpha>beta:
                    break
        else:
            for action in actions:
                next= gameState.getNextState(agentIndex, action)
                _,score=self.AlphaBeta(depth, agentIndex+1, next, alpha, beta)
                if best_score==None or score<best_score :
                    best_score=score
                    best_action=action 
                if score<beta:
                    beta=score
                if alpha>beta:
                    break
        if best_score is None:
            return  None,self.evaluationFunction(gameState)          
        return best_action, best_score
        raise NotImplementedError("To be implemented")
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        """
        1. Same as minimax, but changes the "mini" part to "expect" 
        2. If it is chance (ghost) turn:
           The score is expected value of its children
           The best action is chooseed uniformly at random  
        """
        action, score = self.Expectimax(0, 0, gameState)
        return action
    def Expectimax(self, depth, agentIndex, gameState):
        if agentIndex>= gameState.getNumAgents():
            agentIndex=0
            depth+=1
        if(depth==self.depth):
            return None,self.evaluationFunction(gameState)
        
        best_action, best_score = None, None
        actions= gameState.getLegalActions(agentIndex)
        if agentIndex==0:
            for action in actions:
                next= gameState.getNextState(agentIndex, action)
                _,score=self.Expectimax(depth, agentIndex+1, next)
                if best_score==None or score>best_score :
                    best_score=score
                    best_action=action
                
        else:
            n=len(actions)
            for action in actions:
                next= gameState.getNextState(agentIndex, action)
                _,score=self.Expectimax(depth, agentIndex+1, next)
                if best_score==None:
                    best_score=0
                best_score+=score*1/n    
                best_action=action 
                
        if best_score is None:
            return  None,self.evaluationFunction(gameState)          
        return best_action, best_score
        raise NotImplementedError("To be implemented")
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    """
    1. Calculating distance to the closest food pellet
    2. Calculating the distances from pacman to the ghosts. 
       Also, checking for the ghosts around pacman (at distance of 1).
    3. Obtaining the number of capsules available
    4. Combination of the above calculated metrics.
    """
    position= currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    ghostState=currentGameState.getGhostPositions()
    capsules = currentGameState.getCapsules()
    min_food= -1
    for food in foods:
        distance = manhattanDistance(position, food)
        if  distance < min_food  or min_food == -1:
            min_food = distance
    ghost_dis = 1
    scared_ghost= 0
    for ghost in ghostState:
        distance = manhattanDistance(position, ghost)
        ghost_dis += distance
        if distance <= 1:
            scared_ghost += 1
    capsule = len(capsules)
    return currentGameState.getScore() + (1 / float(min_food)) - (1 / float(ghost_dis)) - scared_ghost - capsule
    raise NotImplementedError("To be implemented")
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
