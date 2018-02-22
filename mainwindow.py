import datetime

from PyQt5 import uic
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox, QTableView, qApp
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QEvent, QDate, QModelIndex

import const
# from contractsearchproxymodel import ContractSearchProxyModel
from checkablecombo import CheckableComboBox
from domainmodel import DomainModel
from mysqlengine import MysqlEngine
from persistencefacade import PersistenceFacade
from taskitem import TaskItem
from taskmodel import TaskModel
from tasksearchproxymodel import TaskSearchProxyModel
from uifacade import UiFacade

# TODO: search controls text, dateEnd, initiator, show active, datebegin, user, strictdeadline, project,
# important, priority, percent

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self._isUserIsResizing = False

        # create instance variables
        # ui
        self.ui = uic.loadUi("mainwindow.ui", self)

        # report manager
        # self._reportManager = ReportManager(parent=self)

        # report engines
        # self._xlsxEngine = XlsxEngine(parent=self)
        # self._reportManager.setEngine(self._xlsxEngine)
        # self._printEngine = PrintEngine(parent=self)
        # self._reportManager.setEngine(self._printEngine)

        # persistence engine
        self._persistenceEngine = MysqlEngine(parent=self, dbItemClass=TaskItem)

        # persistence facade
        self._persistenceFacade = PersistenceFacade(parent=self, persistenceEngine=self._persistenceEngine)

        # domain model
        self._modelDomain = DomainModel(parent=self, persistenceFacade=self._persistenceFacade)

        # connect ui facade to models
        # self._uiFacade = UiFacade(parent=self, reportManager=self._reportManager)
        self._uiFacade = UiFacade(parent=self, domainModel=self._modelDomain)

        # main window models
        self._modelTaskTable = TaskModel(parent=self, domainModel=self._modelDomain)
        self._modelSearchProxy = TaskSearchProxyModel(parent=self)
        self._modelSearchProxy.setSourceModel(self._modelTaskTable)

        # actions
        self.actRefresh = QAction("Обновить", self)
        self.actTaskAdd = QAction("Добавить поставку", self)
        self.actTaskEdit = QAction("Изменить поставку", self)
        self.actTaskDelete = QAction("Удалить поставку", self)

        # try:
        qApp.installEventFilter(self)
        # except Exception as ex:
        #     print(ex)

    def initApp(self):
        # init instances
        # engines
        self._persistenceEngine.initEngine()

        # facades
        self._persistenceFacade.initFacade()
        self._uiFacade.initFacade()

        # models
        self._modelDomain.initModel()
        # self._modelContractTree.initModel()

        # init UI
        # main table
        self.ui.tableTask: QTableView
        self.ui.tableTask.setModel(self._modelSearchProxy)

        # setup search filter widgets
        self.ui.comboUser.setHidden(True)
        self.ui.comboUser = CheckableComboBox(parent=self.ui.grpSearchFilters)
        self.ui.hlayUser.addWidget(self.ui.comboUser)

        self.ui.comboInit.setHidden(True)
        self.ui.comboInit = CheckableComboBox(parent=self.ui.grpSearchFilters)
        self.ui.hlayInit.addWidget(self.ui.comboInit)

        self.ui.comboProject.setHidden(True)
        self.ui.comboProject = CheckableComboBox(parent=self.ui.grpSearchFilters)
        self.ui.hlayProject.addWidget(self.ui.comboProject)

        self.ui.comboUser.setModel(self._modelDomain.dicts[const.DICT_USER])
        self.ui.comboInit.setModel(self._modelDomain.dicts[const.DICT_INITIATOR])
        self.ui.comboProject.setModel(self._modelDomain.dicts[const.DICT_PROJECT])

        # create actions
        self.initActions()

        # setup ui widget signals
        self.createSignals()

        # # tree and selection
        # # self.ui.treeDeviceList.selectionModel().currentChanged.connect(self.onCurrentTreeItemChanged)
        # self.ui.treeContract.doubleClicked.connect(self.onTreeContractDoubleClicked)
        #
        # # search widgets
        # self.ui.comboClientFilter.currentIndexChanged.connect(self.setSearchFilter)
        # self.ui.editSearchFilter.textChanged.connect(self.setSearchFilter)
        # self.setSearchFilter()

        # UI modifications
        self.initUiWidgets()

    def createSignals(self):
        # edit buttons
        self.ui.btnTaskAdd.clicked.connect(self.onBtnTaskAddClicked)
        self.ui.btnTaskEdit.clicked.connect(self.onBtnTaskEditClicked)
        self.ui.btnTaskDelete.clicked.connect(self.onBtnTaskDeleteClicked)

        # search widgets
        # search edit
        self.ui.editSearchFilter.textChanged.connect(self.onEditSearchFilterTextChanged)

        # date checkboxes
        self.ui.chkDateBeginFrom.toggled.connect(self.onChkDateBeginFromToggled)
        self.ui.chkDateBeginTo.toggled.connect(self.onChkDateBeginToToggled)
        self.ui.chkDateEndFrom.toggled.connect(self.onChkDateEndFromToggled)
        self.ui.chkDateEndTo.toggled.connect(self.onChkDateEndToToggled)

        # date edits
        self.ui.dateBeginFrom.dateChanged.connect(self.onDateBeginFromChanged)
        self.ui.dateBeginTo.dateChanged.connect(self.onDateBeginToChanged)
        self.ui.dateEndFrom.dateChanged.connect(self.onDateEndFromChanged)
        self.ui.dateEndTo.dateChanged.connect(self.onDateEndToChanged)

        # comboboxes
        self.ui.comboUser.popupClosed.connect(self.onComboUserPopupClosed)
        self.ui.comboInit.popupClosed.connect(self.onComboInitPopupClosed)
        self.ui.comboProject.popupClosed.connect(self.onComboProjectPopupClosed)

        # TODO: update filter on checkbox toggle?
        # self.ui.comboUser.setModel(self._modelDomain.dicts[const.DICT_USER])
        # self.ui.comboInit.setModel(self._modelDomain.dicts[const.DICT_INITIATOR])
        # self.ui.comboProject.setModel(self._modelDomain.dicts[const.DICT_PROJECT])

        # additional checkboxes
        self.ui.chkActive.toggled.connect(self.onChkActiveToggled)
        self.ui.chkNotActive.toggled.connect(self.onChkNotActiveToggled)
        self.ui.chkStrict.toggled.connect(self.onChkStrictToggled)
        self.ui.chkHundredPercent.toggled.connect(self.onChkHundredPercentToggled)

        # table signals
        self.ui.tableTask.doubleClicked.connect(self.onTableTaskDoubleClicked)
        self.ui.tableTask.selectionModel().currentChanged.connect(self.onTableTaskCurrentChanged)

    def initActions(self):
        self.actRefresh.setShortcut("Ctrl+R")
        self.actRefresh.setStatusTip("Обновить данные")
        self.actRefresh.triggered.connect(self.procActRefresh)

        self.actTaskAdd.setStatusTip("Добавить поставку")
        self.actTaskAdd.triggered.connect(self.procActTaskAdd)

        self.actTaskEdit.setStatusTip("Изменить поставку")
        self.actTaskEdit.triggered.connect(self.procActTaskEdit)

        self.actTaskDelete.setStatusTip("Удалить поставку")
        self.actTaskDelete.triggered.connect(self.procActTaskDelete)

    def initUiWidgets(self):
        self.ui.grpSearchFilters.setVisible(False)

        self.ui.btnSearchFilters.setLayoutDirection(Qt.RightToLeft)

        self.ui.chkDateBeginFrom.setLayoutDirection(Qt.RightToLeft)
        self.ui.chkDateBeginTo.setLayoutDirection(Qt.RightToLeft)
        self.ui.chkDateEndFrom.setLayoutDirection(Qt.RightToLeft)
        self.ui.chkDateEndTo.setLayoutDirection(Qt.RightToLeft)

        self.ui.dateBeginFrom.setDate(QDate().currentDate())
        self.ui.dateBeginTo.setDate(QDate().currentDate())
        self.ui.dateEndFrom.setDate(QDate().currentDate())
        self.ui.dateEndTo.setDate(QDate().currentDate())

        self.setSearchFilter()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton and self._isUserIsResizing:
                self.ui.tableTask.resizeRowsToContents()
                self._isUserIsResizing = False

        return super(MainWindow, self).eventFilter(obj, event)

    def refreshView(self):
        tdwidth = self.geometry().width() - 50
        self.ui.tableTask.setColumnWidth(0, tdwidth * 0.04)
        self.ui.tableTask.setColumnWidth(1, tdwidth * 0.10)
        self.ui.tableTask.setColumnWidth(2, tdwidth * 0.07)
        self.ui.tableTask.setColumnWidth(3, tdwidth * 0.45)  # + 0.04
        self.ui.tableTask.setColumnWidth(4, tdwidth * 0.08)
        self.ui.tableTask.setColumnWidth(5, tdwidth * 0.03)
        self.ui.tableTask.setColumnWidth(6, tdwidth * 0.06)
        self.ui.tableTask.setColumnWidth(7, tdwidth * 0.06)
        self.ui.tableTask.setColumnWidth(8, tdwidth * 0.06)
        # self.ui.tableTask.setColumnWidth(9, tdwidth * 0.03)  # - 0.03
        self.ui.tableTask.setColumnWidth(10, tdwidth * 0.01)  # - 0.01
        self.ui.tableTask.setColumnWidth(11, tdwidth * 0.03)
        self.ui.tableTask.setColumnHidden(9, True)

    def setSearchFilter(self):
        # TODO bind to comboboxes
        self._modelSearchProxy.filterUser = self.ui.comboUser.currentData(const.RoleFilterData)
        self._modelSearchProxy.filterInit = self.ui.comboInit.currentData(const.RoleFilterData)
        self._modelSearchProxy.filterProject = self.ui.comboProject.currentData(const.RoleFilterData)

        self._modelSearchProxy.filterDateBeginFrom = datetime.datetime.strptime(self.ui.dateBeginFrom.date().toString(
            Qt.ISODate), "%Y-%m-%d").date() if self.ui.chkDateBeginFrom.isChecked() else None
        self._modelSearchProxy.filterDateBeginTo = datetime.datetime.strptime(self.ui.dateBeginTo.date().toString(
            Qt.ISODate), "%Y-%m-%d").date() if self.ui.chkDateBeginTo.isChecked() else None
        self._modelSearchProxy.filterDateEndFrom = datetime.datetime.strptime(self.ui.dateEndFrom.date().toString(
            Qt.ISODate), "%Y-%m-%d").date() if self.ui.chkDateEndFrom.isChecked() else None
        self._modelSearchProxy.filterDateEndTo = datetime.datetime.strptime(self.ui.dateEndTo.date().toString(
            Qt.ISODate), "%Y-%m-%d").date() if self.ui.chkDateEndTo.isChecked() else None

        self._modelSearchProxy.filterActive = self.ui.chkActive.isChecked()
        self._modelSearchProxy.filterNotActive = self.ui.chkNotActive.isChecked()
        self._modelSearchProxy.filterStrictDate = self.ui.chkStrict.isChecked()
        self._modelSearchProxy.filterHundredPercent = self.ui.chkHundredPercent.isChecked()
        self._modelSearchProxy.filterString = self.ui.editSearchFilter.text()

        self._modelSearchProxy.invalidate()
        # self.ui.treeDeviceList.setColumnHidden(5, True)

    # ui events
    def onBtnTaskAddClicked(self):
        self.actTaskAdd.trigger()

    def onBtnTaskEditClicked(self):
        self.actTaskEdit.trigger()

    def onBtnTaskDeleteClicked(self):
        self.actTaskDelete.trigger()

    def onChkDateBeginFromToggled(self, checked):
        self.setSearchFilter()

    def onChkDateBeginToToggled(self, checked):
        self.setSearchFilter()

    def onChkDateEndFromToggled(self, checked):
        self.setSearchFilter()

    def onChkDateEndToToggled(self, checked):
        self.setSearchFilter()

    def onDateBeginFromChanged(self, date):
        self.setSearchFilter()

    def onDateBeginToChanged(self, date):
        self.setSearchFilter()

    def onDateEndFromChanged(self, date):
        self.setSearchFilter()

    def onDateEndToChanged(self, date):
        self.setSearchFilter()

    def onComboUserPopupClosed(self):
        self.setSearchFilter()

    def onComboInitPopupClosed(self):
        self.setSearchFilter()

    def onComboProjectPopupClosed(self):
        self.setSearchFilter()

    def onChkActiveToggled(self, checked):
        self.setSearchFilter()

    def onChkNotActiveToggled(self, checked):
        self.setSearchFilter()

    def onChkStrictToggled(self, checked):
        self.setSearchFilter()

    def onChkHundredPercentToggled(self, checked):
        self.setSearchFilter()

    def onEditSearchFilterTextChanged(self, text):
        self.setSearchFilter()

    def onTableTaskDoubleClicked(self, index):
        self.actTaskEdit.trigger()

    def onTableTaskCurrentChanged(self, curr: QModelIndex, prev: QModelIndex):
        self.ui.textNote.setPlainText(curr.data(const.RoleNote))

    # misc events
    def resizeEvent(self, event: QResizeEvent):
        self._isUserIsResizing = True
        self.actRefresh.trigger()

    # def closeEvent(self, *args, **kwargs):
    #     self._uiFacade.requestExit()
    #     super(MainWindow, self).closeEvent(*args, **kwargs)

    # action processing
    # send user commands to the ui facade: (command, parameters (indexes, etc.))
    def procActRefresh(self):
        # print("act refresh triggered")
        # self._uiFacade.requestRefresh()
        self.refreshView()

    def procActTaskAdd(self):
        self._uiFacade.requestTaskAdd()

    def procActTaskEdit(self):
        if not self.ui.tableTask.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка!", "Выберите запись о задаче для редактирования.")
            return False

        selectedIndex = self.ui.tableTask.selectionModel().selectedIndexes()[0]
        self._uiFacade.requestTaskEdit(self._modelSearchProxy.mapToSource(selectedIndex))

    def procActTaskDelete(self):
        print("task delete")
        # if not self.ui.treeContract.selectionModel().hasSelection():
        #     QMessageBox.information(self, "Ошибка!", "Выберите запись о контракте для удаления.")
        #     return False
        #
        # selectedIndex = self.ui.treeContract.selectionModel().selectedIndexes()[0]
        # self._uiFacade.requestContractDelete(self._modelSearchProxy.mapToSource(selectedIndex))

