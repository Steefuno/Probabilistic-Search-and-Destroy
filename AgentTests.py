import Agent1
import Agent2
import ImprovedAgent
import environment

agents = [Agent1, Agent2, ImprovedAgent]
scores = {}
count = 0

# Initialize scores
for agent_module in agents:
    scores[agent_module.__name__] = 0

# For 10 environments
for i in range(0, 10):
    env = environment.Environment()
    print(env)

    # Each 10 of each agent type will search
    for agent_module in agents:
        for i in range(0, 10):
            agent = agent_module.Agent(env)
            agent.run()
            scores[agent_module.__name__] += agent.total_distance + agent.searches
    count += 10
    print(scores)
    print()

# Change sums to averages
for agent_module in agents:
    scores[agent_module.__name__] /= count

print("Averages:")
print(scores)