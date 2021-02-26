# HW2: Linear Interpolation
# Author: Ricky Rodriguez
# Note: More detailed on Jupyter file


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
sns.set()

# Function for linear extrapolation (to get right points)
def getRightPoints(nan_pos, df, column):
    points = []
    slope = 0
    
    for x_coord, value in enumerate(df[column]):
        if pd.isnull(value) == False and len(points) < 2:
            points.append(x_coord)
        
            if len(points) == 2:
                x1 = points[0]
                x2 = points[1]
                y1 = df.loc[x1, column]
                y2 = df.loc[x2, column]
                
                slope = (y2 - y1) / (x2 - x1)
                break
            
    if len(points) != 2:
        raise Exception("No points for prediction!!")
    y3 = y1 + (slope * (nan_pos - x1))
    return y3


# Function of linear extrapolation (to get left points)
def getLeftPoints(nan_pos, df, column):
    points = []
    slope = 0
    
    for x_coord, value in enumerate(df[column].values[::-1]):
        if pd.isnull(value) == False and len(points) < 2:
            reverse_counter = len(df) - 1 - x_coord
            points.append(reverse_counter)
        
            if len(points) == 2:
                x1 = points[0]
                x2 = points[1]
                y1 = df.loc[x1, column]
                y2 = df.loc[x2, column]
                
                slope = (y2 - y1) / (x2 - x1)
                break
            
    if len(points) != 2:
        raise Exception("No points for prediction!!")
    y3 = y1 + (slope * (nan_pos - x1))
    return y3

def interpolate(df, column):
    x1, x2, y1, y2 = np.nan, np.nan, np.nan, np.nan
    left_pos, right_pos = 0, 0
    
    for i, value in enumerate(df[column]):
        if pd.isnull(value):
             # get one left
            left_pos = i - 1
            while left_pos >= 0 and y1 is np.nan:
                y1 = df.loc[left_pos, column]
                if y1 == np.nan:
                    left_pos-=1
            
            #get one right
            right_pos = i + 1
            while right_pos <= len(df) - 1 and y2 is np.nan:
                y2 = df.loc[right_pos, column]
                if y2 == np.nan:
                    right_pos+=1
                    
            # find y3
            if left_pos < 0 or pd.isnull(y1):
                # get both rights
                y3 = getRightPoints(i, df, column)

            elif right_pos >= len(df) or pd.isnull(y2):
                # get both lefts
                y3 = getLeftPoints(i, df, column)
                
            else:
                x1 = left_pos
                x2 = right_pos

                # Calculate slope and apply two point formula
                slope = (y2 - y1) / (x2 - x1)

                y3 = y1 + (slope * (i - x1))
            
            # Input y3 into table
            df.loc[i, column] = y3

if __name__ == "__main__":
    weather_df = pd.read_csv("nyc_weather.csv")

    # Turn DATE column into "datetime" object
    weather_df.DATE = pd.to_datetime(weather_df.DATE)

    # For testing and visualization purposes, I will focus on manipulating the first week of January
    c1 = weather_df.DATE <= datetime(2020, 1, 7)

    # Creating a copy for the original values and predicted values
    original_df = weather_df[c1].copy()
    predicted_df = weather_df[c1].copy()

    # Creating null values for end (extrapolation) and middle (interpolation) values
    predicted_df.loc[3, "TAVG"] = np.nan
    predicted_df.loc[0, "TAVG"] = np.nan
    predicted_df.loc[6, "TAVG"] = np.nan

    # Testing linear interpolation function
    interpolate(predicted_df, "TAVG")

    # Graphing both plots (Works as intended)
    ax = predicted_df.plot(x = "DATE", 
                        y = "TAVG", 
                        label = "Predicted"
                        )
    original_df.plot(x = "DATE", 
                    y = "TAVG", 
                    label = "Original", 
                    xlabel = "Date", 
                    ylabel = "Average Temperature", 
                    title = "Daily Average Temperature in NYC (Week 1 of 2020)", 
                    ax=ax
                    )
    
    plt.show()