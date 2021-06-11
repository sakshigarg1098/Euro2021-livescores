import tweepy
from Match_Info import Football

API_Key = 'Rl2iEuGVcttMr7XJpPZTfgUrb'
API_Secret_Key = 'qW5qKmxnBAWfZhEnudivqLHkN0VVdAg62HB4VfNAr1QlDbZUA9'
Access_Token = '1402255274984026114-VDnOyMDEdwRkWKgifQaPOlUx5lrkVQ'
Access_Token_Secret = 'ZDO4XrLGLa72KvAgiG5wm8q8tukYQa56b7uYePTjapxiU'

auth = tweepy.OAuthHandler(API_Key, API_Secret_Key)
auth.set_access_token(Access_Token, Access_Token_Secret)

api = tweepy.API(auth)
match2 = Football('https://www.livescore.com/en/football/intl/friendlies/france-vs-bulgaria/414456/')
api.update_status(match2.status())
