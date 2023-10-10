# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 17:58:06 2022

@author: 

Only the keys were changed for this software to work in the Twitter account @radarPopocatep

"""

import tweepy
import os

# Consumer keys and access tokens, used for OAuth
consumer_key = 'TVKBG8sNIF3ApwNwkqc6VTpuo'
consumer_secret = 'ATQNeN9AqfNmGez2pmBeM7upIPjGWsxFFAASRH7YV6CyzAUV6e'
access_token = '789706571408257025-rr3DgKrUAKdgDfNhDTvevw9CyjFtpEW'
access_token_secret = '95fvY2UaMwMUBH5Q4nU3kppRNefqPcH1grT0tS79aI1Hv'
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
photo_path = 'c:/Users/radar1/Desktop/0087_20220513_234500_ZDR1.png'
status = 'Subject o text'
api.update_with_media(photo_path, status=status)

    
    # TVKBG8sNIF3ApwNwkqc6VTpuo  #API Key
    # ATQNeN9AqfNmGez2pmBeM7upIPjGWsxFFAASRH7YV6CyzAUV6e # API Key Secret
    # AAAAAAAAAAAAAAAAAAAAANh8eAEAAAAAKdw9%2BTX%2BA%2BwpIwk4kLADjjXM4rs%3D9xx3dSdeMMrpDKAQ16eerAW3380tYcJmSW9JKQzaySLSF57uvo  #Bearer Token
    # 789706571408257025-rr3DgKrUAKdgDfNhDTvevw9CyjFtpEW #Access Token
    # 95fvY2UaMwMUBH5Q4nU3kppRNefqPcH1grT0tS79aI1Hv  #Access token secret