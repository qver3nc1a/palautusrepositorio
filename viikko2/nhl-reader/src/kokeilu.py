from index import PlayerReader
from index import PlayerStats

url = "https://studies.cs.helsinki.fi/nhlstats/2026-27/players"
stats = PlayerStats(PlayerReader(url))

for p in stats.top_scores_by_team("DAL"):
    print(p)
