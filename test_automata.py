from builder import *

def test_example():

    test_cases = [
        {"regexp": "a*b", "input_str": "aaaab", "expected_res": "YES"},
        {"regexp": "a*b", "input_str": "b", "expected_res": "YES"},
        {"regexp": "a*b", "input_str": "a", "expected_res": "NO"},

        {"regexp": "a|b", "input_str": "a", "expected_res": "YES"},
        {"regexp": "a|b", "input_str": "aab", "expected_res": "NO"},
        {"regexp": "a|b", "input_str": "ab", "expected_res": "NO"},

        {"regexp": "(a|b)*(cd)*", "input_str": "", "expected_res": "YES"},
        {"regexp": "(a|b)*(cd)*", "input_str": "cdcdcdcd", "expected_res": "YES"},
        {"regexp": "(a|b)*(cd)*", "input_str": "bcdcd", "expected_res": "YES"},
        {"regexp": "(a|b)*(cd)*", "input_str": "cdaa", "expected_res": "NO"},
        {"regexp": "(a|b)*(cd)*", "input_str": "ddddd", "expected_res": "NO"},
        {"regexp": "(a|b)*(cd)*", "input_str": "d", "expected_res": "NO"},

        {"regexp": "(ab)|(ba)*", "input_str": "ab", "expected_res": "YES"},
        {"regexp": "(ab)|(ba)*", "input_str": "", "expected_res": "YES"},
        {"regexp": "(ab)|(ba)*", "input_str": "aba", "expected_res": "NO"},
    ]
    
    for case in test_cases:
        regexp = case["regexp"]
        input_str = case["input_str"]
        expected_res = case["expected_res"]

        nfda = create_nfa(regexp)
        dfa = convert_to_dfa(nfda)
        mdfa = minimize_dfa(dfa)
        res = mdfa.model_check(input_str)
        assert res == expected_res
