import time
import tweepy
from datetime import datetime
from Match_Info import Football
import re
from requests_html import HTMLSession

API_Key = ''
API_Secret_Key = ''
Access_Token = ''
Access_Token_Secret = ''

auth = tweepy.OAuthHandler(API_Key, API_Secret_Key)
auth.set_access_token(Access_Token, Access_Token_Secret)
api = tweepy.API(auth)

session = HTMLSession()
r = session.get('https://www.livescore.com/en/football/' + datetime.now().strftime('%Y-%m-%d') + '/')
r.html.render(sleep=1)
body = r.html.xpath('//*[@id="match-rows__root"]')[0]
euro_links = body.absolute_links
euro_match_links = []
for link in euro_links:
    if "euro-2020" in link and len(link) > 60:
        euro_match_links.append(link)

        flags = {'Wales': '\U0001F3F4\U000E0067\U000E0062\U000E0077\U000E006C\U000E0073\U000E007F',
                 'Ukraine': '\U0001F1FA\U0001F1E6', 'Turkey': '\U0001F1F9\U0001F1F7',
                 'Switzerland': '\U0001F1E8\U0001F1ED',
                 'Sweden': '\U0001F1F8\U0001F1EA', 'Spain': '\U0001F1EA\U0001F1F8',
                 'Slovakia': '\U0001F1F8\U0001F1F0',
                 'Scotland': '\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F',
                 'Russia': '\U0001F1F7\U0001F1FA', 'Portugal': '\U0001F1F5\U0001F1F9', 'Poland': '\U0001F1F5\U0001F1F1',
                 'North Macedonia': '\U0001F1F2\U0001F1F0', 'Netherlands': '\U0001F1F3\U0001F1F1',
                 'Italy': '\U0001F1EE\U0001F1F9', 'Hungary': '\U0001F1ED\U0001F1FA', 'Germany': '\U0001F1E9\U0001F1EA',
                 'France': '\U0001F1EB\U0001F1F7', 'Finland': '\U0001F1EB\U0001F1EE',
                 'England': '\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F',
                 'Denmark': '\U0001F1E9\U0001F1F0', 'Czech Republic': '\U0001F1E8\U0001F1FF',
                 'Croatia': '\U0001F1ED\U0001F1F7',
                 'Belgium': '\U0001F1E7\U0001F1EA', 'Austria': '\U0001F1E6\U0001F1F9'}


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


def lineups1(lineups_link):
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
    lineup = '#EURO2021 \n#{}vs{} \nLINE-UPS - {} {}:\n{}'.format(
        teams[0].replace(' ', ''), teams[1].replace(' ', ''), teams[0], flags[teams[0]], '\n'.join(players[:11]))
    return lineup


def lineups2(lineups_link):
    session5 = HTMLSession()
    players = []
    teams = []
    lineups_data = session5.get(lineups_link).html.find(
        '.widget-match-lineups__list.widget-match-lineups__starting-eleven .widget-match-lineups__name')
    teams_data = session.get(lineups_link).html.find('.widget-match-header__name--full')
    for team in teams_data:
        teams.append(team.text)
    for player in lineups_data:
        players.append(player.text)
    lineup = '#EURO2021 \n#{}vs{} \nLINE-UPS - {} {}:\n{}'.format(
        teams[0].replace(' ', ''), teams[1].replace(' ', ''), teams[1], flags[teams[1]], '\n'.join(players[11:]))
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
    shots_on_target = '{} - {} | {} - {}'.format(
        match2.team1, stats_data.split()[11], match2.team2, stats_data.split()[12])
    total_passes = '{} - {} | {} - {}'.format(
        match2.team1, stats_data.split()[15], match2.team2, stats_data.split()[16])
    return '#EURO2021 \n#{}vs{} \nPossession: \n{} \nShots on Target: \n{} \nTotal Passes: \n{}'.format(
        match2.team1.replace(' ', ''), match2.team2.replace(' ', ''), possession, shots_on_target, total_passes)

