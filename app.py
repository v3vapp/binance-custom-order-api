from flask import Flask, request, jsonify, render_template
import json
import ccxt
import config
import pandas as pd
import requests

app = Flask(__name__)

##### Pick One Mode ######################
realMode = True
testMode = False
spotMode = False
##########################################

if realMode == True:
    exchange = ccxt.binance({
    "apiKey": config.apiKey,
    "secret": config.secretKey,
    'options': {'defaultType': 'future'},'enableRateLimit': True})

if testMode == True:
    exchange = ccxt.binance({
    "apiKey": config.testapiKey,
    "secret": config.testsecretKey,
    'options': {'defaultType': 'future'},'enableRateLimit': True})
    exchange.set_sandbox_mode(True)
    
if  spotMode == True:
    exchange = ccxt.binance({
    "apiKey": config.apiKey,
    "secret": config.secretKey})

webhook_url = 'https://discord.com/api/webhooks/984492687380078642/XLMVOkLxgpbjdnFMjDckL1wFFVzTVv1xkM28ApUzMPL_gwyePw9RkOJ8bWRVr5LS4nOS'
EntryAvatar = "https://1.bp.blogspot.com/-QoKsMMCJ8-0/WRaTRHKz2OI/AAAAAAABEPk/RlblEittYVoUvpl_VjBzifrx9yjToucXgCLcB/s400/kenkyu_man_seikou.png"
ExitAvatar = "https://1.bp.blogspot.com/-QoKsMMCJ8-0/WRaTRHKz2OI/AAAAAAABEPk/RlblEittYVoUvpl_VjBzifrx9yjToucXgCLcB/s400/kenkyu_man_seikou.png"
faildAvatar = "https://4.bp.blogspot.com/-pi2OEw0-Eew/XJB5M76Zf9I/AAAAAAABR9I/5FrJ3BqUJtUKKUVvvIJnxQ54v6O97HL0ACLcBGAs/s180-c/science_hakase_shippai.png"

##############################################################################################################################

def ENTRY(symbol,side,qty,cost, free):
    try:
        order = exchange.create_order(symbol=symbol,type="market",side=side,amount=qty)

        side = side.replace("SELL","Short").replace("BUY","Long")
        orderInfo = f" ${round(cost)} ({round(qty)}). You have {round(free - cost)} USDT left."
        main_content = {
        "username":     f"{symbol} ({side})",
        "avatar_url":   EntryAvatar,
        "content":      orderInfo}
        requests.post(webhook_url,main_content)

        print(orderInfo)
        
    except Exception as e:
        reason = "an exception occured at Entry Order- {}".format(e)

        main_content = {"username": symbol,"avatar_url": faildAvatar,"content": reason}
        requests.post(webhook_url,main_content)

        print(reason)
        return False
    return order

def EXIT(symbol,side,qty,Exit_param, cost, free):
    try:
        order=exchange.create_order(symbol=symbol, type="market", side=side, amount=qty*1.1, params=Exit_param)

        side = side.replace("SELL","Short").replace("BUY","Long")
        orderInfo = f" $Position Closed. You have {round(free)} USDT left."

        main_content = {
        "username": f" {symbol} ({side})",
        "avatar_url": ExitAvatar,
        "content": orderInfo}
        requests.post(webhook_url,main_content)

    except Exception as e:
        reason = "an exception occured at Exit Order- {}".format(e)
        main_content = {"username": symbol,"avatar_url": faildAvatar,"content": reason}
        requests.post(webhook_url,main_content)
        print(reason)
        return False
    return order

def PositionExists(symbol,side):
    main_content = {"username": f"{symbol} ({side})","avatar_url": faildAvatar,"content": "Order Refused. Position Alredy Exists."}
    requests.post(webhook_url,main_content)
    return False

##############################################################################################################################

@app.route('/', methods=['POST'])
def webhook():

    balance     = exchange.fetch_balance()

    free        = balance["USDT"]["free"]
    used        = balance["USDT"]["used"]
    total       = balance["USDT"]["total"]
    positions   = balance['info']['positions']
    MarginOk    = free/total > 0.5
    
    data        = json.loads(request.data)
    orderType   = data["type"] #Entry or Exit
    symbol      = data['symbol'].replace('PERP','')
    side        = data['side'] #BUY or SELL
    leverage    = float(data['leverage'])
    bars        = exchange.fetch_ohlcv(symbol, timeframe="1m", since = None, limit = 5)
    df          = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])
    price       = float(df["close"][len(df.index) - 1])
    qty         = (free * leverage) / price
    cost        = qty*price
    Exit_param  = {"reduceOnly":True}

    try:
        if orderType == "Entry" and MarginOk:
            for position in positions:
                if position["symbol"] == symbol:
                    print(float(position['positionAmt']))
                    if float(position['positionAmt']) != 0:
                        print(f"You have a position for {symbol}")
                        False
                    else:
                        if orderType == "Entry" :
                            order_response = ENTRY(symbol, side, qty, cost, free)
        if orderType == "Exit":
            order_response = EXIT(symbol, side, qty, Exit_param, cost, free)

        if order_response:
            print("order success")
            return {"code": "market order success","message": "market order executed"}
        else:
            print("market order failed")
            return {"code": "market order error","message": "market order failed"}

    except:
        PositionExists(symbol, side)
        print("\n\n\n Order Refused. Position Already Exists.\n\n\n")




##############################################################################################################################

@app.route('/home')
def welcome():
    return render_template('index.html')
