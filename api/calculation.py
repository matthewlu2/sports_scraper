from scipy.stats import poisson
from scraper import scrape_betr
import pandas as pd
import json


def calculate_percentage(filename):
    stat_mapping = {
        "Pts+Reb": ["Points", "Rebounds"],
        "Pts+Reb+Ast": ["PRA"],
        "Reb+Ast": ["Rebounds", "Assists"],
        "3PT Made": ["Three Pointers Made"],
        "Pts+Ast": ["Points", "Assists"],
        "Points": ["Points"],
        "Rebounds": ["Rebounds"],
        "Assists": ["Assists"],
        "Steals": ["Steals"],
        "Blocks": ["Blocks"],
        "Stl+Blk": ["Steals", "Blocks"],
        "Turnovers": ["Turnovers"],
    }

    threshold_mapping = {
        "EDGE_3": 0.9285,
        "EDGE_2": 0.8621,
        "EDGE_1": 0.6743,
        "REGULAR": 0.5379,
        "MINI_BOOSTED": 0.4405,
        "BOOSTED": 0.3021,
        "SUPER_BOOSTED": 0.1658
    }

    player_list = scrape_betr()

    try:
        df = pd.read_csv(filename)
        df = df[df["Scenario"] == "Default"]
        df = df.set_index('Player')
    except(Exception):
        raise Exception("Error reading CSV file.")

    results = []
    for player in player_list:
        if player["type"] in threshold_mapping and player["stat"] in stat_mapping:           
            name = player["name"]
            if name in df.index:
                prop = player["projectedValue"]
                player_mean = 0.0
                for stat in stat_mapping[player["stat"]]:
                    player_mean += df.loc[name, stat]
                p_under = round(stat_poisson(prop, player_mean), 5)
                p_over = round(1 - p_under, 5)
                threshold = threshold_mapping.get(player["type"])
                results.append({
                    "id": player["id"],
                    "name": name,
                    "stat": player["stat"],
                    "projectedValue": player["projectedValue"],
                    "playerMean": round(player_mean, 2),
                    "percentageOver": p_over,
                    "percentageUnder": p_under,
                    "percentOverThreshold": round(max(p_over - threshold, p_under - threshold), 5),
                    "type": player["type"],
                    "allowedOptions": player["allowedOptions"]
                })
    # with open("player_calcs.json", "w") as f:
    #     json.dump(results, f, indent=2)
    return results

def stat_poisson(prop, player_mean):
    if not (isinstance(prop, (int, float)) and prop == int(prop)):
        return poisson.cdf(prop, player_mean)
    else:
        cdf_prop_minus_1 = poisson.cdf(prop - 1, player_mean)
        pmf_prop = poisson.pmf(prop, player_mean)

        denominator = cdf_prop_minus_1 + (1 - cdf_prop_minus_1 - pmf_prop)
        return cdf_prop_minus_1 / denominator