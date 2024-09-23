import requests
from selectolax.parser import HTMLParser

# Headers for the request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

# Mapping of region abbreviations to full names
REGIONS = {
    "na": "north-america",
    "eu": "europe",
    "ap": "asia-pacific",
    "la": "latin-america",
    "la-s": "la-s",
    "la-n": "la-n",
    "oce": "oceania",
    "kr": "korea",
    "mn": "mena",
    "gc": "gc",
    "br": "Brazil",
    "cn": "china",
    "jp": "japan",
    "col": "collegiate",
}

def vlr_stats(region: str, timespan: str):
    base_url = f"https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region={region}&country=all&min_rounds=200&min_rating=1550&agent=all&map_id=all"
    url = f"{base_url}&timespan={'all' if timespan.lower() == 'all' else f'{timespan}d'}"

    # Requesting the page
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"API response: {response.status_code}")
    
    html = HTMLParser(response.text)
    
    result = []
    for item in html.css("tbody tr"):
        # Extract player name and organization
        player_data = item.text().replace("\t", "").replace("\n", " ").strip().split()
        player_name = player_data[0]
        org = player_data[1] if len(player_data) > 1 else "N/A"

        # Extract agent images and stats
        agents = [img.attributes["src"].split("/")[-1].split(".")[0] for img in item.css("td.mod-agents img")]
        stats = [stat.text() for stat in item.css("td.mod-color-sq")]
        rounds_played = item.css_first("td.mod-rnd").text()

        # Construct player stats dictionary
        result.append({
            "player": player_name,
            "org": org,
            "agents": agents,
            "rounds_played": rounds_played,
            "rating": stats[0],
            "average_combat_score": stats[1],
            "kill_deaths": stats[2],
            "kill_assists_survived_traded": stats[3],
            "average_damage_per_round": stats[4],
            "kills_per_round": stats[5],
            "assists_per_round": stats[6],
            "first_kills_per_round": stats[7],
            "first_deaths_per_round": stats[8],
            "headshot_percentage": stats[9],
            "clutch_success_percentage": stats[10],
        })

    return {"data": {"status": response.status_code, "segments": result}}
