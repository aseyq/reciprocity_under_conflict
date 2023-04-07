import pytest
import random 
import uuid
import attackerdefender.core as ad


types = ["cooperator",
         "defector",
         "match",
         "mismatch",
         "prob05",
        ]

roles = ["attacker", "defender"]


def test_population_regeneration_fullreplace_nomutation():
    differences_sim = []
    num_sims = 100
    for _ in range(num_sims):
        differences = 0
        total_type_number = {t:0 for t in types}

        a01 = ad.Agent(type="match", role="attacker")
        a02 = ad.Agent(type="match", role="attacker")
        a03 = ad.Agent(type="match", role="attacker")
        a04 = ad.Agent(type="match", role="attacker")
        a05 = ad.Agent(type="match", role="attacker")
        a06 = ad.Agent(type="mismatch", role="attacker")
        a07 = ad.Agent(type="mismatch", role="attacker")
        a08 = ad.Agent(type="mismatch", role="attacker")
        a09 = ad.Agent(type="mismatch", role="attacker")
        a10 = ad.Agent(type="mismatch", role="attacker")
        a11 = ad.Agent(type="prob05", role="attacker")
        a12 = ad.Agent(type="prob05", role="attacker")
        a13 = ad.Agent(type="prob05", role="attacker")
        a14 = ad.Agent(type="prob05", role="attacker")
        a15 = ad.Agent(type="prob05", role="attacker")
        a16 = ad.Agent(type="defector", role="attacker")
        a17 = ad.Agent(type="defector", role="attacker")
        a18 = ad.Agent(type="defector", role="attacker")
        a19 = ad.Agent(type="defector", role="attacker")
        a20 = ad.Agent(type="defector", role="attacker")

        agents = [a01,a02,a03,a04,a05,a06,a07,a08,a09,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20]

        pop = ad.Population(role="attacker", agents = agents,allowed_types=types)

        for i, a in enumerate(agents):
            a.earn(i * 10 + random.random() * 10)

        total_type_payoffs = {t:0 for t in types}

        for a in pop.agents:
            total_type_payoffs[a.type] += a.payoff

        sum_payoffs = sum(total_type_payoffs.values())
        relative_type_payoffs = {k:total_type_payoffs[k]/sum_payoffs for k in total_type_payoffs.keys()}


        pop.regenerate(r=1, base_fitness= 0.0, mutation_rate=0.0)
        pop.summarize_types()

        for a in pop.agents:
            total_type_number[a.type] += 1

        number_of_agents_in_total = sum(total_type_number.values())
        total_type_freq = {k:total_type_number[k]/number_of_agents_in_total for k in total_type_number.keys()}
        print("------")
        print(relative_type_payoffs)
        print(total_type_freq)
        
        for t in types:
            differences += abs(total_type_freq[t] - relative_type_payoffs[t])
        differences_sim.append(differences)

    print(differences_sim)
    average_differences_sim = sum(differences_sim)/len(differences_sim)
    assert average_differences_sim <=0.31 # this is an empirical value
    # it is like picking a point around a point in a simplex 
    # and getting the difference. it is always greater than  and its limit
    # doesnt go to zero with the number of reps