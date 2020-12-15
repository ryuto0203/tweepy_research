# coding: UTF-8

import tweepy
import csv
import MeCab
import pandas as pd
import datetime 

tagger = MeCab.Tagger("-Ochasen")
dt = datetime.date.today()

#認証キーの設定
consumer_key = "あなたのconsumer_key"
consumer_secret = "あなたのconsumer_secret"
access_token = "あなたのaccess_token"
access_token_secret = "あなたのaccess_token_secret"

#OAuth認証
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#APIのインスタンスを生成
api = tweepy.API(auth)

#実行したいこと

tweet_data = [] #取得したツイートを格納するリスト
tweet_analysis_result = [] #ツイート解析結果を格納するリスト

#RTが15000件以上のツイートから(id,user名,ツイート作成日,ツイート全文,ツイートの形態素解析結果)の取得
for tweet in api.search(q="lang:ja -filter:links min_retweets:15000 exclude:retweets" ,count=20 ,tweet_mode='extended'):
    try:
        tweet_analyze = tagger.parse(tweet.full_text)
        tweet_data.append([tweet.id, tweet.user.screen_name, tweet.created_at, tweet.full_text.replace('\n',''), tweet.retweet_count, tweet_analyze])
        tweet_analysis_result.append(tweet_analyze)
    except Exception as e:
        print(e)

#データフレームの読み込み
df1 = pd.DataFrame(tweet_data)
df1.columns = ["id","user","created_at","text","RT","analyze"]
df2 = pd.read_excel("total.xlsx")

#データフレーム同士の結合
df_contat = pd.concat([df1, df2])

#df1とdf2を結合したデータをexcelに出力
df_contat.to_excel("total.xlsx",index=False)