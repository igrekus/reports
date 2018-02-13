import pymysql
from PyQt5.QtCore import QObject


class MysqlEngine(QObject):
    def __init__(self, parent=None, dbItemClass=None):
        super(MysqlEngine, self).__init__(parent)

        # TODO make properties
        self._engineType = "mysql"
        self._connection = None
        self._dbItemClass = dbItemClass

    def connectToDatabase(self):
        try:
            f = open("settings.ini")
        except IOError:
            return False, str("Settings.ini not found.")

        lines = f.readlines()
        f.close()

        settings = dict()
        for s in lines:
            # print(s)
            if s.strip() and s[0] != "#":
                sett = s.strip().split("=")
                settings[sett[0]] = sett[1]
            else:
                continue

        try:
            self._connection = pymysql.connect(host=settings['host'],
                                               port=int(settings['port']),
                                               user=settings['username'],
                                               passwd=settings['password'],
                                               db=settings['database'],
                                               charset='utf8mb4')
        except pymysql.MySQLError as e:
            return False, str("DB error: " + str(e.args[0]) + " " + e.args[1])

        return True, "connection established"

    def initEngine(self):
        print("init mysql engine")
        ok, err = self.connectToDatabase()

    def execSimpleQuery(self, string):
        with self._connection:
            cur = self._connection.cursor()
            cur.execute(string)

        print("query:", cur._last_executed, "| rows:", cur.rowcount)
        return cur

    def execParametrizedQuery(self, string, param):
        with self._connection:
        # try:
            cur = self._connection.cursor()
            cur.execute(string, param)

        # except Exception as e:
        #     print(e)

        print("query:", cur._last_executed, "| rows:", cur.rowcount)
        return cur

    def execBulkQuery(self, string, paramlist):
        with self._connection:
            cur = self._connection.cursor()
            cur.executemany(string, paramlist)

        print("query:", cur._last_executed, "| rows:", cur.rowcount)
        return cur

    def fetchMainData(self, param: tuple):
        print(param)
        if param is not None:
            return self.execParametrizedQuery(self._dbItemClass.itemListRequestString(), param).fetchall()
        else:
            return self.execSimpleQuery(self._dbItemClass.itemListRequestString()).fetchall()

    def fetchDict(self, name):
        # TODO make dict ORM
        return self.execSimpleQuery("CALL __get" + name + "List()").fetchall()

    def insertMainDataRecord(self, data):
        # TODO: construct parameter list by number of data items
        q = "CALL insertMainData(%s, %s, %s, %s, %s, %s, %s)"
        print(q, data[:-1])
        # cursor = self.execParametrizedQuery(q, data[:-1])
        # rec_id = cursor.fetchone()[0]
        rec_id = 1000
        return rec_id

    def updateMainDataRecord(self, data):
        # TODO: construct string depending on data size
        q = "CALL updateMainData(%s, %s, %s, %s, %s, %s, %s, %s)"
        print(q, data)
        # self.execParametrizedQuery(q, data)

    def deleteMainDataRecord(self, data):
        q = "CALL deleteMainData(%s)"
        print(q, data)
        # self.execParametrizedQuery(q, data)

    def insertDictRecord(self, dictName, data):
        print("mysql engine insert dict record:", dictName, data)
        # with self._connection:
        #     cursor = self._connection.cursor()
        #     cursor.execute(" INSERT INTO " + dictName +
        #                    "      (" + dictName + "_id" +
        #                    "      , " + dictName + "_name" + ")"
        #                    " VALUES (NULL, %s)", data)
        #     rec_id = cursor.lastrowid
        rec_id = 100
        return rec_id

    def updateDictRecord(self, dictName, data):
        print("mysql engine update dict record:", dictName, data)
        # with self._connection:
        #     cursor = self._connection.cursor()
        #     cursor.execute(" UPDATE " + dictName +
        #                    "    SET " + dictName + "_name = %s" +
        #                    "  WHERE " + dictName + "_id = %s", data)

    def deleteDictRecord(self, dictName, data):
        print("mysql engine delete dict record:", dictName, data)
        # with self._connection:
        #     cursor = self._connection.cursor()
        #     cursor.execute(" DELETE "
        #                    "   FROM " + dictName +
        #                    "  WHERE " + dictName + "_id = %s", data)

    # domain-specific methods
    def fetchContractDetailList(self):
        return self.execSimpleQuery("CALL getContractDetailList()").fetchall()

    def insertContractDetail(self, data: list) -> list:
        q = "CALL insertContractDetail(%s, %s)"
        print(q, data)
        # self.execParametrizedQuery(q, (rec_id, mapping, ))
        return [1111] * len(data)

    def updateContractDetail(self, data: list):
        q = "CALL updateContractDetail(%s, %s)"
        print(q, data)
        # self.execParametrizedQuery(q, (rec_id, mapping, ))

    def deleteContractDetail(self, data: list):
        q = "CALL deleteContractDetail(%s, %s)"
        print(q, data)
        # self.execParametrizedQuery(q, (rec_id, mapping, ))

    def insertProductRecrod(self, data: tuple):
        q = "CALL insertProductRecord(%s, %s)"
        print(q, data)
        return 100

    def updateProductRecord(self, data: tuple):
        q = "CALL updateProductRecord(%s, %s, %s)"
        print(q, data)

    def deleteProductRecord(self, data: tuple):
        q = "CALL deleteProductRecord(%s)"
        print(q, data)
