from requests_html import HTMLSession
import time
import tweepy
from datetime import datetime
from Match_Info import Football
import re

API_Key = ''
API_Secret_Key = ''
Access_Token = ''
Access_Token_Secret = ''

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
match2 = Football('https://www.livescore.com/en/football/euro-2020/group-c/austria-vs-north-macedonia/81035/')


def lineups(goal_homepage):
    session = HTMLSession()
    matches = goal_homepage
    res = session.get(matches)
    match_data = res.html.find('.match-row-list', first=True)
    details = match_data.find('[href^="/en-in/match/"]')
    lineups_link_lst = []
    for detail in details:
        link = str(detail).split("'")[-2].split('/')
        link.insert(4, 'lineups')
        link[0] = 'https://www.goal.com'
        link = '/'.join(link)
        lineups_link_lst.append(link)
    for link in lineups_link_lst:
        if str(match2.team1).lower() in re.split("-|/", link) and str(match2.team2).lower() in re.split("-|/", link):
            players = []
            lineups = session.get(link).html.find('.widget-match-lineups__list.widget-match-lineups__starting-eleven .widget-match-lineups__name')
            for player in lineups:
                players.append(player.text)
            players_team1 = players[:11]
            players_team1_str = '\n'.join(players_team1)
            players_team2 = players[11:]
            players_team2_str = '\n'.join(players_team2)
            return 'Lineups ({}): \n{} \n\nLineups ({}): \n{}'.format(match2.team1, players_team1_str, match2.team2, players_team2_str)


def stats(goal_homepage):
    session = HTMLSession()
    matches = goal_homepage
    res = session.get(matches)
    match_data = res.html.find('.match-row-list', first=True)
    details = match_data.find('[href^="/en-in/match/"]')
    stats_link_lst = []
    for detail in details:
        link = str(detail).split("'")[-2].split('/')
        link.insert(4, 'commentary-result')
        link[0] = 'https://www.goal.com'
        link = '/'.join(link)
        stats_link_lst.append(link)
    for link in stats_link_lst:
        if str(match2.team1).lower() in re.split("-|/", link) and str(match2.team2).lower() in re.split("-|/", link):
            stats = session.get(link).html.find('.widget-match-stats .content')[0].text
            possession = '{} - {} | {} - {}'.format(match2.team1, stats.split()[1], match2.team2, stats.split()[2])
            shots_on_target = '{} - {} | {} - {}'.format(match2.team1, stats.split()[11], match2.team2, stats.split()[12])
            total_passes = '{} - {} | {} - {}'.format(match2.team1, stats.split()[15], match2.team2, stats.split()[16])
            return 'Possession: {} \nShots on Target: {} \nTotal Passes: {}'.format(possession, shots_on_target, total_passes)


def lineups_post_time(scheduled_time_str):
    time_list = scheduled_time_str.split(':')
    if int(time_list[1]) > 15:
        if int(time_list[1]) < 25:
            time_list[1] = '0' + str(int(time_list[1]) - 15)
        else:
            time_list[1] = str(int(time_list[1]) - 15)
    else:
        if time_list[0] == '00':
            time_list[0] = '23'
            time_list[1] = str(60 + (int(time_list[1]) - 15))
        else:
            time_list[1] = str(60 + (int(time_list[1]) - 15))
            if int(time_list[0]) < 11:
                time_list[0] = '0' + str(int(time_list[0]) - 1)
            else:
                time_list[0] = str(int(time_list[0]) - 1)
    return ':'.join(time_list)


def stats_post_time(scheduled_time_str):
    time_list = scheduled_time_str.split(':')
    if int(time_list[1]) < 30:
        time_list[1] = str(int(time_list[1]) + 30)
        if int(time_list[0]) < 9:
            time_list[0] = '0' + str(int(time_list[0]) + 1)
        else:
            time_list[0] = str(int(time_list[0]) + 1)
    else:
        if time_list[0] == '22':
            time_list[0] = '00'
            if 29 < int(time_list[1]) < 40:
                time_list[1] = '0' + str(int(time_list[1]) - 30)
            else:
                time_list[1] = str(int(time_list[1]) - 30)
        elif time_list[0] == '23':
            time_list[0] = '01'
            if 29 < int(time_list[1]) < 40:
                time_list[1] = '0' + str(int(time_list[1]) - 30)
            else:
                time_list[1] = str(int(time_list[1]) - 30)
        else:
            if int(time_list[0]) < 8:
                time_list[0] = '0' + str((int(time_list[0]) + 2))
            else:
                time_list[0] = str((int(time_list[0]) + 2))
            if 29 < int(time_list[1]) < 40:
                time_list[1] = '0' + str(int(time_list[1]) - 30)
            else:
                time_list[1] = str(int(time_list[1]) - 30)
    return ':'.join(time_list)


