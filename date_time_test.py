from datetime import datetime, timezone
created_at_str = 'Sun Apr 25 18:20:34 +0000 2021'
tokenized_time = created_at_str.split()
month, day, time, year = [tokenized_time[i] for i in (1, 2, 3, 5)]

print(month)
# print(tokenized_time)
if month == 'Jan':
    month = 1
elif month == 'Feb':
    month = 2
elif month == 'Mar':
    month = 3
elif month == 'Apr':
    month = 4
elif month == 'May':
    month = 5
elif month == 'Jun':
    month = 6
elif month == 'Jul':
    month = 7
elif month == 'Aug':
    month = 8
elif month == 'Sep' or month =='Sept':
    month = 9
elif month == 'Oct':
    month = 10
elif month == 'Nov':
    month = 11
elif month == 'Dec':
    month = 12

hour, minute, second = time.split(':')


my_date = datetime(year=int(year), month=month, day=int(day),
                            hour=int(hour), minute=int(minute), second=int(second), tzinfo=timezone.utc)

print(my_date)
# date_obj = datetime.datetime.fromtimestamp(float('1619374834103'))
# print(date_obj)