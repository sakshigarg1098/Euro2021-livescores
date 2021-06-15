from requests_html import HTMLSession
from Match_Info import Football

match2 = Football('https://www.livescore.com/en/football/africa-cup-of-nations/qualification-group-l/sierra-leone-vs-benin/152305/')


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