while True:
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
                api.update_status('#EURO2021 \n#{}vs{} \nYellow Card by : {} ({}) \n{}'.format(
                    match2.team1, match2.team2, match2.team1_scorers()[-1], match2.team1, match2.current_score))
            else:
                pass
        elif match2.team1_red() is True:
            if len(current_team1_scorers) > len(previous_team1_scorers):
                previous_team1_scorers = current_team1_scorers
                api.update_status('#EURO2021 \n#{}vs{} \nRed Card by : {} ({}) \n{}'.format(
                    match2.team1, match2.team2, match2.team1_scorers()[-1], match2.team1, match2.current_score))
            else:
                pass
        else:
            if len(current_team1_assists) > len(previous_team1_assists):
                previous_team1_assists = current_team1_assists
                api.update_status('#EURO2021 \n#{}vs{} \nGoal by : {} ({}) \nAssist: {} \n{}'.format(
                    match2.team1, match2.team2, match2.team1_scorers()[-1], match2.team1, match2.team1_assists()[-1], match2.current_score))
            else:
                try:
                    api.update_status('#EURO2021 \n#{}vs{} \nGoal by : {} ({}) \n{}'.format(
                        match2.team1, match2.team2, match2.team1_scorers()[-1], match2.team1, match2.current_score))
                except:
                    api.update_status('#EURO2021 \n#{}vs{} \n{}'.format(
                        match2.team1, match2.team2, match2.current_score))

    elif len(current_team2_events) > len(previous_team2_events):
        previous_team2_events = current_team2_events
        if match2.team2_yellow() is True:
            if len(current_team2_scorers) > len(previous_team2_scorers):
                previous_team2_scorers = current_team2_scorers
                api.update_status('#EURO2021 \n#{}vs{} \nYellow Card by : {} ({}) \n{}'.format(
                    match2.team1, match2.team2, match2.team2_scorers()[-1], match2.team2, match2.current_score))
            else:
                pass
        elif match2.team2_red() is True:
            if len(current_team2_scorers) > len(previous_team2_scorers):
                previous_team2_scorers = current_team2_scorers
                api.update_status('#EURO2021 \n#{}vs{} \nRed Card by : {} ({}) \n{}'.format(
                    match2.team1, match2.team2, match2.team2_scorers()[-1], match2.team2, match2.current_score))
            else:
                pass
        else:
            if len(current_team2_assists) > len(previous_team2_assists):
                previous_team2_assists = current_team2_assists
                api.update_status('#EURO2021 \n#{}vs{} \nGoal by : {} ({}) \nAssist: {} \n{}'.format(
                    match2.team1, match2.team2, match2.team2_scorers()[-1], match2.team2, match2.team2_assists()[-1], match2.current_score))
            else:
                try:
                    api.update_status('#EURO2021 \n#{}vs{} \nGoal by : {} ({}) \n{}'.format(
                        match2.team1, match2.team2, match2.team2_scorers()[-1], match2.team2, match2.current_score))
                except:
                    api.update_status('#EURO2021 \n#{}vs{} \n{}'.format(
                        match2.team1, match2.team2, match2.current_score))

    else:
        if len(previous_times_lst) < len(current_times_lst):
            previous_times_lst = current_times_lst
            if current_times_lst[-1] == 'HT':
                api.update_status('#EURO2021 \n#{}vs{} \nHalf Time: {} \n{}'.format(
                    match2.team1, match2.team2, match2.current_score, match2.winner()))
            elif current_times_lst[-1] == 'FT':
                api.update_status('#EURO2021 \n#{}vs{} \nFull Time: {} \n{}'.format(
                    match2.team1, match2.team2, match2.current_score, match2.winner()))
        else:
            pass

    if datetime.now().strftime('%H:%M') == lineups_post_time(match2.scheduled_time):
        lineups('https://www.goal.com/en-in/live-scores')

    if datetime.now().strftime('%H:%M') == stats_post_time(match2.scheduled_time):
        stats('https://www.goal.com/en-in/live-scores')

    time.sleep(3)
