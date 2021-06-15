from requests_html import HTMLSession
import re


class Football:

    def __init__(self, match_link):
        session = HTMLSession()
        self.res = session.get(match_link)
        self.match_codes = self.res.html.find('#__livescore', first=True)
        self.match_details = self.match_codes.text
        self.match_details_lst = re.split("'|\n", self.match_details)

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

        if self.match_details[0].isdigit():
            if self.match_details_lst[0].isdigit():
                self.team1 = self.match_details_lst[1]
                self.team2 = self.match_details_lst[3]
                self.current_score = '{}   {}   {}'.format(
                    flags[self.team1]+self.team1, self.match_details_lst[2], self.team2+flags[self.team2])
                self.team1_score = int((self.match_details_lst[2])[0])
                self.team2_score = int((self.match_details_lst[2])[4])
                self.scheduled_time = 'None'
            else:
                self.team1 = self.match_details_lst[0][5:]
                self.team2 = self.match_details_lst[2]
                self.current_score = None
                self.team1_score = None
                self.team2_score = None
                self.res.html.render(timeout=30)
                self.scheduled_time = self.res.html.find(".MatchDetailScore_status__16-uQ")[0].text
        else:
            if self.match_details[:2] == 'FT' or self.match_details[:2] == 'HT':
                self.team1 = self.match_details_lst[0][2:]
                self.team2 = self.match_details_lst[2]
                self.current_score = '{}   {}   {}'.format(
                    flags[self.team1]+self.team1, self.match_details_lst[1], self.team2+flags[self.team2])
                self.team1_score = int((self.match_details_lst[1])[0])
                self.team2_score = int((self.match_details_lst[1])[4])
                self.scheduled_time = 'None'
            else:
                self.team2 = self.match_details_lst[2]
                self.current_score = None
                self.team1_score = None
                self.team2_score = None
                self.scheduled_time = 'None'
                if self.match_details[:5] == 'Canc.':
                    self.team1 = self.match_details_lst[0][5:]
                else:
                    self.team1 = self.match_details_lst[0][6:]

    def winner(self):  # gives winning team (or draw)
        if self.team1_score > self.team2_score:
            return '{} Won!'.format(self.team1)
        elif self.team1_score < self.team2_score:
            return '{} Won!'.format(self.team2)
        else:
            return 'DRAW!'

    def times_(self):     # getting list of events (HT and FT)
        times_ = []
        for time_ in self.match_codes.find('.MatchDetailScore_matchScoreRow__1Lkxo .MatchDetailScore_status__16-uQ'):
            times_.append(time_.text)
        return times_[1:]

    def team1_scorers(self):     # team1 players who scored a goal / yellow/red card / goal penalty / own goal
        scorers_team1_lst = []
        for scorer_team1 in self.match_codes.find('.Details_home__3KOJn .Details_player__2bYfI'):
            if scorer_team1.text != '':
                scorers_team1_lst.append(scorer_team1.text)
        return scorers_team1_lst

    def team1_assists(self):     # list of team 1 assists
        assists_team1_lst = []
        for assists_team1 in self.match_codes.find('.Details_home__3KOJn .Details_assist__x9ykY'):
            assists_team1_lst.append(assists_team1.text)
        return assists_team1_lst

    def team1_yellow(self):    # list of yellow card events of team 1
        if self.team1_events()[-1][:18] == 'FootballYellowCard':
            return True

    def team1_red(self):    # list of red card events of team 1
        if self.team1_events()[-1][:15] == 'FootballRedCard':
            return True

    def team2_scorers(self):      # team2 players who scored a goal / yellow/red card / goal penalty / own goal
        scorers_team2_lst = []
        for scorer_team2 in self.match_codes.find('.Details_away__2_UTs .Details_player__2bYfI'):
            if scorer_team2.text != '':
                scorers_team2_lst.append(scorer_team2.text)
        return scorers_team2_lst

    def team2_assists(self):     # list of team 2 assists
        assists_team2_lst = []
        for assists_team2 in self.match_codes.find('.Details_away__2_UTs .Details_assist__x9ykY'):
            assists_team2_lst.append(assists_team2.text)
        return assists_team2_lst

    def team2_yellow(self):    # list of yellow card events of team 2
        if self.team2_events()[-1][:18] == 'FootballYellowCard':
            return True

    def team2_red(self):    # list of red card events of team 2
        if self.team2_events()[-1][:15] == 'FootballRedCard':
            return True

    def score_lst(self):     # list of all scores event wise
        scores = []
        for score in self.match_codes.find('.Details_center__26WH5 .Details_top__cKmrC'):
            scores.append(score.text)
        return scores

    def team1_events(self):     # list of all the events (goal/yellow/red) of team 1
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

    def team2_events(self):     # list of all the events (goal/yellow/red) of team 2
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

    def status(self):     # gives status of a match (FT/HT/current score/winner/scheduled time/cancelled/postponed)
        warning = 'This match has a limited coverage. Score updates may be delayed.'
        if self.match_details[:2] == 'FT':
            return '{} \nScore: {}'.format(self.winner(), self.current_score)
        elif self.match_details[:2] == 'HT':
            return 'HT | Score: {}'.format(self.current_score)
        elif self.match_details[:4] == 'Post':
            return 'This match has been postponed.'
        elif self.match_details[:4] == 'Canc':
            return 'This match has been cancelled.'
        elif self.match_details_lst[0].isdigit():
            return 'Current Score is: {}, Minutes Passed:'.format(self.current_score, self.match_details_lst[0])
        else:
            if self.match_details_lst[3] == warning:
                self.res.html.render(sleep=1)
                return 'Scheduled at: {}. {}'.format(self.res.html.find(".MatchDetailScore_status__16-uQ")[0].text,
                                                     warning)
            else:
                self.res.html.render(sleep=1)
                return 'Scheduled at: {}'.format(self.res.html.find(".MatchDetailScore_status__16-uQ")[0].text)
