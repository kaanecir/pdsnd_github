import time
import pandas as pd
import numpy as np
import datetime as dt

# CITY_DATA dictionary is defined to get data file name by city name within the code.
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# MONTH_DATA dictionary is defined to get month number by month name within the code.
MONTH_DATA = {  'all': 'all',
                'january': 1,
                'february': 2,
                'march': 3,
                'april': 4,
                'may': 5,
                'june': 6,
                'july': 7,
                'august': 8,
                'september': 9,
                'october': 10,
                'november': 11,
                'december': 12 }

# DAY_OF_WEEK_DATA dictionary is defined to get weekday number by weekday name within the code.
DAY_OF_WEEK_DATA = { 'all': 'all',
                'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6 }

# MONTH_NAMES dictionary is defined by using values as keys and keys as values of MONTH_DATA dictionary, to get month name by its number.
MONTH_NAMES = dict()
for (k, v) in MONTH_DATA.items():
    MONTH_NAMES[v] = k.capitalize()

# DAY_OF_WEEK_NAMES dictionary is defined by using values as keys and keys as values of DAY_OF_WEEK_DATA dictionary, to get weekday name by its number.
DAY_OF_WEEK_NAMES = dict()
for (k, v) in DAY_OF_WEEK_DATA.items():
    DAY_OF_WEEK_NAMES[v] = k.capitalize()

# ROW_DISPLAY_LIMIT is the number of rows when displaying the preview of raw data.
ROW_DISPLAY_LIMIT = 5

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
    while True:
        city = input('\nWhich city do you want to analyze? Please enter the name of the one of those cities you want: Chicago, New York City, Washington.\n')
        if CITY_DATA.get(city.lower()) is None:
            unidentified_input(city)
        else:
            print("\nThanks!\n")
            break
    
    filter_method = ""
    while filter_method.lower() not in ['month', 'day', 'none']:
        filter_method = input('\nWould you like to filter the data by month, day, or not at all? Type "none" for no filters.\n')
        if filter_method.lower() == 'month':
            day = 'all'
            # get user input for month (all, january, february, ... , june)
            while True:
                month = input('\nWhich month do you want to analyze? (all, january, february, ... , december)\n')
                if MONTH_DATA.get(month.lower()) is None:
                    unidentified_input(month)
                else:
                    print("\nThanks!\n")
                    break
        elif filter_method.lower() == 'day':
            month = 'all'
            # get user input for day of week (all, monday, tuesday, ... sunday)
            while True:
                day = input('\nWhich day do you want to analyze? (all, monday, tuesday, ... sunday)\n')
                if DAY_OF_WEEK_DATA.get(day.lower()) is None:
                    unidentified_input(day)
                else:
                    print("\nThanks!\n")
                    break
        elif filter_method.lower() == 'none':
            day = 'all'
            month = 'all'
            break
        else:
            unidentified_input(filter_method)


    

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city.lower()])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day Of Week'] = df['Start Time'].dt.dayofweek
    df['Hour'] = df['Start Time'].dt.hour

    if MONTH_DATA[month.lower()] != 'all':
        print('Filtering data by month: {}'.format(month))
        df = df[df['Month'] == MONTH_DATA[month.lower()]]
    
    if DAY_OF_WEEK_DATA[day.lower()] != 'all':
        print('Filtering data by day of week: {}'.format(day))
        df = df[df['Day Of Week'] == DAY_OF_WEEK_DATA[day.lower()]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    freq_month_name = df['Start Time'].dt.month_name().mode()[0]
    print('The most common month is {}.'.format(freq_month_name))
    
    # display the most common day of week
    freq_day_of_week_number = df['Day Of Week'].mode()[0]
    freq_day_of_week_name = DAY_OF_WEEK_NAMES[freq_day_of_week_number]
    print('The most common day of week is {}.'.format(freq_day_of_week_name))

    # display the most common start hour
    freq_start_hour = df['Hour'].mode()[0]
    print('The most common start hour is {} o\'clock.'.format(freq_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station is {}'.format(most_popular_start_station))
    start_station_counts = df.groupby('Start Station')[['Start Station']].count().rename(columns = {'Start Station': 'Count'}).sort_values('Count', ascending=False).head(3)
    print(start_station_counts)
    print()


    # display most commonly used end station
    most_popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station is {}'.format(most_popular_end_station))
    end_station_counts = df.groupby('End Station')[['End Station']].count().rename(columns = {'End Station': 'Count'}).sort_values('Count', ascending=False).head(3)
    print(end_station_counts)
    print()

    # display most frequent combination of start station and end station trip
    most_popular_trip = ('Start: ' + df['Start Station'] + ', End: ' + df['End Station']).mode()[0]
    print('The most frequently used trip: {}'.format(most_popular_trip))
    trip_counts = df.groupby(['Start Station', 'End Station'])[['Start Station']].count().rename(columns = {'Start Station': 'Number of trips'}).sort_values('Number of trips', ascending=False).reset_index().head(3)
    print(trip_counts)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # Trip duration values are seconds.
    total_travel_seconds = int(df['Trip Duration'].sum())
    total_travel_time = dt.timedelta(seconds = total_travel_seconds)
    print('Total travel duration is {}.'.format(total_travel_time))

    # display mean travel time
    mean_travel_seconds = float(df['Trip Duration'].mean())
    mean_travel_time = dt.timedelta(seconds = mean_travel_seconds)
    print('Mean travel duration is {}.'.format(mean_travel_time))
    total_trip_count = df['Trip Duration'].count()
    print('Total number of trips is {}.'.format(total_trip_count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_stats_series = df['User Type'].value_counts()
    user_type_stats_dataframe = pd.DataFrame(user_type_stats_series)
    user_type_stats_dataframe.rename(columns = {'User Type': 'Number of records'}, inplace = True)
    print('Here are number of records for each user type:')
    print(user_type_stats_dataframe)
    print()


    # Display counts of gender
    if 'Gender' in df.columns:
        gender_stats_series = df['Gender'].value_counts()
        gender_stats_dataframe = pd.DataFrame(gender_stats_series)
        gender_stats_dataframe.rename(columns = {'Gender': 'Number of records'}, inplace = True)
        print('Here are number of records for each gender:')
        print(gender_stats_dataframe)
        print()


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("The oldest user's birth year is {}.".format(int(df['Birth Year'].min())))
        print("The youngest user's birth year is {}.".format(int(df['Birth Year'].max())))
        print("The most common birth year of the users is {}.".format(int(df['Birth Year'].mode())))
        birth_year_stats = pd.DataFrame(df['Birth Year'].dropna().astype(int).value_counts()).sort_values('Birth Year', ascending = False).head(5)
        birth_year_stats.index.rename('Birth Years', inplace=True)
        birth_year_stats.rename(columns = {'Birth Year': 'Number of records'}, inplace = True)
        print('Here are number of records for each top 5 birth year:')
        print(birth_year_stats)
        print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data."""

    see_raw_data = input('\nWould you like to see a preview of raw data? Enter yes or no\n')
    if see_raw_data.lower() == 'yes':
        row_index = 0
        print('\nDisplaying raw data preview...\n')
        while row_index <= df.last_valid_index():
            print(df.iloc[row_index : row_index + ROW_DISPLAY_LIMIT])
            continue_raw_data = input('\nPress Enter to continue, or enter \'no\' to stop displaying...\n')
            if continue_raw_data.lower() == 'no':
                print()
                break
            else:
                row_index += ROW_DISPLAY_LIMIT

def unidentified_input(input_str):
    """Displays a generic unidentified input dialog."""
    input('\nSorry!... "{}" could not be identified as a choice. Please press Enter to continue and retry...'.format(input_str))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

    print('\nBye :-)\n')
if __name__ == "__main__":
	main()
