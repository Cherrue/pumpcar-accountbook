# 마니산펌프카 관리프로그램

간단한 장부 프로그램입니다.

## 사용기술
Language : Python 3.9.7

UI : pyqt5

DB : QtSql

## 화면 설명

### 신규자료 입력

이미지 넣기

프로그램 실행 시 첫 화면으로 달력이 오늘로 선택되고, 우측 표에 최근 장부 내용이 보입니다.

QCalendarWidget의 내비게이션 바를 불편해하셔서 별도 위젯들로 붙여 커스텀 내비게이션 바를 만들었습니다.

### 자료 수정 및 삭제

탭 진입 시 당월 자료가 조회됩니다. 원하는 행을 클릭하면 왼쪽 입력 폼에서 수정할 수 있습니다.

미수 기간이 길어지면 악덕업체 버튼을 클릭하여 악덕업체관리 탭에서 확인할 수 있습니다.

### 자료검색 및 출력

탭 진입 시 당해 자료가 조회됩니다. 출력된 데이터에 대한 총 매출액 / 미수금 / 수금액 / 타설량을 확인할 수 있습니다.

출력 버튼을 클릭하면 조회된 자료를 프린트 할 수 있습니다.

### 악덕업체 관리

악덕업체로 저장한 자료가 조회됩니다. 탭 이름과 다르게 자료 단위로 관리합니다. (레거시 사양)

자료 수정 탭에서 악덕업체 버튼을 클릭하면 이 탭에서 확인 가능하고, 풀어주는 것은 여기서만 가능합니다.

자주 사용하는 기능이 아니어서 전체 기간을 조회합니다.