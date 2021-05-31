import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtSql
from PyQt5.QtCore import Qt, QVariant, QDate, Qt
from PyQt5.QtGui import QPdfWriter, QPagedPaintDevice, QPainter, QScreen, QPixmap
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("pumpcar.ui")[0]

db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
TABLE_WORKED_DATA = 'WORKED_DATA1'
WHERE_CONDITION = "#WhereCondition#"
LIST_COL_WORKED_DATA = ['ID', 'GDATE', 'ITEM', 'SIKAN1', 'SIKAN2',
                        'MUL', 'GUM', 'CHONG', 'CAR', 'SUGUM', 'BIGO', 'INCOM', 'NOCOM', "BLACK"]
LIST_HEADER_NAME_TAB1 = ["거래일자", "거래처", "S/T", "E/T", "타설량", "금액", "차량", "수금"]
LIST_HEADER_SIZE_TAB1 = [130, 200, 66, 66, 65, 150, 65, 65]
LIST_HEADER_NAME_TAB2 = ["data_id", "거래일자", "거래처", "시작",
                         "종료", "타설량", "금액", "차량", "수금", "비고"]
LIST_HEADER_SIZE_TAB2 = [10, 130, 130, 66, 66, 65, 100, 65, 65, 136]
LIST_HEADER_NAME_TAB3 = ["거래일자", "거래처", "시작시간",
                         "종료시간", "타설량", "금액", "총매출액", "차량", "수금", "비고"]
LIST_HEADER_SIZE_TAB3 = [130, 200, 80, 80, 65, 150, 200, 65, 65, 200]
LIST_HEADER_NAME_TAB4 = ["순번", "거래일자", "거래처", "시작",
                         "종료", "타설량", "금액", "차량", "수금", "비고"]
LIST_HEADER_SIZE_TAB4 = [60, 130, 200, 80, 80, 65, 150, 65, 65, 200]
QUERY_SELECT_TAB1 = "SELECT GDATE, ITEM, SIKAN1, SIKAN2, MUL, printf('%,d', GUM), CAR, SUGUM FROM WORKED_DATA ORDER BY GDATE DESC, SIKAN1 DESC, ID DESC LIMIT 20"
QUERY_SELECT_TAB2 = "SELECT ID, GDATE, ITEM, SIKAN1, SIKAN2, MUL, printf('%,d', GUM), CAR, SUGUM, BIGO FROM WORKED_DATA WHERE 1=1 " + \
    WHERE_CONDITION + " ORDER BY GDATE DESC, SIKAN1 DESC, ID DESC"
QUERY_UPDATE_BLACK_TAB2 = "UPDATE WORKED_DATA SET BLACK='Y' WHERE 1=1 " + WHERE_CONDITION
QUERY_DELETE_TAB2 = "DELETE FROM WORKED_DATA WHERE 1=1 " + WHERE_CONDITION
QUERY_SELECT_TAB3 = "SELECT GDATE, ITEM, SIKAN1, SIKAN2, MUL, printf('%,d', GUM), printf('%,d', SUM(GUM) OVER(ORDER BY GDATE, SIKAN1, ID)), CAR, SUGUM, BIGO FROM WORKED_DATA WHERE 1=1 " + \
    WHERE_CONDITION + " ORDER BY GDATE DESC, SIKAN1 DESC, ID DESC"
QUERY_TOTAL_TAKE_TAB3 = "SELECT COUNT(*), printf('%,d', SUM(GUM)), printf('%,d', SUM(cast(MUL as INTEGER))) FROM WORKED_DATA WHERE 1=1 " + \
    WHERE_CONDITION
QUERY_SUBTOTAL_TAKE_TAB3 = "SELECT SUGUM, printf('%,d', SUM(GUM)) FROM WORKED_DATA WHERE 1=1 " + \
    WHERE_CONDITION + " GROUP BY SUGUM"
