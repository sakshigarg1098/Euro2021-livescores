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
            try:
                self.team1 = self.match_details_lst[1][2:]
                self.team2 = self.match_details_lst[3]
                self.current_score = self.match_details_lst[2]
                self.team1_score = int((self.match_details_lst[2])[0])
                self.team2_score = int((self.match_details_lst[2])[4])
            except:
                pass
        else:
            self.team1 = self.match_details_lst[0][2:]
            self.team2 = self.match_details_lst[2]
            self.current_score = self.match_details_lst[1]
            self.team1_score = int((self.match_details_lst[1])[0])
            self.team2_score = int((self.match_details_lst[1])[4])

    def winner(self):
        if self.team1_score > self.team2_score:
            return 'Winner is: {}'.format(self.team1)
        elif self.team1_score < self.team2_score:
            return 'Winner is: {}'.format(self.team2)
        else:
            return 'Draw'

    def final_score(self):
        return self.current_score

    def scorers_team1(self):
        scorers_team1_lst = []
        for scorer_team1 in self.match_codes.find('.Details_home__3KOJn .Details_player__2bYfI'):
            scorers_team1_lst.append(scorer_team1.text)
        return scorers_team1_lst

    def assists_team1(self):
        assists_team1_lst = []
        for assists_team1 in self.match_codes.find('.Details_home__3KOJn .Details_assist__x9ykY'):
            assists_team1_lst.append(assists_team1.text)
        return assists_team1_lst

    def scorers_team2(self):
        scorers_team2_lst = []
        for scorer_team2 in self.match_codes.find('.Details_away__2_UTs .Details_player__2bYfI'):
            scorers_team2_lst.append(scorer_team2.text)
        return scorers_team2_lst

    def assists_team2(self):
        assists_team2_lst = []
        for assists_team2 in self.match_codes.find('.Details_away__2_UTs .Details_assist__x9ykY'):
            assists_team2_lst.append(assists_team2.text)
        return assists_team2_lst

    def status(self):
        warning = 'This match has a limited coverage. Score updates may be delayed.'
        if self.match_details[:2] == 'FT':
            return '{} , Score: {}'.format(self.winner(), self.current_score)
        elif self.match_details[:4] == 'Post':
            return 'The match has been postponed.'
        elif self.match_details_lst[0].isdigit():
            return 'Current Score is: {}, Minutes Passed:'.format(self.current_score, self.match_details_lst[0])
        else:
            if self.match_details_lst[3] == warning:
                return 'The match is scheduled at: {}. {}'.format(self.match_details[:5], warning)
            else:
                return 'The match is scheduled at: {}'.format(self.match_details[:5])


match1 = Football('https://www.livescore.com/en/football/algeria/league-cup/nc-magra-vs-usm-alger/434836/')
match2 = Football('https://www.livescore.com/en/football/intl/friendlies/faroe-islands-vs-liechtenstein/432686/')
match3 = Football('https://www.livescore.com/en/football/intl/friendlies/germany-vs-latvia/393055/')

print(match1.status())
print(match2.status())
print(match3.assists_team2())
