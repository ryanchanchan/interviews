from collections import defaultdict
from datetime import date

# 1. Team Assignments
team_assignments = [
    {
        "team_id": "TEAM_A", 
        "operations": ["OP_ALPHA", "OP_BRAVO"], 
        "date": date(2026, 4, 15)
    },
    {
        "team_id": "TEAM_B", 
        "operations": ["OP_BRAVO", "OP_CHARLIE"], 
        "date": date(2026, 4, 18)
    },
    {
        "team_id": "TEAM_C", 
        "operations": ["OP_DELTA"], 
        "date": date(2026, 5, 1)
    },
    {
        "team_id": "TEAM_D", 
        "operations": ["OP_ALPHA", "OP_CHARLIE", "OP_ECHO"], 
        "date": date(2026, 4, 18)  # Same date as TEAM_B for tie-breaker testing
    },
    {
        "team_id": "TEAM_E", 
        "operations": ["OP_ECHO", "OP_FOXTROT"], 
        "date": date(2026, 6, 10)
    },
]

# 2. Required Gear
required_gear = [
    {"gear_id": "GEAR_RADIO",     "required_for_ops": ["OP_ALPHA", "OP_BRAVO", "OP_FOXTROT"]},
    {"gear_id": "GEAR_MEDKIT",    "required_for_ops": ["OP_ALPHA", "OP_ECHO"]},
    {"gear_id": "GEAR_NVG",       "required_for_ops": ["OP_CHARLIE", "OP_ECHO"]},
    {"gear_id": "GEAR_GPS",       "required_for_ops": ["OP_DELTA", "OP_FOXTROT"]},
    {"gear_id": "GEAR_BODY_ARMOR","required_for_ops": ["OP_ALPHA", "OP_CHARLIE"]},
    {"gear_id": "GEAR_DRONE",     "required_for_ops": ["OP_ECHO"]},
]

# 3. Issued Gear
issued_gear = [
    # Team A issued items
    {"team_id": "TEAM_A", "gear_id": "GEAR_RADIO"},
    
    # Team B issued items
    {"team_id": "TEAM_B", "gear_id": "GEAR_NVG"},
    
    # Team C issued items
    {"team_id": "TEAM_C", "gear_id": "GEAR_GPS"},
    
    # Team D issued items
    {"team_id": "TEAM_D", "gear_id": "GEAR_RADIO"},
    {"team_id": "TEAM_D", "gear_id": "GEAR_MEDKIT"},
    
    # Team E issued items (none issued yet to test zero-gear baseline)
]

""" 
we need to find the team with the MOST gear missing, in a senario of a tie, compare the dates 
"""

def team_with_most_missing_gear(team_assignments, required_gear, issued_gear): 
    """ 
    first we need to find out what each team has 

    team_has = team_id --> list of gear_ids

    2nd, we need to find out what the team should have 

        to do this we need what gear is needed for what operation 

        operation_need -> operation ---> list of gear

    now, we can have a tuple with (missing gear, and the date)
    """
    team_has = defaultdict(set)

    for issued in issued_gear: 
        team = issued["team_id"]
        gear = issued["gear_id"]

        team_has[team].add(gear)

    what_need_for_x_operation = defaultdict(set)

    for required in required_gear:
        gear = required["gear_id"]
        oper = required["required_for_ops"]
        for op in oper: 
            what_need_for_x_operation[op].add(gear)

    missing = {}

    for assignment in team_assignments: 
        team = assignment["team_id"]
        date = assignment["date"]
        operation = assignment["operations"]
        needed_items = set()
        c = 0 
        for each_operation in operation: 
            needed_items.update(what_need_for_x_operation[each_operation])
        for item in needed_items: 
            if item not in team_has[team]: 
                c += 1 
        missing[team] = (-c, date)

    curr = (None, None)
    res = ""
    for key, val in missing.items(): 
        if curr == (None, None): 
            curr = val 
            res = key
        elif val < curr: 
            curr = val 
            res = key
    return res

        
        






print(team_with_most_missing_gear(team_assignments, required_gear, issued_gear))



    

