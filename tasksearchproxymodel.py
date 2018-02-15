import datetime
import const
import re
from PyQt5.QtCore import QSortFilterProxyModel, QDate, Qt


class TaskSearchProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(TaskSearchProxyModel, self).__init__(parent)

        self.filterUser = 0
        self.filterInit = 0
        self.filterProject = 0
        self.filterDateBeginFrom = None
        self.filterDateBeginTo = None
        self.filterDateEndFrom = None
        self.filterDateEndTo = None
        self.filterActive = True
        self.filterNotActive = False
        self.filterStrictDate = False
        self.filterHundredPercent = False
        self._filterString = ""
        self._filterRegex = re.compile(self._filterString, flags=re.IGNORECASE)

    @property
    def filterString(self):
        return self._filterString

    @filterString.setter
    def filterString(self, string):
        if type(string) == str:
            self._filterString = string
            self._filterRegex = re.compile(string, flags=re.IGNORECASE)
        else:
            raise TypeError("Filter must be a str.")

    def filterAcceptsSelf(self, row, parent_index):
        item_id, item_userId, item_initiatorId, item_projectId, item_dateBegin, \
        item_dateEnd, item_active, item_strict, item_percent = self.sourceModel().index(row, 0, parent_index).data(
            const.RoleFilterData)
        # nodeId = self.sourceModel().index(row, 0, parent_index).data(const.RoleNodeId)
        # user = self.sourceModel().index(row, 0, parent_index).data(const.RoleUser)
        # init = self.sourceModel().index(row, 0, parent_index).data(const.RoleInit)
        # proj = self.sourceModel().index(row, 0, parent_index).data(const.RoleProject)
        # RoleProject = RoleInit + 1
        # RoleDateBegin = RoleProject + 1
        # RoleDateEnd = RoleDateBegin + 1
        # RoleActive = RoleDateEnd + 1
        # RoleStrict = RoleActive + 1
        # RolePercent = RoleStrict + 1

        # self.filterUser = 0
        # self.filterInit = 0
        # self.filterProject = 0
        # self.filterDateBeginFrom = datetime.date.today()
        # self.filterDateBeginTo = datetime.date.today()
        # self.filterDateEndFrom = datetime.date.today()
        # self.filterDateEndTo = datetime.date.today()
        # self.filterActive = False
        # self.filterNotActive = False
        # self.filterStrictDate = False
        # self.filterHundredPercent = False

        # if self.filterUser != 0 and self.filterUser != item_userId:
        #     return False
        if self.filterUser == 0 or self.filterUser == item_userId:
            if self.filterInit == 0 or self.filterInit == item_initiatorId:
                if self.filterProject == 0 or self.filterProject == item_projectId:
                    if self.filterDateBeginFrom is None or self.filterDateBeginFrom <= item_dateBegin:
                        if self.filterDateBeginTo is None or self.filterDateBeginTo >= item_dateBegin:
                            if self.filterDateEndFrom is None or self.filterDateEndFrom <= item_dateEnd:
                                if self.filterDateEndTo is None or self.filterDateEndTo >= item_dateEnd:
                                    if not self.filterStrictDate or self.filterStrictDate == item_strict:
                                        if not self.filterHundredPercent or 100 == item_percent:
                                            return True
        # if self.filterClient == 0 or self.filterClient == client:
        #     for i in range(self.sourceModel().columnCount()):
        #         string = str(self.sourceModel().index(row, i, parent_index).data(Qt.DisplayRole))
        #         if self._filterRegex.findall(string):
        #             return True
        return False


    def filterAcceptsRow(self, source_row, source_parent_index):
        # check self
        if self.filterAcceptsSelf(source_row, source_parent_index):
            return True

        return False
