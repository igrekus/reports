import const
import datetime
from dateutil.rrule import *
from PyQt5.QtCore import Qt, QModelIndex, QVariant, QAbstractTableModel
from PyQt5.QtGui import QBrush, QColor
from domainmodel import DomainModel
from taskitem import TaskItem


class TreeNode(object):

    def __init__(self, data=None, parent=None):
        self.data = data
        self.parentNode = parent
        self.childNodes = list()

    def appendChild(self, item):
        self.childNodes.append(item)

    def child(self, row):
        return self.childNodes[row]

    def childCount(self):
        return len(self.childNodes)

    def parent(self):
        return self.parentNode

    def row(self):
        if self.parentNode:
            return self.parentNode.childItems.index(self)
        return 0

    def findChild(self, data):
        for i in range(len(self.childNodes)):
            if self.childNodes[i].data == data:
                return i

    def __str__(self):
        return "TreeNode(data:" + str(self.data) + " parent:" + str(id(self.parentNode)) + " children:" + str(
            len(self.childNodes)) + ")"

class TaskModel(QAbstractTableModel):

    ColumnIndex = 0
    ColumnProject = ColumnIndex + 1
    ColumnInitiator = ColumnProject + 1
    ColumnDescription = ColumnInitiator + 1
    ColumnUser = ColumnDescription + 1
    ColumnPercent = ColumnUser + 1
    ColumnDateBegin = ColumnPercent + 1
    ColumnDateChange = ColumnDateBegin + 1
    ColumnDateEnd = ColumnDateChange + 1
    ColumnDifficulty = ColumnDateEnd + 1
    ColumnActive = ColumnDifficulty + 1
    ColumnPriority = ColumnActive + 1
    ColumnCount = ColumnPriority + 1

    _headers = ["№", "Тема", "Инициатор", "Формулировка", "Исполнитель", "%", "Начало", "Изменение", "Срок",
                "Сложность", "Актуальность", "Приоритет"]

    def __init__(self, parent=None, domainModel=None):
        super(TaskModel, self).__init__(parent)
        self._modelDomain: DomainModel = domainModel

        # self.rootNode = TreeNode(None, None)

        # self._modelDomain.contractAdded.connect(self.onContractAdded)
        # self._modelDomain.contractUpdated.connect(self.onContractUpdated)
        # self._modelDomain.contractRemoved.connect(self.onContractRemoved)

        self.cache = dict()

    # def clear(self):
    #     def clearTreeNode(node):
    #         if node.childNodes:
    #             for n in node.childNodes:
    #                 clearTreeNode(n)
    #         node.childNodes.clear()
    #
    #     clearTreeNode(self.rootNode)
    #
    # def buildFirstLevel(self, data):
    #     for k, v in data.items():
    #         self.rootNode.appendChild(TreeNode(k, self.rootNode))

    # def buildSecondLevel(self, mapping):
    #     for n in self.rootNode.childNodes:
    #         for i in mapping[n.data]:
    #             n.appendChild(TreeNode(self._modelDomain.getItemById(i).item_id, n))

    # def buildTree(self):
    #     self.buildFirstLevel(data=self._modelDomain.contractList)
    #     # self.buildSecondLevel(mapping=self._modelDomain.substMap)

    def initModel(self):
        print("init task table model")

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self._headers):
            return QVariant(self._headers[section])
        return QVariant()

    def rowCount(self, parent=QModelIndex(), *args, **kwargs):
        if not parent.isValid():
            return len(self._modelDomain.taskList)
        return 0

    def columnCount(self, parent=QModelIndex(), *args, **kwargs):
        return self.ColumnCount

    def setData(self, index, value, role):
        return True

    def data(self, index: QModelIndex, role=None) -> QVariant:
        if not index.isValid():
            return QVariant()

        row = index.row()
        col = index.column()

        item: TaskItem = self._modelDomain.taskList[row]

        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            if col == self.ColumnIndex:
                return QVariant(str(row + 1).zfill(4) + " id=" + str(item.item_id))
            elif col == self.ColumnProject:
                if not item.item_projectId:
                    return QVariant("ERROR")
                return QVariant(self._modelDomain.dicts[const.DICT_PROJECT].getData(item.item_projectId))
            elif col == self.ColumnInitiator:
                if not item.item_initiatorId:
                    return QVariant("ERROR")
                return QVariant(self._modelDomain.dicts[const.DICT_INITIATOR].getData(item.item_initiatorId))
            elif col == self.ColumnDescription:
                return QVariant(item.item_description)
            elif col == self.ColumnUser:
                return QVariant(self._modelDomain.dicts[const.DICT_USER].getData(item.item_userId))
            elif col == self.ColumnPercent:
                return QVariant(str(item.item_percent) + "%")
            elif col == self.ColumnDateBegin:
                return QVariant(str(item.item_dateBegin))    # TODO: check dates for nulls
            elif col == self.ColumnDateChange:
                return QVariant(str(item.item_dateChange))
            elif col == self.ColumnDateEnd:
                return QVariant(str(item.item_dateEnd))
            elif col == self.ColumnDifficulty:
                return QVariant(str(item.item_difficulty) + "/10")
            # elif col == self.ColumnActive:
            #     return QVariant(str((2 - item.item_active) * 2))   # TODO: rework active column: 0 = no, 2 = yes
            elif col == self.ColumnPriority:
                if not item.item_priorityId:
                    return QVariant("ERROR")
                return QVariant(self._modelDomain.dicts[const.DICT_PRIORITY].getData(item.item_priorityId))

            return QVariant()

        elif role == Qt.CheckStateRole:
            if col == self.ColumnActive:
                return QVariant((2 - item.item_active) * 2)

        elif role == Qt.BackgroundRole:
            if item.item_percent == 100:
                return QVariant(QBrush(QColor(const.COLOR_PERCENT_100)))
            # TODO: make added task highlight
            elif col == self.ColumnDescription:
                if item.item_strict == 1:
                    return QVariant(QBrush(QColor(const.COLOR_STRICT_DATE)))
            elif col == self.ColumnPriority:
                if item.item_priorityId == 1:
                    return QVariant(QBrush(QColor(const.COLOR_PRIORITY_HIGH)))
                if item.item_priorityId == 2:
                    return QVariant(QBrush(QColor(const.COLOR_PRIORITY_MEDIUM)))
                if item.item_priorityId == 3:
                    return QVariant(QBrush(QColor(const.COLOR_PRIORITY_LOW)))
            elif col == self.ColumnDateEnd:
                if not item.item_dateEnd:
                    return QVariant()
                days = (item.item_dateEnd - datetime.date.today()).days
                if days <= 0:
                    return QVariant(QBrush(QColor(const.COLOR_DEADLINE_HIGH)))
                elif days in range(1, 8):
                    return QVariant(QBrush(QColor(const.COLOR_DEADLINE_MEDIUM)))
                elif days > 7:
                    return QVariant(QBrush(QColor(const.COLOR_DEADLINE_LOW)))
                # print(days)
                # if item.item_dateEnd - datetime.date.today() ==

        #     retcolor = Qt.white;
        #
        #     if item.item_status == 1:
        #         retcolor = const.COLOR_PAYMENT_FINISHED
        #
        #     if col == self.ColumnStatus:
        #         if item.item_status == 2:
        #             retcolor = const.COLOR_PAYMENT_PENDING
        #     if col == self.ColumnPriority:
        #         if item.item_status != 1:
        #             if item.item_priority == 2:  # 3 4
        #                 retcolor = const.COLOR_PRIORITY_LOW
        #             elif item.item_priority == 3:
        #                 retcolor = const.COLOR_PRIORITY_MEDIUM
        #             elif item.item_priority == 4:
        #                 retcolor = const.COLOR_PRIORITY_HIGH
        #     if col == self.ColumnShipmentStatus:
        #         if item.item_shipment_status == 2:
        #             retcolor = const.COLOR_ARRIVAL_PENDING
        #         if item.item_shipment_status == 3:
        #             retcolor = const.COLOR_ARRIVAL_PARTIAL
        #         if item.item_shipment_status == 4:
        #             retcolor = const.COLOR_ARRIVAL_RECLAIM
        #     return QVariant(QBrush(QColor(retcolor)))

        elif role == const.RoleNodeId:
            return QVariant(item.item_id)

        # elif role == const.RoleClient:
        #     return QVariant(item.item_clientRef)

        return QVariant()

    def flags(self, index: QModelIndex):
        f = super(TaskModel, self).flags(index)
        if index.column() == self.ColumnActive:
            f = f | Qt.ItemIsUserCheckable
        return f

    # def addRow(self, newId: int):
    #     self.beginInsertRows(QModelIndex(), self.rootNode.childCount(), self.rootNode.childCount())
    #     self.rootNode.appendChild(TreeNode(newId, self.rootNode))
    #     self.endInsertRows()
    #
    # @pyqtSlot(int)
    # def onContractAdded(self, conId: int):
    #     # TODO: if performance issues -- don't rebuild the whole tree, just add inserted item
    #     print("contract added:", conId)
    #     self.addRow(conId)
    #     # self.initModel()
    #
    # @pyqtSlot(int)
    # def onContractUpdated(self, conId: int):
    #     print("contract updated:", conId)
    #     del self.cache[conId]
    #
    # @pyqtSlot(int)
    # def onContractRemoved(self, conId: int):
    #     print("contract removed:", conId, "row:")
    #     del self.cache[conId]
    #     row = self.rootNode.findChild(conId)
    #     self.beginRemoveRows(QModelIndex(), row, row)
    #     self.rootNode.childNodes.pop(row)
    #     self.endRemoveRows()
    #
    # # @property
    # # def treeType(self):
    # #     return self._treeType
    # #
    # # @treeType.setter
    # # def treeType(self, treetype: int):
    # #     self._treeType = treetype
    # #     self.initModel()
    #
    # # @pyqtSlot(int, int)
    # # def itemsInserted(self, first: int, last: int):
    # #     self.beginInsertRows(QModelIndex(), first, last)
    # #     # print("table model slot:", first, last)
    # #     self.endInsertRows()
    # #
    # # @pyqtSlot(int, int)
    # # def itemsRemoved(self, first: int, last: int):
    # #     self.beginRemoveRows(QModelIndex(), first, last)
    # #     # print("table model slot:", first, last)
    # #     self.endRemoveRows()
