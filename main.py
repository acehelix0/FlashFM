try:
    import sys
    import os
    import shutil
    from PySide6.QtWidgets import (
        QApplication,
        QMainWindow,
        QFileSystemModel,
        QTreeView,
        QMenu,
        QMenuBar,
        QInputDialog,
        QMessageBox,
        QWidget,
        QVBoxLayout,
        QLabel
    )
    from PySide6.QtGui import (
        QIcon,
        QDesktopServices,
        QAction,
        QPixmap,
        QFont,
        QGuiApplication,
        )
    from PySide6.QtCore import ( QDir,
        QModelIndex,
        QUrl,
        QFile,
        QIODevice,
        qInfo)
except ImportError:
    print("[ERROR] You do not have \"PySide6\" installed in your Python enviroment,", 
          "which is used for the GUI of this program.")
    exit(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    userScreen = QGuiApplication.primaryScreen()

    class AboutWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("About FlashFM")
            self.setWindowIcon(QIcon("icon.png"))
            WIDTH = 500
            HEIGHT = 200
            self.setGeometry(userScreen.size().width() // 5, userScreen.size().height() // 5, WIDTH, HEIGHT)
            layoutOfWindow = QVBoxLayout()
            iconImageLabel = QLabel(self)
            pixmapOfIcon = QPixmap("./icon.png")
            iconImageLabel.setPixmap(pixmapOfIcon)
            iconImageLabel.setScaledContents(True)
            
            textLabel = QLabel("FlashFM v0.0.1", self)
            textLabel.move(148, 10)
            textLabel.setFont(QFont("Arial", 14))

            textLabel2 = QLabel("FlashFM v0.0.1 is the first ever version of FlashFM,\nwith limited features however.")

            layoutOfWindow.addWidget(iconImageLabel)
            layoutOfWindow.addWidget(textLabel)
            layoutOfWindow.addWidget(textLabel2)
            self.setLayout(layoutOfWindow)

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("FlashFM")
            self.setWindowIcon(QIcon("icon.png"))

            WIDTH = 900
            HEIGHT = 500
            self.setGeometry(userScreen.size().width() // 5, userScreen.size().height() // 5, WIDTH, HEIGHT)
            
            mainMenuBar = QMenuBar()

            fileMenu = QMenu("&File/Folder", self)
            mainMenuBar.addMenu(fileMenu)

            newAction = QAction("&New", self)
            fileMenu.addAction(newAction)

            deleteAction = QAction("&Delete", self)
            fileMenu.addAction(deleteAction)
            
            helpMenu = QMenu("&Help", self)
            mainMenuBar.addMenu(helpMenu)

            aboutAction = QAction("&About", self)
            self.aboutWindow = AboutWindow()
            helpMenu.addAction(aboutAction)

            self.treeModel = QFileSystemModel()
            self.treeModel.setRootPath(QDir.rootPath())

            self.treeView = QTreeView()
            self.treeView.setModel(self.treeModel)
            self.treeView.setRootIsDecorated(True)
            self.treeView.setSortingEnabled(True)

            self.setCentralWidget(self.treeView)
            self.setMenuBar(mainMenuBar)

            self.treeView.doubleClicked.connect(self.openFileThroughURL)
            newAction.triggered.connect(self.newFileFolderAction)
            deleteAction.triggered.connect(self.deleteFileFolderAction)
            aboutAction.triggered.connect(self.aboutWindow.show)

        def openFileThroughURL(self, modelIndex: QModelIndex):
            if not self.treeModel.isDir(modelIndex):
                QDesktopServices.openUrl(QUrl.fromLocalFile(self.treeModel.filePath(modelIndex)))
                qInfo("File (" + self.treeModel.filePath(modelIndex) + ") has been opened.")
    
        def newFileFolderAction(self):
            modelIndex = self.treeView.currentIndex()
            if self.treeModel.filePath(modelIndex).startswith("C:/Windows"):
                QMessageBox.warning(self, "Unable to create files in Windows", "You can't create new files in the Windows folder.")
                return
            if self.treeModel.isDir(modelIndex):
                path, ok = QInputDialog.getText(self, "New file/folder name", "Name your new file/folder that will be created in the selected folder. (" + self.treeModel.filePath(modelIndex) + ")\n" +
                                                "Note: You can make a path aswell! (e.g. path/to/file.txt)")
                if path and ok:
                    foldersAndFiles = path.split('/')
                    folderOrFile = path
                        
                    if len(foldersAndFiles) > 1:
                        folders: str = ""
                        file: str
                        if not foldersAndFiles[-1] == '':
                            file = foldersAndFiles[-1]
                            foldersAndFiles.pop()
                            for folder in foldersAndFiles:
                                folders += folder + "/"
                            if QDir.mkpath(QDir(), self.treeModel.filePath(modelIndex) + "/" + folders):
                                newFile = QFile(self.treeModel.filePath(modelIndex) + "/" + folders + "/" + file)
                                if newFile.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text):
                                    newFile.write
                                    newFile.close
                                    qInfo("Path and file (" + self.treeModel.filePath(modelIndex) + folders + file + ") has been created!")
                                else:
                                    QMessageBox.critical(self, "File/folder creation failure", self.treeModel.filePath(modelIndex) + "/" + folders + "/" + file + " has failed to be created.")
                        else:
                            for folder in foldersAndFiles:
                                folders += folder + "/"
                            folders = folders[:-1]
                            if QDir.mkpath(QDir(), self.treeModel.filePath(modelIndex) + "/" + folders):
                                qInfo("Path (" + self.treeModel.filePath(modelIndex) + "/" + folders + ") has been created!")
                    else:
                        if folderOrFile.endswith('/'):
                            if QDir.mkpath(QDir(), self.treeModel.filePath(modelIndex) + "/" + folderOrFile):
                                qInfo(self.treeModel.filePath(modelIndex) + "/" + folderOrFile + "/ has been created!")
                        else:
                            newFile = QFile(self.treeModel.filePath(modelIndex) + "/" + folderOrFile)
                            if newFile.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text):
                                newFile.write
                                newFile.close
                            else:
                                QMessageBox.critical(self, "File creation failure", "Creating " + folderOrFile + " has failed.")
            else:
                QMessageBox.warning(self, "Invalid Selection", "Please select a folder to create a new file or folder.")

                            
    
        def deleteFileFolderAction(self):
            modelIndex = self.treeView.currentIndex()
            if self.treeModel.filePath(modelIndex).endswith(":\\") or self.treeModel.filePath(modelIndex).endswith(":/"):
                QMessageBox.critical(self, "Couldn't delete", "You cannot delete drives. Only files and folders.")
            elif (self.treeModel.filePath(modelIndex).startswith("C:/Windows")
                  or self.treeModel.filePath(modelIndex) == "C:/Program Files"
                  or self.treeModel.filePath(modelIndex) == "C:/Program Files (x86)"
                  or self.treeModel.filePath(modelIndex) == "C:/Users"):
                QMessageBox.critical(self, "System files protection", "We are trying to keep your system files safe from deletion, as it can lead to serious issues in your OS.\n" +
                                     "(e.g OS rendering unbootable, system crashes)")
            else:
                confirmation = QMessageBox.question(self, "Are you sure?", self.treeModel.fileName(modelIndex) + " will be deleted and you won't be able to undo this process.\nAre you sure you wanna make this change?")
                if confirmation == QMessageBox.StandardButton.Yes:
                    try:
                        if os.path.isdir(self.treeModel.filePath(modelIndex)):
                            shutil.rmtree(self.treeModel.filePath(modelIndex))
                            qInfo(self.treeModel.filePath(modelIndex) + " has been deleted.")
                        else:
                            os.remove(self.treeModel.filePath(modelIndex))
                            qInfo(self.treeModel.filePath(modelIndex) + " has been deleted.")
                    except PermissionError:
                        QMessageBox.critical(self, "Restricted access", "You need admin privileges to delete " + self.treeModel.fileName(modelIndex) + "\nPlease try to run this program as administrator")
                else:
                    qInfo("File deletion has been aborted.")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())