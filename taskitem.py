import datetime
import const


class TaskItem:
    # TODO: make DB-aware orm?
    # TODO: make properties
    def __init__(self, id_=None, dateBegin=None, dateChange=None, dateEnd=None, initId=None, projId=None, descript=None,
                 order=None, percent=None, difficulty=None, urgent=None, important=None, active=None, userid=None,
                 priorityid=None, strict=None, dateMove=None, note=None, dateCreated=None, sdr=None):
        self.item_id = id_
        self.item_dateBegin = dateBegin
        self.item_dateChange = dateChange
        self.item_dateEnd = dateEnd
        self.item_initiatorId = initId
        self.item_projectId = projId
        self.item_description = descript
        self.item_order = order
        self.item_percent = percent
        self.item_difficulty = difficulty
        self.item_urgent = urgent
        self.item_important = important
        self.item_active = active
        self.item_userId = userid
        self.item_priorityId = priorityid
        self.item_strict = strict
        self.item_dateMove = dateMove
        self.item_note = note
        self.item_dateCreated = dateCreated
        self.item_sdr = sdr

    def __str__(self):
        return "TaskItem(" + "id:" + str(self.item_id) + " " \
               + "begin:" + str(self.item_dateBegin) + " " \
               + "change:" + str(self.item_dateChange) + " " \
               + "end:" + str(self.item_dateEnd) + " " \
               + "init:" + str(self.item_initiatorId) + " " \
               + "proj:" + str(self.item_projectId) + " " \
               + "desc:" + str(self.item_description) + " " \
               + "order:" + str(self.item_order) + " " \
               + "perc:" + str(self.item_percent) + " " \
               + "diff:" + str(self.item_difficulty) + " " \
               + "urgent:" + str(self.item_urgent) + " " \
               + "important:" + str(self.item_important) + " " \
               + "active:" + str(self.item_active) + " " \
               + "user:" + str(self.item_userId) + " " \
               + "priority:" + str(self.item_priorityId) + " " \
               + "strict:" + str(self.item_strict) + " " \
               + "move:" + str(self.item_dateMove) + " " \
               + "note:" + str(self.item_note) + " " \
               + "created:" + str(self.item_dateCreated) + " " \
               + "sdr:" + str(self.item_sdr) + ")"

    @classmethod
    def fromSqlTuple(cls, sql_tuple: tuple):
        return cls(id_=sql_tuple[0]
                   , dateBegin=sql_tuple[1]
                   , dateChange=sql_tuple[2]
                   , dateEnd=sql_tuple[3]
                   , initId=sql_tuple[4]
                   , projId=sql_tuple[5]
                   , descript=sql_tuple[6]
                   , order=sql_tuple[7]
                   , percent=sql_tuple[8]
                   , difficulty=sql_tuple[9]
                   , urgent=sql_tuple[10]
                   , important=sql_tuple[11]
                   , active=sql_tuple[12]
                   , userid=sql_tuple[13]
                   , priorityid=sql_tuple[14]
                   , strict=sql_tuple[15]
                   , dateMove=sql_tuple[16]
                   , note=sql_tuple[17]
                   , dateCreated=sql_tuple[18]
                   , sdr=sql_tuple[19])

    @classmethod
    def newItem(cls):
        return cls(id_=0
                   , dateBegin=datetime.datetime.today().date()
                   , dateChange=datetime.datetime.today().date()
                   , dateEnd=datetime.datetime.today().date()
                   , initId=0
                   , projId=0
                   , descript=""
                   , order=0
                   , percent=0
                   , difficulty=1
                   , urgent=0
                   , important=0
                   , active=1
                   , userid=0
                   , priorityid=0
                   , strict=0
                   , dateMove=datetime.datetime.today().date()
                   , note=""
                   , dateCreated=datetime.datetime.today().date()
                   , sdr="")


    def toTuple(self):
        def formatDate(indate):
            if isinstance(indate, datetime.date):
                return indate.isoformat()
            return "2000-01-01"

        return tuple([formatDate(self.item_dateBegin)
                      , formatDate(self.item_dateChange)
                      , formatDate(self.item_dateEnd)
                      , self.item_initiatorId
                      , self.item_projectId
                      , self.item_description
                      , self.item_order
                      , self.item_percent
                      , self.item_difficulty
                      , self.item_urgent
                      , self.item_important
                      , self.item_active
                      , self.item_userId
                      , self.item_priorityId
                      , self.item_strict
                      , formatDate(self.item_dateMove)
                      , self.item_note
                      , formatDate(self.item_dateCreated)
                      , self.item_sdr
                      , self.item_id])

    @classmethod
    def itemListRequestString(self):
        return str("CALL __getTaskListForUser(%s)")
