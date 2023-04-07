import pytest
import random 

import attackerdefender.core as ad


types = ["cooperator",
         "defector",
         "match",
         "mismatch",
         "prob05",
        ]

roles = ["attacker", "defender"]

def test_get_size():
    agent1 = ad.Agent(type="defector")
    agent2 = ad.Agent(type="mismatch")

    group = ad.Group([agent1, agent2])
    assert group.get_size() == 2

def test_agents():
    agent1 = ad.Agent(type="cooperator")
    agent2 = ad.Agent(type="prob05")

    group = ad.Group([agent1, agent2])

    assert group.agents == [agent1, agent2]


def test_agents_except_this():
    agent1 = ad.Agent(type="match")
    agent2 = ad.Agent(type="mismatch")

    group = ad.Group([agent1, agent2])

    assert group.agents_except_this(agent1) == [agent2]
    assert group.agents_except_this(agent2) == [agent1]


def test_get_roles():

    role1= random.choices(roles,k=1)[0]
    role2= random.choices(roles,k=1)[0]

    agent1 = ad.Agent(type="cooperator", role=role1)
    agent2 = ad.Agent(type="prob05", role=role2)

    group = ad.Group([agent1, agent2])

    assert group.get_roles()[0] ==  role1
    assert group.get_roles()[1] ==  role2