QUERY_SELECT_TAB4 = "SELECT ID, GDATE, ITEM, SIKAN1, SIKAN2, MUL, printf('%,d', GUM), CAR, SUGUM, BIGO FROM WORKED_DATA WHERE BLACK = 'Y' ORDER BY GDATE DESC, SIKAN1 DESC, ID DESC"
QUERY_UPDATE_NOBLACK_TAB4 = "UPDATE WORKED_DATA SET BLACK='N' WHERE 1=1 " + WHERE_CONDITION


def createConnection():
    global db
    db.setDatabaseName("pumpdb.db")
    if not db.open():
        QMessageBox.critical(None, "Cannot open memory database",
                             "Unable to establish a database connection.\n\n"
                             "Click Cancel to exit.", QMessageBox.Cancel)
        return False
    query = QtSql.QSqlQuery()
    # query.exec("DROP TABLE IF EXISTS WORKED_DATA")
    # query.exec(
    #     "CREATE TABLE WORKED_DATA (ID INTEGER PRIMARY KEY NOT NULL, " + "GDATE VARCHAR(12), " + "ITEM VARCHAR(100), " + "SIKAN1 VARCHAR(6), " + "SIKAN2 VARCHAR(6), " +
    #     "MUL VARCHAR(5), " + "GUM INTEGER, " + "CAR VARCHAR(10), " +
    #     "SUGUM VARCHAR(10), " + "BIGO VARCHAR(100), " +
    #     "INCOM INTEGER, " + "NOCOM INTEGER, " + "BLACK CHAR(1))")
    # query.exec(
    #     "INSERT INTO WORKED_DATA (GDATE) VALUES('2021-05-24')")
    # dictSampleData = {LIST_COL_WORKED_DATA[1]: "2021-05-24", LIST_COL_WORKED_DATA[2]: "윤 민구", LIST_COL_WORKED_DATA[3]: "13:00", LIST_COL_WORKED_DATA[4]: "",
    #                   LIST_COL_WORKED_DATA[5]: "38", LIST_COL_WORKED_DATA[6]: 200000, LIST_COL_WORKED_DATA[7]: "1", LIST_COL_WORKED_DATA[8]: "수금", LIST_COL_WORKED_DATA[9]: "양도", LIST_COL_WORKED_DATA[10]: 0, LIST_COL_WORKED_DATA[11]: 0, LIST_COL_WORKED_DATA[12]: "Y"}
    # for i in range(20):
    #     insertWorkedData(query, dictSampleData)
    return True


def insertWorkedData(query, dict_data: dict):
    for key in LIST_COL_WORKED_DATA:
        if not key in dict_data:
            dict_data[key] = ""
    query.exec(
        f"INSERT INTO WORKED_DATA (GDATE, ITEM, SIKAN1, SIKAN2, MUL, GUM, CAR, SUGUM, BIGO, INCOM, NOCOM, BLACK) VALUES('{dict_data[LIST_COL_WORKED_DATA[1]]}', '{dict_data[LIST_COL_WORKED_DATA[2]]}', '{dict_data[LIST_COL_WORKED_DATA[3]]}', '{dict_data[LIST_COL_WORKED_DATA[4]]}', '{dict_data[LIST_COL_WORKED_DATA[5]]}', '{dict_data[LIST_COL_WORKED_DATA[6]]}', '{dict_data[LIST_COL_WORKED_DATA[7]]}', '{dict_data[LIST_COL_WORKED_DATA[8]]}', '{dict_data[LIST_COL_WORKED_DATA[9]]}', '{dict_data[LIST_COL_WORKED_DATA[10]]}', '{dict_data[LIST_COL_WORKED_DATA[11]]}', '{dict_data[LIST_COL_WORKED_DATA[12]]}')")


