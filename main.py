# --- IMPORT ---
try:
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileSystemModel, QTreeView, QWidget
    from PySide6.QtGui import QIcon, QDesktopServices
    from PySide6.QtCore import QDir, QModelIndex, QUrl
except ImportError:
    print("[ERROR] You do not have \"PySide6\" installed in your Python enviroment,", 
          "which is used for the GUI of this program.")
    exit(1)
# --- IMPORT --- (END)

# --- LOGGING ---
MESSAGE = 1
WARNING = 2
ERROR = 3

def log(logLevel: int, string: str):
    if logLevel == MESSAGE:
        print("[MESSAGE]", string)
    elif logLevel == WARNING:
        print("[WARNING]", string)
    elif logLevel == ERROR:
        print("[ERROR]", string)
# --- LOGGING --- (END)

# --- MAIN WINDOW ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlashFM")
        self.setWindowIcon(QIcon("icon.ico"))

        # -- MAIN WINDOW SIZE ---
        POS_X = 200
        POS_Y = 200
        WIDTH = 720
        HEIGHT = 500
        self.setGeometry(POS_X, POS_Y, WIDTH, HEIGHT)
        # -- MAIN WINDOW SIZE --- (END)

        # -- LAYOUT ---
        centralWidget = QWidget()
        boxLayout = QVBoxLayout()
        centralWidget.setLayout(boxLayout)
        self.setCentralWidget(centralWidget)
        
        # -- TREE MODEL/VIEW ---
        self.treeModel = QFileSystemModel()
        self.treeModel.setRootPath(QDir.rootPath())

        self.treeView = QTreeView()
        self.treeView.setModel(self.treeModel)
        self.treeView.setRootIsDecorated(True)
        self.treeView.setSortingEnabled(True)

        boxLayout.addWidget(self.treeView)
        # -- TREE MODEL/VIEW --- (END)
        # -- LAYOUT --- (END)

        # --- SIGNALS ---
        self.treeView.doubleClicked.connect(self.openFile)
        # --- SIGNALS --- (END)
    # --- MAIN WINDOW --- (END)

    # --- FILE OPERATIONS ---
    def openFile(self, modelIndex: QModelIndex):
        if not self.treeModel.isDir(modelIndex):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.treeModel.filePath(modelIndex)))
            log(MESSAGE, "File opened: " + self.treeModel.filePath(modelIndex))
    # --- FILE OPERATIONS --- (END)

# --- EXECUTION ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
# --- EXECUTION --- (END)
