import time
import tweepy
from Match_Info import Football

API_Key = 'Rl2iEuGVcttMr7XJpPZTfgUrb'
API_Secret_Key = 'qW5qKmxnBAWfZhEnudivqLHkN0VVdAg62HB4VfNAr1QlDbZUA9'
Access_Token = '1402255274984026114-VDnOyMDEdwRkWKgifQaPOlUx5lrkVQ'
Access_Token_Secret = 'ZDO4XrLGLa72KvAgiG5wm8q8tukYQa56b7uYePTjapxiU'

auth = tweepy.OAuthHandler(API_Key, API_Secret_Key)
auth.set_access_token(Access_Token, Access_Token_Secret)

api = tweepy.API(auth)

previous_team1_events = []
previous_team2_events = []
previous_team1_assists = []
previous_team2_assists = []
previous_team1_scorers = []
previous_team2_scorers = []
previous_times_lst = []

while True:
    match2 = Football('https://www.livescore.com/en/football/intl/friendlies/japan-vs-serbia/432275/')

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
                api.update_status('Yellow Card by : {} ({})'.format(match2.team1_scorers()[-1], match2.team1))
                api.update_status(match2.current_score)
            else:
                pass
        elif match2.team1_red() is True:
            if len(current_team1_scorers) > len(previous_team1_scorers):
                previous_team1_scorers = current_team1_scorers
                api.update_status('Red Card by : {} ({})'.format(match2.team1_scorers()[-1], match2.team1))
                api.update_status(match2.current_score)
            else:
                pass
        else:
            if len(current_team1_assists) > len(previous_team1_assists):
                previous_team1_assists = current_team1_assists
                api.update_status('Goal by : {} ({})'.format(match2.team1_scorers()[-1], match2.team1))
                api.update_status('Assist: {}'.format(match2.team1_assists()[-1]))
                api.update_status(match2.current_score)
            else:
                try:
                    api.update_status('Goal by : {} ({})'.format(match2.team1_scorers()[-1], match2.team1))
                    api.update_status(match2.current_score)
                except:
                    api.update_status(match2.current_score)

    elif len(current_team2_events) > len(previous_team2_events):
        previous_team2_events = current_team2_events
        if match2.team2_yellow() is True:
            if len(current_team2_scorers) > len(previous_team2_scorers):
                previous_team2_scorers = current_team2_scorers
                api.update_status('Yellow Card by : {} ({})'.format(match2.team2_scorers()[-1], match2.team2))
                api.update_status(match2.current_score)
            else:
                pass
        elif match2.team2_red() is True:
            if len(current_team2_scorers) > len(previous_team2_scorers):
                previous_team2_scorers = current_team2_scorers
                api.update_status('Red Card by : {} ({})'.format(match2.team2_scorers()[-1], match2.team2))
                api.update_status(match2.current_score)
            else:
                pass
        else:
            if len(current_team2_assists) > len(previous_team2_assists):
                previous_team2_assists = current_team2_assists
                api.update_status('Goal by : {} ({})'.format(match2.team2_scorers()[-1], match2.team2))
                api.update_status('Assist: {}'.format(match2.team2_assists()[-1]))
                api.update_status(match2.current_score)
            else:
                try:
                    api.update_status('Goal by : {} ({})'.format(match2.team2_scorers()[-1], match2.team2))
                    api.update_status(match2.current_score)
                except:
                    api.update_status(match2.current_score)

    else:
        if len(previous_times_lst) < len(current_times_lst):
            previous_times_lst = current_times_lst
            if current_times_lst[-1] == 'HT':
                api.update_status('Half Time: {}'.format(match2.current_score))
            elif current_times_lst[-1] == 'FT':
                api.update_status('Full Time: {}'.format(match2.current_score))
                api.update_status(match2.winner())
        else:
            pass
    time.sleep(3)
