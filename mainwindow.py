from PyQt5 import uic
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox, QTableView, qApp
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QEvent

import const
# from contractsearchproxymodel import ContractSearchProxyModel
from domainmodel import DomainModel
from mysqlengine import MysqlEngine
from persistencefacade import PersistenceFacade
from taskitem import TaskItem
from taskmodel import TaskModel
from uifacade import UiFacade


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

        # facades
        self._persistenceFacade = PersistenceFacade(parent=self, persistenceEngine=self._persistenceEngine)
        # self._uiFacade = UiFacade(parent=self, reportManager=self._reportManager)
        self._uiFacade = UiFacade(parent=self)

        # models
        # domain
        self._modelDomain = DomainModel(parent=self, persistenceFacade=self._persistenceFacade)

        # task table + search proxy
        self._modelTaskTable = TaskModel(parent=self, domainModel=self._modelDomain)
        self._modelSearchProxy = QSortFilterProxyModel(parent=self)
        self._modelSearchProxy.setSourceModel(self._modelTaskTable)

        # connect ui facade to models
        # self._uiFacade.setDomainModel(self._modelDomain)

        # actions
        self.actRefresh = QAction("Обновить", self)
        self.actContractAdd = QAction("Добавить поставку", self)
        self.actContractEdit = QAction("Изменить поставку", self)
        self.actContractDelete = QAction("Удалить поставку", self)
        self.actCatalogOpen = QAction("Открыть каталог приборов", self)

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

        # # setup filter widgets
        # self.ui.comboClientFilter.setModel(self._modelDomain.dicts[const.DICT_CLIENT])

        # create actions
        self.initActions()

        # # setup ui widget signals
        # # buttons
        # self.ui.btnContractAdd.clicked.connect(self.onBtnContractAddClicked)
        # self.ui.btnContractEdit.clicked.connect(self.onBtnContractEditClicked)
        # self.ui.btnContractDelete.clicked.connect(self.onBtnContractDeleteClicked)
        # self.ui.btnCatalogOpen.clicked.connect(self.onBtnCatalogOpenClicked)
        #
        # # tree and selection
        # # self.ui.treeDeviceList.selectionModel().currentChanged.connect(self.onCurrentTreeItemChanged)
        # self.ui.treeContract.doubleClicked.connect(self.onTreeContractDoubleClicked)
        #
        # # search widgets
        # self.ui.comboClientFilter.currentIndexChanged.connect(self.setSearchFilter)
        # self.ui.editSearchFilter.textChanged.connect(self.setSearchFilter)

        # UI modifications
        # self.ui.btnDictEditor.setVisible(False)
        # self.setSearchFilter()

    def initActions(self):
        self.actRefresh.setShortcut("Ctrl+R")
        self.actRefresh.setStatusTip("Обновить данные")
        self.actRefresh.triggered.connect(self.procActRefresh)

        self.actContractAdd.setStatusTip("Добавить поставку")
        self.actContractAdd.triggered.connect(self.procActContractAdd)

        self.actContractEdit.setStatusTip("Изменить поставку")
        self.actContractEdit.triggered.connect(self.procActContractEdit)

        self.actContractDelete.setStatusTip("Удалить поставку")
        self.actContractDelete.triggered.connect(self.procActContractDelete)

        self.actCatalogOpen.setStatusTip("Открыть каталог приборов")
        self.actCatalogOpen.triggered.connect(self.procActCatalogOpen)

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
        self.ui.tableTask.setColumnWidth(3, tdwidth * 0.42)
        self.ui.tableTask.setColumnWidth(4, tdwidth * 0.08)
        self.ui.tableTask.setColumnWidth(5, tdwidth * 0.03)
        self.ui.tableTask.setColumnWidth(6, tdwidth * 0.06)
        self.ui.tableTask.setColumnWidth(7, tdwidth * 0.06)
        self.ui.tableTask.setColumnWidth(8, tdwidth * 0.06)
        self.ui.tableTask.setColumnWidth(9, tdwidth * 0.03)
        self.ui.tableTask.setColumnWidth(10, tdwidth * 0.02)
        self.ui.tableTask.setColumnWidth(11, tdwidth * 0.03)

    # ui events
    def onBtnContractAddClicked(self):
        self.actContractAdd.trigger()

    def onBtnContractEditClicked(self):
        self.actContractEdit.trigger()

    def onBtnContractDeleteClicked(self):
        self.actContractDelete.trigger()

    def onBtnCatalogOpenClicked(self):
        self.actCatalogOpen.trigger()

    # def onCurrentTreeItemChanged(self, cur: QModelIndex, prev: QModelIndex):
    #     sourceIndex = self._modelSearchProxy.mapToSource(cur)
    #     self.updateItemInfo(sourceIndex)

    def onTreeContractDoubleClicked(self, index):
        # if index.column() != 0:
        self.actContractEdit.trigger()

    def setSearchFilter(self, dummy=0):
        self._modelSearchProxy.filterString = self.ui.editSearchFilter.text()
        self._modelSearchProxy.filterClient = self.ui.comboClientFilter.currentData(const.RoleNodeId)

        self._modelSearchProxy.invalidate()
        # self.ui.treeDeviceList.setColumnHidden(5, True)

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

    def procActContractAdd(self):
        self._uiFacade.requestContractAdd()

    def procActContractEdit(self):
        if not self.ui.treeContract.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка!", "Выберите запись о контракте для редактирования.")
            return False

        selectedIndex = self.ui.treeContract.selectionModel().selectedIndexes()[0]
        self._uiFacade.requestContractEdit(self._modelSearchProxy.mapToSource(selectedIndex))

    def procActContractDelete(self):
        if not self.ui.treeContract.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка!", "Выберите запись о контракте для удаления.")
            return False

        selectedIndex = self.ui.treeContract.selectionModel().selectedIndexes()[0]
        self._uiFacade.requestContractDelete(self._modelSearchProxy.mapToSource(selectedIndex))

    def procActCatalogOpen(self):
        self._uiFacade.requestCatalogOpen()
