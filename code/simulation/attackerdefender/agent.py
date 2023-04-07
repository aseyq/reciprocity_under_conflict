import uuid
import random

class Agent:
    def __init__(self, 
                type, 
                payoff=0,  
                role=None, 
                name=None, 
                group=None, 
                population=None, 
                field=None):
                
        # Make sure the type is valid
        if type not in ["cooperator",
                        "defector",
                        "match",
                        "mismatch",
                        "prob05",
                        "tft",
                        ]:
            raise ValueError("type not defined")

        # If name is not given, generate one
        if name:
            self.name = name
        else:
            self.name = uuid.uuid4().hex[:10]


        self.payoff = payoff
        self.type = type
        self.field = field
        self.role = role
        self.group = group
        self.population = population
        self.last_gen_c = 0
        self.last_gen_d = 0
    
    def __str__(self):
    # printing an agent like: (myname P: 0 T: cooperator)
        return ("(" + self.name +
                " P: " + str(round(self.payoff, 2)) +
                " R: " + str(self.role) +
                " T: " + self.type + ")")

    def __repr__(self):
        return self.__str__()

    def reset_counter(self):
        self.last_gen_c = 0
        self.last_gen_d = 0

    def strategy(self, memory=1, discount=1):
        # Each agent have three prob. responses:
        #  - initial move
        #  - reaction to C
        #  - reaction to D
        #  - Format: [prob_c, prob_d]
        #  - For this case, p_d is a little unnecessary but good for 
        # generalizability
        if self.type == "defector":
            return dict(initial=[0,1], c=[0,1], d=[0,1])

        if self.type == "cooperator":
            return dict(initial=[1,0], c=[1,0], d=[1,0])

        if self.type == "prob05":
            return dict(initial=[0.5,0.5], c=[0.5,0.5], d=[0.5,0.5])

        if self.type == "match":
            return dict(initial=[0.5,0.5], c=[1,0], d=[0,1]) 

        if self.type == "mismatch":
            return dict(initial=[0.5,0.5], c=[0,1], d=[1,0])
        
        if self.type == "tft":
            return dict(initial=[1,0], c=[1,0], d=[0,1]) 
            


    def respond(self, others_previous_move=None, mistake_rate=0):
        if mistake_rate > 0:
            if mistake_rate > random.random():
                return random.choices(["c", "d"])[0]

        if others_previous_move==None or others_previous_move==[]:
            response = random.choices(["c", "d"], self.strategy()['initial'])[0]
        else:
            response = random.choices(["c", "d"], self.strategy()[others_previous_move])[0]
 
        if response == "c":
            self.last_gen_c += 1
        if response == "d":
            self.last_gen_d += 1
        
        return response

    def get_group_except_me(self):
        return self.group.agents_except_this(self)

    def get_group_history_except_me(self):
        return self.group.history_except_this(self)

    def get_group_history_last_n_except_me(self, n):
        return self.group.history_last_n_except_this(self, n)

    def append_to_my_history(self, item, generation=None):
        # Group history is based on the name
        if self.group:
            self.group.history[self.name].append(item)

    def earn(self, payoff):
        self.payoff += payoff

    def copy(self):
        return Agent(self.type, payoff=0, group=self.group, population=self.population, role=self.role)

    def index_in_population(self):
        if self.population: # Or maybe AttributeError
            try:
                return self.population.agents.index(self)
            except ValueError:
                return None
        else:
            return None
