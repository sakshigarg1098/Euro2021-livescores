from requests_html import HTMLSession
from datetime import datetime, timedelta
import re
from Match_Info import Football

session = HTMLSession()
matches = 'https://www.goal.com/en-in/live-scores'
res = session.get(matches)
match_data = res.html.find('.match-row-list', first=True)
details = match_data.find('[href^="/en-in/match/"]')
m = Football('https://www.livescore.com/en/football/euro-2020/group-b/belgium-vs-russia/80736/')
'''lineups_link_lst = []
for detail in details:
    link = str(detail).split("'")[-2].split('/')
    link.insert(4, 'lineups')
    link[0] = 'https://www.goal.com'
    link = '/'.join(link)
    lineups_link_lst.append(link)
print(lineups_link_lst)
for link in lineups_link_lst:
    if str(m.team1).lower() in re.split("-|/", link) and str(m.team2).lower() in re.split("-|/", link):
        if lineups_post_time == datetime.now().strftime('%H:%M'):
            players = []
            lineups = session.get(link).html.find('.widget-match-lineups__list.widget-match-lineups__starting-eleven .widget-match-lineups__name')
            for player in lineups:
                players.append(player.text)
            players_team1 = players[:11]
            players_team2 = players[11:]
            print('{} Lineups: {} \n{} Lineups: {}'.format(m.team1, players_team1, m.team2, players_team2))'''

stats_link_lst = []
for detail in details:
    link = str(detail).split("'")[-2].split('/')
    link.insert(4, 'commentary-result')
    link[0] = 'https://www.goal.com'
    link = '/'.join(link)
    stats_link_lst.append(link)
print(stats_link_lst)
for link in stats_link_lst:
    if str(m.team1).lower() in re.split("-|/", link) and str(m.team2).lower() in re.split("-|/", link):
        stats = session.get(link).html.find('.widget-match-stats .content')[0].text
        possession = '{} - {} | {} - {}'.format(m.team1, stats.split()[1], m.team2, stats.split()[2])
        shots_on_target = '{} - {} | {} - {}'.format(m.team1, stats.split()[11], m.team2, stats.split()[12])
        total_passes = '{} - {} | {} - {}'.format(m.team1, stats.split()[15], m.team2, stats.split()[16])
        print('Possession: {} \nShots on Target: {} \nTotal Passes: {}'.format(possession, shots_on_target, total_passes))

