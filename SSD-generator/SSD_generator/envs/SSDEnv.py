import gym
from gym import spaces
from SSD import SSD
import numpy as np
import matplotlib.pyplot as plt 
import random 
class SSDEnv(gym.Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self):
    super(SSDEnv, self).__init__()
    # Define action and observation space
    # They must be gym.spaces objects
    # Example when using discrete actions:
    initial_heading = 0 #degree
    initial_speed = 400 #kts
    self.target_heading = random.choice(np.arange(-80,81,20))
    self.heading = initial_heading
    self.speed = initial_speed
    self.current_step = 0
    self.state, self.ssd_image_ds = SSD(300, 600, self.speed, self.heading, self.target_heading, 180, 30, 60).get_SSD(self.current_step, False, False)
    print('init?')
    self.reward = 0

    self.action_space = spaces.Discrete(19)
    # Example for using image as input:
    #print(np.shape(self.ssd_image_ds))
    self.observation_space = spaces.Box(0, 255, np.shape(self.state), dtype=np.uint8)
 
  
  def step(self, action):
    err_msg = "%r (%s) invalid" % (action, type(action))
    assert self.action_space.contains(action), err_msg
    actions = np.arange(-180,181,20)
    action_taken = actions[action]
    self.heading = action_taken 
    self.state, self.ssd_image_ds = SSD(300, 600, self.speed, self.heading, self.target_heading, 180, 30, 60).get_SSD(self.current_step, False, False)
    self.current_step += 1
    if 30<self.target_heading<60:
      min_distance_heading = 20
      #print(f'heading: {self.heading}, target: {self.target_heading}')
    else:
      min_distance_heading = 0
      #print(f'action: {action_taken} heading: {self.heading}, target: {self.target_heading}')
    self.delta_heading_new = abs(self.heading - self.target_heading)
    done1 = bool(self.heading == self.target_heading)
    done2 = bool(self.delta_heading_new == min_distance_heading)
    done = max([done1, done2])
    if 30<self.heading<60:
      self.reward = -30
    elif done:
      self.reward = 10
      print('DONNNEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
    elif self.current_step == 50:
      self.reward = -10
      done=True
    elif self.delta_heading_new < self.delta_heading_old:
      self.reward = -0.5
    else:
      #print('not done')
      self.reward = -1

    print(f'current timestep {self.current_step}, action {action}, reward {self.reward}')
    
    self.delta_heading_old = self.delta_heading_new  
    #print(self.reward)
    info = {}
    #self.ssd_image_ds.show()
    return self.state, self.reward, done, info
    # Execute one time step within the environment
    
  def reset(self):
    initial_heading = random.choice(np.arange(-80,81,20)) #degree
    initial_speed = 400 #kts
    #print('here')
    self.target_heading = random.choice(np.arange(-80,81,20))
    self.heading = initial_heading
    self.speed = initial_speed
    self.current_step = 0
    self.state, self.ssd_image_ds = SSD(300, 600, self.speed, self.heading, self.target_heading, 180, 30, 60).get_SSD(self.current_step, False, False)
    self.reward = 0
    self.delta_heading_old = abs(initial_heading-self.target_heading)
    # Reset the state of the environment to an initial state
    
    
    return self.state
  def render(self, mode='human', close=False):
    # Render the environment to the screen
    self.ssd_image_ds.show()
    
  def close(self):
    pass
    