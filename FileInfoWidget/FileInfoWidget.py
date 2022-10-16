## Change / update path to your location on line 140 to your maya file

import os
import maya.cmds as cmds
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide2 import QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import fileDetails


class AnimatedPreview(QWidget):
    def __init__(self, filePath, placeX, placeY):
        super(AnimatedPreview, self).__init__()
        self.fileLocation = filePath.rsplit('/',1)[0]
        self.fileName = filePath.rsplit('/',1)[1]

        self.imageSequence = self.fileLocation + '/.mayaSwatches/' + self.fileName + '/' +self.fileName + ".1.preview"
        if os.path.isfile(self.imageSequence) == True:

            self.delayTimer = QtCore.QTimer()
            self.delayTimer.setInterval(1000 / 25)
            self.countDelay = 1
            self.delayTimer.start()
            self.timer = QtCore.QTimer()
            self.timer.setInterval(1000 / 25)
            self.count = 2

            self.mainLayout = QVBoxLayout()
            self.animLabel = QLabel()
            self.nextImage = self.fileLocation + '/.mayaSwatches/' + self.fileName + '/' +self.fileName + '.' + str(self.count) +".preview"
            self.setGeometry(QtCore.QRect(placeX, placeY-500, 500, 500))
            self.mainLayout.addWidget(self.animLabel)
            self.mainLayout.setContentsMargins(2, 2, 2, 2)
            self.setLayout(self.mainLayout)
            self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

            self.delayTimer.timeout.connect(self.delayCountDown)
            self.timer.timeout.connect(self.tick)
            
    def tick(self):
        pixmap = QPixmap(self.nextImage)
        self.animLabel.setPixmap(pixmap)
        self.count +=1
        self.nextImage = self.fileLocation + '/.mayaSwatches/' + self.fileName + '/' +self.fileName + '.' + str(self.count) +".preview"
        if os.path.isfile(self.nextImage) == False:
            self.timer.stop()
            self.close()

    def delayCountDown(self):
        if self.countDelay > 10:
            self.delayTimer.stop()
            self.timer.start() 
            self.show()
        else:
            self.countDelay += 1

class PreviewImageWidget(QWidget):
    def __init__(self, parentUi=None, *args):
        super(PreviewImageWidget, self).__init__()
        self.bgImage = "icons/blankThumbnailBG.png"
        self.imageControl = cmds.image(image=self.bgImage, parent = parentUi)
        self.imageQWidget = wrapInstance( long( omui.MQtUtil.findControl( self.imageControl ) ), QWidget )
        self.imageQWidget.setContentsMargins(0, 0, 0, 0)
        imageBoxLayout = QVBoxLayout()
        imageBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.imageLbl = QLabel()
        imageBoxLayout.addWidget(self.imageLbl)
        self.imageQWidget.setLayout(imageBoxLayout)
        self.imageLbl.installEventFilter(self) 

    def checkAndUpdateImage(self, filePath):
        self.filePath = filePath
        if self.filePath != None and self.filePath != '':
            self.fileLocation = self.filePath.rsplit('/',1)[0]
            self.fileName = self.filePath.rsplit('/',1)[1]
            self.imagePath = self.fileLocation + '/.mayaSwatches/' + self.fileName + '.swatch'
            if os.path.isfile(self.imagePath) == False:
                self.imagePath = "icons/blankThumbnailBG.png"
            myImage = QPixmap(self.imagePath)
            myImage = myImage.scaled(50, 50) 
            self.imageLbl.setPixmap(myImage)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Enter:
            self.imageSequence = self.fileLocation + '/.mayaSwatches/' + self.fileName + '/' +self.fileName + ".1.preview"
            if os.path.isfile(self.imageSequence) == True:
                cursorPos = QtGui.QCursor.pos()
                self.newAnimation = AnimatedPreview(self.filePath, cursorPos.x(), cursorPos.y())
            elif os.path.isfile(self.imagePath) == True:
                self.imageLbl.setToolTip('<img src="{0}"; >'.format(self.imagePath))
                self.imageLbl.setStyleSheet("QToolTip { background-color: rgb(67,67,67); qproperty-margin: 1; qproperty-indent: 1; }")
        elif event.type() == QtCore.QEvent.Leave:
            if os.path.isfile(self.imageSequence) == True:
                self.newAnimation.close()
                self.newAnimation.delayTimer.stop()
        return super(PreviewImageWidget, self).eventFilter(object, event)


class FileInfoWidget():
    
    def __init__(self, parentUi=None, *args):
        
        self.infoWidgetLayout = cmds.formLayout(numberOfDivisions=100, parent=parentUi, height=60, manage=True)
        self.fileModifyTime = cmds.text(l='', align='left', font='obliqueLabelFont', parent=self.infoWidgetLayout )
        self.fileOwnerInfo = cmds.text(l='', align='left', font='obliqueLabelFont', parent=self.infoWidgetLayout )
        self.imageWidget = PreviewImageWidget(self.infoWidgetLayout)
        image_layout = self.imageWidget.imageControl
        
        cmds.formLayout(self.infoWidgetLayout, edit=True, attachForm = [(self.fileModifyTime, 'left', 0), (self.fileModifyTime, 'top', 15), (self.fileModifyTime, 'bottom', 0),
                                                                        (self.fileOwnerInfo, 'left', 0), (self.fileOwnerInfo, 'top', 15), (self.fileOwnerInfo, 'bottom', 0),
                                                                        (image_layout, 'right', 0)], 
                                                       attachControl = [(self.fileModifyTime, 'bottom',0, self.fileOwnerInfo)])

    def updateInfo(self, filePath):
        self.filePath = filePath
        if self.filePath == '' or self.filePath == None:
            cmds.formLayout(self.infoWidgetLayout, edit=True, manage=False)
        else:
            cmds.formLayout(self.infoWidgetLayout, edit=True, manage=True)
            cmds.text(self.fileModifyTime, edit=True, l='Last modified on: {}'.format(fileDetails.getFileTime(self.filePath)))
            cmds.text(self.fileOwnerInfo, edit=True, l='Modified by: {} '.format (fileDetails.getFileOwner(self.filePath)))
            
        self.imageWidget.checkAndUpdateImage(self.filePath)


class MainUi():
    def __init__(self):
        cmds.window(title='File Info Widget')
        mainLayout = cmds.formLayout()

        self.infoWidget = FileInfoWidget(mainLayout)
        info_layout = self.infoWidget.infoWidgetLayout
        self.validateFileLocation()

        cmds.showWindow()
        
    def validateFileLocation(self):
        fileLocation = "C:/Users/alexandrakimbui/Desktop/hello.ma"
        if os.path.isfile(fileLocation):
            self.infoWidget.updateInfo(fileLocation)
        else:
            self.infoWidget.updateInfo('')

window = MainUi()