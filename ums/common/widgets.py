from PySide2.QtWidgets import QLabel, QMessageBox
from PySide2.QtCore import Qt


class QBorderedLabel(QLabel):
    def __init__(self, text, parent=None):
        QLabel.__init__(self, text, parent)
        self.setStyleSheet('border: 3px inset grey;')
        self.setAlignment(Qt.AlignCenter)
    
class ErrorMessage(QMessageBox):
    def __init__(self, error_message):
        super().__init__()
        self.setIcon(QMessageBox.Critical)
        self.setText(error_message)
        self.setWindowTitle("Ошибка")
        self.exec_()