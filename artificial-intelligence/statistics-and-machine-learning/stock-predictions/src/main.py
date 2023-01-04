#!/usr/bin/py
import os
import numpy as np
import math
import pickle


def erasePickles():
    # Create a database of past data points
    historical_prices = {}  # an 2d float array prices of stock prices containing >=k arrays of length >=5
    historical_prices_last_day = {}
    historical_prices_days = {}

    with open('historical_prices.pickle', 'wb') as f:
        pickle.dump(historical_prices, f)
    with open('historical_prices_last_day.pickle', 'wb') as f:
        pickle.dump(historical_prices_last_day, f)
    with open('historical_prices_days.pickle', 'wb') as f:
        pickle.dump(historical_prices_days, f)


def loadPickleIfAny():
    # Create a database of past data points
    historical_prices = {}  # an 2d float array prices of stock prices containing >=k arrays of length >=5
    historical_prices_last_day = {}
    historical_prices_days = {}

    if os.path.isfile('historical_prices.pickle'):
        with open('historical_prices.pickle', 'rb') as f:
            historical_prices = pickle.load(f)
        with open('historical_prices_last_day.pickle', 'rb') as f:
            historical_prices_last_day = pickle.load(f)
        with open('historical_prices_days.pickle', 'rb') as f:
            historical_prices_days = pickle.load(f)
    return historical_prices, historical_prices_last_day, historical_prices_days


def updateHistoricalPrices(stock_name,
                           d,
                           length,
                           five_prices, historical_prices,
                           historical_prices_last_day,
                           historical_prices_days):
    if stock_name not in historical_prices:
        # Take all data points
        # Store the last day of data because we don't want to have duplicates
        historical_prices_last_day[stock_name] = d
        historical_prices_days[stock_name] = [d - i for i in range(length)]
        historical_prices[stock_name] = five_prices
    else:
        # Update existing data points
        last_day = historical_prices_last_day[stock_name]
        diff_days = last_day - d
        if diff_days < length:
            # Take only the new consecutive data points
            historical_prices[stock_name].extend(five_prices[-diff_days:])
            historical_prices_last_day[stock_name] = d
            historical_prices_days[stock_name].extend([d - i for i in range(diff_days)])
        else:
            # Take all the new data points but acknowledge the empty previous data points
            historical_prices[stock_name].extend(five_prices)
            historical_prices_last_day[stock_name] = d
            historical_prices_days[stock_name] = [d - i for i in range(length)]

    print("historical_prices", historical_prices)
    print("historical_prices_last_day", historical_prices_last_day)
    print("historical_prices_days", historical_prices_days)
    return historical_prices, historical_prices_last_day, historical_prices_days


def savePickles(historical_prices, historical_prices_last_day, historical_prices_days):
    with open('historical_prices.pickle', 'wb') as f:
        pickle.dump(historical_prices, f)
    with open('historical_prices_last_day.pickle', 'wb') as f:
        pickle.dump(historical_prices_last_day, f)
    with open('historical_prices_days.pickle', 'wb') as f:
        pickle.dump(historical_prices_days, f)

    ###### BASICS


def predictNextPrice(x, y, option):
    """
    :param x: x-axis array of integers
    :param y: y-axis of values to predict, corresponds to price
    :param option: can be 'average' or 'poly1d'
    """

    prediction = -1

    if option == 'average':
        # Please note this is EXACTLY the same result as poly1d of degree 0
        prediction = np.mean(y)

    elif option == 'poly1d':
        # Fit a basic polynomial regression model
        model = np.poly1d(np.polyfit(x, y, deg=2))  # deg 2 gives best performances
        prediction = model([6])

    return prediction


