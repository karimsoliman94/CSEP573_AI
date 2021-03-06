"""
UW, CSEP 573, Win19
"""
from pomdp import POMDP
from offlineSolver import OfflineSolver
import numpy as np


class QMDP(OfflineSolver):
    def __init__(self, pomdp, precision = .001):
        super(QMDP, self).__init__(pomdp, precision)
        """
        ****Your code
        Remember this is an offline solver, so compute the policy here
        """
        self.states = pomdp.states
        self.actions = pomdp.actions
        self.values = np.zeros(len(self.states))
        self.qvalues = np.zeros((len(self.states), len(self.actions)))
        self.precision = precision
        self.discount = pomdp.discount
        self.T = pomdp.T
        self.reward = self.computeReward(pomdp)
        self.runValueIteration()

    def chooseAction(self, cur_belief):
        """
        ***Your code
        """
        q= np.dot(cur_belief,self.qvalues)
        return np.argmax(q)

    
    def getValue(self, belief):
        """
        ***Your code
        """
        q = np.dot(belief, self.qvalues)
        return np.max(q)
    
    def getActionAndValue(self,belief):
        q = np.dot(belief, self.qvalues)
        maxa = np.argmax(q)
        return maxa,q[maxa]

    """
    ***Your code
    Add any function, data structure, etc that you want
    """
    def runValueIteration(self):
        """while True:
            tempQ = np.dot(self.T,self.values)*self.discount
            tempQ = np.add(tempQ,self.reward)
            iterationQvalues = np.swapaxes(tempQ,0,1)

            iterationValues = np.max(iterationQvalues,axis=1)
            diff = []
            for i in range(len(self.values)):
                diff.append(abs(self.values[i] - iterationValues[i]))
            maxDiff = max(diff)

            self.values = iterationValues
            self.qvalues = iterationQvalues
            if maxDiff <= self.precision:
                break"""

        while True:
            iterationValues = np.zeros(len(self.states))
            iterationQvalues = np.zeros((len(self.states), len(self.actions)))
            for state in range(len(self.states)):
                maxValue = None
                for action in range(len(self.actions)):
                    tempQ = self.computeQValueFromValues(state, action)
                    iterationQvalues[state,action] = tempQ
                    if maxValue is None or tempQ>=maxValue:
                        maxValue = tempQ
                iterationValues[state] = maxValue

            diff = []
            for i in range(len(self.values)):
                diff.append(abs(self.values[i] - iterationValues[i]))
            maxDiff = max(diff)

            self.values = iterationValues
            self.qvalues = iterationQvalues
            if maxDiff <= self.precision:
                break


    def computeQValueFromValues(self, state, action):
        q = np.dot(self.T[action, state, :], self.values)
        return q * self.discount + self.reward[action, state]


    def computeReward(self, pomdp):
        temp = np.multiply(pomdp.R[:,:,:,0],pomdp.T)
        return np.sum(temp,2)

class MinMDP(OfflineSolver):
    
    def __init__(self, pomdp, precision = .001):
        super(MinMDP, self).__init__(pomdp, precision)
        """
        ***Your code 
        Remember this is an offline solver, so compute the policy here
        """
        self.actions = pomdp.actions
        self.discount = pomdp.discount
        self.reward = self.computeReward(pomdp)
        self.rmin = np.min(pomdp.R)
    
    def getValue(self, cur_belief):
        """
        ***Your code
        """
        actionValue = np.dot(cur_belief, self.reward)
        maxValue =  np.max(actionValue)
        return maxValue + (self.discount / (1-self.discount))* self.rmin


    def chooseAction(self, cur_belief):
        """
        ***Your code
        """  
        q=np.dot(cur_belief, self.reward)
        return np.argmax(q)

    """
    ***Your code
    Add any function, data structure, etc that you want
    """
    def computeReward(self, pomdp):
        temp = np.multiply(pomdp.R[:,:,:,0],pomdp.T)
        sum = np.sum(temp,2)
        return np.swapaxes(sum,0,1)