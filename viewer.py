import io
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine
import os


class MyApp(QWidget):

    update = pyqtSignal()

    def __init__(self, m):
        super().__init__()
        self.setWindowTitle("Mapa Interactivo CABA v1.0")
        self.window_width, self.window_height = 1200, 920
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # data = io.BytesIO()
        # m.save(data, close_file=False)
        plot_path = os.path.abspath("./mapa.html")
        self.plot_url = QUrl.fromLocalFile(plot_path)

        self.webView = QWebEngineView()
        self.webView.load(self.plot_url)
        #self.webView.setHtml(data.getvalue().decode())
        layout.addWidget(self.webView)

        self.button = QPushButton("Reposicionar", self)
        ph = self.button.parent().geometry().height()
        pw = self.button.parent().geometry().width() 
        self.button.setGeometry((pw-60)/2, ph-30, 90, 30)
        self.button.clicked.connect(self.refreshing)
        self.update.connect(self.refreshing)

    @pyqtSlot()
    def refreshing(self):
        self.webView.reload()
