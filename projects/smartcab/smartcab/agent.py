import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import operator
import csv

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.Q_chart = {}
        self.rewards_table = [('positive rewards','negative rewards','steps','Succeed')]
        self.positiveRewards = 0
        self.negativeRewards = 0
        self.done = False
        self.steps = 0 # number of steps in each trial
        self.alpha = 0.9 # learning rate
        self.gamma = 0.2 # discount factor
        self.epsilon = 0.5 # probability of random action
        self.count = 1

    def reset(self, destination=None):
        self.planner.route_to(destination)
        self.rewards_table.append((self.positiveRewards,self.negativeRewards,self.steps, self.done))
        self.positiveRewards = 0
        self.negativeRewards = 0
        self.done = False
        self.steps = 0
        self.count += 1
        self.epsilon = 0.5/self.count
        # TODO: Prepare for a new trip; reset any variables here, if required


    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (inputs['light'],inputs['oncoming'],inputs['left'],inputs['right'],self.next_waypoint)
        
        # TODO: Select action according to your policy
        if random.random() < self.epsilon: # explore a little
            action = self.select_action(self.state, randomnize = True)
        else:
            action =  self.select_action(self.state, randomnize = False)

        self.steps += 1


        # Execute action and get reward
        reward = self.env.act(self, action)
        self.done = self.env.done
        if reward > 0:
            self.positiveRewards += reward
        else:
            self.negativeRewards += reward


        # TODO: Learn policy based on state, action, reward
        inputs = self.env.sense(self)
        self.next_waypoint = self.planner.next_waypoint()
        self.next_state = (inputs['light'],inputs['oncoming'], inputs['left'], inputs['right'], self.next_waypoint)
        self.Q_chart[self.state][action] = (1-self.alpha)*self.Q_chart[self.state][action]+self.alpha*(reward+self.gamma*self.max_Q(self.next_state))
        #a = self.Q_chart[self.state][action]

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

    def select_action(self, state, randomnize = False):
        if not self.Q_chart.has_key(state):
            self.Q_chart[state] = {None:1, 'forward':1, 'left':1, 'right':1}
            return random.choice([None,'forward','left','right'])
        elif randomnize:
            return random.choice([None,'forward','left','right'])
        else:
            return max(self.Q_chart[state].iteritems(), key=operator.itemgetter(1))[0]

    def max_Q (self, state):
        if not self.Q_chart.has_key(state):
            self.Q_chart[state] = {None:1, 'forward':1, 'left':1, 'right':1}
        return max(self.Q_chart[state].values())




def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line
    

    with open("output.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(a.rewards_table)


if __name__ == '__main__':
    run()
