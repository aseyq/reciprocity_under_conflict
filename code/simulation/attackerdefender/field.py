import uuid
import numpy as np
from attackerdefender.group import Group
from attackerdefender.game import Game
import pandas as pd

class Field:
    def __init__(self, populations=[]):
        # I disabled creating a field without population but that can be re-enabled
        self.agents = []
        self.groups = []
        self.populations = []
        self.generation = 0
        self.all_types = set()
        self.simulation_parameters = None

        if populations:
            for pop in populations:
                self.add_population(pop)

    def __str__(self):
        pop_print = ""
        for a in self.agents:
            pop_print += str(a) + "\n"
        return pop_print

    def __repr__(self):
        pop_print = ""
        for a in self.agents:
            pop_print += str(a) + "\n"
        return pop_print


    def get_size(self):
        return len(self.agents)

    def get_all_types(self):
        return sorted(list(self.all_types))

    def add_population(self, pop):
        if not pop in self.populations:
            self.populations.append(pop)
            self.all_types = self.all_types.union(set(pop.allowed_types))
            for a in pop:
                a.field = self
                self.agents.append(a)

        else:
            print("population is already in the field")


    def match_groups(self, method="random"):
        self.groups = []

        if method == "random":
            # create a random index of matching
            matching_index = np.random.permutation(self.get_size())
            # divide it into two and match indexes
            matching_index_pairs = zip(matching_index[:self.get_size()//2],matching_index[self.get_size()//2:])

            # create the matching groups from these indexes
            matching = []
            for i,j in matching_index_pairs:
                matching.append([self.agents[i], self.agents[j]])

            self.matching = matching

            for m in self.matching:
                self.groups.append(Group([m[0], m[1]]))

        if method == "cross-random":
            if not self.populations[0].get_size() ==  self.populations[1].get_size():
                raise ValueError('the size of the two populations don\'t match: ' +
str(self.populations[0].get_size())  + " vs " +  str(self.populations[1].get_size()))

            matching_index_p1 = np.random.permutation(self.populations[0].get_size())
            matching_index_p2 = np.random.permutation(self.populations[1].get_size())
            matching_index_pairs = zip(matching_index_p1, matching_index_p2)

            matching = []
            for i,j in matching_index_pairs:
                
                matching.append([self.populations[0].agents[i], self.populations[1].agents[j]])

            self.matching = matching

            for m in self.matching:
                self.groups.append(Group([m[0], m[1]]))


    def simulate(self, 
                sim_no, 
                num_generations, 
                prob_rep, 
                moran_r, 
                base_fit, 
                mutation_rate, 
                mistake_rate, 
                popstr, 
                totalsize,  
                verbose=False):
        sim_code = uuid.uuid4().hex[:20]


        for gen in range(0,num_generations):
            self.generation = gen

            number_of_encounters = np.random.geometric(p=1-prob_rep, size=num_generations)
            self.match_groups()

            for g in self.groups:
                current_game = Game(g)
                current_game.play(repeat=number_of_encounters[gen], mistake_rate=mistake_rate)


            for p in self.populations:
                type_summary = dict(p.summarize_types())
                payoff_summary = dict(p.summarize_payoffs())

                dataline = dict(
                    sim_code=sim_code, # inside
                    sim_no=sim_no, # arg
                    population=p.role, 
                    generation=p.generation,
                    totalsize=totalsize, # arg
                    size=p.get_size(),
                    num_generations=num_generations, # arg
                    prob_rep=prob_rep, #arg
                    moran_r=moran_r, #arg
                    base_fit=base_fit, #arg
                    mutation_rate=mutation_rate, #arg
                    popstr=popstr,# arg
                    mistake_rate=mistake_rate,
                    num_coop = p.get_coop(),
                    num_def = p.get_def(),
                    **type_summary,
                    **payoff_summary
                )

                yield dataline


            for p in self.populations:
                p.regenerate(r=moran_r, base_fitness=base_fit, mutation_rate=mutation_rate)
                if verbose:
                    print(p)
                    print("\n")
            if verbose:
                print("-" * 30)
            self.__init__(populations=self.populations)  # This is needed so agents are cleaned.


    def get_header_columns(self):
        # Rewriting it
        all_types = self.get_all_types()
        payoff_columns = [a + "_payoff" for a in all_types]
        

        # This is where we set the order 
        data_cols = ['sim_code',
                     'sim_no',
                     'population',
                     'generation',
                     'totalsize',
                     'size',
                     'num_generations',
                     'prob_rep',
                     'moran_r',
                     'base_fit',
                     'mutation_rate',
                     'popstr',
                     'mistake_rate',
                     'num_coop',
                     'num_def',
                     ] + all_types + payoff_columns

        return data_cols
