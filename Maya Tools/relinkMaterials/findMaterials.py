import os

class relinkPathsWin():
    def getFolderPath(self, *args):
        filename = cmds.fileDialog2(fileMode=3, caption="Select path")
        cmds.textField(self.inputLocation, e=True, text=filename[0])
        
        
    def relinkPaths(self, *args):
        location = cmds.textField(self.inputLocation, query=True, text=True)
        if location:
            filePaths = [location]
            subFilePaths = []
            for filePath in filePaths:
                subFilePaths = subFilePaths + [x[0] for x in os.walk(filePath)]
                
            for subFilePath in subFilePaths:
                for fileObj in allMaterials:
                    oldPath = cmds.getAttr(fileObj + '.fileTextureName')
                    if os.path.isfile(oldPath) == False:
                        fileName = '/' + oldPath.split('/')[-1]
                        if os.path.isfile(subFilePath + fileName):
                            cmds.setAttr(fileObj + '.fileTextureName', subFilePath+'\\'+fileName, type='string')
    
    ################################
    ############  UI  ##############
    ################################
    
    def __init__( self, selected ):

        window = "relinkPaths"
        if cmds.window( window, exists=True ) :
            cmds.deleteUI( window )
        
        width = 500
        height = 70
        window = cmds.window( window, title='Relink paths to locate textures',sizeable=False, width=width, height=height, resizeToFitChildren=True )
        
        cmds.rowColumnLayout(width=width, height=40, numberOfColumns=4, columnWidth=[(1, width*0.02), (2, width*0.17), (3, width*0.68), (4, width*0.1)] )
        cmds.separator( height=20, style='none' )
        cmds.separator( height=20, style='none' )
        cmds.separator( height=20, style='none' )
        cmds.separator( height=20, style='none' )
        
        cmds.separator( style="none" )
        cmds.text( label='Folder location:')
        self.inputLocation = cmds.textField()
        cmds.button('Browse',command=self.getFolderPath)
        cmds.setParent('..')
        
        cmds.rowColumnLayout(width=width, numberOfColumns=3, columnWidth=[(1, width*0.4), (2, width*0.2), (3, width*0.4)] )
        cmds.separator( height=10, style='none' )
        cmds.separator( height=10, style='none' )
        cmds.separator( height=10, style='none' )
        
        cmds.separator( style="none" )
        cmds.button(l='Apply', c=self.relinkPaths)
        cmds.setParent('..')

        cmds.showWindow(window)

cmds.select(cmds.ls(type='file'))
allMaterials = cmds.ls(sl=True)
findMat = relinkPathsWin()

