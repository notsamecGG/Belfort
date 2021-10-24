from datetime import datetime
import time


FMT = '%S:%M:%H,%d-%m-%Y'
x = datetime.now().strftime(FMT)

time.sleep(2)

y = datetime.now().strftime(FMT)

print(datetime.strptime(y, FMT) - datetime.strptime(x, FMT))

#print(datetime.strptime(y, "%Y-%m-%d %H:%M:%S") - datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
