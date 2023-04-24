import mariadb
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick

connection = mariadb.connect(
    user = "web_read_only",
    password = "capstone2023",
    host = "107.175.8.57",
    port = 3306,
    database = "plant_moisture"
)

cursor = connection.cursor()
time_stamps = []
percentages = []
cursor.execute("SELECT time_stamp, percentage FROM moisture ORDER BY time_stamp DESC LIMIT 9")
connection.commit()
for time_stamp, percentage in cursor:
    time_stamps.append(time_stamp.strftime("%H:%M:%S"))
    percentages.append(percentage)

time_stamps.reverse()
percentages.reverse()

print(time_stamps)
print(percentages)

fig, ay = plt.subplots()

plt.plot(time_stamps, percentages)
plt.gcf().autofmt_xdate()
ay.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.xticks(rotation=45)
plt.xlabel('Time')
plt.ylabel('Moisture')
plt.title('Plant Moisture')

plt.show()