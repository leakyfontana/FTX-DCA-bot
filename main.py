import os

from pyparsing import null_debug_action
from classes.coin import Coin
from ftx import get
import json


def setCoins():

    response = get('/wallet/balances')
    balances = response['result']

    coins = {}
    for coin in balances:

        temp = Coin(coin)
        coins[temp.coin] = temp

    return coins

def getPurchaseDist():
    purchaseValues = os.getenv("PURCHASE").split(' ')

    if purchaseValues.__len__() % 2 != 0:

        raise Exception('Purchase input formatted incorrectly: Value missing')

    order = { }
    totalPercent = 0
    for idx, x in enumerate(purchaseValues):

        if idx % 2 == 0 and x.isdigit():            
            raise Exception(f'Purchase input formatted incorrectly: Index {idx} should be a coin ticker')

        if idx % 2 == 1:

            if x.isdigit():
                percent = int(x)

                totalPercent += percent
                if totalPercent > 100:
                    raise Exception(f'Purchase input formatted incorrectly: Dsitribution is more than 100%')

                order[purchaseValues[idx - 1]] = percent

            else:
                raise Exception(f'Purchase input formatted incorrectly: Index {idx} should be a distribution percentage (1 - 100)')

    return order

def dca():
    coins = setCoins()
    purchaseDist = getPurchaseDist()

    sellTicker = os.getenv("SELL")
    sellAmount = coins[sellTicker].total
    buyAmount = int(os.getenv("AMOUNT"))
    if  sellAmount < buyAmount:
        diff = buyAmount - sellAmount
        raise Exception(f'Insufficient funds: Please deposit {diff} {sellTicker}')
    
    for key in purchaseDist:
        data = {}
        data['market'] = f'{key}/{sellTicker}'
        data['side'] = 'buy'
        data['price'] = None
        data['type'] = 'market'
        

        print(data)

    
if __name__ == "__main__":
    dca()