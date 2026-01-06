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

    player_list = scrape_betr()

    try:
        df = pd.read_csv(filename)
        df = df[df["Scenario"] == "Default"]
        df = df.set_index('Player')
    except(Exception):
        raise Exception("Error reading CSV file.")

    results = []
    for player in player_list:
        if player["type"] == "REGULAR" and player["stat"] in stat_mapping:           
            name = player["name"]
            if name in df.index:
                prop = player["projectedValue"]
                player_mean = 0.0
                for stat in stat_mapping[player["stat"]]:
                    player_mean += df.loc[name, stat]
                p_under = round(stat_poisson(prop, player_mean), 2)
                p_over = round(1 - p_under, 2)
                results.append({
                    "id": player["id"],
                    "name": name,
                    "stat": player["stat"],
                    "projectedValue": player["projectedValue"],
                    "playerMean": round(player_mean, 2),
                    "percentageOver": p_over,
                    "percentageUnder": p_under,
                    "percentOverThreshold": round(max(p_over - 0.55, p_under - 0.55), 2),
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