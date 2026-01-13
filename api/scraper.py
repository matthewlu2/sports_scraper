import requests
import json

def scrape_betr():
    url = "https://api.fantasy.betr.app/graphql"
    payload = "{\"query\":\"query LeagueUpcomingEvents($league: League!) {\\n  getUpcomingEventsV2(league: $league) {\\n    ...EventInfoData\\n    ... on TeamTournamentEvent {\\n      teams {\\n        ...TeamInfoWithPlayers\\n        __typename\\n      }\\n      __typename\\n    }\\n    ... on TeamVersusEvent {\\n      teams {\\n        ...TeamInfoWithPlayers\\n        __typename\\n      }\\n      __typename\\n    }\\n    ... on IndividualTournamentEvent {\\n      players {\\n        ...PlayerInfoWithProjections\\n        __typename\\n      }\\n      __typename\\n    }\\n    ... on IndividualVersusEvent {\\n      players {\\n        ...PlayerInfoWithProjections\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\nfragment EventInfoData on EventV2 {\\n  id\\n  date\\n  status\\n  sport\\n  league\\n  competitionType\\n  dataFeedSourceIds {\\n    id\\n    source\\n    __typename\\n  }\\n  playerStructure\\n  venueDetails {\\n    name\\n    city\\n    country\\n    __typename\\n  }\\n  headerImage\\n  attributes {\\n    key\\n    value\\n    __typename\\n  }\\n  name\\n  icon\\n  dedicated\\n  __typename\\n}\\nfragment TeamInfoWithPlayers on Team {\\n  ...TeamInfo\\n  players {\\n    ...PlayerInfoWithProjections\\n    __typename\\n  }\\n  __typename\\n}\\nfragment TeamInfo on Team {\\n  id\\n  name\\n  league\\n  sport\\n  icon\\n  color\\n  secondaryColor\\n  largeIcon\\n  __typename\\n}\\nfragment PlayerInfoWithProjections on Player {\\n  ...PlayerInfo\\n  projections {\\n    ...PlayerProjection\\n    __typename\\n  }\\n  __typename\\n}\\nfragment PlayerInfo on Player {\\n  id\\n  firstName\\n  lastName\\n  icon\\n  position\\n  jerseyNumber\\n  attributes {\\n    key\\n    value\\n    __typename\\n  }\\n  record\\n  rank\\n  __typename\\n}\\nfragment PlayerProjection on Projection {\\n  marketId\\n  marketStatus\\n  isLive\\n  type\\n  playerRecentStats {\\n    stats {\\n      ...RecentStat\\n      __typename\\n    }\\n    averageValue\\n    __typename\\n  }\\n  label\\n  name\\n  key\\n  order\\n  value\\n  nonRegularPercentage\\n  nonRegularValue\\n  allowedOptions {\\n    marketOptionId\\n    outcome\\n    __typename\\n  }\\n  currentValue\\n  __typename\\n}\\nfragment RecentStat on PlayerRecentStat {\\n  value\\n  matchupDescription\\n  date\\n  __typename\\n}\",\"variables\":{\"league\":\"NBA\"}}"
    headers = {
        'accept': 'application/graphql-response+json, application/graphql+json, application/json, text/event-stream, multipart/mixed',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': '',
        'channel': 'MOBILE_WEB',
        'content-type': 'application/json',
        'fantasy-api-version': '13.0',
        'fantasy-application-version': '3.32.11',
        'jurisdiction': 'PA',
        'origin': 'https://picks.betr.app',
        'priority': 'u=1, i',
        'promotions-api-version': '3.0',
        'referer': 'https://picks.betr.app/',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36'
    }
    

    #use to load from local file for testing

    # with open('/Users/matthewlu/Documents/Projects/sports-scraper/api/events.json', 'r') as file:
    #     playerData = json.load(file)
    # events = playerData

    response = requests.request("POST", url, headers=headers, data=payload)
    playerData = response.json()
    results = []
    events = playerData["data"]["getUpcomingEventsV2"]
    

    #write to local file for testing            

    # events_pretty = json.dumps(events, indent=2)
    # with open("events.json", "w", encoding="utf-8") as f:
    #     f.write(events_pretty)


    id = 0
    for event in events:
        players = []
        # Case 1: Individual events
        if event.get("players"):
            players = event["players"]
        # Case 2: Team events (NBA)
        elif event.get("teams"):
            for team in event["teams"]:
                players.extend(team.get("players", []))
        for player in players:
            name = player.get("firstName") + " " + player.get("lastName")
            for proj in player.get("projections", []):
                type = proj.get("type")
                value = None
                if type == "REGULAR":
                    value = proj.get("value")
                else:
                    value = proj.get("nonRegularValue")
                if value is None:
                    continue
                #Extract options (e.g. More, Less, Both)
                allowed_options = [
                    opt["outcome"]
                    for opt in proj.get("allowedOptions", [])
                    if "outcome" in opt
                ]
                results.append({
                    "id": id,
                    "name": name,
                    "stat": proj.get("label"),
                    "projectedValue": value,
                    "type": type,
                    "allowedOptions": allowed_options
                })
                id += 1

    # dump results to local file for viewing

    # with open("player_projections.json", "w") as f:
    #     json.dump(results, f, indent=2)

    return results
