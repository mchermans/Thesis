from gym.envs.registration import register

register(
    id='SSD_generator-v0',
    entry_point='SSD_generator.envs:SSDEnv',
)