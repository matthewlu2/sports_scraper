from scipy.stats import poisson
from scraper import scrape_betr
import pandas as pd

def calculate_percentage(filename, selected_teams=None, secondary_filename=None):
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
        df = df.set_index('Player')
    except(Exception):
        raise Exception("Error reading CSV file.")
    
    if secondary_filename:
        try:
            df_secondary = pd.read_csv(secondary_filename)
            df_secondary = df_secondary.set_index('Player')
        except(Exception):
            raise Exception("Error reading secondary CSV file.")

    results = []
    for player in player_list:
        if player["type"] in threshold_mapping and player["stat"] in stat_mapping:  
            name = player["name"] # Player Name
            #If player exists in dataframe (uploaded projections)
            if name in df.index:
                team = df.loc[name, "Team"] # Player Team
                prop = player["projectedValue"] # Player prop (from Betr)
                player_mean = 0.0 # Player mean calculation
                # Player mean calculation based on stat mapping
                for stat in stat_mapping[player["stat"]]:
                    player_mean += df.loc[name, stat]
                # Initial probability calculations
                mean = player_mean
                p_under = round(stat_poisson(prop, player_mean), 5)
                p_over = round(1 - p_under, 5)
                option = "OVER" if p_over > p_under else "UNDER"
                # If player mean is 0, skip calculations
                if player_mean == 0:
                    continue
                threshold = threshold_mapping.get(player["type"]) # Get threshold based on bet type
                allowed_options = player.get("allowedOptions", []) # Get allowed options (MORE/LESS, or Both)
                # If selected teams are provided from frontend.
                if selected_teams and team in selected_teams:
                    # If a second file exists and player is in second file and "LESS" is an allowed option
                    if secondary_filename and name in df_secondary.index and "LESS" in allowed_options: 
                        second_player_mean = 0.0
                        # Player second mean calculation based on stat mapping
                        for stat in stat_mapping[player["stat"]]:
                            second_player_mean += df_secondary.loc[name, stat]
                        if second_player_mean == 0:
                            continue
                        if option == "OVER":
                            if player_mean > second_player_mean:
                                mean = second_player_mean
                                p_under = round(stat_poisson(prop, second_player_mean), 5)
                                p_over = round(1 - p_under, 5)
                        if option == "UNDER":
                            if player_mean < second_player_mean:
                                mean = second_player_mean
                                p_under = round(stat_poisson(prop, second_player_mean), 5)
                                p_over = round(1 - p_under, 5)
                    # If no second file but still LESS is allowed, or if second file exists but player not in it (and LESS is allowed), skip player
                    if ("LESS" in allowed_options and secondary_filename is None) or ("LESS" in allowed_options and secondary_filename and name not in df_secondary.index):
                        continue
                if "MORE" not in allowed_options and p_over > p_under:
                    continue
                if "LESS" not in allowed_options and p_under > p_over:
                    continue
                results.append({
                    "id": player["id"],
                    "name": name,
                    "team": team,
                    "stat": player["stat"],
                    "projectedValue": player["projectedValue"],
                    "playerMean": round(mean, 2),
                    "percentageOver": p_over,
                    "percentageUnder": p_under,
                    "percentOverThreshold": round(max(p_over - threshold, p_under - threshold), 5),
                    "odds": convert_odds(max(p_over, p_under)),
                    "type": player["type"],
                    "option": option
                })
    return results

def stat_poisson(prop, player_mean):
    if not (isinstance(prop, (int, float)) and prop == int(prop)):
        return poisson.cdf(prop, player_mean)
    else:
        cdf_prop_minus_1 = poisson.cdf(prop - 1, player_mean)
        pmf_prop = poisson.pmf(prop, player_mean)

        denominator = cdf_prop_minus_1 + (1 - cdf_prop_minus_1 - pmf_prop)
        return cdf_prop_minus_1 / denominator
    
def convert_odds(percentage):
    if percentage == 0 or percentage == 1:
        return "NULL"
    elif percentage > 0.5:
        odds = percentage / (1 - percentage) * 100
        return f"-{int(round(odds))}"
    else:
        odds = (1 - percentage) / percentage * 100
        return f"+{int(round(odds))}"