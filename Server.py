import time
import tweepy
from datetime import datetime
from Match_Info import Football
import re
from requests_html import HTMLSession

API_Key = 'Rl2iEuGVcttMr7XJpPZTfgUrb'
API_Secret_Key = 'qW5qKmxnBAWfZhEnudivqLHkN0VVdAg62HB4VfNAr1QlDbZUA9'
Access_Token = '1402255274984026114-VDnOyMDEdwRkWKgifQaPOlUx5lrkVQ'
Access_Token_Secret = 'ZDO4XrLGLa72KvAgiG5wm8q8tukYQa56b7uYePTjapxiU'

auth = tweepy.OAuthHandler(API_Key, API_Secret_Key)
auth.set_access_token(Access_Token, Access_Token_Secret)
api = tweepy.API(auth)

session = HTMLSession()
r = session.get('https://www.livescore.com/en/football/euro-2020/')
r.html.render(sleep=1)
body = r.html.find('#match-rows__root')[0]
euro_links = body.find('[target=_blank]')
euro_match_links = []
for link in euro_links:
    euro_match_links.append('https://www.livescore.com' + str(link).split("'")[3])


def lineups_links():
    session2 = HTMLSession()
    matches = 'https://www.goal.com/en-in/live-scores'
    res = session2.get(matches)
    match_data = res.html.find('.match-row-list', first=True)
    details = match_data.find('[href^="/en-in/match/"]')
    lineups_link_lst = []
    for detail in details:
        link_data = str(detail).split("'")[-2].split('/')
        link_data.insert(4, 'lineups')
        link_data[0] = 'https://www.goal.com'
        link_data = '/'.join(link_data)
        lineups_link_lst.append(link_data)
    return lineups_link_lst


def lineups(lineups_link):
    session1 = HTMLSession()
    players = []
    teams = []
    lineups_data = session1.get(lineups_link).html.find(
        '.widget-match-lineups__list.widget-match-lineups__starting-eleven .widget-match-lineups__name')
    teams_data = session.get(lineups_link).html.find('.widget-match-header__name--full')
    for team in teams_data:
        teams.append(team.text)
    for player in lineups_data:
        players.append(player.text)
    lineup = 'LINEUPS-\n\n{}:\n{}\n\n{}:\n{}'.format(teams[0], '\n'.join(players[:11]), teams[1], '\n'.join(players[11:]))
    return lineup


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


def stats_links():
    session3 = HTMLSession()
    matches = 'https://www.goal.com/en-in/live-scores'
    res = session3.get(matches)
    match_data = res.html.find('.match-row-list', first=True)
    details = match_data.find('[href^="/en-in/match/"]')
    stats_link_lst = []
    for detail in details:
        link_data = str(detail).split("'")[-2].split('/')
        link_data.insert(4, 'commentary-result')
        link_data[0] = 'https://www.goal.com'
        link_data = '/'.join(link_data)
        stats_link_lst.append(link_data)
    return stats_link_lst


def stats(stats_link):
    session4 = HTMLSession()
    stats_data = session4.get(stats_link).html.find('.widget-match-stats .content')[0].text
    possession = '{} - {} | {} - {}'.format(match2.team1, stats_data.split()[1], match2.team2, stats_data.split()[2])
    shots_on_target = '{} - {} | {} - {}'.format(match2.team1, stats_data.split()[11], match2.team2, stats_data.split()[12])
    total_passes = '{} - {} | {} - {}'.format(match2.team1, stats_data.split()[15], match2.team2, stats_data.split()[16])
    return 'Possession: {} \nShots on Target: {} \nTotal Passes: {}'.format(possession, shots_on_target, total_passes)


