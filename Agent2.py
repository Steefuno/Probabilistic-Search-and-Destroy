import random
import environment

class Agent:
    # Creates an Agent instance
    def __init__(self, env):
        self.env = env # The environment this agent must search
        self.total_distance = 0 # The total distance this agent has travelled
        self.searches = 0 # The number of searches this agent has done
        self.position = ( # The current position of the agent
            random.randrange(0, env.d-1),
            random.randrange(0, env.d-1)
        )

        self.cells = {} # Information on each cell
        self.observations_product = 1 # Subset of triggered search event of all search events

        self.env_size = env.d * env.d
        # Initialize each cells' data
        for y in range(0, env.d):
            for x in range(0, env.d):
                position = (y, x)
                self.cells[position] = {
                    "fail_probability" : env.environment_data[y][x].false_negative, # The probability that the target will not be found if this cell has the target
                    "belief" : 1 / self.env_size, # The belief that this cell has the target
                    "searches" : 0, # The number of times this cell has been searched
                }
        return

    # Iteratively search cells until the target is found
    def run(self):
        while self.step() == False:
            pass
        return

    # Finds the best cell to find the target, moves to the cell, then searches
    def step(self):
        # Find the best cell to find the target
        best_cell = self.find_target()
        # Update total distance and position based on the new best cell
        self.total_distance += best_cell[2]
        self.position = best_cell[0]
        # Searches the current cell and update beliefs
        return self.search()

    # Finds the current cell on the env_size with the highest probability of finding the target
    def find_target(self):
        best_cell = (None, -1, None) # (position, find_probability, distance from agent)
        # For each cell, find cell with the best belief
        for (cell_position, cell_data) in self.cells.items():
            # Get the probability that searching the new cell will yield the target
            find_probability = cell_data["belief"] * (1 - self.cells[cell_position]["fail_probability"])
            # If the best cell's belief matches with another, get closest
            if find_probability == best_cell[1]:
                # If the best cell's distance is not stored, calculate and store
                if best_cell[2] == None:
                    best_cell = (
                        best_cell[0],
                        best_cell[1],
                        self.distance_to(best_cell[0])
                    )
                # If the new cell is closer, replace best cell
                new_distance = self.distance_to(cell_position)
                if new_distance < best_cell[2]:
                    best_cell = (cell_position, find_probability, new_distance)
            # If the new cell has a better belief, replace best cell
            elif find_probability > best_cell[1]:
                best_cell = (cell_position, find_probability, None)

        # Get position if not found yet
        if best_cell[2] == None:
            best_cell = (
                best_cell[0],
                best_cell[1],
                self.distance_to(best_cell[0])
            )
        return best_cell

    # Searches the current position and updates beliefs
    def search(self):
        self.searches += 1
        # If target is found, return True
        if self.env.query(self.position):
            return True
        # If target is not found, update beliefs and return False
        else:
            self.update_beliefs(self.position)
            return False

    # Update beliefs of the position failed to search in and all other positions
    def update_beliefs(self, failed_search_position):
        cell_data = self.cells[failed_search_position]

        # Get the data to calculate the new belief of the failed cell
        old_belief = cell_data["belief"]
        fail_probability = cell_data["fail_probability"]
        target_probability = 1 / self.env_size
        not_target_probability = 1 - target_probability

        # Get the amount of belief to assign to the failed cell
        new_belief = (
            (old_belief * fail_probability) /
            ((fail_probability * target_probability) + (not_target_probability))
        )

        # Get the amount of belief to add to all cells except the failed cell
        change_in_belief = new_belief - old_belief
        distributed_belief = change_in_belief / (self.env_size - 1)

        for (cell_position, cell_data) in self.cells.items():
            if cell_position == failed_search_position:
                cell_data["belief"] = new_belief
            else:
                cell_data["belief"] += distributed_belief
        return

    # Finds the current distance to a select cell using manhattan distance
    def distance_to(self, cell_position):
        return abs(self.position[0] - cell_position[0]) + abs(self.position[1] - cell_position[1])

    # tostring
    def __str__(self):
        return "Target was found at {}. The agent moved {}x and searched {}x.".format(self.position, self.total_distance, self.searches)