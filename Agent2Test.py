import Agent2
import environment

score = (0, 0)

for i in range(0, 50):
    env = environment.Environment()
    agent = Agent2.Agent(env)
    agent.run()

    score = (
        score[0] + agent.total_distance + agent.searches,
        score[1] + 1
    )
    print(agent)

print(score)
print(score[0] / score[1])