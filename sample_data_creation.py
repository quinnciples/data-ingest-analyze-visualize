import datetime
import random
import string
from typing import Tuple
from art import tprint


def create_sample_data(number_of_items: int = 10) -> None:
    ERROR_RATE: float = 0.05
    NEW_USERID_RATE: float = 0.25
    INCOMPLETE_ITEM_RATE: float = 0.02

    def generate_user_id() -> str:
        return f'KB{"".join(random.choices(string.ascii_uppercase + string.digits, k=4))}'

    def generate_time_increment() -> datetime.timedelta:
        return datetime.timedelta(
            days=random.randrange(1, 4) if random.random() < 0.25 else 0,
            hours=random.randrange(0, 24) if random.random() < 0.5 else 0,
            minutes=random.randrange(0, 60) if random.random() < 0.25 else 0,
            seconds=random.randrange(0, 60),
            microseconds=random.randrange(0, 1_000_000),
        )

    primary_key: int = 1
    departments: Tuple[str] = ('Marketing', 'Sales', 'Operations')
    categories: Tuple[str] = ('Hiring_Plan', 'Perf_Review', 'Comp_Review', 'Budget')
    steps: Tuple[str] = ('Received', 'Reviewed', 'Handled', 'Finished')
    steps_branch: Tuple[str] = ('Errors_Found', 'Corrected')
    padding_length: int = len(str(number_of_items))

    for item in range(1, number_of_items + 1):
        days_back = random.randrange(20, 365)
        hours_back: int = random.randrange(0, 24)
        minutes_back: int = random.randrange(0, 60)
        seconds_back: int = random.randrange(0, 60)
        microseconds_back: int = random.randrange(0, 1_000_000)

        department: str = random.choice(departments)
        category: str = random.choice(categories)
        user_id = generate_user_id()

        starting_date_time = datetime.datetime.now() - datetime.timedelta(
            days=days_back, hours=hours_back, minutes=minutes_back, seconds=seconds_back, microseconds=microseconds_back
        )
        item_id: str = f'{item:0{padding_length}}--{"".join(random.choices(string.hexdigits.upper(), k=5))}'
        log_time = starting_date_time
        print('\n\n\n')
        tprint(item_id, font='future_7')

        for step in steps[:-1]:
            print(f'{primary_key},{item_id},{user_id},{log_time.isoformat()},{department},{category},{step}')
            primary_key += 1
            time_increment = generate_time_increment()
            log_time += time_increment
            if random.random() < ERROR_RATE:
                if random.random() < NEW_USERID_RATE:
                    user_id = generate_user_id()
                for branch_step in steps_branch:
                    print(
                        f'{primary_key},{item_id},{user_id},{log_time.isoformat()},{department},{category},{branch_step}'
                    )
                    primary_key += 1
                    time_increment = generate_time_increment()
                    log_time += time_increment
            if random.random() < NEW_USERID_RATE:
                user_id = generate_user_id()

        if random.random() > INCOMPLETE_ITEM_RATE:
            step = steps[-1]
            print(f'{primary_key},{item_id},{user_id},{log_time.isoformat()},{department},{category},{step}')
            primary_key += 1


if __name__ == '__main__':
    create_sample_data()
