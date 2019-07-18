# calendar  General calendar-related functions
> GitHub@[orcaj35](https://github.com/orcaj35)，所有笔记均托管于 [python_notes](https://github.com/orcaj35/python_notes) 仓库
>
> 参考: [`calendar`](https://docs.python.org/3/library/calendar.html#modulecalendar) — General calendarrelated functions

## class Calendar

🔨 *class* calendar.Calendar(*firstweekday=0*)

Creates a [`Calendar`](https://docs.python.org/3/library/calendar.html#calendar.Calendar) object. *firstweekday* is an integer specifying the first day of the week. `0` is Monday (the default), `6` is Sunday.

A [`Calendar`](https://docs.python.org/3/library/calendar.html#calendar.Calendar) object provides several methods that can be used for preparing the calendar data for formatting. This class doesn’t do any formatting itself. This is the job of subclasses.

[`Calendar`](https://docs.python.org/3/library/calendar.html#calendar.Calendar) instances have the following methods:

### iterweekdays

🔨 iterweekdays()

Return an iterator for the week day numbers that will be used for one week. The first value from the iterator will be the same as the value of the [`firstweekday`](https://docs.python.org/3/library/calendar.html#calendar.firstweekday) property.

```python
import calendar
c=calendar.Calendar()
list(c.iterweekdays())
#> [0, 1, 2, 3, 4, 5, 6]
```

### itermonthdates

🔨 itermonthdates(*year*, *month*)

Return an iterator for the month *month* (1–12) in the year *year*. This iterator will return all days (as [`datetime.date`](https://docs.python.org/3/library/datetime.html#datetime.date) objects) for the month and all days before the start of the month or after the end of the month that are required to get a complete week.

```python
import calendar
c=calendar.Calendar()
list(c.itermonthdates(2013,2))
'''Out:
[datetime.date(2013, 1, 28),
 datetime.date(2013, 1, 29),
 datetime.date(2013, 1, 30),
 datetime.date(2013, 1, 31),
 datetime.date(2013, 2, 1),
 datetime.date(2013, 2, 2),
 datetime.date(2013, 2, 3),
 --snip--
 datetime.date(2013, 2, 26),
 datetime.date(2013, 2, 27),
 datetime.date(2013, 2, 28),
 datetime.date(2013, 3, 1),
 datetime.date(2013, 3, 2),
 datetime.date(2013, 3, 3)]
'''
```

### itermonthdays

🔨 itermonthdays(*year*, *month*)

Return an iterator for the month *month* in the year *year* similar to [`itermonthdates()`](https://docs.python.org/3/library/calendar.html#calendar.Calendar.itermonthdates), but not restricted by the [`datetime.date`](https://docs.python.org/3/library/datetime.html#datetime.date) range. Days returned will simply be day of the month numbers. For the days outside of the specified month, the day number is `0`.

```python
import calendar
c=calendar.Calendar()
list(c.itermonthdays(2013,2))
#> [0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,25, 26, 27, 28, 0, 0, 0]
```

### itermonthdays2

🔨 itermonthdays2(*year*, *month*)

Return an iterator for the month *month* in the year *year* similar to [`itermonthdates()`](https://docs.python.org/3/library/calendar.html#calendar.Calendar.itermonthdates), but not restricted by the [`datetime.date`](https://docs.python.org/3/library/datetime.html#datetime.date) range. Days returned will be tuples consisting of a day of the month number and a week day number.

```python
import calendar
c=calendar.Calendar()
list(c.itermonthdays2(2013,2))
#> [(0, 0), (0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 6), (4, 0), (5, 1), (6, 2), (7, 3), (8, 4), (9, 5), (10, 6), (11, 0), (12, 1), (13, 2), (14, 3), (15, 4), (16, 5), (17, 6), (18, 0), (19, 1), (20,2), (21, 3), (22, 4), (23, 5), (24, 6), (25, 0), (26, 1), (27, 2), (28, 3), (0, 4), (0, 5), (0, 6)]
```

### itermonthdays3

🔨 itermonthdays3(*year*, *month*)

Return an iterator for the month *month* in the year *year* similar to [`itermonthdates()`](https://docs.python.org/3/library/calendar.html#calendar.Calendar.itermonthdates), but not restricted by the [`datetime.date`](https://docs.python.org/3/library/datetime.html#datetime.date) range. Days returned will be tuples consisting of a year, a month and a day of the month numbers.

*New in version 3.7.*

```python
import calendar
c=calendar.Calendar()
list(c.itermonthdays3(2013,2))
#> [(2013, 1, 28), (2013, 1, 29), (2013, 1, 30), (2013, 1, 31), (2013, 2, 1), (2013, 2, 2), (2013, 2, 3), (2013, 2, 4), (2013, 2, 5), (2013, 2, 6), (2013, 2, 7), (2013, 2, 8), (2013, 2, 9), (2013, 2, 10), (2013, 2, 11), (2013, 2, 12), (2013, 2, 13), (2013, 2, 14), (2013, 2, 15), (2013, 2, 16), (2013, 2, 17), (2013, 2, 18), (2013, 2, 19), (2013, 2, 20), (2013, 2, 21), (2013, 2, 22), (2013, 2, 23), (2013, 2, 24), (2013, 2, 25), (2013, 2, 26), (2013, 2, 27), (2013, 2, 28), (2013, 3, 1), (2013, 3, 2),
(2013, 3, 3)]
```

### itermonthdays4

🔨 itermonthdays4(*year*, *month*)

Return an iterator for the month *month* in the year *year* similar to [`itermonthdates()`](https://docs.python.org/3/library/calendar.html#calendar.Calendar.itermonthdates), but not restricted by the [`datetime.date`](https://docs.python.org/3/library/datetime.html#datetime.date) range. Days returned will be tuples consisting of a year, a month, a day of the month, and a day of the week numbers.

*New in version 3.7.*

```python
import calendar
c=calendar.Calendar()
list(c.itermonthdays4(2013,2))
'''Out:
[(2013, 1, 28, 0), (2013, 1, 29, 1), (2013, 1, 30, 2), (2013, 1, 31, 3), (2013, 2, 1, 4), (2013, 2, 2, 5), (2013, 2, 3, 6), (2013, 2, 4, 0), (2013, 2, 5, 1), (2013, 2, 6, 2), (2013, 2, 7, 3), (2013, 2, 8, 4), (2013, 2, 9, 5), (2013, 2, 10, 6), (2013, 2, 11, 0), (2013, 2, 12, 1), (2013, 2, 13, 2), (2013, 2, 14, 3), (2013, 2, 15, 4), (2013, 2, 16, 5), (2013, 2, 17, 6), (2013, 2, 18, 0), (2013, 2, 19, 1), (2013, 2, 20, 2), (2013, 2, 21, 3), (2013, 2, 22, 4), (2013, 2, 23, 5), (2013, 2, 24, 6), (2013, 2, 25, 0), (2013, 2, 26, 1), (2013, 2, 27, 2), (2013, 2, 28, 3), (2013, 3, 1, 4), (2013, 3, 2, 5), (2013, 3, 3, 6)]
'''
```

### monthdatescalendar

🔨monthdatescalendar(*year*, *month*)

Return a list of the weeks in the month *month* of the *year* as full weeks. Weeks are lists of seven [`datetime.date`](https://docs.python.org/3/library/datetime.html#datetime.date) objects.

```python
import calendar
c=calendar.Calendar()
c.monthdatescalendar(2013,2)
'''Out:
[[datetime.date(2013, 1, 28),
  datetime.date(2013, 1, 29),
  datetime.date(2013, 1, 30),
  datetime.date(2013, 1, 31),
  datetime.date(2013, 2, 1),
  datetime.date(2013, 2, 2),
  datetime.date(2013, 2, 3)],
 [datetime.date(2013, 2, 4),
  datetime.date(2013, 2, 5),
  datetime.date(2013, 2, 6),
  datetime.date(2013, 2, 7),
  datetime.date(2013, 2, 8),
  datetime.date(2013, 2, 9),
  datetime.date(2013, 2, 10)],
 [datetime.date(2013, 2, 11),
  datetime.date(2013, 2, 12),
  datetime.date(2013, 2, 13),
  datetime.date(2013, 2, 14),
  datetime.date(2013, 2, 15),
  datetime.date(2013, 2, 16),
  datetime.date(2013, 2, 17)],
 [datetime.date(2013, 2, 18),
  datetime.date(2013, 2, 19),
  datetime.date(2013, 2, 20),
  datetime.date(2013, 2, 21),
  datetime.date(2013, 2, 22),
  datetime.date(2013, 2, 23),
  datetime.date(2013, 2, 24)],
 [datetime.date(2013, 2, 25),
  datetime.date(2013, 2, 26),
  datetime.date(2013, 2, 27),
  datetime.date(2013, 2, 28),
  datetime.date(2013, 3, 1),
  datetime.date(2013, 3, 2),
  datetime.date(2013, 3, 3)]]
'''
```

### monthdays2calendar

🔨 monthdays2calendar(*year*, *month*)

Return a list of the weeks in the month *month* of the *year* as full weeks. Weeks are lists of seven tuples of day numbers and weekday numbers.

```python
import calendar
c=calendar.Calendar()
c.monthdays2calendar(2013,2)
'''Out:
[[(0, 0), (0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 6)],
 [(4, 0), (5, 1), (6, 2), (7, 3), (8, 4), (9, 5), (10, 6)],
 [(11, 0), (12, 1), (13, 2), (14, 3), (15, 4), (16, 5), (17, 6)],
 [(18, 0), (19, 1), (20, 2), (21, 3), (22, 4), (23, 5), (24, 6)],
 [(25, 0), (26, 1), (27, 2), (28, 3), (0, 4), (0, 5), (0, 6)]]
'''
```

### monthdayscalendar

🔨 monthdayscalendar(*year*, *month*)

Return a list of the weeks in the month *month* of the *year* as full weeks. Weeks are lists of seven day numbers.

```python
import calendar
c=calendar.Calendar()
c.monthdayscalendar(2013,2)
'''Out:
[[0, 0, 0, 0, 1, 2, 3],
 [4, 5, 6, 7, 8, 9, 10],
 [11, 12, 13, 14, 15, 16, 17],
 [18, 19, 20, 21, 22, 23, 24],
 [25, 26, 27, 28, 0, 0, 0]]
'''
```

### yeardatescalendar

🔨 yeardatescalendar(*year*, *width=3*)

Return the data for the specified year ready for formatting. The return value is a list of month rows. Each month row contains up to *width* months (defaulting to 3). Each month contains between 4 and 6 weeks and each week contains 1–7 days. Days are [`datetime.date`](https://docs.python.org/3/library/datetime.html#datetime.date) objects.

### yeardays2calendar

🔨 yeardays2calendar(*year*, *width=3*)

Return the data for the specified year ready for formatting (similar to[`yeardatescalendar()`](https://docs.python.org/3/library/calendar.html#calendar.Calendar.yeardatescalendar)). Entries in the week lists are tuples of day numbers and weekday numbers. Day numbers outside this month are zero.

🔨 yeardayscalendar(*year*, *width=3*)

### yeardays2calendar

Return the data for the specified year ready for formatting (similar to[`yeardatescalendar()`](https://docs.python.org/3/library/calendar.html#calendar.Calendar.yeardatescalendar)). Entries in the week lists are day numbers. Day numbers outside this month are zero.

## 处理文本日历的函数

在 `calendar` 模块中，提供了一些用于处理文本日历的函数，如下：

### setfirstweekday

🔨 calendar.setfirstweekday(*weekday*)

Sets the weekday (`0` is Monday, `6` is Sunday) to start each week. The values `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, and `SUNDAY` are provided for convenience. 

```python
# source code
c = TextCalendar()

def setfirstweekday(firstweekday):
    if not MONDAY <= firstweekday <= SUNDAY:
        raise IllegalWeekdayError(firstweekday)
    c.firstweekday = firstweekday
```

For example, to set the first weekday to Sunday:

```python
import calendar
calendar.setfirstweekday(calendar.SUNDAY)
```

### firstweekday

🔨 calendar.firstweekday()
Returns the current setting for the weekday to start each week.

```python
# source code
c = TextCalendar()

firstweekday = c.getfirstweekday
```

### isleap

🔨 calendar.isleap(*year*)
Returns True if year is a leap year, otherwise False. 

```python
# source code 
def isleap(year):
    """Return True for leap years, False for nonleap years."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

### leapdays

🔨 calendar.leapdays(*y1*, *y2*)

Returns the number of leap years in the range from *y1* to *y2* (exclusive), where *y1* and *y2* are years.

This function works for ranges spanning a century change.

```python
# source code 
def leapdays(y1, y2):
    """Return number of leap years in range [y1, y2).
       Assume y1 <= y2."""
    y1 = 1
    y2 = 1
    return (y2//4  y1//4)  (y2//100  y1//100) + (y2//400  y1//400)
```

### weekday

🔨 calendar.weekday(*year*, *month*, *day*)

Returns the day of the week (`0` is Monday) for *year* (`1970`–…), *month* (`1`–`12`), *day* (`1`–`31`).

```python
# source code
def weekday(year, month, day):
    """Return weekday (0-6 ~ Mon-Sun) for year, month (1-12), day (1-31)."""
    if not datetime.MINYEAR <= year <= datetime.MAXYEAR:
        year = 2000 + year % 400
    return datetime.date(year, month, day).weekday()
```

示例：

```python
print(calendar.weekday(2013, 2, 13))
```

### weekheader

🔨  calendar.weekheader(*n*)

Return a header containing abbreviated weekday names. *n* specifies the width in characters for one weekday.

```python
# source code
c = TextCalendar()
weekheader = c.formatweekheader
```

示例：

```python
print(calendar.weekheader(1))
print(calendar.weekheader(3))
'''Out:
M T W T F S S
Mon Tue Wed Thu Fri Sat Sun
'''
```

### monthrange

🔨 calendar.monthrange(*year*, *month*)

Returns weekday of first day of the month and number of days in month, for the specified *year* and *month*.

```python
# source code
def monthrange(year, month):
    """Return weekday (0-6 ~ Mon-Sun) and number of days (28-31) for
       year, month."""
    if not 1 <= month <= 12:
        raise IllegalMonthError(month)
    day1 = weekday(year, month, 1)
    ndays = mdays[month] + (month == February and isleap(year))
    return day1, ndays
```

示例：

```python
print(calendar.monthrange(2013, 2))
#> (4, 28)
```

### monthcalendar

🔨 calendar.monthcalendar(*year*, *month*)

Returns a matrix representing a month’s calendar. Each row represents a week; days outside of the month a represented by zeros. Each week begins with Monday unless set by [`setfirstweekday()`](https://docs.python.org/3/library/calendar.html#calendar.setfirstweekday).

```python
# source code
c = TextCalendar()
monthcalendar = c.monthdayscalendar
```

示例：

```python
pprint(calendar.monthcalendar(2013, 2))
'''Out:
[[0, 0, 0, 0, 1, 2, 3],
 [4, 5, 6, 7, 8, 9, 10],
 [11, 12, 13, 14, 15, 16, 17],
 [18, 19, 20, 21, 22, 23, 24],
 [25, 26, 27, 28, 0, 0, 0]]
'''
```

### prmonth

🔨 calendar.prmonth(*theyear*, *themonth*, *w=0*, *l=0*)

Prints a month’s calendar as returned by [`month()`](https://docs.python.org/3/library/calendar.html#calendar.month).

```python
# source code
c = TextCalendar()
prmonth = c.prmonth
```

示例：

```python
calendar.prmonth(2013, 2)
'''Out:
   February 2013
Mo Tu We Th Fr Sa Su
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28
'''
```

### month

🔨 calendar.month(*theyear*, *themonth*, *w=0*, *l=0*)

Returns a month’s calendar in a multiline string using the `formatmonth()` of the [`TextCalendar`](https://docs.python.org/3/library/calendar.html#calendar.TextCalendar) class.

```python
# source code
c = TextCalendar()
month = c.formatmonth
```

示例：

```python
print(calendar.month(2013, 2), end='')
'''Out:
   February 2013
Mo Tu We Th Fr Sa Su
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28
'''
```

### prcal

🔨 calendar.prcal(*year*, *w=0*, *l=0*, *c=6*, *m=3*)

Prints the calendar for an entire year as returned by [`calendar()`](https://docs.python.org/3/library/calendar.html#modulecalendar).

```python
# source code
c = TextCalendar()
prcal = c.pryear
```

### calendar

🔨 calendar.calendar(*year*, *w=2*, *l=1*, *c=6*, *m=3*)

Returns a 3column calendar for an entire year as a multiline string using the `formatyear()` of the [`TextCalendar`](https://docs.python.org/3/library/calendar.html#calendar.TextCalendar) class.

```python
# source code
c = TextCalendar()
calendar = c.formatyear
```

### timegm

🔨 calendar.timegm(*tuple*)

An unrelated but handy function that takes a time tuple such as returned by the [`gmtime()`](https://docs.python.org/3/library/time.html#time.gmtime)function in the [`time`](https://docs.python.org/3/library/time.html#moduletime) module, and returns the corresponding Unix timestamp value, assuming an epoch of 1970, and the POSIX encoding. In fact, [`time.gmtime()`](https://docs.python.org/3/library/time.html#time.gmtime) and [`timegm()`](https://docs.python.org/3/library/calendar.html#calendar.timegm) are each others’ inverse.

```python
def timegm(tuple):
    """Unrelated but handy function to calculate Unix timestamp from GMT."""
    year, month, day, hour, minute, second = tuple[:6]
    days = datetime.date(year, month, 1).toordinal() - _EPOCH_ORD + day - 1
    hours = days*24 + hour
    minutes = hours*60 + minute
    seconds = minutes*60 + second
    return seconds
```

## 数据属性

The [`calendar`](https://docs.python.org/3/library/calendar.html#module-calendar) module exports the following data attributes:

🔨 calendar.day_name

An array that represents the days of the week in the current locale.

```python
import calendar
calendar.day_name #> calendar._localized_day
list(calendar.day_name)
#> ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
```

🔨 calendar.day_abbr

An array that represents the abbreviated days of the week in the current locale.

```python
import calendar
list(calendar.day_abbr)
#> ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
```

🔨 calendar.month_name

An array that represents the months of the year in the current locale. This follows normal convention of January being month number 1, so it has a length of 13 and `month_name[0]`is the empty string.

```python
import calendar
list(calendar.month_name)
'''out:
['',
 'January',
 'February',
 'March',
 'April',
 'May',
 'June',
 'July',
 'August',
 'September',
 'October',
 'November',
 'December']
 '''
```

🔨 calendar.month_abbr

An array that represents the abbreviated months of the year in the current locale. This follows normal convention of January being month number 1, so it has a length of 13 and`month_abbr[0]` is the empty string.

```python
import calendar
list(calendar.month_abbr)
'''Out:
['',
 'Jan',
 'Feb',
 'Mar',
 'Apr',
 'May',
 'Jun',
 'Jul',
 'Aug',
 'Sep',
 'Oct',
 'Nov',
 'Dec']
'''
```

