class Group:
    def __init__(self, agents):
        self.agents = agents
        
        # The history of the group is a dictionary
        # which the keys are player names and values
        # are the action history of the player
        for a in agents:
            a.group = self

    def __str__(self):
        return str(self.agents)

    def __repr__(self):
        return str(self.agents)

    def __iter__(self):
        return iter(self.agents)
    
    def __next__(self):
        return next(self.agents)

    def __getitem__(self, item):
        return self.agents[item]

    def get_size(self):
        return len(self.agents)

    def agents_except_this(self, this):
        # This function takes the agent object itself 
        agent_list_except_this = self.agents.copy()
        agent_list_except_this.remove(this)
        return agent_list_except_this

    def get_roles(self):
        roles = [self.agents[0].role, self.agents[1].role]
        return roles

