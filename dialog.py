# 导入我们需要的组件
from PySide6.QtWidgets import QApplication, QWidget
# 处理命令行参数的组件，能嵌入QT程序
import sys

app = QApplication(sys.argv)
window = QWidget()
window.show()
app.exec()