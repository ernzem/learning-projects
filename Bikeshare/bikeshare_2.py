import time
import pandas as pd
import numpy as np
from colorama import Fore, Style, Back, init

init(autoreset=True)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Colour settings
label_clr = Back.YELLOW + Fore.BLACK
yellow = Fore.YELLOW
bright_yellow = Fore.YELLOW + Style.BRIGHT
green = Fore.GREEN
red = Fore.RED

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print(label_clr + 'Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city_inpt = input(green + '\nWould you like to see data for Chicago, New York or Washington? To select, type a city name: ')

    while city_inpt.lower() not in CITY_DATA.keys() or city_inpt == "All":
        city_inpt = input(red + 'Unfortunately your city is not in our database. Please city name based on your city choice: ')
        print(Style.RESET_ALL)

    # get user input for month (all, january, february, ... , june)
    month_lst = ['','January', 'February', 'March', 'April', 'May', 'June']
    month_inpt = input(green + '\nChoose month by typing month name: \nOptions: [January, February, March, April, May, June]. To include all months leave input empty: ')

    while month_inpt not in month_lst:
        month_inpt = input(red + "Unfortunately your month doesn't exist or it is mispelled. Please retype: ")
        print(Style.RESET_ALL)

    month_indx = month_lst.index(month_inpt)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days_lst = ['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_inpt = input(green + '\nSelect a day of the week by typing its name: \nOptions: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]. To include all days leave input empty: ')

    while day_inpt not in days_lst:
        day_inpt = input(red + "Unfortunately, this day doesn't exist or it is mispelled. Please retype: ")
        print(Style.RESET_ALL)


    print(bright_yellow + '-'*40)
    return city_inpt, month_inpt, day_inpt, month_indx


def load_data(city, month, month_index, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    csv_file = CITY_DATA[city.lower()]
    df = pd.read_csv(csv_file, sep=',', encoding='utf8')
    month_data = pd.to_datetime(df['Start Time']).dt.month
    weekday_data = pd.to_datetime(df['Start Time']).dt.weekday_name
    if month != '':
        df = df.loc[month_data == month_index]
    if day != '':
        df = df.loc[weekday_data == day]


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print(yellow + '\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_lst = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    com_mnth_nr = pd.to_datetime(df['Start Time']).dt.month.mode()[0]
    com_mnth = month_lst[com_mnth_nr]
    print('The most common month - {}.'.format(com_mnth))

    # display the most common day of week
    com_week = pd.to_datetime(df['Start Time']).dt.weekday_name.mode()[0]
    print('The most common day of the week - {}.'.format(com_week))

    # display the most common start hour
    com_hour = pd.to_datetime(df['Start Time']).dt.hour.mode()[0]
    print('The most common start hour - {}h.'.format(com_hour))

    print(yellow + "\nThis took %s seconds." % round((time.time() - start_time), 4))
    print(bright_yellow + '-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print(yellow + '\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    com_strt = df['Start Station'].mode()[0]
    # display most commonly used end station
    com_end = df['End Station'].mode()[0]
    # display most frequent combination of start station and end station trip
    concat_strt_end = pd.concat([df['Start Station'], df['End Station']])
    com_strt_end = concat_strt_end.mode()[0]

    print('Most commonly used start station - {}.'.format(com_strt))
    print('Most commonly used end station - {}.'.format(com_strt))
    print('Most frequent combination of start station and end station trip - {}.'.format(com_strt))

    print(yellow + "\nThis took %s seconds." % round((time.time() - start_time), 4))
    print(bright_yellow + '-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print(yellow + '\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].count()
    print('Total travel time - {} seconds.'.format(round(travel_time, 0)))

    # display mean travel time
    travel_mean = df['Trip Duration'].mean()
    print('Mean travel time - {} seconds.'.format(int(round(travel_mean, 0))))


    print(yellow + "\nThis took %s seconds." % round((time.time() - start_time), 4))
    print(bright_yellow + '-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print(yellow + '\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Number of user types: {}\n'.format(user_types))

    # Display counts of gender
    try:
        gender_nr = df['Gender'].value_counts()
        print('Number of gender types: {}'.format(gender_nr))
    except KeyError:
        print("Unfortunately, no gender data is provided")

    # Display earliest, most recent, and most common year of birth
    try:
        birth_earlst = df['Birth Year'].min().astype(int)
        birth_recnt = df['Birth Year'].max().astype(int)
        birth_comm = df['Birth Year'].mode()[0].astype(int)
        print('Most earliest year of birth - {}.'.format(birth_earlst,0))
        print('Most recent year of birth - {}.'.format(birth_recnt,0))
        print('Most common year of birth - {}.'.format(birth_comm,0))
    except KeyError:
        print("Unfortunately, no birth data is provided")

    print(yellow + "\nThis took %s seconds." % round((time.time() - start_time), 4))
    print(bright_yellow + '-'*40)

def raw_data(df):
        i = 5
        data_view_inpt = df.head()
        print('\n', data_view_inpt)
        while data_view_inpt is not '':
            data_view_inpt = input(green + '\nPlease enter additional number of lines you want to see of raw data. To see all, type "All". To exit, leave input empty: ')
            print(Style.RESET_ALL)

            if not (data_view_inpt == '' or data_view_inpt == 'All'):
                i += int(data_view_inpt)
                print(df.head(i))

            if data_view_inpt == 'All':
                print(yellow + 'One moment...')
                pd.set_option('display.max_rows', len(df))
                print('\n', df)

def main():
    while True:
        city_inpt, month_inpt, day_inpt, month_indx = get_filters()
        df = load_data(city_inpt, month_inpt, month_indx, day_inpt)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input(green + '\nWould you like to restart? Enter yes or no.\n')
        print(Style.RESET_ALL)
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
