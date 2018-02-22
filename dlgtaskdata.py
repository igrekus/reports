from funcy import walk
import const
import datetime
from copy import deepcopy
# from comboboxdelegate import ComboBoxDelegate
from mapmodel import MapModel
from taskitem import TaskItem
# from dateeditdelegate import DateEditDelegate
# from productlistmodel import ProductListModel
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableView
from PyQt5.QtCore import Qt, QDate, QModelIndex
# from spinboxdelegate import SpinBoxDelegate


class DlgTaskData(QDialog):

    def __init__(self, parent=None, domainModel=None, uifacade=None, item=None):
        super(DlgTaskData, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("dlgtaskdata.ui", self)

        # init instances
        self._domainModel = domainModel
        self._uiFacade = uifacade

        # data members
        self._currentItem: TaskItem = item
        self.newItem = None
        self._productList = list()

        self.initDialog()

    def initDialog(self):
        print("init taskdata dialog")
        # init widgets
        self.ui.comboUser.setModel(self._domainModel.dicts[const.DICT_USER])
        self.ui.comboProject.setModel(self._domainModel.dicts[const.DICT_PROJECT])
        self.ui.comboInit.setModel(self._domainModel.dicts[const.DICT_INITIATOR])
        self.ui.comboPriority.setModel(self._domainModel.dicts[const.DICT_PRIORITY])

        walk(lambda model: model.makeUncheckable(), self._domainModel.dicts.values())

        # for k, v in self._domainModel.dicts.items():
        #     v.itemsCheckable = False
        # self.ui.tableProduct.setModel(self._productModel)
        # self._productModel.initModel(self._productList)

        # setup signals
        self.ui.btnOk.clicked.connect(self.onBtnOkClicked)
        self.ui.btnUserAdd.clicked.connect(self.onBtnUserAddClicked)
        self.ui.btnUserEdit.clicked.connect(self.onBtnUserEditClicked)
        self.ui.btnProjectAdd.clicked.connect(self.onBtnProjectAddClicked)
        self.ui.btnProjectEdit.clicked.connect(self.onBtnProjectEditClicked)
        self.ui.btnInitAdd.clicked.connect(self.onBtnInitAddClicked)
        self.ui.btnInitEdit.clicked.connect(self.onBtnInitEditClicked)

        # set widget data
        if self._currentItem is None:
            self.resetWidgets()
        else:
            self.updateWidgets()

    def updateWidgets(self):

        def formatDate(date: datetime.date):
            if isinstance(date, datetime.date):
                return QDate().fromString(date.isoformat(), "yyyy-MM-dd")
            else:
                return QDate().fromString("2000-01-01", "yyyy-MM-dd")

        self.ui.comboUser.setCurrentText(self._domainModel.dicts[const.DICT_USER].getData(self._currentItem.item_userId))
        self.ui.comboProject.setCurrentText(self._domainModel.dicts[const.DICT_PROJECT].getData(self._currentItem.item_projectId))
        self.ui.comboInit.setCurrentText(self._domainModel.dicts[const.DICT_INITIATOR].getData(self._currentItem.item_initiatorId))
        self.ui.spinPercent.setValue(self._currentItem.item_percent)
        self.ui.dateBegin.setDate(formatDate(self._currentItem.item_dateBegin))
        self.ui.dateChange.setDate(formatDate(self._currentItem.item_dateChange))
        self.ui.dateEnd.setDate(formatDate(self._currentItem.item_dateEnd))
        self.ui.comboPriority.setCurrentText(self._domainModel.dicts[const.DICT_PRIORITY].getData(self._currentItem.item_priorityId))
        self.ui.spinDifficulty.setValue(self._currentItem.item_difficulty)
        self.ui.chkImportant.setChecked(self._currentItem.item_important)
        self.ui.chkUrgent.setChecked(self._currentItem.item_urgent)
        self.ui.chkStrict.setChecked(self._currentItem.item_strict)
        self.ui.chkActive.setChecked(self._currentItem.item_active)
        self.ui.editDescript.setText(self._currentItem.item_description)
        self.ui.textNote.setPlainText(self._currentItem.item_note)

    def resetWidgets(self):
        currentDate = QDate().currentDate()
        self.ui.comboUser.setCurrentIndex(0)
        self.ui.comboProject.setCurrentIndex(0)
        self.ui.comboInit.setCurrentIndex(0)
        self.ui.spinPercent.setValue(0)
        self.ui.dateBegin.setDate(currentDate)
        self.ui.dateChange.setDate(currentDate)
        self.ui.dateEnd.setDate(currentDate)
        self.ui.comboPriority.setCurrentIndex(0)
        self.ui.spinDifficulty.setValue(1)
        self.ui.chkImportant.setChecked(False)
        self.ui.chkUrgent.setChecked(False)
        self.ui.chkStrict.setChecked(False)
        self.ui.chkActive.setChecked(True)
        self.ui.editDescript.setText("")
        self.ui.textNote.setPlainText("")

    def verifyInputData(self):

        if not self.ui.editIndex.text():
            QMessageBox.information(self, "Ошибка", "Введите индекс поставки.")
            return False

        if self.ui.comboClient.currentData(const.RoleNodeId) == 0:
            QMessageBox.information(self, "Ошибка", "Выберите клиента.")
            return False

        if not self.ui.editProject.text():
            QMessageBox.information(self, "Ошибка", "Введите код работы.")
            return False

        if not self.ui.editRequestN.text():
            QMessageBox.information(self, "Ошибка", "Введите номер запроса.")
            return False

        if not self.ui.editDogozN.text():
            QMessageBox.information(self, "Ошибка", "Введите номер ДОГОЗ.")
            return False

        if self.ui.spinSum.value() <= 0:
            QMessageBox.information(self, "Ошибка", "Введите сумму.")
            return False

        if self.ui.spinShipPeriod.value() <= 0:
            QMessageBox.information(self, "Ошибка", "Введите срок поставки.")
            return False

        if self._productModel.rowCount() == 0:
            QMessageBox.information(self, "Ошибка", "Добавьте товары в список.")
            return False
        else:
            ids = self._productModel.getProductIdList()
            if len(ids) > len(set(ids)):
                QMessageBox.information(self, "Ошибка", "Товары в списке не должны повторяться.")
                return False

            # TODO: move to the model
            for i in range(self._productModel.rowCount()):
                if self._productModel.data(self._productModel.index(i, 0, QModelIndex()), Qt.DisplayRole).value() == "Все":
                    # TODO: fix crash on message dismissal
                    QMessageBox.information(self, "Ошибка", "Выберите товар из списка.")
                    return False

            # TODO: reject dupes in product list
        return True

    def collectData(self):

        # def getDate(strdate):
        #     return str

        id_ = None
        if self._currentItem is not None:
            id_ = self._currentItem.item_id

        completed = False
        if self._currentItem is not None:
            completed = self._currentItem.item_completed

        # TODO: change date formats
        self.newItem = ContractItem(id_=id_,
                                    index=self.ui.editIndex.text(),
                                    clientRef=self.ui.comboClient.currentData(const.RoleNodeId),
                                    projCode=self.ui.editProject.text(),
                                    requestN=self.ui.editRequestN.text(),
                                    requestDate=datetime.datetime.strptime(
                                        self.ui.dateRequest.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    dogozName=self.ui.dateDogoz.text(),
                                    dogozDate=datetime.datetime.strptime(
                                        self.ui.dateDogoz.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    deviceRequestN=self.ui.editDevRequestN.text(),
                                    deviceRequestCode=self.ui.editDevRequestCode.text(),
                                    contractN=self.ui.editContractN.text(),
                                    contractDate=datetime.datetime.strptime(
                                        self.ui.dateContract.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    specReturnDate=datetime.datetime.strptime(
                                        self.ui.dateSpecReturn.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    sum=int(self.ui.spinSum.value() * 100),
                                    billNumber=self.ui.editBillN.text(),
                                    billDate=datetime.datetime.strptime(self.ui.dateBill.date().toString("yyyy-MM-dd"),
                                                                        "%Y-%m-%d").date(),
                                    milDate=datetime.datetime.strptime(self.ui.dateMil.date().toString("yyyy-MM-dd"),
                                                                       "%Y-%m-%d").date(),
                                    addLetterDate=datetime.datetime.strptime(
                                        self.ui.dateAddLetter.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    responseDate=datetime.datetime.strptime(
                                        self.ui.dateResponse.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    paymentOrderN=self.ui.editPaymentN.text(),
                                    paymentDate=datetime.datetime.strptime(
                                        self.ui.datePayment.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    matPurchaseDate=datetime.datetime.strptime(
                                        self.ui.dateMatPurchase.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    planShipmentDate=datetime.datetime.strptime(
                                        self.ui.datePlanShip.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    shipmentPeriod=self.ui.spinShipPeriod.value(),
                                    invoiceN=self.ui.editInvoiceN.text(),
                                    invoiceDate=datetime.datetime.strptime(
                                        self.ui.dateInvoice.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    packingListN=self.ui.editPacklistN.text(),
                                    packingListDate=datetime.datetime.strptime(
                                        self.ui.datePacklist.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    shipNote=self.ui.editShipNote.text(),
                                    shipDate=datetime.datetime.strptime(self.ui.dateShip.date().toString("yyyy-MM-dd"),
                                                                        "%Y-%m-%d").date(),
                                    completed=completed,
                                    contacts=self.ui.textContact.toPlainText(),
                                    manufPlanDate=datetime.datetime.strptime(
                                        self.ui.dateManufPlan.date().toString("yyyy-MM-dd"), "%Y-%m-%d"))

        self._productList = self._productModel.getProductList()

    def getData(self):
        return self.newItem, self._productList

    def onBtnOkClicked(self):
        print("ok")
        # if not self.verifyInputData():
        #     return
        # self.collectData()
        # self.accept()

    def onBtnUserAddClicked(self):
        print("on_btnUserAdd_clicked")

    def onBtnUserEditClicked(self):
        print("on_btnUserEdit_clicked")

    def onBtnProjectAddClicked(self):
        print("on_btnProjectAdd_clicked")

    def onBtnProjectEditClicked(self):
        print("on_btnProjectEdit_clicked")

    def onBtnInitAddClicked(self):
        print("on_btnInitAdd_clicked")

    def onBtnInitEditClicked(self):
        print("on_btnInitEdit_clicked")

    def done(self, code):
        walk(lambda model: model.makeCheckable(), self._domainModel.dicts.values())
        super(DlgTaskData, self).done(code)

