# from unicodedata import decimal
import pytest

import attackerdefender.core as ad

def test_default_payoff():
    a1 = ad.Agent(type="defector")
    assert a1.payoff == 0


@pytest.mark.parametrize("payoff", [(0), (10), (-5.4), (8)])
def test_earn(payoff):
    a1 = ad.Agent(type="defector")
    a1.earn(payoff)
    assert a1.payoff == payoff


@pytest.mark.parametrize("payoff", [(0), (10), (-5.4), (8)])
def test_earn_twice(payoff):
    a1 = ad.Agent(type="defector")
    a1.earn(payoff)
    a1.earn(payoff)
    assert a1.payoff == 2 * payoff


@pytest.mark.parametrize("payoff", [(0), (10), (-5.4), (8)])
def test_starting_payffs(payoff):
    a1 = ad.Agent(type="defector", payoff=payoff)
    assert a1.payoff == payoff


# Testing types
@pytest.mark.parametrize("typename, action, expected_prop_c, deviation, mistake_rate", 
                        [
                            # reaction to c - # nomistakes
                            ("cooperator", "c", 1, 0, 0),
                            ("defector", "c", 0, 0, 0), 
                            ("match", "c", 1, 0, 0),
                            ("mismatch", "c", 0, 0, 0),
                            ("prob05", "c", 0.5, 0.05, 0),
                            
                            # reaction to d # nomistakes
                            ("cooperator", "d", 1, 0, 0),
                            ("defector", "d", 0, 0, 0), 
                            ("match", "d", 0, 0, 0),
                            ("mismatch", "d", 1, 0, 0),
                            ("prob05", "d", 0.5, 0.05, 0),

                            # reaction to c - # mistakes - 0.3
                            ("cooperator", "c", 0.85, 0.05, 0.3),
                            ("defector", "c", 0.15, 0.05, 0.3), 
                            ("match", "c", 0.85, 0.05, 0.3),
                            ("mismatch", "c", 0.15, 0.05, 0.3),
                            ("prob05", "c", 0.5, 0.05, 0.3),
                            
                            # reaction to d # mistakes 0.3
                            ("cooperator", "d", 0.85, 0.05, 0.3),
                            ("defector", "d", 0.15, 0.05, 0.3), 
                            ("match", "d", 0.15, 0.05, 0.3),
                            ("mismatch", "d", 0.85, 0.05, 0.3),
                            ("prob05", "d", 0.5, 0.05, 0.3),
                                     
                        ], 
                        )
def test_react_to_action(typename,
                         action, 
                         expected_prop_c,
                         deviation,
                         mistake_rate,
                         number_of_runs=1000):
 
    a1 = ad.Agent(type=typename)
    
    responses = [a1.respond(action, mistake_rate=mistake_rate) for _ in range(number_of_runs)]

    responses_c = responses.count('c')
    responses_d = responses.count('d')

    proportion_c = responses_c / number_of_runs

    assert proportion_c >= expected_prop_c - deviation and proportion_c <= expected_prop_c + deviation
    assert responses_c + responses_d == number_of_runs



def test_invalid_type():
    with pytest.raises(ValueError):
        a1 = ad.Agent(type="invalid")


