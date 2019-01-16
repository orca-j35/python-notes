import calendar


class MeetupDayException(Exception):
    pass


week = dict(zip((calendar.day_name), range(7)))
cal = calendar.Calendar()


def meetup_day(year, month, day_of_the_week, which):
    days = [
        d for d in cal.itermonthdates(year, month)
        if d.month == month and d.weekday() == week.get(day_of_the_week)
    ]
    if which.lower() == 'teenth':
        return [d for d in days if d.day in range(13, 20)][0]
    elif which.lower() == 'last':
        return days[-1]
    elif int(which[0]) <= len(days):
        return days[int(which[0]) - 1]
    raise MeetupDayException('No such day!')
