"""
Initialize a sqlite local database called test.db. console input 0 to exit.
Intialized different set of log entries using SqlManagers, it will clear the test.db
everytime this program is runned.
"""
from log_entry import LogEntry as E
import datetime as dt
from sql_manager import SqlManager as SM
import random

# no entry
set1 = []
# different fixed entries
set2 = [E(dt.datetime.now(), 10, 12),
        E(dt.datetime(2025,4,9,12,39), 0, 12.4),
        E(dt.datetime(2025,3,30,15,20), 6.6, 8.5),
        E(dt.datetime(2025,3,24,17,15), 8, 10),
        E(dt.datetime(2025,3,22,19,13), 4.5, 3),
        E(dt.datetime(2025,3,15,16,39), 8, 10),
        E(dt.datetime(2025,3,2,14,21), 8, 16),
        E(dt.datetime(2025,2,28,6,56), 8, 12),
        E(dt.datetime(2025,2,20,8,33), 8, 5),
        E(dt.datetime(2025,2,14,9,6), 10, 3),
        E(dt.datetime(2025,2,10,22,5), 8, 4),
        E(dt.datetime(2025,1,23,23,16), 8, 10),
        E(dt.datetime(2025,1,31,17,47), 8, 16),
        E(dt.datetime(2025,1,1,19,51), 2, 3),
        E(dt.datetime(2024,12,31,20,00), 10, 11),
        E(dt.datetime(2024,12,24,3,33), 8, 20),
        E(dt.datetime(2024,12,2,0,46), 2, 6),
        E(dt.datetime(2024,11,17,16,23), 13.2, 15),
        E(dt.datetime(2024,11,13,11,55), 8, 12),
        E(dt.datetime(2024,11,11,10,4), 5.4, 12),
        E(dt.datetime(2024,11,6,13,53), 8, 12)]
# Random entries
set3 = []
for i in range(100):
    try:
        e = E(dt.datetime(random.randint(2023,2025)
                , random.randint(1,12)
                , random.randint(1,31)
                , random.randint(0,23)
                , random.randint(0,59))
                , round(random.uniform(0,24),2)
                , round(random.uniform(0,24),2))
        set3.append(e)
    except:
        pass

choice = -1
data_sets = [set1, set2, set3]

while (choice < 0 or choice > len(data_sets)):
    try:
        choice = int(input("data set # to start with in test.db: "))
    except:
        choice = -1 

if(choice == 0):
    exit()

manager = SM("test.db")
manager.cur.execute("DROP TABLE IF EXISTS logs")
manager.con.commit()
manager = SM("test.db")

for e in data_sets[choice-1]:
    manager.add_entry(e)

current_content = manager.get_timestamps()
for timestamp in current_content:
    print(timestamp)