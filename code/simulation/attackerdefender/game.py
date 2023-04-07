
class Game:
    def __init__(self, group):
        self.actions = ["c", "d"]
        self.group = group
        self.roles = self.group.get_roles()
        self.previous_actions = [None, None]


    def get_payoffs(self, actions):
        if self.roles == ['defender','defender']:
            # Assurance Game
            if actions == ["c", "c"]:
                return (2, 2)
         
            if actions == ["c", "d"]:
                return (0, 1)

            if actions == ["d", "c"]:
                return (1, 0)

            if actions == ["d", "d"]:
                return (1, 1)

        if self.roles == ['attacker','attacker']:
            # Chicken Game
            if actions == ["c", "c"]:
                return (1, 1)
         
            if actions == ["c", "d"]:
                return (1, 2)

            if actions == ["d", "c"]:
                return (2, 1)

            if actions == ["d", "d"]:
                return (0, 0)

        if self.roles == ['attacker','defender']:
            # Attacker Defender P1 is attacker
            if actions == ["c", "c"]:
                return (1, 2)
         
            if actions == ["c", "d"]:
                return (1, 1)

            if actions == ["d", "c"]:
                return (2, 0)

            if actions == ["d", "d"]:
                return (0, 1)

        if self.roles == ['defender','attacker']:
            # Attacker Defender P1 is defender
            if actions == ["c", "c"]:
                return (2, 1)
         
            if actions == ["d", "c"]:
                return (1, 1)

            if actions == ["c", "d"]:
                return (0, 2)

            if actions == ["d", "d"]:
                return (1, 0)

        if self.roles == ['prisoner','prisoner']:
            
            if actions == ["c", "c"]:
                return (2, 2)
         
            if actions == ["d", "c"]:
                return (3, 0)

            if actions == ["c", "d"]:
                return (0, 3)

            if actions == ["d", "d"]:
                return (1, 1)


    def previous_action_of_other(self, player):
        player_index = self.group.agents.index(player)
        others_previous_action = self.previous_actions[:player_index] + self.previous_actions[player_index+1:]
        # TODO add exception for -not in list
        # it should return a list for multiplayer but for my purpose, ill take the first element
        return others_previous_action[0]


    def play(self, repeat=1, verbose=False, mistake_rate=0):
        for period in range(0,repeat):
            # first person always first mover?
            actions = [p.respond(self.previous_action_of_other(p), mistake_rate=mistake_rate) for p in self.group.agents]
            payoffs = self.get_payoffs(actions)
            if verbose:
                print('-' * 20)
                print('previous_actions:', self.previous_actions)
                print('group:', self.group)
                print('actions:',actions)
                print('payoffs:',payoffs)

            for i, p in enumerate(self.group.agents):
                p.payoff += payoffs[i]
            if verbose:
                print('new_group:', self.group)
            self.previous_actions = actions.copy()
