import datetime
import random
import string
from typing import Tuple, List
from art import text2art


def create_sample_data(number_of_items: int = 1) -> List[str]:
    ERROR_RATE: float = 0.05
    NEW_USERID_RATE: float = 0.25
    INCOMPLETE_ITEM_RATE: float = 0.02

    def generate_user_id() -> str:
        """
        Helper function for creating fake user id's following a specified pattern.
        """
        return f'KB{str().join(random.choices(string.ascii_uppercase + string.digits, k=4))}'

    def generate_item_id(item: int, padding_length: int) -> str:
        """
        Helper function for creating an item id string following a specified pattern.
        """
        return f'{item:0{padding_length}}--{str().join(random.choices(string.hexdigits.upper(), k=5))}'

    def generate_starting_time() -> datetime.datetime:
        """
        Helper function for calculating starting time at some point in the past.
        """
        days_back = random.randrange(20, 365)
        hours_back: int = random.randrange(0, 24)
        minutes_back: int = random.randrange(0, 60)
        seconds_back: int = random.randrange(0, 60)
        microseconds_back: int = random.randrange(0, 1_000_000)
        return datetime.datetime.now() - datetime.timedelta(
            days=days_back, hours=hours_back, minutes=minutes_back, seconds=seconds_back, microseconds=microseconds_back
        )

    def generate_time_increment() -> datetime.timedelta:
        """
        Helper function for calculating a random time interval between events.
        """
        # random.normalvariate(mu=average, sigma=stdev)

        return datetime.timedelta(
            days=random.randrange(1, 4) if random.random() < 0.25 else 0,
            hours=random.randrange(0, 24) if random.random() < 0.5 else 0,
            minutes=random.randrange(0, 60) if random.random() < 0.25 else 0,
            seconds=random.randrange(0, 60),
            microseconds=random.randrange(0, 1_000_000),
        )

    data_rows: list = []
    primary_key: int = 1
    departments: Tuple[str] = ('Marketing', 'Sales', 'Operations')
    categories: Tuple[str] = ('Hiring_Plan', 'Perf_Review', 'Comp_Review', 'Budget')
    steps: Tuple[str] = ('Received', 'Reviewed', 'Handled', 'Finished')
    steps_branch: Tuple[str] = ('Errors_Found', 'Corrected')
    padding_length: int = len(str(number_of_items))

    for item in range(1, number_of_items + 1):

        department: str = random.choice(departments)
        category: str = random.choice(categories)
        user_id = generate_user_id()

        starting_date_time = generate_starting_time()
        item_id: str = generate_item_id(item, padding_length)
        log_time = starting_date_time

        # Real-world data isn't perfect, so let's introduce some blank rows,
        # and a mainframe style header at the beginning of each section.
        data_rows.append('')
        data_rows.append('')
        data_rows.append('')
        data_rows.extend(''.join(text2art(item_id, font='future_7')).split('\n'))

        for step in steps[:-1]:
            # steps[-1] is used because we reserve the final record entry for something special.
            data_rows.append(f'{primary_key},{item_id},{user_id},{log_time.isoformat()},{department},{category},{step}')
            primary_key += 1
            time_increment = generate_time_increment()
            log_time += time_increment
            if random.random() < ERROR_RATE:
                # Not everyhing is going to be handled correctly,
                # so we'll introducte some noise into our data.
                if random.random() < NEW_USERID_RATE:
                    # Not everything is going to be started and finished by the same person,
                    # so we'll introducte some noise into our data.
                    user_id = generate_user_id()
                for branch_step in steps_branch:
                    data_rows.append(
                        f'{primary_key},{item_id},{user_id},{log_time.isoformat()},{department},{category},{branch_step}'
                    )
                    primary_key += 1
                    time_increment = generate_time_increment()
                    log_time += time_increment
            if random.random() < NEW_USERID_RATE:
                # Not everything is going to be started and finished by the same person,
                # so we'll introducte some noise into our data.
                user_id = generate_user_id()

        if random.random() > INCOMPLETE_ITEM_RATE:
            # Not every item has been completed yet, or maybe the final row of data was lost...
            step = steps[-1]
            data_rows.append(f'{primary_key},{item_id},{user_id},{log_time.isoformat()},{department},{category},{step}')
            primary_key += 1

    return data_rows


def write_data_to_csv(data_rows: list) -> None:
    with open('dirty_data_export.csv', 'w', newline='\n') as writer:
        for row in data_rows:
            writer.write(row)
            writer.write('\n')


if __name__ == '__main__':
    dirty_data_rows = create_sample_data()
    write_data_to_csv(data_rows=dirty_data_rows)
