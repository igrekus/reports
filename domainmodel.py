import const
from taskitem import TaskItem
from mapmodel import MapModel
from PyQt5.QtCore import QObject, pyqtSignal


class DomainModel(QObject):

    contractAdded = pyqtSignal(int)
    contractUpdated = pyqtSignal(int)
    contractRemoved = pyqtSignal(int)

    productAdded = pyqtSignal(int)
    productUpdated = pyqtSignal(int)
    productRemoved = pyqtSignal(int)

    def __init__(self, parent=None, persistenceFacade=None):
        super(DomainModel, self).__init__(parent)

        self._persistenceFacade = persistenceFacade

        self.taskList = list()
        self.dicts = dict()

        self.dictNameList = [const.DICT_PROJECT,
                             const.DICT_INITIATOR,
                             const.DICT_PRIORITY,
                             const.DICT_USER]

    def buildMapModel(self, name: str):
        self.dicts[name] = MapModel(self, self._persistenceFacade.getDict(name))
        self.dicts[name].addItemAtPosition(0, 0, "Все")

    def initModel(self):
        print("init domain model")
        self.taskList = self._persistenceFacade.getTaskList(userId=0)

        # FIXME: make uniform dict
        for name in self.dictNameList:
            self.buildMapModel(name)

    # def getItemById(self, id_):
    #     return self.contractList[id_]
    #
    # def addContractItem(self, item: TaskItem, products: list):
    #     print("domain model add contract item call:", item)
    #     print("products:", products)
    #
    #     newItem, newDetaiList = self._persistenceFacade.insertContractItem(item, products)
    #
    #     self.contractList[newItem.item_id] = newItem
    #     self.contractDetailList[newItem.item_id] = newDetaiList
    #
    #     self.contractAdded.emit(newItem.item_id)
    #
    # def updateContractItem(self, item: TaskItem, products: list, updates: list):
    #     print("domain model update contract item call:", item)
    #     print("products", products)
    #     print("updates", updates)
    #
    #     self.contractList[item.item_id] = item
    #     self.contractDetailList[item.item_id] = products
    #
    #     self._persistenceFacade.updateContractItem(item, updates)
    #
    #     self.contractUpdated.emit(item.item_id)
    #
    # def deleteContractItem(self, item: TaskItem):
    #     print("domain model delete contract item call:", item)
    #     print("deleting bound products")
    #
    #     self.contractList.pop(item.item_id, 0)
    #     self.contractDetailList.pop(item.item_id, 0)
    #
    #     self._persistenceFacade.deleteContractItem(item)
    #
    #     self.contractRemoved.emit(item.item_id)
    #
    # # dictionary methods
    #
    # def addDictRecord(self, name, data):
    #     print("domain model add dict record:", name, data)
    #     newId = self._persistenceFacade.addDictRecord(name, data)
    #     self.dicts[name].addItem(newId, data)
    #
    # # domain-specific methods
    #
    # def addProduct(self, name: str, price: int):
    #     print("domain model add product record: ", name, price)
    #     newId = self._persistenceFacade.addProductRecord(name, price)
    #     print("new id:", newId)
    #
    #     self.dicts[const.DICT_PRODUCT].addItem(newId, name)
    #     self.dicts[const.DICT_PRICE][newId] = price
    #
    #     self.productAdded.emit(newId)
    #
    # def updateProduct(self, id_, name: str, price: int):
    #     print("domain model update product record: ", id_, name, price)
    #     self._persistenceFacade.updateProductRecord(id_, name, price)
    #
    #     self.dicts[const.DICT_PRODUCT].updateItem(id_, name)
    #     self.dicts[const.DICT_PRICE][id_] = price
    #
    #     self.productUpdated.emit(id_)
    #
    # def removeProduct(self, id_: int):
    #     print("domain model remove product record: ", id_)
    #     # TODO: make product usage check, ask if delete product from all of the contracts, redraw the main table
    #
    #     self._persistenceFacade.removeProductRecord(id_)
    #
    #     self.dicts[const.DICT_PRODUCT].removeItem(id_)
    #     self.dicts[const.DICT_PRICE].pop(id_)
