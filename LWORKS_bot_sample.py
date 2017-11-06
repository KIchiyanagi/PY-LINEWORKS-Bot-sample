import json
import requests
import jwt
import cryptography
from datetime import datetime

# this file is designed for python3 on mac

#テナント情報
APIKEY = 'APIKEY'
SERVER_CKEY = 'SERVER CONSUMER KEY'
SERVERID = "Server ID(ID 登録タイプの方)"
PRIVKEY = '認証キーファイルのパス'


#JWT から server token の生成。成功すると token とexpire date を返す。失敗すると 0 を返す。
def gettoken(ServerId,PrivateKey):
        # claimset 生成時間及び 終了時間 (30分設定)
        crnttime = int(datetime.now().strftime('%s'))
        exptime = crnttime + 1800

        # claimset
        claimset = {
                "iss":ServerId,
                "iat":crnttime,
                "exp":exptime
                }
        #RSA秘密鍵
        key = open(PrivateKey).read()
        #JWT生成
        lw_jwt = jwt.encode(claimset,key,algorithm='RS256')

        # Token 発行
        url = 'https://authapi.worksmobile.com/b/' +APIKEY +'/server/token'
        header = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'charset': 'utf-8'
                }
        payload = {
                'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                'assertion' : lw_jwt.decode('utf-8')
                }
        r = requests.post(url, headers=header, params=payload)
        if r.status_code == 200:
                return r.text
        else:
                return 0
#Bot 登録。成功した場合には BotNo を返す
def regbot(BotName, PhotoURL,Status,ServerTOKEN):
        #リクエスト URL の作成
        url = 'https://apis.worksmobile.com/' + APIKEY + '/message/registerBot/v2'

        header = {
                'consumerKey': SERVER_CKEY,
                'Authorization': 'Bearer ' + ServerTOKEN,
                'Content-Type': 'application/json',
                'charset': 'utf-8'
                }

        payload = {
                "name" : BotName,
                "photoUrl": PhotoURL,
                "status": Status
                }
        r = requests.post(url, headers = header, data = json.dumps(payload))
        if r.json()["code"] == 200:
                return r.json()['botNo']
        else:
                print('registration error.')
                return r.json()
#Bot 修正。成功した場合には 200 を返す
def updatebot(BotNo, BotName, PhotoURL,Status,ServerTOKEN):
        #リクエスト URL の作成
        url = 'https://apis.worksmobile.com/' + APIKEY + '/message/updateBot/v2'

        header = {
                'consumerKey': SERVER_CKEY,
                'Authorization': 'Bearer ' + ServerTOKEN,
                'Content-Type': 'application/json',
                'charset': 'utf-8'
                }

        payload = {
                "botNo": BotNo,
                "name" : BotName,
                "photoUrl": PhotoURL,
                "status": Status
                }

        r = requests.post(url, headers = header, data = json.dumps(payload))
        if r.status_code == 200:
                if r.json()["code"] == 200:
                        return r.json()['code']
                else:
                        print('registration error.')
                        return r.json()
        else:
                return 0
#Bot ドメイン登録。成功した場合には 200 を返す
def regbotdomain(BotNo,domainid,ServerTOKEN):
        #リクエスト URL の作成
        url = 'https://apis.worksmobile.com/' + APIKEY + '/message/registerBotDomain/v2'

        header = {
                'consumerKey': SERVER_CKEY,
                'Authorization': 'Bearer ' + ServerTOKEN,
                'Content-Type': 'application/json',
                'charset': 'utf-8'
        }
        payload = {
                "botNo": BotNo,
                "domainId": domainid
                }
        r = requests.post(url, headers = header, data = json.dumps(payload))
        if r.status_code == 200 :
                return r
        else:
                return 0
#Bot ドメイン削除。成功した場合には 200 を返す。
def removebotdomain(BotNo,domainid,ServerTOKEN):
        #リクエスト URL の作成
        url = 'https://apis.worksmobile.com/' + APIKEY + '/message/removeBotDomain/v2'

        header = {
                'consumerKey': SERVER_CKEY,
                'Authorization': 'Bearer ' + ServerTOKEN,
                'Content-Type': 'application/json',
                'charset': 'utf-8'
        }
        payload = {
                "botNo": BotNo,
                "domainId": domainid
                }
        r = requests.post(url, headers = header, data = json.dumps(payload))
        return r
#Bot リストの取得。成功した場合にはjsonで Bot list を返す
def getbotlist(ServerTOKEN):
        #リクエスト URL の作成
        url = 'https://apis.worksmobile.com/' + APIKEY + '/message/getBotList/v2'

        header = {
                'consumerKey': SERVER_CKEY,
               'Authorization': 'Bearer ' + ServerTOKEN,
                'Content-Type': 'application/json',
                'charset': 'UTF-8' 
               }

        payload = {
                'isActive': True
                }

        r = requests.post(url, headers = header, data = json.dumps(payload))
        if r.status_code == 200:
                if r.json()["code"] == 200:
                        return r.json()
                else:
                        return r.json()['code']
        else:
                print('error')
                return r.json()
#Bot 詳細の取得。成功した場合にはjsonで Bot info を返す
def getbotinfo(BotNo,ServerTOKEN):
        #リクエスト URL の作成
        url = 'https://apis.worksmobile.com/' + APIKEY + '/message/getBotInfo/v2'

        header = {
                'consumerKey': SERVER_CKEY,
               'Authorization': 'Bearer ' + ServerTOKEN,
                'Content-Type': 'application/json',
                'charset': 'UTF-8' 
               }

        payload = {
                'botNo': BotNo
                }

        r = requests.post(url, headers = header, data=json.dumps(payload))
        if r.json()["code"] == 200:
                return r.json()
        else:
                print('cannot get botlists')
                return r.json()['code']
#Bot の callback URL をセットする
def setcallbackurl(BotNo, callbackURL,ServerTOKEN):
        #リクエスト URL の作成
        url = 'https://apis.worksmobile.com/' + APIKEY + '/message/setCallback/v2'

        header = {
                'consumerKey': SERVER_CKEY,
               'Authorization': 'Bearer ' + ServerTOKEN,
                'Content-Type': 'application/json',
                'charset': 'UTF-8' 
               }

        payload = {
                'botNo':BotNo,
                'callbackUrl':callbackURL,
                'callbackEventList':["text"]                
                }

        r = requests.post(url, headers = header, data=json.dumps(payload))
        if r.json()["code"] == 200:
                return r.json()
        else:
                print('cannot get botlists')
                return r.json()['code']
#メッセージ送信。成功した場合にはjsonメッセージを返す。
def sendmsg(BotNo, TargetId, Message,ServerTOKEN):
        #リクエストURLの作成
        url = 'https://apis.worksmobile.com/' + APIKEY + '/message/sendMessage/v2'
        
        header = {
                'consumerKey': SERVER_CKEY,
                'Authorization': 'Bearer ' + ServerTOKEN,
                'Content-Type': 'application/json'
                }
        
        payload = {
                "botNo" : BotNo,
                "accountId" : TargetId,
                "content" : {
                        "type": "text",
                        "text": Message
                        }
                }

        #jsonデータの作成
        r = requests.post(url, headers = header, data = json.dumps(payload))
        if r.json()["code"] == 200:
                return r.json()
        else:
                print('cannot send your message.')
                return r.json()['code']


#TOKEN 取得の例
#f = open('token.txt','w')
#tokentext = gettoken(SERVERID,PRIVKEY)
#f.write(tokentext)
