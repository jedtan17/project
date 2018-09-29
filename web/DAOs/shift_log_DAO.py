import datetime, os, sys
import pandas as pd

if __name__ == '__main__':  sys.path.append("..")
from DAOs.connection_manager import connection_manager

sys.path.append('../Entities')
from Entities.shift_log import Shift_log


class shift_log_DAO(object):
    '''
    This class handles connection between app and the database table
    '''

    table_name = "stbern.shift_log"

    def __init__(self):
        '''
        Constructor
        '''
        self.min_datetime = None
        self.max_datetime = None
        self.set_min_max_datetime()


    def set_min_max_datetime(self):
        '''
        Sets obj vars and returns max_datetime and min_datetime found in the database

        Returns:
        (max_datetime, min_datetime) or (None, None) if nothing found
        '''
        query = """SELECT MAX({}) as 'max' ,
                          MIN({}) as 'min'
                          FROM {};"""                    \
                    .format(Shift_log.datetime_tname,    \
                            Shift_log.datetime_tname,    \
                            shift_log_DAO.table_name)

        # Get connection
        factory = connection_manager()
        connection = factory.connection
        cursor = connection.cursor()

        try:
            cursor.execute(query)
            result = cursor.fetchone()

            #set class vars
            if result != None:
                self.max_datetime = result['max']
                self.min_datetime = result['min']
                return result['max'], result['min']
            else: return None, None

        except:
            print("error")
        finally:
            factory.close_all(cursor=cursor, connection=connection)


    def insert_shift_log(self, shift_log):
        '''
        Inserts an entry into the database table

        Keyword arguments:
        shift_log -- Entities.shift_log, class vars used to create a new DB row
        '''
        query = """INSERT INTO {} VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""" \
                    .format(shift_log_DAO.table_name)

         # Get connection
        factory = connection_manager()
        connection = factory.connection
        cursor = connection.cursor()


        try:
            cursor.execute(query, shift_log.var_list)
        except:
            return
        finally:
            factory.close_all(cursor=cursor, connection=connection)

    def get_all_logs():
        """
        Returns all logs in a dataframe
        """

        query = "SELECT * FROM {}".format(shift_log_DAO.table_name)

        # Get connection
        factory = connection_manager()
        connection = factory.connection

        return pd.read_sql_query(query, connection)


# # TEST-1 insert
# sl_dao = shift_log_DAO()
# obj = Shift_log(datetime.datetime.now(), 101, 20)
# print("Inserting obj: " + str(obj))
# sl_dao.insert_shift_log(obj)

# # TEST-2 set min max
# sl_dao.set_min_max_datetime()
# print("min - max datetime in dao: {}, {}".format(sl_dao.min_datetime, sl_dao.max_datetime))
