from requests_html import HTMLSession
from datetime import datetime
import re


'''def stats(goal_homepage):
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
        if str(m.team1).lower() in re.split("-|/", link) and str(m.team2).lower() in re.split("-|/", link):
            stats = session.get(link).html.find('.widget-match-stats .content')[0].text
            possession = '{} - {} | {} - {}'.format(m.team1, stats.split()[1], m.team2, stats.split()[2])
            shots_on_target = '{} - {} | {} - {}'.format(m.team1, stats.split()[11], m.team2, stats.split()[12])
            total_passes = '{} - {} | {} - {}'.format(m.team1, stats.split()[15], m.team2, stats.split()[16])
            print('Possession: {} \nShots on Target: {} \nTotal Passes: {}'.format(possession, shots_on_target, total_passes))'''



'''def stats_post_time(scheduled_time_str):
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
    return ':'.join(time_list)'''
