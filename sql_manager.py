import sqlite3 as sql
from log_entry import LogEntry
import datetime as dt

class SqlManager:
    """
    A class that manage the logs table in a sqlite local database file.
    The logs table contains the columns: 
        timestamp TEXT PRIMARY KEY, 
        drivetime FLOAT, 
        resttime FLOAT.
    Any errors generated from sqlite3 operations will NOT be handled by the manager.

    Attributes:
        filename(str): name of the sqlite database file
        con(sqlite3.Connection): SQLite connection to the database
        cur(sqlite3.Cursor): SQLite cursor for the SQL connection con
    """
    TIMESTAMP_FORMAT = "%m/%d/%Y %H:%M"
    
    def __init__(self, filename : str):
        """
        Constructor of the SqlManager. It will try to connect to the filename provided.
        """
        self.filename = filename
        # connect to the database
        self.con = sql.connect(filename)
        self.cur = self.con.cursor()
        # create a table named logs if not exists. timestamp set to primary key for fast lookup
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS logs(
                         timestamp TEXT PRIMARY KEY, 
                         drivetime FLOAT, 
                         resttime FLOAT)""")
        # create an index for logs based on the timestamp to enhance sorting
        self.cur.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON logs(timestamp)")
        self.con.commit()

    def get_entry(self, timestamp : dt.datetime):
        """
        Creates a LogEntry according to a sql data row.
        (date and time of the entry will be stored in iso format text in sql for easy ordering)

        Returns: a logEntry stored in the databased 
        """
        row = self.cur.execute("SELECT timestamp, drivetime, resttime FROM logs WHERE timestamp = ?"
                               , (self._to_text(timestamp),)).fetchone()
        if(row == None):
            return None
        return self._row_to_entry(row)
    
    def get_timestamps(self, n = -1):
        """
        Get n entries's timestamp in descending order. 
        When n is less than or equals to 0, it gets all entries.
        Args:
            n: (default to -1) the number to the latest entry needed.
        Returns:
            A 2D list of datetime objects, for example [[a],[b],[c]]
        """
        rows = [[]]
        if (n > 0):
            rows = self.cur.execute("SELECT timestamp from logs ORDER BY timestamp DESC LIMIT ?", (n,)).fetchall()
        else:
            rows = self.cur.execute("SELECT timestamp FROM logs ORDER BY timestamp DESC").fetchall()
        result = []
        for r in rows:
            result.append([self._to_timestamp(r[0])])
        return result
    
    def add_entry(self, entry : LogEntry):
        """
        Add the entry to the database
        """
        self.cur.execute("INSERT OR IGNORE INTO logs VALUES(?, ?, ?)", self._entry_to_row(entry))
        self.con.commit()

    def update_entry(self, timestamp : dt.datetime, entry : LogEntry):
        """
        Update the entry in database where its timestamp is similar to the input datetime object
        (same year, month, day, hour, and minutes).
        the new entry stored will be the input LogEntry instance.
        Note: timestamp input is a datetime object, similarly, the timestamp attribute of a LogEntry object
        also is a datetime object, but to store in our database, they will be convert to equivalent
        text representation according to format defined by the sql manager.
        """
        row = self._entry_to_row(entry)
        row.append(self._to_text(timestamp))
        # update the new entry information in sql file
        self.cur.execute("UPDATE logs SET timestamp = ?, drivetime = ?, resttime = ? WHERE timestamp = ?"
                         , row)
        self.con.commit()

    def delete_entry(self, timestamp : dt.datetime):
        """
        delete the entry with the input timestamp from the database.
        Returns:
            a LogEntry object that represent the deleted entry
        """
        if(isinstance(timestamp, LogEntry)):
            timestamp = timestamp.timestamp
        deleted_entry = self.get_entry(timestamp=timestamp)
        self.cur.execute("DELETE FROM logs WHERE timestamp = ?", [self._to_text(timestamp)])
        self.con.commit()
        return deleted_entry

    def get_time_data_between_dates(self, start_date, end_date):
        """
        Fetch drive and rest time logs between two dates from the database.
        Returns a list of rows: [(timestamp, drivetime, resttime), ...]
        """
        try:
            query = """
            SELECT timestamp, drivetime, resttime
            FROM logs
            WHERE date(timestamp) BETWEEN ? AND ?
            ORDER BY timestamp;
            """
            self.cur.execute(query, (start_date, end_date))
            return self.cur.fetchall()
        except Exception as e:
            print(f"Database error: {e}")
            return []

    def _entry_to_row(self, entry : LogEntry):
        """
        helper method that create a row representation of the entry to be stored in database.
        that is, create a list [string timestamp, float drivetime, float resttime] for the entry.
        """
        result = []
        result.append (self._to_text(entry.timestamp))
        result.append (float(entry.drivetime))
        result.append (float(entry.resttime))
        return result
    
    def _row_to_entry(self, row):
        """
        Returns a LogEntry object with data stored in row.
        row[0] should be a string in the format TIMESTAMP_FORMAT, representing the timestamp.
        row[1] and row[2] should be floats that represents the drivetime and resttime respectively.
        """
        return LogEntry(self._to_timestamp(row[0]), row[1], row[2])

    def _to_text(self, timestamp : dt.datetime):
        """
        helper method that used to format the timestamp of a LogEntry to be 
        stored in the database, for easier ordering
        """
        return timestamp.strftime(self.TIMESTAMP_FORMAT)

    def _to_timestamp(self, timestamp_str : str):
        """
        helper method that create a datetime.datetime object from 
        a text representation of the timestamp stored in our database
        """
        return dt.datetime.strptime(timestamp_str, self.TIMESTAMP_FORMAT)


# test:
# e = LogEntry(dt.datetime.now(), 10, 12)
# manager = SqlManager("test.db")
# manager.cur.execute("DROP TABLE logs")
# manager.con.commit()
# manager = SqlManager("test.db")
# print(manager._to_text(e.timestamp))
# print(manager._entry_to_row(e))

# manager.add_entry(e)
# print(manager.delete_entry(e.timestamp))

# manager.add_entry(e)
# print(manager.get_entry(e.timestamp))

# e1 = LogEntry(dt.datetime(2025,4,9,12,39), 0, 12.4)
# manager.update_entry(e.timestamp, e1)
# print(manager.get_entry(e1.timestamp))
# manager.cur.execute("DROP TABLE logs")
# manager.con.commit()