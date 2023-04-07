from attackerdefender.group import Group
from attackerdefender.agent import Agent

import uuid 
import random
import numpy as np
import collections

class Population(Group):
    def __init__(self, role, agents=[], allowed_types=[], create_agents=True, size=None):
        self.agents = agents
        self.generation = 0
        self.role = role
        self.allowed_types = allowed_types
        self.name = uuid.uuid4().hex[:4]
        for a in agents:
            a.population = self

        #self.history = []
        
        if create_agents and size and not agents:
            self.create_pop(size, allowed_types)

        if size and agents:
            print("Warning: Looks like you set custom agents and size at the same time. Size is ignored. You can add as many as agents")


    def __str__(self):
        pop_print = "Population " + self.name + " of " + self.role + " with " + str(dict(self.summarize_types()))
        # for a in self.agents:
        #     pop_print += str(a) + "\n"
        return pop_print

    def __repr__(self):
        return "Population "+ self.name

    def get_size(self):
        return len(self.agents)

    def get_payoffs(self):
        return np.asarray([x.payoff for x in self.agents])

    def get_coop(self):
        num_coop = 0
        for a in self.agents:
            num_coop += a.last_gen_c
        return num_coop 

    def get_def(self):
        num_def = 0
        for a in self.agents:
            num_def += a.last_gen_d
        return num_def

    def get_total_payoff(self):
        return sum(self.get_payoffs())
    
    def get_fitness(self, measure="basic", base_fitness=0):
        # Fitnesses always should be >0
        # Base fitness=0, harsh fitness run
        # Base fitness=1, payoffs doesn't matter at all
        if measure == "basic":
            payoffs = self.get_payoffs()
            tp = self.get_total_payoff()
            if np.any(payoffs < 0):
                raise ValueError('Some payoff values are smaller than zero')
            if np.all(payoffs == 0):
                print("Warning: all fitnesses are equal to zero.")
                score_fitness = np.asarray([1/len(self.agents) for a in self.agents])
                score_fitness_w_base = score_fitness
            else:
                score_fitness = np.asarray([a.payoff/tp for a in self.agents])
                # I don't exactly remember why I used this form of base fitness calc
                # although it makes a lot of sense. Check later
                score_fitness_w_base = score_fitness * (1 - base_fitness) + base_fitness


                score_fitness_w_base_sum = score_fitness_w_base.sum()
                score_fitness_w_base = score_fitness_w_base / score_fitness_w_base_sum
            return score_fitness_w_base


    def regenerate(self, n=None, r=None, base_fitness=0, mutation_rate=0, type="moran"):
        if n is None and r is None:
            print("No moran death date(r) or number (n) specified. Taking r=0.5")
            r=0.5
            n = round(self.get_size() * r)

        elif not (n is None) and (not r is None):
            print("Both death rate(r) and number(n) specified. Ignoring death rate")

        elif n is None and not r is None:
            n = round(self.get_size() * r)

        if type == "moran":
            selected_agents = random.choices(self.agents, self.get_fitness(base_fitness=base_fitness), k=n)
            agents_index_killed = random.sample(range(len(self.agents)),k=n)

            for i, a in enumerate(agents_index_killed):
                if mutation_rate > random.random():
                    self.agents[a] = Agent(random.choices(self.allowed_types)[0],0)
                    self.agents[a].population = self
                    self.agents[a].role = self.role
                    # I am not very sure about it but so far I defined
                    # a population role So in each population
                    # everybody has the same role (attacker/defender)
                    # and when mutation happens. The agents takes this role from the population
                else:
                    self.agents[a] = selected_agents[i].copy()

        self.next_generation()
        for a in self.agents:
            a.payoff = 0
            a.reset_counter()

    def summarize_types(self):
        types = [a.type for a in self.agents]
        counted = dict(collections.Counter(types))

        for t in self.allowed_types:
            if t not in counted:
                counted[t] = 0
        return counted

    def summarize_payoffs(self):
        total_payoff = dict()
        for t in self.allowed_types:
            current_t_payoff = [a.payoff for a in self.agents if a.type == t]
            total_payoff[t + "_payoff"] = sum(current_t_payoff)
        return total_payoff

    def print_summary(self):
        print(dict(self.summarize_types()))

    def create_pop(self, number_of_people, types, type_frequency= None):
        if not type_frequency:
            type_frequency = [1/len(types) for i in range(len(types))]

        self.agents = []
        for i in range(1,number_of_people + 1):
            self.agents.append(Agent(
                type=random.choices(types, type_frequency)[0], 
                payoff=0, 
                role=self.role))

        for a in self.agents:
            a.population = self


    def next_generation(self):
        self.generation += 1
