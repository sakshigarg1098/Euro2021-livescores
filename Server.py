import time
from Match_Info import Football

previous_team1_events = []
previous_team2_events = []
previous_team1_assists = []
previous_team2_assists = []
previous_team1_scorers = []
previous_team2_scorers = []
previous_times_lst = []

while True:
    match2 = Football('https://www.livescore.com/en/football/world-cup/afc-qualification-2nd-round-group-f/myanmar-vs-kyrgyzstan/26498/')

    current_team1_events = match2.team1_events()
    current_team2_events = match2.team2_events()
    current_team1_assists = match2.team1_assists()
    current_team2_assists = match2.team2_assists()
    current_team1_scorers = match2.team1_scorers()
    current_team2_scorers = match2.team2_scorers()
    current_times_lst = match2.times_()

    if len(current_team1_events) > len(previous_team1_events):
        previous_team1_events = current_team1_events
        if match2.team1_yellow() is True:
            if len(current_team1_scorers) > len(previous_team1_scorers):
                previous_team1_scorers = current_team1_scorers
                print('Yellow Card by : {} ({})'.format(match2.team1_scorers()[-1], match2.team1))
            else:
                pass
        elif match2.team1_red() is True:
            if len(current_team1_scorers) > len(previous_team1_scorers):
                previous_team1_scorers = current_team1_scorers
                print('Red Card by : {} ({})'.format(match2.team1_scorers()[-1], match2.team1))
            else:
                pass
        else:
            if len(current_team1_assists) > len(previous_team1_assists):
                previous_team1_assists = current_team1_assists
                print(match2.final_score())
                try:
                    print('Goal by : {} ({})'.format(match2.team1_scorers()[-1], match2.team1))
                    print('Assist: {}'.format(match2.team1_assists()[-1]))
                except:
                    pass
            else:
                print('Goal by : {} ({})'.format(match2.team1_scorers()[-1], match2.team1))
                print(match2.final_score())

    elif len(current_team2_events) > len(previous_team2_events):
        previous_team2_events = current_team2_events
        if match2.team2_yellow() is True:
            if len(current_team2_scorers) > len(previous_team2_scorers):
                previous_team2_scorers = current_team2_scorers
                print('Yellow Card by : {} ({})'.format(match2.team2_scorers()[-1], match2.team2))
            else:
                pass
        elif match2.team2_red() is True:
            if len(current_team2_scorers) > len(previous_team2_scorers):
                previous_team2_scorers = current_team2_scorers
                print('Red Card by : {} ({})'.format(match2.team2_scorers()[-1], match2.team2))
            else:
                pass
        else:
            if len(current_team2_assists) > len(previous_team2_assists):
                previous_team2_assists = current_team2_assists
                print(match2.final_score())
                try:
                    print('Goal by : {} ({})'.format(match2.team2_scorers()[-1], match2.team2))
                    print('Assist: {}'.format(match2.team2_assists()[-1]))
                except:
                    pass
            else:
                print('Goal by : {} ({})'.format(match2.team2_scorers()[-1], match2.team2))
                print(match2.final_score())

    else:
        if len(previous_times_lst) < len(current_times_lst):
            previous_times_lst = current_times_lst
            if current_times_lst[-1] == 'HT':
                print('Half Time: {}'.format(match2.current_score))
            elif current_times_lst[-1] == 'FT':
                print('Full Time: {}'.format(match2.final_score))
                print(match2.winner())
        else:
            pass
    time.sleep(120)