# running an infinite while loop to set the timings for each match, every day automatically and posts:
# the lineups before the match starts,
# the statistics at HT,
# the live scores, yellow cards, red cards and player name,
# winner and final score

while True:

    for link in euro_match_links:
        match = Football(link)

        if match.scheduled_time[0].isdigit():

            if datetime.now().strftime('%H') == match.scheduled_time.split(":")[0]:

                if int(match.scheduled_time.split(":")[1])-15 < int(datetime.now().strftime("%M")) < int(
                        match.scheduled_time.split(":")[1]):

                    for lineup_link in lineups_links():

                        if str(match.team1).lower() in re.split("-|/", lineup_link) or str(
                                match.team2).lower() in re.split("-|/", lineup_link):

                            match2 = Football(link)

                            print('{} vs {} about to begin!'.format(
                                match2.team1.upper(), match2.team2.upper()))
                            print(lineups1(lineup_link))
                            print(lineups2(lineup_link))
                            print()

                            api.update_status('{} vs {} about to begin!'.format(
                                match2.team1.upper(), match2.team2.upper()))
                            api.update_status(lineups1(lineup_link))
                            api.update_status(lineups2(lineup_link))

                            previous_team1_events = []
                            previous_team2_events = []
                            previous_team1_assists = []
                            previous_team2_assists = []
                            previous_team1_scorers = []
                            previous_team2_scorers = []
                            previous_times_lst = []

                            while True:

                                match2 = Football(link)
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
                                            api.update_status('#EURO2021 \n#{}vs{} \nYellow Card : {} ({})'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.team1_scorers()[-1], match2.team1))

                                            print(match2.team1)
                                            print(match2.team2)
                                            print('#EURO2021 \n#{}vs{} \nYellow Card : {} ({})'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.team1_scorers()[-1], match2.team1))
                                            print()

                                        else:
                                            pass
                                    elif match2.team1_red() is True:
                                        if len(current_team1_scorers) > len(previous_team1_scorers):
                                            previous_team1_scorers = current_team1_scorers
                                            api.update_status('#EURO2021 \n#{}vs{} \nRed Card : {} ({})'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.team1_scorers()[-1], match2.team1))

                                            print(match2.team1)
                                            print(match2.team2)
                                            print('#EURO2021 \n#{}vs{} \nRed Card : {} ({})'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.team1_scorers()[-1], match2.team1))
                                            print()

                                        else:
                                            pass

                                    elif match2.team1_red() is True:
                                        if len(current_team1_scorers) > len(previous_team1_scorers):
                                            previous_team1_scorers = current_team1_scorers
                                            api.update_status('#EURO2021 \n#{}vs{} \nRed Card : {} ({})'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.team1_scorers()[-1], match2.team1))

                                            print(match2.team1)
                                            print(match2.team2)
                                            print('#EURO2021 \n#{}vs{} \nRed Card : {} ({})'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.team1_scorers()[-1], match2.team1))
                                            print()

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

                                            print(match2.team1)
                                            print(match2.team2)
                                            print('#EURO2021 \n#{}vs{} \nGoal by : {} ({}) \nAssist: {} \n{}'.format(
                                                    match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                    match2.team1_scorers()[-1], match2.team1,
                                                    match2.team1_assists()[-1], match2.current_score))
                                            print()

                                        else:
                                            try:
                                                api.update_status('#EURO2021 \n#{}vs{} \nGoal by : {} ({}) \n{}'.format(
                                                    match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                    match2.team1_scorers()[-1], match2.team1,
                                                    match2.current_score))

                                                print(match2.team1)
                                                print(match2.team2)
                                                print('#EURO2021 \n#{}vs{} \nGoal by : {} ({}) \n{}'.format(
                                                    match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                    match2.team1_scorers()[-1], match2.team1,
                                                    match2.current_score))
                                                print()

                                            except:
                                                api.update_status('#EURO2021 \n#{}vs{} \n{}'.format(
                                                    match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                    match2.current_score))

                                                print(match2.team1)
                                                print(match2.team2)
                                                print('#EURO2021 \n#{}vs{} \n{}'.format(
                                                    match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                    match2.current_score))
                                                print()

                                elif len(current_team2_events) > len(previous_team2_events):
                                    previous_team2_events = current_team2_events
                                    if match2.team2_yellow() is True:
                                        if len(current_team2_scorers) > len(previous_team2_scorers):
                                            previous_team2_scorers = current_team2_scorers
                                            api.update_status('#EURO2021 \n#{}vs{} \nYellow Card : {} ({})'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.team2_scorers()[-1], match2.team2))

                                            print(match2.team1)
                                            print(match2.team2)
                                            print('#EURO2021 \n#{}vs{} \nYellow Card : {} ({})'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.team2_scorers()[-1], match2.team2))
                                            print()

                                        else:
                                            pass
                                    elif match2.team2_red() is True:
                                        if len(current_team2_scorers) > len(previous_team2_scorers):
                                            previous_team2_scorers = current_team2_scorers
                                            api.update_status('#EURO2021 \n#{}vs{} \nRed Card : {} ({})'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.team2_scorers()[-1], match2.team2))

                                            print(match2.team1)
                                            print(match2.team2)
                                            print('#EURO2021 \n#{}vs{} \nRed Card : {} ({})'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.team2_scorers()[-1], match2.team2))
                                            print()

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

                                            print(match2.team1)
                                            print(match2.team2)
                                            print('#EURO2021 \n#{}vs{} \nGoal by : {} ({}) \nAssist: {} \n{}'.format(
                                                    match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                    match2.team2_scorers()[-1], match2.team2,
                                                    match2.team2_assists()[-1], match2.current_score))
                                            print()

                                        else:
                                            try:
                                                api.update_status('#EURO2021 \n#{}vs{} \nGoal by : {} ({}) \n{}'.format(
                                                    match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                    match2.team2_scorers()[-1], match2.team2,
                                                    match2.current_score))

                                                print(match2.team1)
                                                print(match2.team2)
                                                print('#EURO2021 \n#{}vs{} \nGoal by : {} ({}) \n{}'.format(
                                                    match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                    match2.team2_scorers()[-1], match2.team2,
                                                    match2.current_score))
                                                print()

                                            except:
                                                api.update_status('#EURO2021 \n#{}vs{} \n{}'.format(
                                                    match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                    match2.current_score))

                                                print(match2.team1)
                                                print(match2.team2)
                                                print('#EURO2021 \n#{}vs{} \n{}'.format(
                                                    match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                    match2.current_score))
                                                print()

                                else:
                                    if len(previous_times_lst) < len(current_times_lst):
                                        previous_times_lst = current_times_lst
                                        if current_times_lst[-1] == 'HT':
                                            for stat_link in stats_links():
                                                if str(match2.team1).lower() in re.split("-|/", stat_link) or str(
                                                        match2.team2).lower() in re.split("-|/", stat_link):
                                                    api.update_status(stats(stat_link))
                                            api.update_status('#EURO2021 \n#{}vs{} \nHalf Time: {}'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.current_score))
                                        elif current_times_lst[-1] == 'FT':
                                            for stat_link in stats_links():
                                                if str(match2.team1).lower() in re.split("-|/", stat_link) or str(
                                                        match2.team2).lower() in re.split("-|/", stat_link):
                                                    api.update_status(stats(stat_link))
                                            api.update_status('#EURO2021 \n#{}vs{} \nFull Time: {} \n{}'.format(
                                                match2.team1.replace(' ', ''), match2.team2.replace(' ', ''),
                                                match2.current_score, match2.winner()))
                                            break
                                    else:
                                        pass

                                time.sleep(60)
            else:
                time.sleep(600)
