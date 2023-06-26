import time
import pyupbit
import datetime

access = ""
secret = ""

ticker = "KRW-ETH"

# 로그인
upbit = pyupbit.Upbit(access, secret)

# 이전 15분봉의 시가, 종가, 저가를 가져오는 함수
def get_previous_candle_data(ticker):
    """이전 15분봉의 시가, 종가, 저가 조회"""
    now = datetime.datetime.now()
    previous_time = now - datetime.timedelta(minutes=15)
    df = pyupbit.get_ohlcv(ticker, interval="minute15", to=previous_time, count=2)
    previous_open = df.iloc[0]['open']
    previous_close = df.iloc[0]['close']
    previous_low = df.iloc[0]['low']
    return previous_open, previous_close, previous_low

def get_pprevious_candle_data(ticker):
    """이전전 15분봉의 시가, 종가, 저가 조회"""
    now = datetime.datetime.now()
    pprevious_time = now - datetime.timedelta(minutes=30)
    df = pyupbit.get_ohlcv(ticker, interval="minute15", to=pprevious_time, count=3)
    pprevious_open = df.iloc[0]['open']
    pprevious_close = df.iloc[0]['close']
    pprevious_low = df.iloc[0]['low']
    return pprevious_open, pprevious_close, pprevious_low

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]



check = 0
print("start")
# target_price =  previous_close + (previous_open- previous_low)*2 #목표가
# stop_loss = previous_low #손절가

# 자동매매
while True:
    try:
        get_previous_candle_data
        get_current_price

        # 특정 암호화폐의 이전 15분봉 시가, 종가, 저가 조회 예시
        previous_open, previous_close, previous_low = get_previous_candle_data(ticker)
        #print(f"이전 15분봉의 시가: {previous_open}")
        #print(f"이전 15분봉의 종가: {previous_close}")
        #print(f"이전 15분봉의 저가: {previous_low}")

        pprevious_open, pprevious_close, pprevious_low = get_pprevious_candle_data(ticker)
        #print(f"이전전 15분봉의 시가: {pprevious_open}")
        #print(f"이전전 15분봉의 종가: {pprevious_close}")
        #print(f"이전전 15분봉의 저가: {pprevious_low}")

        current_price = get_current_price("KRW-ETH")
        #print(f"현재가: {current_price}")
        # print(f"목표가: {target_price}")
        # print(f"손절가: {stop_loss}")
        # print(f"check: {check}")

        #전략1
        #if previous_close - previous_open > 0 and previous_open - previous_low >= previous_close - previous_open and check == 0:
            # 목표가 손절가
            #target_price =  previous_close + (previous_open - previous_low)*2 #목표가
            #stop_loss = previous_low #손절가
            # 매수 주문
            #balance = upbit.get_balance("KRW")
            #if balance is not None and balance > 0:
                #upbit.buy_market_order(ticker, balance*0.9995)
                #check = 1
                #print("oo")

        # 전략 2
        # 이전 캔들 == 양봉 and 이전전 캔들 음봉
        # 이전 캔들 몸통 길이 (이전_종가 - 이전_시작가) > 이전전 캔들 몸통 길이 (이전전_시작가 - 이전전_종가)
        if previous_close - previous_open > 0 and pprevious_open - pprevious_close > 0 and check == 0:
            if previous_close - previous_open > pprevious_open - pprevious_close:
                # 목표가 손절가
                target_price =  previous_close + (previous_close - previous_open)*2 #목표가
                stop_loss = previous_low #손절가
                #print(f"목표가: {target_price}")
                #print(f"손절가: {stop_loss}")
                # 매수 주문
                balance = upbit.get_balance("KRW")
                if balance is not None and balance > 0:
                    upbit.buy_market_order(ticker, balance*0.9995)
                    check = 1
                    #print("oo")
        

        # 매도 주문 목표가
        if check==1:
            if current_price > target_price:
                btc_balance = upbit.get_balance(ticker)
                if btc_balance is not None and btc_balance > 0:
                    upbit.sell_market_order("KRW-ETH", btc_balance*0.9995)
                    check = 2
                    # 반복 주문 막기 위한 코드
                    a = previous_close
                    target_price = 0
                    stop_loss = 0
                    #print("good")

        # 매도 주문 손절가
        if check==1:
            if current_price < stop_loss:
                btc_balance = upbit.get_balance(ticker)
                if btc_balance is not None and btc_balance > 0:
                    upbit.sell_market_order("KRW-ETH", btc_balance*0.9995)
                    check = 2
                    # 반복 주문 막기 위한 코드
                    a = previous_close
                    target_price = 0
                    stop_loss = 0
                    #print("not good")

        # 매도 주문 체결 후 이전 종가가 이전전 종가가 될 때(15분이 지나고 나서), 주문 가능하도록 check를 0으로 바꿈
        if check==2:
            if a==pprevious_close:
                check = 0
                #print(f"check값: {check}")

        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)

