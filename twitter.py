import tweepy
from Match_Info import Football

API_Key = ''
API_Secret_Key = ''
Access_Token = ''
Access_Token_Secret = ''

auth = tweepy.OAuthHandler(API_Key, API_Secret_Key)
auth.set_access_token(Access_Token, Access_Token_Secret)

api = tweepy.API(auth)

