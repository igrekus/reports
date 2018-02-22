import const
from PyQt5.QtCore import QObject, QModelIndex
from PyQt5.QtWidgets import QDialog, QMessageBox, QInputDialog, QLineEdit

from dlgtaskdata import DlgTaskData
from taskitem import TaskItem
# from dlgproductcatalog import DlgProductCatalog


class UiFacade(QObject):

    def __init__(self, parent=None, domainModel=None, reportManager=None):
        super(UiFacade, self).__init__(parent)
        self._domainModel = domainModel
        self._reportManager = reportManager

    def setDomainModel(self, domainModel=None):
        self._domainModel = domainModel

    def initFacade(self):
        print("init ui facade")

    # def findDiffBetweenProductLists(self, old: list, new: list):
    #     added = list()
    #     changed = list()
    #     deleted = list()
    #
    #     for n in new:
    #         if n in old:
    #             continue
    #         elif any(o[0] == n[0] for o in old):
    #             changed.append(n)
    #         else:
    #             added.append(n)
    #
    #     for o in old:
    #         if not any(n[0] == o[0] for n in new):
    #             deleted.append(o)
    #
    #     return added, changed, deleted

    def requestTaskAdd(self):
        print("ui facade add contract request")
        dialog = DlgTaskData(domainModel=self._domainModel, uifacade=self, item=None)  # empty dialog for a new item

        if dialog.exec() != QDialog.Accepted:
            return

        # newItem, products = dialog.getData()
        #
        # self._domainModel.addTaskItem(newItem, products)

    def requestTaskEdit(self, index: QModelIndex):
        item: TaskItem = self._domainModel.getItemByRow(index.row())

        print("ui facade edit task request", item)

        try:
            dialog = DlgTaskData(domainModel=self._domainModel, uifacade=self, item=item)

            if dialog.exec() != QDialog.Accepted:
                return
        except Exception as ex:
            print(ex)

        # updatedItem, updatedProducts = dialog.getData()
        #
        # added, changed, deleted = self.findDiffBetweenProductLists(oldProducts, updatedProducts)
        #
        # self._domainModel.updateContractItem(updatedItem, updatedProducts, (added, changed, deleted))

    # def requestContractDelete(self, index: QModelIndex):
    #     item = self._domainModel.getItemById(index.data(const.RoleNodeId))
    #     print("ui facade delete contract request", item)
    #
    #     result = QMessageBox.question(self.parent(), "Внимание!",
    #                                   "Вы хотите удалить выбранную запись?")
    #
    #     if result != QMessageBox.Yes:
    #         return
    #
    #     self._domainModel.deleteContractItem(item)
    #
    # def requestClientAdd(self, caller):
    #     print("ui facade add client request")
    #
    #     data, ok = QInputDialog.getText(caller, "Добавить нового клиента", "Введите название:", QLineEdit.Normal, "")
    #
    #     if not ok:
    #         return
    #
    #     self._domainModel.addDictRecord(const.DICT_CLIENT, data)
    #
    # def requestProductAdd(self, caller):
    #     print("ui facade add new product request")
    #
    #     data, ok = QInputDialog.getText(caller, "Добавить новый прибор", "Введите наименование:", QLineEdit.Normal, "")
    #
    #     if not ok:
    #         return
    #
    #     self._domainModel.addDictRecord(const.DICT_PRODUCT, data)
    #
    # def requestCatalogOpen(self):
    #     print("ui facade open catalog request")
    #
    #     dialog = DlgProductCatalog(domainModel=self._domainModel, uiFacade=self)
    #
    #     dialog.exec()

    # def requestExit(self, index):
    #     # TODO make settings class if needed, only current week is saved for now
    #     print("ui facade exit request...")
    #     print("saving preferences...", index)
    #     # TODO extract saving process into settings class, only send a message from UI
    #     with open("settings.ini", mode='tw') as f:
    #         f.write("week="+str(index + 1))
    #
    #     if self._domainModel.savePlanData():
    #         print("...exit request ok")
    #     else:
    #         raise RuntimeError("DB connection error")
