import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "0" to apply no month filter
        (str) day - name of the day of week to filter by, or "0" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    global city, month, day
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    answers = ["chicago", "new york city", "washington"]
    city = None
    while city not in answers:
        city = input(
            "Would you like to see data for Chicago, New York City, or Washington? Please make sure your input is "
            "correct.\n").lower()

    # get user input for month (all, january, february, ... , june) or for day of week (all, monday, tuesday,
    # ... sunday)
    time_filter = input(
        "\nWould you like to filter the data by month or day of week? Enter words other than 'month' and 'day' for no "
        "filter:\n")
    if time_filter == "month":
        answers = ["january", "february", "march", "april", "may", "june"]
        month = None
        while month not in answers:
            month = input(
                "\nWhich month, January, February, March, April, May, or June? Please make sure your input is "
                "correct.\n").lower()

        print("\nDisplaying data for {}, restart program if there was a mistake.".format(month.title()))
        day = "all"
    elif time_filter == "day":
        answers = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        day = None
        while day not in answers:
            day = input(
                "\nWhich day, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Please make sure "
                "your input is correct.\n").lower()

        print("\nDisplaying data for {}, restart program if there was a mistake.".format(day.title()))
        month = "all"
    else:
        month = "all"
        day = "all"
        print("\nDisplaying data without filter, restart program if there was a mistake.")

    print('-' * 40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('Calculating The Most Frequent Times of Travel...\n(City: {}, Month: {}, Day of Week: {})\n'.format(
        city.title(), month.title(), day.title()))
    start_time = time.time()

    # display the most common month, skip when using month filter as only one month is being considered
    if month == "all":
        df['month'] = df['Start Time'].dt.month_name()
        common_month = df['month'].mode()[0]
        print('Most Common Month:', common_month)

    # display the most common day of week, skip when using day filter as only one day is being considered
    if day == "all":
        df['day_of_week'] = df['Start Time'].dt.day_name()
        common_dow = df['day_of_week'].mode()[0]
        print('Most Common Day of Week:', common_dow)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trip...\n(City: {}, Month: {}, Day of Week: {})\n'.format(
        city.title(), month.title(), day.title()))
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("Most commonly used start station:", common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("Most commonly used end station:", common_end)

    # display most frequent combination of start station and end station trip
    common_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("Most frequent combination of start station and end station trip:", common_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('Calculating Trip Duration...\n(City: {}, Month: {}, Day of Week: {})\n'.format(city.title(), month.title(),
                                                                                          day.title()))
    start_time = time.time()

    # display total travel time
    total_travel = df["Trip Duration"].sum()
    print("Total travel time:", total_travel, "seconds")

    # display mean travel time
    mean_travel = df["Trip Duration"].mean()
    print("Mean travel time:", mean_travel, "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('Calculating User Stats...\n(City: {}, Month: {}, Day of Week: {})\n'.format(city.title(), month.title(),
                                                                                       day.title()))
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print("User types:\n", user_types)

    # display counts of gender
    gender_counts = df['Gender'].value_counts().to_string()
    print("\nGender counts:\n", gender_counts)

    # display earliest, most recent, and most common year of birth
    min_by = int(df['Birth Year'].min())
    max_by = int(df['Birth Year'].max())
    common_by = int(df['Birth Year'].mode()[0])
    print("\nEarliest user birth year:", min_by)
    print("Most recent user birth year:", max_by)
    print("Most common user birth year:", common_by)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """Displays some raw data on bikeshare users based on user response."""
    # track the amount of times the user asked for more data
    x = 0
    # enable pandas to display all the columns in the dataframe when printing
    pd.set_option('display.max_columns', 200)
    while True:
        ask_user = input(
            "Enter Y to access some raw data on bikeshare users, enter any other key to skip.\n".format(city.title()))
        if ask_user.lower() == 'y':
            x += 1
            print("\nHere is the data:\n", df.iloc[(x - 1) * 5:x * 5], "\n")
        else:
            print("No data will be displayed.")
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city == "chicago" or city == "new york city":
            user_stats(df)
        else:
            print("Note: User data not available for Washington.")
        raw_data(df)

        restart = input('\nEnd of Program. Enter Y to restart, enter any other key to quit.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
