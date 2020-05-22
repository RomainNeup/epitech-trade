#!/usr/bin/env python3
# -- coding: utf-8 --
import itertools

def actionTrade(action, curOrigin, curDest, quantity):
    action = action + " " + curOrigin + "_" + curDest + " " + str(quantity)
    return action

def getSettings(settings, inputTxt):
    settings[inputTxt[1]] = inputTxt[2]
    return settings

def getUpdate(inputTxt, update):
    value = inputTxt[3].split(";")
    for x in value:
        valuecur = x.split(',')
        if (valuecur[0] not in update):
            update[valuecur[0]] = {}
            update[valuecur[0]]["date"] = []
            update[valuecur[0]]["hight"] = []
            update[valuecur[0]]["low"] = []
            update[valuecur[0]]["open"] = []
            update[valuecur[0]]["close"] = []
            update[valuecur[0]]["volume"] = []
        update[valuecur[0]]["date"].append(float(valuecur[1]))
        update[valuecur[0]]["hight"].append(float(valuecur[2]))
        update[valuecur[0]]["low"].append(float(valuecur[3]))
        update[valuecur[0]]["open"].append(float(valuecur[4]))
        update[valuecur[0]]["close"].append(float(valuecur[5]))
        update[valuecur[0]]["volume"].append(float(valuecur[6]))
    return(update)

def calculateS(lastTemp):
    aver = sum(lastTemp) / len(lastTemp)
    temp = []
    for last in lastTemp:
        temp.append(pow(last - aver, 2))
    return round((pow(sum(temp) / len(temp), 0.5)), 2)

def calculateBol(period):
    down = average(period) - 2 * calculateS(period)
    up = average(period) + 2 * calculateS(period)
    if (period[-1] < down):
        return -1
    elif (period[-1] >= up):
        return 1
    return 0

#return 0 = rien -1 = vendre 1 = acheter
def calculateMACD(inputArray) :
    first_aver = average(inputArray[:12])
    sec_aver  = average(inputArray[-26:])
    macd = first_aver - sec_aver
    if (macd < -0,25):
        return -1
    elif (macd > 0,25):
        return 1
    return 0

def calculateM(inputArray):
    momentum = inputArray[-1] - inputArray[-10]
    last = inputArray[-11]
    lall = []
    for tmp in inputArray[:-10]:
        lall.append(abs(tmp - last))
        last = tmp
    aver = average(lall)
    if (momentum < 0 and abs(momentum) > aver * 1.5):
        return -1
    elif (momentum > 0 and abs(momentum) > aver * 1.5):
        return 1
    return 0

def average(inputArray):
    aver = sum(inputArray) / len(inputArray)
    return aver

def getStocks(txt):
    stocks = {}
    currency = txt.split(',')
    for cur in currency:
        tmp = cur.split(':')
        stocks[tmp[0]] = float(tmp[1])
    return stocks

def betcurr(currpair, update, bank):
    action = ""
    money = 0
    curr = currpair.split('_')
    macd = calculateMACD(update[currpair]['close'])
    bol = calculateBol(update[currpair]['close'][-12:])
    m = calculateM(update[currpair]['close'])
    if (macd == 1 or bol == 1 or m == 1):
        if (macd != bol or bol != m or macd != m):
            money = bank[curr[0]] / 2 / update[currpair]["close"][-1]
        else:
            money = bank[curr[0]] / 4 / update[currpair]["close"][-1]
        if (money <= bank[curr[0]] and round(money,5) > 0):
            action = actionTrade("buy", curr[0], curr[1], money)
    elif (macd == -1 and bol == -1 and m == -1):
        money = bank[curr[1]] / 2
        if (money <= bank[curr[1]] and round(money,5) > 0):
            action = actionTrade("sell", curr[0], curr[1], money)
    return action

def main():
    inputTxt = input().split()
    settings = {}
    update = {}
    bank = {}
    while inputTxt[0]:
        action = []
        if (inputTxt[0] == "settings"):
            settings = getSettings(settings, inputTxt)
        elif (inputTxt[0] == "update"):
            if (inputTxt[2] == "next_candles"):
                update = getUpdate(inputTxt, update)
            elif (inputTxt[2] == "stacks"):
                bank = getStocks(inputTxt[3])
        elif (inputTxt[0] == "action"):
            for key in update:
                act = betcurr(key, update, bank)
                if act != "":
                    action.append(act)
            if (len(action)):
                print(';'.join(action))
            else:
                print("pass")
        inputTxt = input().split()

if __name__ == "__main__":
    main()