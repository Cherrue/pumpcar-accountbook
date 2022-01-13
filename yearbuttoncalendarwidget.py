from PyQt5.QtWidgets import QCalendarWidget


class YearButtonCalendarWidget(QCalendarWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("hello")

    def customEvent(self):
        print("event called")
        print(self.monthShown())
        print(self.yearShown())