while True:
    for link in euro_match_links:  # all links of euro matches
        match2 = Football(link)
        if match2.scheduled_time[0].isdigit():
            if datetime.now().strftime('%H:%M') == lineups_post_time(
                    match2.scheduled_time):  # if current time is 15 min before scheduled time
                for lineup_link in lineups_links():  # list of line-ups links of matches in a day
                    if str(match2.team1).lower() in re.split("-|/", lineup_link) or str(match2.team2).lower() in re.split("-|/", lineup_link):
                        api.update_status(lineups(link))  # if team names are in line-ups link, print line-ups
                        previous_team1_events = []
                        previous_team2_events = []
                        previous_team1_assists = []
                        previous_team2_assists = []
                        previous_team1_scorers = []
                        previous_team2_scorers = []
                        previous_times_lst = []

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
                                        api.update_status('#EURO2021 \n#{}vs{} \nYellow Card : {} ({}) \n{}'.format(
                                            match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                            match2.team1_scorers()[-1], match2.team1,
                                            match2.current_score))
                                    else:
                                        pass
                                elif match2.team1_red() is True:
                                    if len(current_team1_scorers) > len(previous_team1_scorers):
                                        previous_team1_scorers = current_team1_scorers
                                        api.update_status('#EURO2021 \n#{}vs{} \nRed Card : {} ({}) \n{}'.format(
                                            match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                            match2.team1_scorers()[-1], match2.team1,
                                            match2.current_score))
                                    else:
                                        pass
                                else:
                                    if len(current_team1_assists) > len(previous_team1_assists):
                                        previous_team1_assists = current_team1_assists
                                        api.update_status(
                                            '#EURO2021 \n#{}vs{} \nGoal by : {} ({}) \nAssist: {} \n{}'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.team1_scorers()[-1], match2.team1,
                                                match2.team1_assists()[-1], match2.current_score))
                                    else:
                                        try:
                                            api.update_status('#EURO2021 \n#{}vs{} \nGoal by : {} ({}) \n{}'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.team1_scorers()[-1], match2.team1,
                                                match2.current_score))
                                        except:
                                            api.update_status('#EURO2021 \n#{}vs{} \n{}'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.current_score))

                            elif len(current_team2_events) > len(previous_team2_events):
                                previous_team2_events = current_team2_events
                                if match2.team2_yellow() is True:
                                    if len(current_team2_scorers) > len(previous_team2_scorers):
                                        previous_team2_scorers = current_team2_scorers
                                        api.update_status('#EURO2021 \n#{}vs{} \nYellow Card : {} ({}) \n{}'.format(
                                            match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                            match2.team2_scorers()[-1], match2.team2,
                                            match2.current_score))
                                    else:
                                        pass
                                elif match2.team2_red() is True:
                                    if len(current_team2_scorers) > len(previous_team2_scorers):
                                        previous_team2_scorers = current_team2_scorers
                                        api.update_status('#EURO2021 \n#{}vs{} \nRed Card : {} ({}) \n{}'.format(
                                            match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                            match2.team2_scorers()[-1], match2.team2,
                                            match2.current_score))
                                    else:
                                        pass
                                else:
                                    if len(current_team2_assists) > len(previous_team2_assists):
                                        previous_team2_assists = current_team2_assists
                                        api.update_status(
                                            '#EURO2021 \n#{}vs{} \nGoal by : {} ({}) \nAssist: {} \n{}'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.team2_scorers()[-1], match2.team2,
                                                match2.team2_assists()[-1], match2.current_score))
                                    else:
                                        try:
                                            api.update_status('#EURO2021 \n#{}vs{} \nGoal by : {} ({}) \n{}'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.team2_scorers()[-1], match2.team2,
                                                match2.current_score))
                                        except:
                                            api.update_status('#EURO2021 \n#{}vs{} \n{}'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.current_score))

                            else:
                                if len(previous_times_lst) < len(current_times_lst):
                                    previous_times_lst = current_times_lst
                                    if current_times_lst[-1] == 'HT':
                                        api.update_status('#EURO2021 \n#{}vs{} \nHalf Time: {} \n{}'.format(
                                            match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                            match2.current_score, match2.winner()))
                                        for stat_link in stats_links():
                                            if str(match2.team1).lower() in re.split("-|/", stat_link) or str(
                                                    match2.team2).lower() in re.split("-|/", stat_link):
                                                api.update_status(stats(stat_link))
                                    elif current_times_lst[-1] == 'FT':
                                        api.update_status('#EURO2021 \n#{}vs{} \nFull Time: {} \n{}'.format(
                                            match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                            match2.current_score, match2.winner()))
                                        for stat_link in stats_links():
                                            if str(match2.team1).lower() in re.split("-|/", stat_link) or str(
                                                    match2.team2).lower() in re.split("-|/", stat_link):
                                                api.update_status(stats(stat_link))
                                        break
                                else:
                                    pass
                            time.sleep(60)
