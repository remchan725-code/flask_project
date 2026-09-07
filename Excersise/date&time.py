import datetime
date = datetime.date.today()
time = datetime.datetime.now()
now = time.strftime("%H:%M:%S %m-%d-%y")
target_datetime = datetime.datetime(2020,2,22,12,30,1)
current_datetime = datetime.datetime.now()
if target_datetime < current_datetime:
    print("Target date got passed")
else:
    print("Target date NOT passed")
print(date)
print (now)