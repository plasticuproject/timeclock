#!/usr/bin/env python3
"""Timeclock CLI app.
A CLI app that accepts start and end times from users
for multiple days then calculates and prints the total
time."""
from typing import List, Tuple, Union

BOOLS: List[str] = ["0", "1"]


class FormatError(Exception):
    """Custom error class used when a user inputs an invalid
    time string."""

    # pylint: disable=useless-super-delegation
    # # Actually need this to add custom message.
    def __init__(self, message: str = "Not a vaild time format") -> None:
        # Call the base class constructor with the parameters it needs.
        super(FormatError, self).__init__(message)


class ChoiceError(Exception):
    """Custom error class used when a user inputs an invalid
    AM/PM boolean indicator."""

    # pylint: disable=useless-super-delegation
    # # Actually need this to add custom message.
    def __init__(self, message: str = "Invalid choice") -> None:
        # Call the base class constructor with the parameters it needs.
        super(ChoiceError, self).__init__(message)


def calc_time(time: Tuple[int, int], start_time: str, start_tod: bool,
              end_time: str, end_tod: bool) -> Tuple[int, int]:
    """Calculates times. Takes previous hour and minute totals via time
    argument tuple, as well as arguments for calculating a new hour and
    minute total. It then adds them together and returns the resulting
    hours and minutes as a tuple.

    :param Tuple[int, int] time: Previous hour and minute total integers.
    :param str start_time: Formatted start time string.
    :param bool start_tod: Start time PM boolean identifier.
    :param str end_time: Formatted end time string.
    :param bool end_tod: End time PM boolean identifier.
    :return: Newly updated hour and minute total integers.
    :rtype: Tuple[int, int]

    USAGE:

        >>> add_time = calc_time((2, 17), "1015", False, "0230", True)
        >>> assert add_time == (6, 32)
    """
    hours: int
    minutes: int
    previous_hours: int = time[0]
    previous_minutes: int = time[1]

    if start_time == "1200":  # Deal with new day hour rollover conversion.
        start_time = "0000"
    if end_time == "1200" and end_tod is False:
        end_time = "2400"

    start_hours: int = int(start_time[:2])  # Split up hours and minutes
    start_minutes: int = int(start_time[2:])  # and typecast.
    end_hours: int = int(end_time[:2])
    end_minutes: int = int(end_time[2:])

    if start_tod is True:  # Convert from 12 to 24 hour format.
        start_hours += 12
    if end_tod is True:
        end_hours += 12

    if start_hours > end_hours:  # Adjustment when end time is in a new day.
        hours = (end_hours + 24) - start_hours
        hours += previous_hours
    else:
        hours = end_hours - start_hours  # Calculate hours worked.
        hours += previous_hours

    if start_minutes > end_minutes:  # Adjustment when minutes roll over hour.
        hours -= 1
        minutes = (end_minutes + 60) - start_minutes
        minutes += previous_minutes
    else:
        minutes = end_minutes - start_minutes  # Calculate minutes worked.
        minutes += previous_minutes

    if minutes >= 60:  # Adjustment when minutes roll over hour.
        hours += minutes // 60
        minutes = minutes % 60

    return (hours, minutes)


def format_time(time: str) -> str:
    """Format time string. Performs checks on supplied time string argument
    ensuring it is numerical, then formats string to vaild 12 hour time format
    'hhmm'. Method will return 'TypeError' when supplied argument is
    non-numerical, or 'ValueError' if it cannot be converted to a valid time
    string, otherwise it will return the valid, formatted time string.

    :param str time: Time string.
    :rasies: timeclock.FormatError: Not a valid time format
    :return: Valid, formatted time string.
    :rtype: str

    USAGE:

        >>> assert format_time("3") == "0300"
        >>> assert format_time("11") == "1100"
        >>> assert format_time("106") == "0106"
        >>> assert format_time("0212") == "0212"
        >>>
        >>> format_time("03:12")
        ...
        timeclock.FormatError: Not a valid time format
        >>>
        >>> format_time("3200")
        ...
        timeclock.FormatError: Not a valid time format
        >>>
        >>> format_time("0960")
        ...
        timeclock.FormatError: Not a valid time format
    """
    if not time.isdigit():  # Numerical check.
        raise FormatError

    if len(time) == 1:  # Format time string to 'hhmm'.
        time = "0" + time + "00"
    elif len(time) == 2:
        time = time + "00"
    elif len(time) == 3:
        time = "0" + time
    elif len(time) == 4:
        pass
    else:
        raise FormatError  # If time string is > 4 characters.

    if int(time) > 1200 or int(time[2:]) > 59:
        raise FormatError  # If numbers cannot convert to 12 hour format.

    return time


