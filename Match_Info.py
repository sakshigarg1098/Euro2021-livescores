import time
from requests_html import HTMLSession
import re


class Football:

    def __init__(self, match_link):
        session = HTMLSession()
        res = session.get(match_link)
        self.match_codes = res.html.find('#__livescore', first=True)
        self.match_details = self.match_codes.text
        self.match_details_lst = re.split("'|\n", self.match_details)
        if self.match_details[0].isdigit():
            if self.match_details_lst[0].isdigit():
                self.team1 = self.match_details_lst[1]
                self.team2 = self.match_details_lst[3]
                self.current_score = '{}   {}   {}'.format(self.team1, self.match_details_lst[2], self.team2)
                self.team1_score = int((self.match_details_lst[2])[0])
                self.team2_score = int((self.match_details_lst[2])[4])
            else:
                self.team1 = self.match_details_lst[0][5:]
                self.team2 = self.match_details_lst[2]
                self.current_score = None
                self.team1_score = None
                self.team2_score = None
        else:
            if self.match_details[:2] == 'FT' or self.match_details[:2] == 'HT':
                self.team1 = self.match_details_lst[0][2:]
                self.team2 = self.match_details_lst[2]
                self.current_score = '{}   {}   {}'.format(self.team1, self.match_details_lst[1], self.team2)
                self.team1_score = int((self.match_details_lst[1])[0])
                self.team2_score = int((self.match_details_lst[1])[4])
            else:
                self.team2 = self.match_details_lst[2]
                self.current_score = None
                self.team1_score = None
                self.team2_score = None
                if self.match_details[:5] == 'Canc.':
                    self.team1 = self.match_details_lst[0][5:]
                else:
                    self.team1 = self.match_details_lst[0][6:]

    def winner(self):
        if self.team1_score > self.team2_score:
            return 'Winner is: {}'.format(self.team1)
        elif self.team1_score < self.team2_score:
            return 'Winner is: {}'.format(self.team2)
        else:
            return 'Draw'

    def final_score(self):
        return self.current_score

    def team1_scorers(self):
        scorers_team1_lst = []
        for scorer_team1 in self.match_codes.find('.Details_home__3KOJn .Details_player__2bYfI'):
            if scorer_team1.text != '':
                scorers_team1_lst.append(scorer_team1.text)
        return scorers_team1_lst

    def team1_assists(self):
        assists_team1_lst = []
        for assists_team1 in self.match_codes.find('.Details_home__3KOJn .Details_assist__x9ykY'):
            assists_team1_lst.append(assists_team1.text)
        return assists_team1_lst

    def team2_scorers(self):
        scorers_team2_lst = []
        for scorer_team2 in self.match_codes.find('.Details_away__2_UTs .Details_player__2bYfI'):
            if scorer_team2.text != '':
                scorers_team2_lst.append(scorer_team2.text)
        return scorers_team2_lst

    def team2_assists(self):
        assists_team2_lst = []
        for assists_team2 in self.match_codes.find('.Details_away__2_UTs .Details_assist__x9ykY'):
            assists_team2_lst.append(assists_team2.text)
        return assists_team2_lst

    def score_lst(self):
        scores = []
        for score in self.match_codes.find('.Details_center__26WH5 .Details_top__cKmrC'):
            scores.append(score.text)
        return scores

    def team1_events(self):
        events = []
        icon_list = self.match_codes.find('.Common_iconWrapper__3p9Oo')
        for icon in icon_list:
            if len(icon.html.split("><")) > 1:
                s1 = icon.html.split("><")[1].split('"')[-2] + str(icon_list.index(icon))
                events.append(s1)
            else:
                s2 = 'None' + str(icon_list.index(icon))
                events.append(s2)
        team1_events = []
        for event in events:
            if events.index(event) % 2 == 0 and event[0:4] != 'None':
                team1_events.append(event)
        return team1_events

    def team2_events(self):
        events = []
        icon_list = self.match_codes.find('.Common_iconWrapper__3p9Oo')
        for icon in icon_list:
            if len(icon.html.split("><")) > 1:
                s1 = icon.html.split("><")[1].split('"')[-2] + str(icon_list.index(icon))
                events.append(s1)
            else:
                s2 = 'None' + str(icon_list.index(icon))
                events.append(s2)
        team2_events = []
        for event in events:
            if events.index(event) % 2 == 1 and event[0:4] != 'None':
                team2_events.append(event)
        return team2_events

    def status(self):
        warning = 'This match has a limited coverage. Score updates may be delayed.'
        if self.match_details[:2] == 'FT':
            return '{} , Score: {}'.format(self.winner(), self.current_score)
        elif self.match_details[:2] == 'HT':
            return 'HT, Score: {}'.format(self.current_score)
        elif self.match_details[:4] == 'Post':
            return 'This match has been postponed.'
        elif self.match_details[:4] == 'Canc':
            return 'This match has been cancelled.'
        elif self.match_details_lst[0].isdigit():
            return 'Current Score is: {}, Minutes Passed:'.format(self.current_score, self.match_details_lst[0])
        else:
            if self.match_details_lst[3] == warning:
                return 'Scheduled at: {}. {}'.format(self.match_details[:5], warning)
            else:
                return 'Scheduled at: {}'.format(self.match_details[:5])


previous_team1_events = []
previous_team2_events = []
while True:
    match2 = Football(
        'https://www.livescore.com/en/football/argentina/primera-nacional-zone-b/tristan-suarez-vs-guillermo-brown/383924/')

    current_team1_events = match2.team1_events()
    current_team2_events = match2.team2_events()

    if len(current_team1_events) > len(previous_team1_events):
        previous_team1_events = current_team1_events
        if current_team1_events[-1][:18] == 'FootballYellowCard':
            print('Yellow Card by : {} ({})'.format(match2.team1_scorers()[-1], match2.team1))
        elif current_team1_events[-1][:15] == 'FootballRedCard':
            print('Red Card by : {}'.format(match2.team1_scorers()[-1], match2.team1))
        else:
            print(match2.final_score())
            print('Goal by : {} ({})'.format(match2.team1_scorers()[-1], match2.team1))

    elif len(current_team2_events) > len(previous_team2_events):
        previous_team2_events = current_team2_events
        if current_team2_events[-1][:18] == 'FootballYellowCard':
            print('Yellow Card by : {} ({})'.format(match2.team2_scorers()[-1], match2.team2))
        elif current_team2_events[-1][:15] == 'FootballRedCard':
            print('Red Card by : {}'.format(match2.team2_scorers()[-1], match2.team2))
        else:
            print(match2.final_score())
            print('Goal by : {} ({})'.format(match2.team2_scorers()[-1], match2.team2))

    else:
        pass
    time.sleep(300)
