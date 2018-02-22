import const
import re
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QModelIndex, QVariant


class TaskSearchProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(TaskSearchProxyModel, self).__init__(parent)

        self.filterUser = list()
        self.filterInit = list()
        self.filterProject = list()
        self.filterDateBeginFrom = None
        self.filterDateBeginTo = None
        self.filterDateEndFrom = None
        self.filterDateEndTo = None
        self.filterActive = True
        self.filterNotActive = True
        self.filterStrictDate = False
        self.filterHundredPercent = True
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

        def rowMatchesString():
            for i in range(self.sourceModel().columnCount()):
                string = str(self.sourceModel().index(row, i, parent_index).data(Qt.DisplayRole))
                if self._filterRegex.findall(string):
                    return True
            return False

        item_id, item_userId, item_initiatorId, item_projectId, item_dateBegin, \
        item_dateEnd, item_active, item_strict, item_percent = self.sourceModel().index(row, 0, parent_index).data(
            const.RoleFilterData)

        # TODO match user, initiator, project against a list
        if not self.filterUser or not self.filterInit or not self.filterProject:
            return False

        if self.filterUser and item_userId not in self.filterUser:
            return False

        if self.filterInit and item_initiatorId not in self.filterInit:
            return False

        if self.filterProject and item_projectId not in self.filterProject:
            return False

        if self.filterDateBeginFrom is not None and self.filterDateBeginFrom > item_dateBegin:
            return False

        if self.filterDateBeginTo is not None and self.filterDateBeginTo < item_dateBegin:
            return False

        if self.filterDateEndFrom is not None and self.filterDateEndFrom > item_dateEnd:
            return False

        if self.filterDateEndTo is not None and self.filterDateEndTo < item_dateEnd:
            return False

        if self.filterStrictDate and not item_strict:
            return False

        if not self.filterHundredPercent and item_percent == 100:
            return False

        if not self.filterActive and item_active:
            return False

        if not self.filterNotActive and not item_active:
            return False

        if self._filterString and not rowMatchesString():
            return False

        return True

    def filterAcceptsRow(self, source_row, source_parent_index):
        # check self
        if self.filterAcceptsSelf(source_row, source_parent_index):
            return True

        return False

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return QVariant(index.row() + 1)
        return super(TaskSearchProxyModel, self).data(index, role)

    # def rowCount(self, parent=None, *args, **kwargs):
    #     rows = super(TaskSearchProxyModel, self).rowCount(parent, *args, **kwargs)
    #     print(rows)
    #     return rows
