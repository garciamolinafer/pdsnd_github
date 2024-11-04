import time
import pandas as pd
import numpy as np
from tkinter import Tk, filedialog

Tk().withdraw()

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_list=['all', 'january','february','march','april','may','june','july','august','september','october','november','december']
day_list=['all', 'monday', 'tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = list(CITY_DATA.keys())
    while True:
        try:
            city=int(input("Please insert the city: 1-Chicago / 2-New York / 3 -Washington:"))
            if city>3 or city<1:
                print("Wrong input. Try again \n")
            else:
                break
        except ValueError:
            print("Wrong input. Try again")
    city=city_list[city-1]

    # get user input for month (all, january, february, ... , june)
    
    month_df=pd.DataFrame({'Month':month_list})
    while True:
        try:
            print('\n Now select the month number \n',month_df)
            month_sel=int((input('Choose your month number (0-12):')))
            if month_sel>12 or month_sel<0:
                print("Wrong input. Try again \n")
            else:
                break
        except ValueError:
            print("Wrong input. Try again")
    month=month_list[month_sel]


    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    day_df=pd.DataFrame({'Week Day':day_list})
    while True:
        try:
            print('\n Now select the week day number \n',day_df)
            day_sel=int((input('Choose your day number (0-7):')))
            if day_sel>7 or day_sel<0:
                print("Wrong input. Try again \n")
            else:
                break
        except ValueError:
            print("Wrong input. Try again")
    day=day_list[day_sel]
    print('-'*40)
    day_sel=day_sel-1 #we want to start from 0 for Monday
    print(f'\nYour selection is {city.title()}, {month.title()}, {day.title()}\n')
    return city, month_sel, day_sel


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    path=CITY_DATA[city]
    bucle=True
    while bucle:
        try:
            df = pd.read_csv(path)
            bucle=False
        except FileNotFoundError:
            print(f"Error: File for {city} not found on the project's folder. Please select a valid path")
            path = filedialog.askopenfilename(title="Select the CSV file", filetypes=[("CSV files", "*.csv")])



    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['Month']=df['Start Time'].dt.month
    df['Day']=df['Start Time'].dt.day_of_week
    df['Hour']=df['Start Time'].dt.hour

    if month!=0:
        df=df[df['Month']==month]
    if day!=-1:
        df=df[df['Day']==day]
    
    
    print('Total number of data:', df['Start Time'].count())
    #print(df.head(20))

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month=df['Month'].mode()[0]
    number_months=df['Month'].value_counts()[common_month]
    
    print(f"\nThe most frequent month is {month_list[common_month].title()}, with {number_months} cases out of a total of {df['Month'].count()} fields")


    # display the most common day of week
    common_day=df['Day'].mode()[0]
    number_days=df['Day'].value_counts()[common_day]
    
    print(f"\nThe most frequent weekday is {day_list[common_day+1].title()}, with {number_days} cases out of a total of {df['Day'].count()} fields")

    # display the most common start hour
    common_hour=df['Hour'].mode()[0]
    number_hours=df['Hour'].value_counts()[common_hour]
    
    print(f"\nThe most frequent start hour is {common_hour}h, with {number_hours} cases out of a total of {df['Hour'].count()} fields")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    if 'Start Station' not in df.columns or 'End Station' not in df.columns:
        print ('\nIt seems that the selected file does not contain information about the stations, sorry')
        return
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start=df['Start Station'].mode()[0]
    number_start=df['Start Station'].value_counts()[common_start]
    
    print(f'\nThe most frequent start station is {common_start.upper()}, with {number_start} cases out of a total of {df['Hour'].count()} fields')

    # display most commonly used end station
    common_end=df['End Station'].mode()[0]
    number_end=df['End Station'].value_counts()[common_end]
    
    print(f"\nThe most frequent end station is {common_end.upper()}, with {number_end} cases out of a total of {df['Hour'].count()} fields")

    # display most frequent combination of start station and end station trip
    df['Start End']=df['Start Station'] + " TO " + df['End Station']
    common_se=df['Start End'].mode()[0]
    number_se=df['Start End'].value_counts()[common_se]
    
    print(f"\nThe most frequent start and end station combo is {common_se.upper()}, with {number_se} cases out of a total of {df['Hour'].count()} fields")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    if 'Trip Duration' not in df.columns:
        print ('\nIt seems that the selected file does not contain information about the trip duration, sorry')
        return
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel=df['Trip Duration'].sum()
    print(f'\nThe total travel time of the selection was {total_travel} minutes ')

    # display mean travel time
    mean_travel=df['Trip Duration'].mean()
    print(f'\nThe mean travel time per trip of the selection was {mean_travel} minutes ')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' not in df.columns:
        print ('\nIt seems that the selected file does not contain information about the user types, sorry')
    else:
        print('\nCounts per user type:\n', df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' not in df.columns:
        print ('\nIt seems that the selected file does not contain information about the gender, sorry')
    else:
        print('\nCounts per gender:\n', df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print ('\nIt seems that the selected file does not contain information about the year of birth of the users, sorry')
    else:
        older=int(df['Birth Year'].min())
        younger=int(df['Birth Year'].max())
        common_year=int(df['Birth Year'].mode()[0])
        print(f"\nOlder users were born in {older}")
        print(f"\nYounger users were born in {younger}")
        print(f"\nMost common users' birth year is {common_year}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
