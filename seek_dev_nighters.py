import requests
from pytz import timezone, utc
from datetime import datetime, time

API_URL = 'https://devman.org/api/challenges/solution_attempts/'


def load_attempts():
    page = 1
    number_of_pages = 1
    while page <= number_of_pages:
        devman_response = requests.get(API_URL, params={'page': page})
        page_info = devman_response.json()
        number_of_pages = int(page_info['number_of_pages'])
        for record in page_info['records']:
            if record['timestamp']:
                yield record
        page += 1


def local_time(time_stamp, zone):
    local_date_time = datetime.fromtimestamp(float(time_stamp), tz=timezone(zone))
    return local_date_time.time()


def get_midnighters():
    set_of_midnighters = set()
    for record in load_attempts():
        user_time = local_time(record['timestamp'], record['timezone'])
        if time(0, 0, 0) < user_time < time(6, 0, 0):
            set_of_midnighters.add(record['username'])
    return sorted(set_of_midnighters)


def print_the_list(list_to_print):
    print('The list of midnighters:')
    for username in list_to_print:
        print(username)


if __name__ == '__main__':
    list_of_midnighters = get_midnighters()
    print_the_list(list_of_midnighters)