def updateWorkedData(query, row_no, dict_data: dict):
    for key in LIST_COL_WORKED_DATA:
        if not key in dict_data:
            dict_data[key] = ""

    queryString = f"UPDATE WORKED_DATA SET GDATE='{dict_data[LIST_COL_WORKED_DATA[1]]}', ITEM='{dict_data[LIST_COL_WORKED_DATA[2]]}', SIKAN1='{dict_data[LIST_COL_WORKED_DATA[3]]}', SIKAN2='{dict_data[LIST_COL_WORKED_DATA[4]]}', MUL='{dict_data[LIST_COL_WORKED_DATA[5]]}', GUM='{dict_data[LIST_COL_WORKED_DATA[6]]}', CAR='{dict_data[LIST_COL_WORKED_DATA[7]]}', SUGUM='{dict_data[LIST_COL_WORKED_DATA[8]]}', BIGO='{dict_data[LIST_COL_WORKED_DATA[9]]}' WHERE ID={row_no}"
    query.exec(queryString)


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.showMaximized()

        self.tabWidgetMain.currentChanged.connect(
            self.tabWidgetMainChangeFunction)
        self.buttonUpdatedInfo.clicked.connect(self.buttonUpdatedInfoFunction)

        # tab 1 start
        self.modelWorkedDataTab1 = QtSql.QSqlQueryModel(self)
        self.modelWorkedDataTab1.setQuery(QUERY_SELECT_TAB1)
        for i in range(len(LIST_HEADER_NAME_TAB1)):
            self.modelWorkedDataTab1.setHeaderData(
                i, Qt.Horizontal, QVariant(LIST_HEADER_NAME_TAB1[i]))

        # show the view with model
        self.tableDataTab1.setModel(self.modelWorkedDataTab1)
        self.tableDataTab1.setItemDelegate(
            QtSql.QSqlRelationalDelegate(self.tableDataTab1))
        for i in range(len(LIST_HEADER_SIZE_TAB1)):
            self.tableDataTab1.setColumnWidth(i, LIST_HEADER_SIZE_TAB1[i])

        self.calendarWidgetTab1.setGridVisible(True)
        self.calendarWidgetTab1.clicked.connect(
            self.calendarWidgetTab1Function)
        self.calendarWidgetTab1Function()

        self.buttonSaveTab1.clicked.connect(self.buttonSaveTab1Function)
        self.buttonResetTab1.clicked.connect(self.buttonResetTab1Function)
        # tab 1 end

        # tab 2 start
        initDate = QDate.currentDate()
        initStartDate = QDate(initDate.year(), initDate.month(), 1)
        initEndDate = QDate(
            initDate.year(), initDate.month(), initDate.daysInMonth())
        self.inputSearchDateStartTab2.setDate(initStartDate)
        self.inputSearchDateEndTab2.setDate(initEndDate)

        self.modelWorkedDataTab2 = QtSql.QSqlQueryModel(self)
        self.buttonSearchTab2Function()
        for i in range(len(LIST_HEADER_NAME_TAB2)):
            self.modelWorkedDataTab2.setHeaderData(
                i, Qt.Horizontal, QVariant(LIST_HEADER_NAME_TAB2[i]))

        # show the view with model
        self.tableDataTab2.setModel(self.modelWorkedDataTab2)
        self.tableDataTab2.setItemDelegate(
            QtSql.QSqlRelationalDelegate(self.tableDataTab2))
        for i in range(len(LIST_HEADER_SIZE_TAB2)):
            self.tableDataTab2.setColumnWidth(i, LIST_HEADER_SIZE_TAB2[i])
        self.tableDataTab2.clicked.connect(self.tableDataTab2Function)
        self.tableDataTab2.setColumnHidden(0, True)

        self.buttonSearchTab2.clicked.connect(self.buttonSearchTab2Function)
        self.buttonResetTab2.clicked.connect(self.buttonResetTab2Function)
        self.modifyModelWorkedDataTab2 = QtSql.QSqlQueryModel(self)
        self.buttonDeleteTab2.clicked.connect(self.buttonDeleteTab2Function)
        self.buttonModifyTab2.clicked.connect(self.buttonModifyTab2Function)
        self.buttonBlackTab2.clicked.connect(self.buttonBlackTab2Function)

        self.tableDataTab2.selectRow(0)
        self.buttonResetTab2.clicked.emit()
        # tab 2 end

        # tab 3 start
        self.inputSearchDateStartTab3.setDate(QDate(2000, 1, 1))
        self.inputSearchDateEndTab3.setDate(QDate.currentDate())

        self.modelWorkedDataTab3 = QtSql.QSqlQueryModel(self)
        self.buttonSearchTab3Function()
        for i in range(len(LIST_HEADER_NAME_TAB3)):
            self.modelWorkedDataTab3.setHeaderData(
                i, Qt.Horizontal, QVariant(LIST_HEADER_NAME_TAB3[i]))

        # show the view with model
        self.tableDataTab3.setModel(self.modelWorkedDataTab3)
        self.tableDataTab3.setItemDelegate(
            QtSql.QSqlRelationalDelegate(self.tableDataTab3))
        for i in range(len(LIST_HEADER_SIZE_TAB3)):
            self.tableDataTab3.setColumnWidth(i, LIST_HEADER_SIZE_TAB3[i])

        self.buttonSearchTab3.clicked.connect(self.buttonSearchTab3Function)
        self.buttonPrintTab3.clicked.connect(self.buttonPrintTab3Function)
        # tab 3 end

        # tab 4 start
        self.modelWorkedDataTab4 = QtSql.QSqlQueryModel(self)
        self.modelWorkedDataTab4.setQuery(QUERY_SELECT_TAB4)
        for i in range(len(LIST_HEADER_NAME_TAB4)):
            self.modelWorkedDataTab4.setHeaderData(
                i, Qt.Horizontal, QVariant(LIST_HEADER_NAME_TAB4[i]))

        # show the view with model
        self.tableDataTab4.setModel(self.modelWorkedDataTab4)
        self.tableDataTab4.setItemDelegate(
            QtSql.QSqlRelationalDelegate(self.tableDataTab4))
        for i in range(len(LIST_HEADER_SIZE_TAB4)):
            self.tableDataTab4.setColumnWidth(i, LIST_HEADER_SIZE_TAB4[i])

        self.buttonBlackTab4.clicked.connect(self.buttonBlackTab4Function)

    def tabWidgetMainChangeFunction(self, _index):
        if _index == 0:
            self.modelWorkedDataTab1.setQuery(QUERY_SELECT_TAB1)
        elif _index == 1:
            self.buttonSearchTab2.clicked.emit()
        elif _index == 2:
            self.buttonSearchTab3.clicked.emit()
        elif _index == 3:
            self.modelWorkedDataTab4.setQuery(QUERY_SELECT_TAB4)

    def buttonUpdatedInfoFunction(self):
        QMessageBox.about(
            self, " v1.2 정보창", "v1.2\n업데이트내역 추가\n총매출액 글씨 겹치는 오류 수정\n금액 수정 시 데이터 날라가는 오류 수정\n시간 입력 방식 수정\n프린트 데모 기능 추가\n\n\
v1.1\n창 켜자마자 최대화\n탭 입력 시 폼 포커스 순서 변경\n금액에 , 추가\n입력 버튼 클릭 시 거래처로 커서\n총타설량 추가(조회탭)\n글씨체 전반적으로 굵게 변경\n\n\
v1.0\n최초개발")

    # tab 1
    def calendarWidgetTab1Function(self):
        self.inputDateTab1.setText(
            self.calendarWidgetTab1.selectedDate().toString("yyyy-MM-dd"))

    def buttonSaveTab1Function(self):
        query = QtSql.QSqlQuery()
        dictInputData = {LIST_COL_WORKED_DATA[1]: self.inputDateTab1.text(), LIST_COL_WORKED_DATA[2]: self.inputCompanyTab1.text(), LIST_COL_WORKED_DATA[3]: self.inputTimeStartTab1.currentText(), LIST_COL_WORKED_DATA[4]: self.inputTimeEndTab1.currentText(),
                         LIST_COL_WORKED_DATA[5]: self.inputAmountTab1.text(), LIST_COL_WORKED_DATA[6]: self.inputPriceTab1.text(), LIST_COL_WORKED_DATA[7]: self.inputCarTab1.text(), LIST_COL_WORKED_DATA[8]: self.inputCollectTab1.currentText(), LIST_COL_WORKED_DATA[9]: self.inputRemarkTab1.text()}

        insertWorkedData(query, dictInputData)
        self.modelWorkedDataTab1.setQuery(QUERY_SELECT_TAB1)

        self.buttonResetTab1.clicked.emit()

    def buttonResetTab1Function(self):
        self.calendarWidgetTab1.setSelectedDate(QDate.currentDate())
        self.calendarWidgetTab1Function()  # label까지 업데이트
        self.inputCompanyTab1.clear()
        self.inputTimeStartTab1.setCurrentIndex(0)
        self.inputTimeEndTab1.setCurrentIndex(0)
        self.inputAmountTab1.clear()
        self.inputPriceTab1.clear()
        self.inputCarTab1.clear()
        self.inputCollectTab1.setCurrentIndex(0)
        self.inputRemarkTab1.clear()

        self.inputCompanyTab1.setFocus()

    # tab 2 start
    def buttonSearchTab2Function(self):
        queryString = QUERY_SELECT_TAB2
        inputStartDate = self.inputSearchDateStartTab2.date().toString("yyyy-MM-dd")
        inputEndDate = self.inputSearchDateEndTab2.date().toString("yyyy-MM-dd")
        inputCollect = self.inputSearchCollectTab2.currentText()
        inputCompany = self.inputSearchCompanyTab2.text()

        whereCondition = f"AND GDATE BETWEEN '{inputStartDate}' AND '{inputEndDate}'"
        if inputCollect != "전체":
            whereCondition += f" AND SUGUM = '{inputCollect}'"
        if inputCompany != "":
            whereCondition += f" AND ITEM LIKE '%{inputCompany}%'"

        queryString = queryString.replace(WHERE_CONDITION, whereCondition)
        self.modelWorkedDataTab2.setQuery(queryString)

        self.tableDataTab2.selectRow(0)
        self.buttonResetTab2.clicked.emit()

    def tableDataTab2Function(self):
        objSelectedCell = self.tableDataTab2.selectedIndexes()[0]

        selectedDate = list(map(
            int, objSelectedCell.siblingAtColumn(1).data().split("-")))
        self.inputDateTab2.setDate(
            QDate(selectedDate[0], selectedDate[1], selectedDate[2]))
        self.inputCompanyTab2.setText(
            objSelectedCell.siblingAtColumn(2).data())
        self.inputCarTab2.setText(
            objSelectedCell.siblingAtColumn(7).data())
        self.inputPriceTab2.setText(
            str(objSelectedCell.siblingAtColumn(6).data()).replace(",", ""))

        idxStartTime = self.inputTimeStartTab2.findText(
            objSelectedCell.siblingAtColumn(3).data(), Qt.MatchFixedString)
        self.inputTimeStartTab2.setCurrentIndex(idxStartTime)
        idxEndTime = self.inputTimeEndTab2.findText(
            objSelectedCell.siblingAtColumn(4).data(), Qt.MatchFixedString)
        self.inputTimeEndTab2.setCurrentIndex(idxEndTime)
        idxCollect = self.inputCollectTab2.findText(
            objSelectedCell.siblingAtColumn(8).data(), Qt.MatchFixedString)
        self.inputCollectTab2.setCurrentIndex(idxCollect)

        self.inputAmountTab2.setText(
            objSelectedCell.siblingAtColumn(5).data())
        self.inputRemarkTab2.setText(
            objSelectedCell.siblingAtColumn(9).data())

        self.tableDataTab2.selectRow(objSelectedCell.row())

    def buttonBlackTab2Function(self):
        queryString = QUERY_UPDATE_BLACK_TAB2
        if not len(self.tableDataTab2.selectedIndexes()):
            return
        selectedRowNumber = self.tableDataTab2.selectedIndexes()[
            0].siblingAtColumn(0).data()

        whereCondition = f"AND ID = {selectedRowNumber}"
        queryString = queryString.replace(WHERE_CONDITION, whereCondition)
        self.modifyModelWorkedDataTab2.setQuery(queryString)
        self.buttonSearchTab2.clicked.emit()

    def buttonResetTab2Function(self):
        if not len(self.tableDataTab2.selectedIndexes()):
            self.inputDateTab2.setDate(QDate.currentDate())
            self.inputCompanyTab2.clear()
            self.inputTimeStartTab2.setCurrentIndex(0)
            self.inputTimeEndTab2.setCurrentIndex(0)
            self.inputAmountTab2.clear()
            self.inputPriceTab2.clear()
            self.inputCarTab2.clear()
            self.inputCollectTab2.setCurrentIndex(0)
            self.inputRemarkTab2.clear()
        else:
            self.tableDataTab2Function()

    def buttonDeleteTab2Function(self):
        queryString = QUERY_DELETE_TAB2
        if not len(self.tableDataTab2.selectedIndexes()):
            return
        selectedRowNumber = self.tableDataTab2.selectedIndexes()[
            0].siblingAtColumn(0).data()

        whereCondition = f"AND ID = {selectedRowNumber}"
        queryString = queryString.replace(WHERE_CONDITION, whereCondition)
        self.modifyModelWorkedDataTab2.setQuery(queryString)
        self.buttonSearchTab2.clicked.emit()

    def buttonModifyTab2Function(self):
        if not len(self.tableDataTab2.selectedIndexes()):
            return
        selectedRowNumber = self.tableDataTab2.selectedIndexes()[
            0].siblingAtColumn(0).data()

        query = QtSql.QSqlQuery()
        dictInputData = {LIST_COL_WORKED_DATA[1]: self.inputDateTab2.date().toString("yyyy-MM-dd"), LIST_COL_WORKED_DATA[2]: self.inputCompanyTab2.text(), LIST_COL_WORKED_DATA[3]: self.inputTimeStartTab2.currentText(), LIST_COL_WORKED_DATA[4]: self.inputTimeEndTab2.currentText(),
                         LIST_COL_WORKED_DATA[5]: self.inputAmountTab2.text(), LIST_COL_WORKED_DATA[6]: self.inputPriceTab2.text(), LIST_COL_WORKED_DATA[7]: self.inputCarTab2.text(), LIST_COL_WORKED_DATA[8]: self.inputCollectTab2.currentText(), LIST_COL_WORKED_DATA[9]: self.inputRemarkTab2.text()}

        updateWorkedData(query, selectedRowNumber, dictInputData)

        self.buttonSearchTab2.clicked.emit()
        self.tableDataTab2.selectRow(0)
        self.buttonResetTab2.clicked.emit()

    # tab 3 start
    def buttonSearchTab3Function(self):
        queryString = QUERY_SELECT_TAB3
        inputStartDate = self.inputSearchDateStartTab3.date().toString("yyyy-MM-dd")
        inputEndDate = self.inputSearchDateEndTab3.date().toString("yyyy-MM-dd")
        inputCollect = self.inputSearchCollectTab3.currentText()
        inputCompany = self.inputSearchCompanyTab3.text()
        inputCar = self.inputSearchCarTab3.text()
        inputRemark = self.inputSearchRemarkTab3.text()

        whereCondition = f"AND GDATE BETWEEN '{inputStartDate}' AND '{inputEndDate}'"
        if inputCollect != "전체":
            whereCondition += f" AND SUGUM = '{inputCollect}'"
        if inputCompany != "":
            whereCondition += f" AND ITEM LIKE '%{inputCompany}%'"
        if inputCar != "":
            whereCondition += f" AND CAR LIKE '%{inputCar}%'"
        if inputRemark != "":
            whereCondition += f" AND BIGO LIKE '%{inputRemark}%'"

        queryString = queryString.replace(WHERE_CONDITION, whereCondition)
        self.modelWorkedDataTab3.setQuery(queryString)

        # SUMMARY
        query = QtSql.QSqlQuery()

        queryStringTotalTake = QUERY_TOTAL_TAKE_TAB3
        queryStringTotalTake = queryStringTotalTake.replace(
            WHERE_CONDITION, whereCondition)
        query.exec(queryStringTotalTake)
        rec = query.record()
        query.next()
        countData, totalTake, totalAmount = str(
            query.value(0)), str(query.value(1)), str(query.value(2))

        self.inputRowNoTab3.setText(countData)
        self.inputTotalTab3.setText(totalTake)
        self.inputTotalAmountTab3.setText(totalAmount)
        if totalTake == "":
            self.inputTotalTab3.setText("0")
        if totalAmount == "":
            self.inputTotalAmountTab3.setText("0")

        queryStringSubtotalTake = QUERY_SUBTOTAL_TAKE_TAB3
        queryStringSubtotalTake = queryStringSubtotalTake.replace(
            WHERE_CONDITION, whereCondition)
        query.exec(queryStringSubtotalTake)
        rec = query.record()
        dictSubtotal = {}
        while query.next():
            dictSubtotal[query.value(0)] = str(query.value(1))

        if "수금" in dictSubtotal:
            self.inputTotalCollectTab3.setText(dictSubtotal["수금"])
        else:
            self.inputTotalCollectTab3.setText("0")
        if "미수" in dictSubtotal:
            self.inputTotalNoCollectTab3.setText(dictSubtotal["미수"])
        else:
            self.inputTotalNoCollectTab3.setText("0")

    def buttonPrintTab3Function(self):
        # 프린터 생성, 실행
        printer = QPrinter()
        dlg = QPrintDialog(printer, self)
        if dlg.exec() == QDialog.Accepted:
            # Painter 생성
            qp = QPainter()
            qp.begin(printer)

            # 여백 비율
            wgap = printer.pageRect().width()*0.1
            hgap = printer.pageRect().height()*0.1

            # 화면 중앙에 위젯 배치
            xscale = (printer.pageRect().width()-wgap) / \
                self.tableDataTab3.width()
            yscale = (printer.pageRect().height()-hgap) / \
                self.tableDataTab3.height()
            scale = xscale if xscale < yscale else yscale
            qp.translate(printer.paperRect().x() + printer.pageRect().width()/2,
                         printer.paperRect().y() + printer.pageRect().height()/2)
            qp.scale(scale, scale)
            qp.translate(-self.tableDataTab3.width() /
                         2, -self.tableDataTab3.height()/2)

            # 인쇄
            self.tableDataTab3.render(qp)

            qp.end()

    # tab 4 start

    def buttonBlackTab4Function(self):
        queryString = QUERY_UPDATE_NOBLACK_TAB4
        if not len(self.tableDataTab4.selectedIndexes()):
            return
        selectedRowNumber = self.tableDataTab4.selectedIndexes()[
            0].siblingAtColumn(0).data()

        whereCondition = f"AND ID = {selectedRowNumber}"
        queryString = queryString.replace(WHERE_CONDITION, whereCondition)
        self.modifyModelWorkedDataTab2.setQuery(queryString)
        self.modelWorkedDataTab4.setQuery(QUERY_SELECT_TAB4)


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    if not createConnection():
        sys.exit(-1)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