def get_times() -> Tuple[str, bool, str, bool]:
    """Prompts user for start time, end time, and their time
    of day indicators, catching invalid inputs. Returns formatted
    time strings with time of day indicators.

    :return: Tuple containing time string, start time PM boolean,
              end time string, and end time PM boolean.
    :rtype: Tuple[str, bool, str, bool]

    USAGE:

        >>> times = get_times()
        START TIME: 1
        AM(0) OR PM(1): 0
        END TIME: 2
        AM(0) OR PM(1): 1
        >>> assert times == ("0100", False, "0200", True)
        >>>
        >>> times = get_times()
        START TIME: ff
        ...
        [!]Not a valid time format[!]
        ...
        START TIME: 5
        AM(0) OR PM(1): ff
        ...
        [!]Invalid choice[!]
        ...
        START TIME:
        ...
    """
    while True:  # Loop until all inputs are valid.
        try:
            start_time: str = input("START TIME: ").replace(":", "")
            start_time = format_time(start_time)
            start_tod: str = input("AM(0) OR PM(1): ")
            if start_tod not in BOOLS:
                raise ChoiceError

            end_time: str = input("END TIME: ").replace(":", "")
            end_time = format_time(end_time)
            end_tod: str = input("AM(0) OR PM(1): ")
            if end_tod not in BOOLS:
                raise ChoiceError

            break

        except (FormatError, ChoiceError) as error:
            print(f"\n[!]{error}[!]\n")
            continue

    return (start_time, bool(int(start_tod)), end_time, bool(int(end_tod)))


def main() -> None:
    """Main program loop.
    :return: None
    :rtype: None

    USAGE:

        >>> main()
        ...
        DAY # 1
        START TIME: 1:15
        AM(0) OR PM(1): 0
        END TIME: 6:32
        AM(0) OR PM(1): 0
        ...
        ADD MORE TIMES: NO(0) OR YES(1): 1
        ...
        DAY # 2
        START TIME: 6:00
        AM(0) OR PM(1): 1
        END TIME: 8:12
        AM(0) OR PM(1): 1
        ...
        ADD MORE TIMES: NO(0) OR YES(1): 0
        ...
        TOTAL TIME WORKED:
        HOURS: 7
        MINUTES: 29
    """
    time: Tuple[int, int] = (0, 0)
    add_time: Union[bool, str] = True
    start_time: str
    start_tod: bool
    end_time: str
    end_tod: bool
    day: int = 1

    # Welcome message.
    print("\nA timeclock app.")

    # Loop through functions collecting and calculating times from
    # user. When user indicates they are finished, print combined
    # total of hours and minutes worked.
    while add_time is True:
        print(f"\nDAY # {day}")
        start_time, start_tod, end_time, end_tod = get_times()
        time = calc_time(time, start_time, start_tod, end_time, end_tod)
        while True:
            try:
                add_time = input("\nADD MORE TIMES: NO(0) OR YES(1): ")
                if add_time not in BOOLS:
                    raise ChoiceError
                add_time = bool(int(add_time))
                break
            except ChoiceError as error:
                print(f"\n[!]{error}[!]")
                continue
        day += 1

    print(f"\nTOTAL TIME WORKED:\nHOURS: {time[0]}\nMINUTES: {time[1]}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        quit()