def computeTransactions(m, k, d, name, owned, prices, option, historical_prices):
    """
    In this basic strategy, independent decisions are made daily based only on the information of the current day: i.e. purely on the last 5-day price.
    Each day:
    * A new set of k stocks is given.
    * We predict the price of the next day for each stock
    * We compute the slopes from the 5 prices which are stored and sorted in ascending order (from most negative to most positive slope).

    Note: d is not used.
    :param option: can be 'average', 'poly1d'
    :return: the transactions to make
    :rtype: dictionnary with key a string corresponding to a stock name
    and as item an integer. If positive, it is a 'BUY', if negative it is a 'SELL'. Don't report if nothing
    """

    transactions = {}  # List of effective transactions
    current_money = m
    slopes = []  # List of slopes for each of the k stocks

    # For each stock of that day, compute the slopes
    for i in range(k):
        x = range(5)
        # Extract passed 5-day prices
        y = prices[i]

        prediction = predictNextPrice(x, y, option)

        slope = prediction - y[-1]
        slopes.append(slope)

    sorted_slopes = sorted(slopes, key=abs,
                           reverse=True)  # We should focus on the biggest slopes first = descending order of absolute slopes

    # Iterate on sorted_slopes from the biggest absolute value to the smallest one (reverse order)
    for i in range(k):

        # i-th biggest slope in absolute value: determine the associate stock index
        stock_index = slopes.index(sorted_slopes[i])  # stock index of current considered slope

        # Starting with SELL WON'T give you more budget, so no update of remaining money
        # SELL if:
        # * the predicted price for tomorrow is above the price of today (positive slope)
        # * I own some stocks (sell totatily of the stocks)
        if sorted_slopes[i] >= 0 and owned[stock_index] > 0:
            transactions[name[stock_index]] = - owned[stock_index]

            # BUY if:
        # * the predicted price for tomorrow is below the price of today (negative slope)
        # * I have enough money for at least 1 unit of stock (last price)
        current_stock_price = prices[stock_index][-1]
        if sorted_slopes[i] < 0 and current_money >= current_stock_price:
            num_stock = math.floor(current_money / current_stock_price)
            current_money = current_money - current_stock_price * num_stock
            transactions[name[stock_index]] = int(num_stock)

    return transactions


def printTransactions(m, k, d, name, owned, prices, option, historical_prices):
    """
    Print transactions.

    :param float m: the amount of money you could spend that day
    :param int k  : the number of different stocks available for buying or selling: 1 <= k <= 10, it gives the number of rows in the input file
    :param int d  : the number of remaining days for trading stocks
    :param name   : a string array of stock names
    :param owned  : an integer array of stocks owned
    :param prices : an 2d float array of stock prices containing k arrays of length 5

    For index i, the name of the stock is name[i], the number of shares of it you hold is owned[i] and the data about it is prices[i].
    """
    #
    transactions = computeTransactions(m, k, d, name, owned, prices, option, historical_prices)

    if transactions:
        # Print the number of transactions
        num_trans = len(transactions.keys())
        print(num_trans)

        # Print the actual transactions
        for trans in transactions.items():
            to_print = trans[0]
            amount = int(trans[1])
            if amount > 0:
                to_print += " BUY " + str(amount)
            else:
                to_print += " SELL " + str(-1 * amount)
            print(to_print)
    else:
        print("0")


if __name__ == '__main__':

    # erasePickles()
    # exit()

    historical_prices, historical_prices_last_day, historical_prices_days = loadPickleIfAny()  # For advanced version using more than 5 past points

    option = 'average'  # 'poly1d'

    # Start by reading the input
    # In Python 3, input() takes the user input and put it in string format.
    first_row = input().split()
    m, k, d = float(first_row[0]), int(first_row[1]), int(first_row[2])

    # Initialization of required arrays
    name = []  # a string array of stock names
    owned = []  # an integer array of stocks owned
    prices = []  # an 2d float array prices of stock prices containing k arrays of length 5
    length = 5

    # Read the k rows
    for _ in range(k):
        row = input().split()
        stock_name = row[0]
        name.append(stock_name)
        owned.append(int(row[1]))
        five_prices = [float(row[i + 2]) for i in range(length)]
        prices.append(five_prices)

        historical_prices, \
        historical_prices_last_day, \
        historical_prices_days = updateHistoricalPrices(stock_name, d, length, five_prices, historical_prices,
                                                        historical_prices_last_day,
                                                        historical_prices_days)

    printTransactions(m, k, d, name, owned, prices, option, historical_prices)

    savePickles(historical_prices, historical_prices_last_day, historical_prices_days)