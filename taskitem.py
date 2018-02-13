import datetime
import const


class TaskItem:
    # TODO: make DB-aware orm?
    # TODO: make properties
    def __init__(self, id_=None, projId=None, initId=None, descript=None, userid=None, percent=None, dateBegin=None,
                 dateChange=None, dateEnd=None, difficulty=None, active=None, priorityid=None, strict=None):
        self.item_id = id_
        self.item_projectId = projId
        self.item_initiatorId = initId
        self.item_description = descript
        self.item_userId = userid
        self.item_percent = percent
        self.item_dateBegin = dateBegin
        self.item_dateChange = dateChange
        self.item_dateEnd = dateEnd
        self.item_difficulty = difficulty
        self.item_active = active
        self.item_priorityId = priorityid
        self.item_strict = strict

    def __str__(self):
        return "ContractItem(" + "id:" + str(self.item_id) + " " \
               + "proj:" + str(self.item_projectId) + " " \
               + "init:" + str(self.item_initiatorId) + " " \
               + "desc:" + str(self.item_description) + " " \
               + "user:" + str(self.item_userId) + " " \
               + "perc:" + str(self.item_percent) + " " \
               + "begin:" + str(self.item_dateBegin) + " " \
               + "change:" + str(self.item_dateChange) + " " \
               + "end:" + str(self.item_dateEnd) + " " \
               + "diff:" + str(self.item_difficulty) + " " \
               + "active:" + str(self.item_active) + " " \
               + "priority:" + str(self.item_priorityId) + ")"

    @classmethod
    def fromSqlTuple(cls, sql_tuple: tuple):
        return cls(id_=sql_tuple[0],
                   projId=sql_tuple[1],
                   initId=sql_tuple[2],
                   descript=sql_tuple[3],
                   userid=sql_tuple[4],
                   percent=(sql_tuple[5] - 1) * 10,
                   dateBegin=sql_tuple[6],
                   dateChange=sql_tuple[7],
                   dateEnd=sql_tuple[8],
                   difficulty=sql_tuple[9],
                   active=sql_tuple[10],
                   priorityid=sql_tuple[11],
                   strict=sql_tuple[12])

    def toTuple(self):
        def formatDate(indate):
            if isinstance(indate, datetime.date):
                return indate.isoformat()
            return "2000-01-01"

        return tuple([self.item_projectId,
                      self.item_initiatorId,
                      self.item_description,
                      self.item_userId,
                      self.item_percent,
                      formatDate(self.item_dateBegin),
                      formatDate(self.item_dateChange),
                      formatDate(self.item_dateEnd),
                      self.item_difficulty,
                      self.item_active,
                      self.item_priorityId,
                      self.item_strict,
                      self.item_id])

    @classmethod
    def itemListRequestString(self):
        return str("CALL __getTaskListForUser(%s)")
