import hou
from PySide2 import QtCore, QtUiTools, QtWidgets

class Separator():
    def __init__(self, ref, space, name, newPos):
        self.geoSpace = hou.node(space)
        self.ref = hou.node(ref)
        self.newPos = newPos
        self.name = name
        
        self.pieces = len(self.ref.geometry().points())
        netbox = self.geoSpace.createNetworkBox()
        netbox.setColor(hou.Color(0, 0.3, 0.6))
        netbox.setComment(name + ' objects')
        
        for p in range(self.pieces):
            newObj = self.geoSpace.createNode('geo')
            newObj.setName(name+str(p))
            newObj.move([(p//5)*2.5, p%5])
            netbox.addItem(newObj)
            objMerge = newObj.createNode('object_merge')
            objMerge.parm('objpath1').set(self.newPos + '/SEP_CTRL')
            blast = newObj.createNode('blast')
            blast.move([0,-2])
            blast.setInput(0, objMerge)
            blast.parm('group').set(str(p))
            blast.parm('negate').set(True)
            blast.setGenericFlag(hou.nodeFlag.Display, True)
            blast.setGenericFlag(hou.nodeFlag.Render, True)

class SepUi(QtWidgets.QWidget):
    def __init__(self):
        super(SepUi,self).__init__()
        ui_file = "form.ui"
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        self.ui.sepBttn.clicked.connect(self.sepClicked)
        self.ui.selectNodeBttn.clicked.connect(self.selectNodeClicked)
        self.ui.selectLocationBttn.clicked.connect(self.spaceClicked)
        self.path = self.ui.nodeSelect
        self.location = self.ui.locSelect
        self.space = '/obj'
        self.customName = self.ui.pieceName
        
    def selectNodeClicked(self):
        self.ls = hou.selectedNodes(self)
        if self.ls:
            self.path.setText(self.ls[0].path())
            self.dirPath = self.ls[0].path()
            self.newPos = self.selectLocationClicked()
            if not hou.node(str(self.selectLocationClicked())+'/SEP_CTRL') in self.ls[0].outputs():
                if hou.node(str(self.selectLocationClicked())+'/SEP_CTRL') == None:
                    self.nullCtrl = hou.node(self.selectLocationClicked()+'/').createNode('null')
                    self.nullCtrl.setName('SEP_CTRL')
                    self.nullCtrl.setInput(0, self.ls[0])
                elif self.ls[0] == hou.node(self.selectLocationClicked()+'/SEP_CTRL'):
                    self.nullCtrl = hou.node(str(self.selectLocationClicked())+'/SEP_CTRL')
                else:
                    pass
                    # disconnect and reconnect SEP_CTRL
            else:
                hou.ui.displayMessage('SEP_CTRL node already exists')
                self.nullCtrl = hou.node(str(self.selectLocationClicked())+'/SEP_CTRL')
            self.nullCtrl.setGenericFlag(hou.nodeFlag.Display, True)
            self.nullCtrl.setGenericFlag(hou.nodeFlag.Render, True)
        else:
            hou.ui.displayMessage('Select a node')
        
    def selectLocationClicked(self):
        desktop = hou.ui.curDesktop()
        pane = desktop.paneTabOfType(hou.paneTabType.NetworkEditor)
        location = pane.currentNode().parent()
        return location.path()
        
    def spaceClicked(self):
        self.location.setText(self.selectLocationClicked())
        
    def sepClicked(self):
        if self.ls:
            self.sep = Separator(self.dirPath, self.space, self.customName.text(), self.newPos)
        else:
            hou.ui.displayMessage('Select a node')

            
win = SepUi()
win.show()

