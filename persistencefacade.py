from collections import defaultdict
from PyQt5.QtCore import QObject
from taskitem import TaskItem


class PersistenceFacade(QObject):

    def __init__(self, parent=None, persistenceEngine=None):
        super(PersistenceFacade, self).__init__(parent)

        self._engine = persistenceEngine
        self.engineType = self._engine._engineType

    def initFacade(self):
        print("init persistence facade:", self._engine._engineType)

    def getTaskList(self, userId: int) -> list:
        return [TaskItem.fromSqlTuple(r) for r in self._engine.fetchMainData((userId, ))]

    def getContractDetailList(self):
        # TODO: make contractdetail class
        d = defaultdict(list)
        for r in self._engine.fetchContractDetailList():
            d[r[0]].append([r[1], r[2], r[3], r[4], r[5]])

        return d

    def getDict(self, name):
        return {r[0]: r[1] for r in self._engine.fetchDict(name)}

    def insertContractItem(self, item: TaskItem, products: list):
        print("persistence facade insert contract item call:", item, products)

        newContractId = self._engine.insertMainDataRecord(item.toTuple())
        newDetailIdList = self._engine.insertContractDetail(products)

        item.item_id = newContractId

        newDetailList = [[i, d[1], d[2]] for i, d in zip(newDetailIdList, products)]

        return item, newDetailList

    def updateContractItem(self, item: TaskItem, updates: list):
        print("persistence facade update contract item call:", item)
        print("products", updates)

        self._engine.updateMainDataRecord(item.toTuple())

        self.updateContractDetail(updates)

    def deleteContractItem(self, item: TaskItem):
        print("persistence facade delete contract item call:", item)
        self._engine.deleteMainDataRecord(item.toTuple())
        self._engine.deleteContractDetail([item.item_id])

    def updateContractDetail(self, updates: list):
        print("persistence facade update contract detail call:", updates)
        # TODO: prepare data for queries here
        if updates[0]:
            self._engine.insertContractDetail(updates[0])
        if updates[1]:
            self._engine.updateContractDetail(updates[1])
        if updates[2]:
            self._engine.deleteContractDetail(updates[2])

    def addDictRecord(self, name: str, data):
        print("persistence facade add dict record:", name, data)
        return self._engine.insertDictRecord(name, (data,))

    # def editDictRecord(self, dictName, data):
    #     print("persistence facade add dict record:", dictName, data)
    #     self._engine.updateDictRecord(dictName, (data[1], data[0]))
    #
    # def deleteDictRecord(self, dictName, data):
    #     print("persistence facade add dict record:", dictName, data)
    #     self._engine.deleteDictRecord(dictName, (data, ))

    def addProductRecord(self, name: str, price: int):
        print("persistence facade add product record:", name, price)
        return self._engine.insertProductRecrod((name, price, ))

    def updateProductRecord(self, id_: int, name: str, price: int):
        print("persistence facade update product record:", id_, name, price)
        self._engine.updateProductRecord((name, price, id_, ))

    def removeProductRecord(self, id_: int):
        print("persistence facade remove product record:", id_)
        self._engine.deleteProductRecord((id_, ))
