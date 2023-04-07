from datetime import datetime
from joblib import Parallel, delayed
import pandas as pd
from attackerdefender.population import Population
from attackerdefender.field import Field

nowname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

all_types = ["cooperator",
            "defector",
            "match",
            "mismatch",
            "prob05",
            ]


class Simulation:
   
    def simulate_once_df(sim_no, num_gen, popstr, prob_rep, mistake_rate, pop_size, base_fit, mutation_rate, moran_r):
        
        parameter_dict = dict(
            num_generations = num_gen,
            prob_rep = prob_rep,
            moran_r = moran_r,
            base_fit = base_fit, 
            mutation_rate = mutation_rate,
            mistake_rate = mistake_rate,
            popstr = popstr,
            totalsize = pop_size,
        )

        df = pd.DataFrame()

        if popstr == "prisoner":
            pop1_size=pop_size
            pop1 = Population(role="prisoner", size=pop1_size, allowed_types=all_types)
            gamefield = Field(populations=[pop1])

        if popstr == "onlyattacker":
            pop1_size=pop_size
            pop1 = Population(role="attacker", size=pop1_size, allowed_types=all_types)
            gamefield = Field(populations=[pop1])

        if popstr == "onlydefender":
            pop1_size=pop_size
            pop1 = Population(role="defender", size=pop1_size, allowed_types=all_types)
            gamefield = Field(populations=[pop1])

        if popstr == "attackermaj":
            pop1_size=int(pop_size * 0.75)
            pop2_size=int(pop_size * 0.25)
            pop1 = Population(role="attacker", size=pop1_size, allowed_types=all_types)
            pop2 = Population(role="defender", size=pop2_size, allowed_types=all_types)
            gamefield = Field(populations=[pop1, pop2])

        if popstr == "attackermin":
            pop1_size=int(pop_size * 0.25)
            pop2_size=int(pop_size * 0.75)
            pop1 = Population(role="attacker", size=pop1_size, allowed_types=all_types)
            pop2 = Population(role="defender", size=pop2_size, allowed_types=all_types)
            gamefield = Field(populations=[pop1, pop2])

        if popstr == "equal":
            pop1_size=int(pop_size * 0.5)
            pop2_size=int(pop_size * 0.5)
            pop1 = Population(role="attacker", size=pop1_size, allowed_types=all_types)
            pop2 = Population(role="defender", size=pop2_size, allowed_types=all_types)
            gamefield = Field(populations=[pop1, pop2])

        
        sim = gamefield.simulate(sim_no=sim_no, **parameter_dict)

        for _ in sim:
            _df = pd.DataFrame(_, index=[0])
            df = pd.concat([df, _df])

        return df


    def simulate_n_df_par(num_cores, num_gen, num_iter, popstr, prob_rep, mistake_rate, pop_size, base_fit, mutation_rate, moran_r):
        output = Parallel(n_jobs=num_cores)(delayed(Simulation.simulate_once_df)(sim_no=i,
                                            num_gen=num_gen,
                                            popstr=popstr,
                                            prob_rep=prob_rep,
                                            mistake_rate=mistake_rate,
                                            pop_size=pop_size,
                                            base_fit=base_fit,
                                            mutation_rate=mutation_rate,
                                            moran_r=moran_r) for i in range(num_iter))

        return pd.concat(output)



    def simulate_n_csv_par(output_folder, num_cores, num_iter, num_gen, popstr, prob_rep, mistake_rate, pop_size, base_fit, mutation_rate, moran_r):
        filename = f"{output_folder}/{nowname}_iter{num_iter}_{popstr}_probrep{prob_rep}_mis{mistake_rate}_size{pop_size}_base{base_fit}_mut{mutation_rate}_moran{moran_r}.csv"

        df_all = Simulation.simulate_n_df_par(num_cores=num_cores, 
                                num_iter=num_iter, 
                                num_gen=num_gen,
                                popstr=popstr, 
                                prob_rep=prob_rep, 
                                mistake_rate=mistake_rate, 
                                pop_size=pop_size, 
                                base_fit=base_fit,
                                mutation_rate=mutation_rate,
                                moran_r=moran_r)

        df_summary = df_all.drop(['sim_code','sim_no'], axis=1).groupby([
                    "population",
                    "generation",
                    "totalsize",
                    "size",
                    "num_generations",
                    "prob_rep",
                    "moran_r",
                    "base_fit",
                    "mutation_rate",
                    "popstr",
                    "mistake_rate",
                    ], as_index=False).agg(['size','std', 'mean', 'min','max'])

        df_summary.columns = list(map('__'.join, df_summary.columns.values))

        df_summary.to_csv(filename, index=True)

