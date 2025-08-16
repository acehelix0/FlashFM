# --- IMPORT ---
try:
    import sys
    from colorama import Fore
except ImportError:
    print("[ERROR] You do not have \"colorama\" installed in your Python enviroment,",
          "which is used for making logging pretty")
    exit(1)
    
try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileSystemModel, QTreeView, QWidget
    from PySide6.QtGui import QIcon, QDesktopServices
    from PySide6.QtCore import QDir, QModelIndex, QUrl
except ImportError:
    print("[ERROR] You do not have \"PySide6\" installed.", 
          "Which is used for the GUI of this program.")
    exit(1)
# --- IMPORT --- (END)

# --- LOGGING ---
message = 1
warning = 2
error = 3

def log( log_level: int, string: str):
    if log_level == message:
        print(Fore.BLUE + "[MESSAGE]", string + Fore.RESET)
    elif log_level == warning:
        print(Fore.YELLOW + "[WARNING]", string + Fore.RESET)
    elif log_level == error:
        print(Fore.RED + "[ERROR]", string + Fore.RESET)
# --- LOGGING --- (END)

# --- MAIN WINDOW ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlashFM")
        self.setWindowIcon(QIcon("icon.png"))

        posX = 200
        posY = 200
        width = 720
        height = 500
        self.setGeometry(posX, posY, width, height)

        centralWidget = QWidget()
        boxLayout = QVBoxLayout()
        centralWidget.setLayout(boxLayout)
        self.setCentralWidget(centralWidget)

        self.treeModel = QFileSystemModel()
        self.treeModel.setRootPath(QDir.rootPath())

        self.treeView = QTreeView()
        self.treeView.setModel(self.treeModel)
        self.treeView.setRootIsDecorated(True)
        self.treeView.setSortingEnabled(True)

        boxLayout.addWidget(self.treeView)

        # --- CHECKS ---
        self.treeView.doubleClicked.connect(self.openFile)
        # --- CHECKS --- (END)

    def openFile(self, modelIndex: QModelIndex):
        if not self.treeModel.isDir(modelIndex):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.treeModel.filePath(modelIndex)))
            log(message, "File opened: " + self.treeModel.filePath(modelIndex))
# --- MAIN WINDOW --- (END)

# --- EXECUTION ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
# --- EXECUTION --- (END)