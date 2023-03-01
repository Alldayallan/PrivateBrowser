from qtpy.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction, QMenu
from qtpy.QtCore import Qt, QUrl
from qtpy.QtWebEngineWidgets import QWebEngineView, QWebEngineHistory


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)
        self.showMaximized()
        self.history = QWebEngineHistory.defaultHistory(self.browser)
        self.history.addHistoryEntry(self.browser.url())
        self.history.changed.connect(self.update_history_menu)

    def update_history_menu(self):
        self.history_menu.clear()
        for i, item in enumerate(self.history.items()):
            action = QAction(f"{i + 1}. {item.title()}", self)
            action.setData(item.url())
            action.triggered.connect(self.navigate_to_url)
            self.history_menu.addAction(action)

    def navigate_to_url(self):
        action = self.sender()
        if action:
            url = action.data()
            self.browser.setUrl(url)

        self.browser_url.setText(self.browser.url().toString())
        self.history.addHistoryEntry(self.browser.url())


class Toolbar(QToolBar):
    def __init__(self):
        super().__init__()
        self.browser_url = QLineEdit()
        self.addAction(QAction("Go", self, triggered=self.navigate_to_url))
        self.addAction(QAction("Back", self, triggered=self.browser.back))
        self.addAction(QAction("Forward", self, triggered=self.browser.forward))
        self.addSeparator()
        self.history_menu = QMenu("History", self)
        self.addMenu(self.history_menu)
        self.browser_url.returnPressed.connect(self.navigate_to_url)

    def navigate_to_url(self):
        url = self.browser_url.text()
        if url.startswith("http"):
            self.parent().browser.setUrl(QUrl(url))
        else:
            self.parent().browser.setUrl(QUrl(f"https://{url}"))
