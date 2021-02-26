# HW1: Linear Interpolation
# Author: Ricky Rodriguez
# Note: More detailed on Jupyter file

import matplotlib.pyplot as plt

# Linear Interpolation function
def getEstimation(value, x_list, y_list):
    
    # Data has to be within range
    if value > x_list[-1] or value < x_list[0]:
         raise Exception("Value is not within data range")
    
    # Find which slope to use
    diff = -1
    count = 1
    x1, x2, y1, y2 = 0, 0, 0, 0
    
    while(diff < 0 and count <= len(x_list)):
        diff = x_list[count] - value
        if diff >= 0:
            x1 = x_list[count - 1]
            y1 = y_list[count - 1]
            x2 = x_list[count]
            y2 = y_list[count]
        count += 1
    
    # Calculate slope and apply two point formula
    slope = (y2 - y1) / (x2 - x1)
    
    return y1 + (slope * (value - x1))


if __name__ == "__main__":
    # NYC Census Data for Hunts Point, Bronx
    # Link: https://data.cityofnewyork.us/City-Government/New-York-City-Population-By-Community-Districts/xi7c-iiu2
    years = [1970, 1980, 1990, 2000, 2010]
    pop = [99493, 34399, 39443, 46824, 52246]

    # Create graph
    plt.scatter(years, pop)

    # Create point for missing years using linear interpolation
    for x3 in range(1971, 2010):
        if x3 in years:
            continue
        y3 = getEstimation(x3, years, pop)
        plt.plot(x3, y3, "ro")

    plt.title("Population in Hunts Point from 1970 to 2010")
    plt.xlabel("Population Size")
    plt.ylabel("Year")
    plt.show()