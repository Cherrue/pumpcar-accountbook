from PyQt5.QtWidgets import QCalendarWidget


class YearButtonCalendarWidget(QCalendarWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
