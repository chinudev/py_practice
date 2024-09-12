
from nba_api.stats.static import teams  # remember to do pip3 install nba_api
from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
import matplotlib.pyplot as plt


# convert from a list of dictionaries into a single dictionary 
def one_dict(list_dict):
    keys = list_dict[0].keys()
    out_dict = {key: [] for key in keys}
    for dict_ in list_dict:
        for key, value in dict_.items():
            out_dict[key].append(value)
    return out_dict


# Get the nba teams and convertto data frame
nba_teams = teams.get_teams()
df = pd.DataFrame(one_dict(nba_teams))

print(df.head())

# Get an entry for the warrios 
warriors = df[df['nickname'] == 'Warriors'] 
print(warriors)
id_warriors = warriors[['id']].values[0][0]

# get games played by the warriors
gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=id_warriors)
#print(gamefinder.get_json())
games = gamefinder.get_data_frames()[0]
print(games.head())

# get games played by the warriors against the raptors
games_home=games[games['MATCHUP']=='GSW vs. TOR']
games_away=games[games['MATCHUP']=='GSW @ TOR']
print(games_home['PLUS_MINUS'].mean(), games_away['PLUS_MINUS'].mean())     


fig, ax = plt.subplots()

games_away.plot(x='GAME_DATE',y='PLUS_MINUS', ax=ax)
games_home.plot(x='GAME_DATE',y='PLUS_MINUS', ax=ax)
ax.legend(["away", "home"])
plt.show()