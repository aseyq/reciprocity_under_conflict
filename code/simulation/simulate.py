from datetime import datetime
from time import time
import numpy as np

from terminalcolors import c 

from attackerdefender.simulation import Simulation 

output_folder = "../../output/simulationdata"

start_time = time()
popstr = ["onlydefender", "attackermin", "equal", "attackermaj", "onlyattacker"]

prob_reps = np.append(np.arange(0.6, 0.96, 0.05), 0.99)

## baseline parameters
mistake_rates = [0.005]
population_sizes = [240]
base_fitnesses = [0.01]
mutation_rates = [0.001]
moran_rs = [0.5]

num_generations = 300 # 1000 in the original
num_sims_each = 12 ## 1000 in the original

## full parameters 
# mistake_rates = [0.005, 0.05]
# population_sizes = [240, 120, 60]
# base_fitnesses = [0.1, 0.01]
# mutation_rates = [0.01, 0.001]
# moran_rs = [0.5]

# you can change the number of cores used according to the your 
# machine specifications
num_cores =  8

## Here we loop for different parameters
currentsim = 0
for ps in popstr:
    for pr in prob_reps:
        for mis in mistake_rates:
            for bf in base_fitnesses:
                for mr in mutation_rates:
                    for mor in moran_rs:
                        for popsize in population_sizes:
                            datetimenow=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                            currentsim += 1

                            totalsims = len(popstr) * len(prob_reps) * len(mistake_rates) * len(base_fitnesses) * len(mutation_rates) * len(moran_rs) * len(population_sizes)

                            print(f"{c.YELLOW}{datetimenow} {c.E}- {c.GREEN} running {c.E}{currentsim}/{totalsims} - {c.B} popstr: {c.E}{ps} {c.B}prob rep:{c.E}{pr} {c.B}mistake:{c.E}{mis} {c.B}basefit:{c.E}{bf} {c.B}mutation:{c.E}{mr} {c.B}moran:{c.E}{mor} {c.B}popsize:{c.E}{popsize}")
                            
                            print("The number of cores: {}".format(num_cores))

                            Simulation.simulate_n_csv_par(output_folder=output_folder+ "/",  # without the ending slash
                                               num_cores=num_cores, 
                                               num_iter=num_sims_each, 
                                               num_gen=num_generations,
                                               popstr=ps,
                                               prob_rep=pr, 
                                               mistake_rate=mis,
                                               pop_size=popsize,
                                               base_fit=bf,
                                               mutation_rate=mr,
                                               moran_r=mor)
                            

print("DONE")
print("(running time: {0:.1f}s)".format(time() - start_time))

