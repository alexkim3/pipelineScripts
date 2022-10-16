import maya.cmds as cmds
from random import *
from functools import partial

class Randomizer():

    def __init__(self):
        
        self.Ui()

        self.distanceValue = cmds.floatSliderGrp(self.distance, query=True, value=True)
        self.multiplyAmount = cmds.floatSliderGrp(self.multiplier, query=True, value=True)
        self.minValue = float(cmds.floatSliderGrp(self.minSlider, query=True, value=True))
        self.maxValue = float(cmds.floatField(self.maxSliderAmount, query=True, value=True))

        self.initializeNewChannels()

        self.attribMove = cmds.scriptJob( event= ["ChannelBoxLabelSelected",partial(self.checkSelection, 'channel')])
        self.changingGeoSel = cmds.scriptJob( event=["SelectionChanged",partial(self.checkSelection, 'geometry')])

        if (len(self.objects)> 0 and self.channels!=None):
            self.checkSelection('channel')
        else:
            self.checkSelection('geometry')

    def initializeNewChannels(self):
        self.objects = cmds.ls(sl=True, type='transform')
        self.channels = cmds.channelBox('mainChannelBox', query=True, selectedMainAttributes=True)

    def checkSelection(self, status):
        self.initializeNewChannels()
        
        if status == 'geometry':
            if (len(self.objects)> 0 and self.channels!=None):
                status=True
                self.generateRandomDict()
            else:
                status = False

        elif status == 'channel':
            status = True
            self.generateRandomDict()

        cmds.radioButtonGrp(self.operations, edit=True, enable=status)
        cmds.floatSliderGrp(self.distance, edit=True, enable=status)
        cmds.floatSliderGrp(self.multiplier, edit=True, enable=status)
        cmds.floatSliderGrp(self.minSlider, edit=True, enable=status)
        cmds.formLayout(self.maxSlider, edit=True, enable=status)
        cmds.checkBox(self.step, edit=True, enable=status)

    def operationChanged(self, *args):
        operation = cmds.radioButtonGrp(self.operations, query=True, select=True)

        if operation == 1:
            cmds.floatSliderGrp(self.distance, edit=True, manage=True)
            cmds.floatSliderGrp(self.multiplier, edit=True, manage=True)
            cmds.floatSliderGrp(self.minSlider, edit=True, manage=False)
            cmds.formLayout(self.maxSlider, edit=True, manage=False)

            cmds.checkBox(self.alignCheck, edit=True, label='Compress', annotation='Pushes all the geometry to start from the minimum value and doesnt skip a step size during the iteration')
            cmds.radioButton(self.alignUniformly, edit=True, manage=False)

        elif operation == 2:
            cmds.floatSliderGrp(self.distance, edit=True, manage=False)
            cmds.floatSliderGrp(self.multiplier, edit=True, manage=False)
            cmds.floatSliderGrp(self.minSlider, edit=True, manage=True)
            cmds.formLayout(self.maxSlider, edit=True, manage=True)

            cmds.checkBox(self.alignCheck, edit=True, label='Align', annotation='')
            cmds.radioButton(self.alignUniformly, edit=True, manage=True)
            
        self.eval()

    def maxSliderChanged(self, *args):
        val = cmds.floatSlider(self.maxSliderSlider, query=True, value=True)
        cmds.floatField(self.maxSliderAmount, edit=True, value=val)
        self.sliderChanged()

    def multChanged(self, *args):
        self.multiplyAmount = cmds.floatSliderGrp(self.multiplier, query=True, value=True)
        self.eval()

    def sliderChanged(self, *args):
        if cmds.checkBox(self.alignCheck, query=True, value=True) == 0:
            cmds.floatSliderGrp(self.distance, edit=True, enable=True)
            cmds.floatSliderGrp(self.multiplier, edit=True, enable=True)
            
        elif cmds.checkBox(self.alignCheck, query=True, value=True) == 1:
            cmds.floatSliderGrp(self.distance, edit=True, enable=False)
            cmds.floatSliderGrp(self.multiplier, edit=True, enable=False)

        self.distanceValue = cmds.floatSliderGrp(self.distance, query=True, value=True)
        self.multiplyAmount = cmds.floatSliderGrp(self.multiplier, query=True, value=True)
        self.minValue = float(cmds.floatSliderGrp(self.minSlider, query=True, value=True))
        self.maxValue = float(cmds.floatField(self.maxSliderAmount, query=True, value=True))
        self.eval()

    def stepChanged(self, *args):
        stepCheck = cmds.checkBox(self.step, query=True, value=True)

        if stepCheck == 0:
            cmds.floatSliderGrp(self.distance, edit=True, enable=True)
            cmds.floatSliderGrp(self.multiplier, edit=True, enable=True)
            cmds.floatFieldGrp(self.stepSize, edit=True, enable=False)
            cmds.checkBox(self.alignCheck, edit=True, value=0)
            cmds.checkBox(self.alignCheck, edit=True, enable=False)
            cmds.radioButton(self.alignFromMin, edit=True, enable=False)
            cmds.radioButton(self.alignFromMax, edit=True, enable=False)
            cmds.radioButton(self.alignUniformly, edit=True, enable=False)

            
        elif stepCheck == 1:
            cmds.floatFieldGrp(self.stepSize, edit=True, enable=True)
            cmds.checkBox(self.alignCheck, edit=True, enable=True)

        self.eval()

    def alignChanged(self, *args):
        if cmds.checkBox(self.alignCheck, query=True, value=True) == True:
            cmds.radioButton(self.alignFromMin, edit=True, enable=True)
            cmds.radioButton(self.alignFromMax, edit=True, enable=True)
            cmds.floatSliderGrp(self.distance, edit=True, enable=False)
            cmds.floatSliderGrp(self.multiplier, edit=True, enable=False)
            if cmds.radioButtonGrp(self.operations, query=True, select=True) == 2:
                cmds.radioButton(self.alignUniformly, edit=True, enable=True)

        elif cmds.checkBox(self.alignCheck, query=True, value=True) == False:
            cmds.checkBox(self.step, edit=True, enable=True)
            cmds.floatFieldGrp(self.stepSize, edit=True, enable=True)
            cmds.radioButton(self.alignFromMin, edit=True, select=True)
            cmds.radioButton(self.alignFromMin, edit=True, enable=False)
            cmds.radioButton(self.alignFromMax, edit=True, enable=False)
            cmds.floatSliderGrp(self.distance, edit=True, enable=True)
            cmds.floatSliderGrp(self.multiplier, edit=True, enable=True)
            if cmds.radioButtonGrp(self.operations, query=True, select=True) == 2:
                cmds.radioButton(self.alignUniformly, edit=True, enable=False)

        self.eval()

    def spreadChange(self, *args):
        if cmds.radioButton(self.alignUniformly, query=True, select=True) == True:
            cmds.checkBox(self.step, edit=True, enable=False)
            cmds.floatFieldGrp(self.stepSize, edit=True, enable=False)

        elif cmds.radioButton(self.alignUniformly, query=True, select=True) == False:
            cmds.checkBox(self.step, edit=True, enable=True)
            cmds.floatFieldGrp(self.stepSize, edit=True, enable=True)

    def generateRandomDict(self, *args):
        if not cmds.checkBox(self.alignCheck, query=True, value=True) == 1:
            self.randomDict = {}
            for obj in self.objects:
                if self.channels !=None:
                    for attrib in self.channels:
                        objChannel =  obj + '.' + attrib
                        randInit = random()
                        self.prevVal = cmds.getAttr(obj+ '.' + attrib)
                        self.randomDict[objChannel] = (randInit, self.prevVal)

    def alignNumber(self, number, alignToNumber):
        return alignToNumber * round(number/alignToNumber)

    def eval(self, *args):
        
        stepVal = cmds.floatFieldGrp(self.stepSize, query=True, value1=True)
        if cmds.radioButtonGrp(self.operations, query=True, select=True) == 1:
            for obj, val in self.randomDict.items():
                self.setPlacement = val[1] + (val[0] * self.distanceValue * self.multiplyAmount)
                
                if cmds.checkBox(self.step, query=True, value=True) == 1:
                    self.setPlacement = self.alignNumber(self.setPlacement, stepVal)
                cmds.setAttr(obj, self.setPlacement)

        elif cmds.radioButtonGrp(self.operations, query=True, select=True) == 2:
            for obj, val in self.randomDict.items():
                dist = self.maxValue - self.minValue
                self.setPlacement = (val[0] * dist) + self.minValue

                if cmds.checkBox(self.step, query=True, value=True) == 1:
                    self.setPlacement = self.alignNumber(self.setPlacement, stepVal)
                cmds.setAttr(obj, self.setPlacement)

        # align
        if cmds.checkBox(self.alignCheck, query=True, value=True) == 1:
            keys = self.randomDict.keys()
            uniformPiece = abs(cmds.floatField(self.maxSliderAmount, query=True, value=True) - cmds.floatSliderGrp(self.minSlider, query=True, value=True)) / len(keys)

            for ch in self.channels:
                objChannels = []
                for obj in self.objects:
                    objChannels.append(cmds.getAttr(obj+ '.' + ch))

                    if cmds.radioButton(self.alignFromMin, query=True, select=True) == True:
                        if cmds.radioButtonGrp(self.operations, query=True, select=True) == 1:
                            minChannel = min(objChannels)
                        elif cmds.radioButtonGrp(self.operations, query=True, select=True) == 2:
                            minChannel = cmds.floatSliderGrp(self.minSlider, query=True, value=True)
                        values = [(stepVal * i) + minChannel for i in range(len(keys))]

                    elif cmds.radioButton(self.alignFromMax, query=True, select=True) == True:
                        if cmds.radioButtonGrp(self.operations, query=True, select=True) == 1:
                            maxChannel = max(objChannels)
                        elif cmds.radioButtonGrp(self.operations, query=True, select=True) == 2:
                            maxChannel = cmds.floatField(self.maxSliderAmount, query=True, value=True)
                        values = [maxChannel - (stepVal * i) for i in range(len(keys))]

                    elif cmds.radioButton(self.alignUniformly, query=True, select=True) == True:
                        minChannel = cmds.floatSliderGrp(self.minSlider, query=True, value=True)
                        values = [(uniformPiece * i) + minChannel for i in range(len(keys))]

                shuffle(values)
                shuffled = dict(zip(keys, values))
                for obj, val in shuffled.items():
                    cmds.setAttr(obj, val)
                        

    def zeroValues(self):
        cmds.floatSliderGrp(self.distance, edit=True, value=0)
        cmds.floatSliderGrp(self.multiplier, edit=True, value=1)
        cmds.floatSliderGrp(self.minSlider, edit=True, value=0)
        cmds.floatField(self.maxSliderAmount, edit=True, value=0)
        cmds.floatSlider(self.maxSliderSlider, edit=True, value=0)

    def applyPressed(self, *args):
        self.objects = cmds.ls(sl=True, type='transform')
        self.channels = cmds.channelBox('mainChannelBox', query=True, selectedMainAttributes=True)
        self.generateRandomDict()
        self.zeroValues()
        if cmds.checkBox(self.alignCheck, query=True, value=1):
            cmds.checkBox(self.step, edit=True, value=0)
            cmds.checkBox(self.alignCheck, edit=True, value=0)
            cmds.checkBox(self.alignCheck, edit=True, enable=False)
            cmds.floatSliderGrp(self.distance, edit=True, enable=True)
            cmds.floatSliderGrp(self.multiplier, edit=True, enable=True)
            cmds.radioButton(self.alignFromMin, edit=True, enable=False)
            cmds.radioButton(self.alignFromMax, edit=True, enable=False)


    def seedPressed(self, *args):
        if cmds.radioButtonGrp(self.operations, query=True, select=True) == 1:
            oldDist = cmds.floatSliderGrp(self.distance, query=True, value=True)
            oldMult = cmds.floatSliderGrp(self.multiplier, query=True, value=True)
            self.resetPressed()
            self.generateRandomDict()
            self.eval()
            cmds.floatSliderGrp(self.distance, edit=True, value=oldDist)
            cmds.floatSliderGrp(self.multiplier, edit=True, value=oldMult)

        elif cmds.radioButtonGrp(self.operations, query=True, select=True) == 2:
            oldMin = cmds.floatSliderGrp(self.minSlider, query=True, value=True)
            oldMax = cmds.floatField(self.maxSliderAmount, query=True, value=True)
            oldMaxSlider = cmds.floatSlider(self.maxSliderSlider, query=True, value=True)
            self.resetPressed()
            self.generateRandomDict()
            self.eval()
            cmds.floatSliderGrp(self.minSlider, edit=True, value=oldMin)
            cmds.floatField(self.maxSliderAmount, edit=True, value=oldMax)
            cmds.floatSlider(self.maxSliderSlider, edit=True, value=oldMaxSlider)

    def resetPressed(self, *args):
        for key, value in self.randomDict.items():
            cmds.setAttr(key, value[1])
        self.zeroValues()

    def killAllEventsAndReset(self, *args):
        if cmds.checkBox(self.alignCheck, query=True, value=True) == False:
            for key, value in self.randomDict.items():
                cmds.setAttr(key, value[1])
        cmds.scriptJob( kill=self.attribMove, force=True)
        cmds.scriptJob( kill=self.changingGeoSel, force=True)


    def Ui(self):

        if cmds.window( 'randomizer_Window', exists=True) :
            cmds.deleteUI( 'randomizer_Window' )

        width = 345
        height = 470
        randWindow = cmds.window('randomizer_Window', title='Randomizer', closeCommand=self.killAllEventsAndReset, resizeToFitChildren=True)
        mainWindow = cmds.formLayout(numberOfDivisions=100, parent=randWindow, width=width, height=height)
        titleImg = cmds.image(image="C:/Users/alexandrakimbui/Desktop/images/randLogo.png", parent=mainWindow)
        attribsImg = cmds.image(image="C:/Users/alexandrakimbui/Desktop/images/randAttribsImage.png", parent=mainWindow)
        instructions = cmds.text( label='- Select geo/s', align='left', font='obliqueLabelFont', parent=mainWindow )
        instructions2 = cmds.text( label='- Select channel/s', align='left', font='obliqueLabelFont', parent=mainWindow )
        instructions3 = cmds.text( label='- Choose randomize operations', align='left', font='obliqueLabelFont', parent=mainWindow )
        self.operations = cmds.radioButtonGrp( label='', columnWidth3=[0, 50, 50], labelArray2=['Add', 'Fit'], numberOfRadioButtons=2, select=1, changeCommand1=self.operationChanged, parent = mainWindow)
        self.distance = cmds.floatSliderGrp( label='Distance', field=True , columnWidth3=[50, 30, 150], value=0, minValue=0, maxValue=50, manage=True, enable=False, changeCommand=self.sliderChanged, dragCommand=self.sliderChanged, parent = mainWindow, annotation='Random values in the set distance starting from the minimal existing position')
        self.multiplier = cmds.floatSliderGrp( label='Multiplier', field=True , columnWidth3=[50, 30, 150], value=1, changeCommand=self.multChanged, dragCommand=self.multChanged, parent = mainWindow)
        
        self.minSlider = cmds.floatSliderGrp( label='Min', field=True , columnWidth3=[50, 30, 70], value=0, minValue=-50, maxValue=0, changeCommand=self.sliderChanged, dragCommand=self.sliderChanged, manage=False, parent = mainWindow)
        self.maxSlider = cmds.formLayout(manage=False)
        self.maxSliderSlider = cmds.floatSlider( width=80, changeCommand=self.sliderChanged, dragCommand=self.maxSliderChanged, minValue=0, maxValue=50, value=0, parent = self.maxSlider)
        self.maxSliderAmount = cmds.floatField(width = 30, precision=1, parent = self.maxSlider)
        maxSliderText = cmds.text(l='Max', width=30, parent = self.maxSlider)
        
        self.step = cmds.checkBox(label = ' Step', changeCommand=self.stepChanged, parent=mainWindow)
        self.stepSize = cmds.floatFieldGrp(label = 'Step size', value1=1.0, numberOfFields=1,columnWidth2=[60, 30], enable=False, changeCommand=self.sliderChanged, parent = mainWindow, annotation='aligns all the selected objects into the closest step iterations')

        self.nameAligners = cmds.text(l='Aligners', font='obliqueLabelFont', parent = mainWindow)
        self.aligners = cmds.formLayout(parent = mainWindow, backgroundColor=[0.2,0.2,0.2], height=85)
        self.alignCheck = cmds.checkBox(label = ' Compress', manage=True, enable=False, changeCommand=self.alignChanged, parent=self.aligners, annotation='Pushes all the geometry to start from the minimum value and doesnt skip a step size iteration')
        self.addAligners = cmds.radioCollection( parent=self.aligners)
        self.alignFromMin = cmds.radioButton(label='From Min', select=True, enable=False, changeCommand=self.eval, parent=self.aligners)
        self.alignFromMax = cmds.radioButton(label='From Max', enable=False, parent=self.aligners)
        self.alignUniformly = cmds.radioButton(label='Spread uniformly', manage=False, enable=False, changeCommand=self.spreadChange, parent=self.aligners)

        cmds.formLayout(self.aligners, edit=True, attachForm=[(self.alignCheck, 'left', 5), (self.alignCheck, 'top', 3), 
                                                              (self.alignUniformly, 'left', 5),(self.alignFromMin, 'left', 5),(self.alignFromMax, 'left', 5)],
                                               attachControl=[(self.alignFromMin, 'top', 2, self.alignCheck),
                                                              (self.alignFromMax, 'top', 2, self.alignFromMin),
                                                              (self.alignUniformly, 'top', 2, self.alignFromMax)])

        self.helpImage = cmds.checkBox( label = 'Help image', enable=False, parent = mainWindow, annotation='TBC')
        
        apply = cmds.button(label = 'Apply',width=width/3-10, command=self.applyPressed, parent = mainWindow)
        seed = cmds.button(label = 'Seed', width=width/3-10, command=self.seedPressed, parent = mainWindow)
        reset = cmds.button(label = 'Reset',width=width/3-10, command=self.resetPressed, parent = mainWindow)
        
        cmds.formLayout(self.maxSlider, edit=True, attachForm=[(self.maxSliderSlider, 'top', 3), (self.maxSliderAmount,'top', 0), (maxSliderText, 'right', 0), (maxSliderText, 'top', 3)], 
                                             attachControl=[(self.maxSliderSlider, 'right', 3, self.maxSliderAmount), (self.maxSliderAmount, 'right', 3, maxSliderText)])

        cmds.formLayout(mainWindow, edit=True, attachForm=[(titleImg, 'top', 22),
                                                           (instructions, 'left', 100), (instructions2, 'left', 100), (instructions3, 'left', 100),
                                                           (apply, 'bottom', 10), (apply, 'left', 10), 
                                                           (reset, 'bottom', 10), (reset, 'right', 10),
                                                           (seed, 'bottom', 10),
                                                           (self.helpImage, 'top', 400),
                                                           (self.aligners, 'right', 0), (self.aligners, 'top', 336), 
                                                           (self.nameAligners, 'right', 20)],
                                           attachPosition=[(titleImg, 'left', 22, 0),
                                                           (attribsImg, 'left', 22, 0),
                                                           (self.operations, 'left', 120, 0),
                                                           (self.distance, 'left', 50, 0), (self.maxSlider, 'left', 170, 0),
                                                           (self.minSlider, 'left', 10, 0),
                                                           (self.multiplier, 'left', 50, 0),
                                                           (self.step, 'left', 10, 0), (self.stepSize, 'left', 92, 0),
                                                           (self.helpImage, 'left', 10, 0)],
                                            attachControl=[(attribsImg, 'top', 5, titleImg),
                                                           (instructions, 'top', 5, attribsImg),
                                                           (instructions2, 'top', 5, instructions),
                                                           (instructions3, 'top', 5, instructions2),
                                                           (self.operations, 'top', 100, titleImg),
                                                           (self.distance, 'top', 6, self.operations),
                                                           (self.minSlider, 'top', 6, self.operations),
                                                           (self.maxSlider, 'top', 6, self.operations),
                                                           (self.multiplier, 'top', 32, self.operations),
                                                           (self.step, 'top', 7, self.multiplier),
                                                           (self.stepSize, 'top', 5, self.multiplier),
                                                           (self.aligners, 'left', 15, self.stepSize), 
                                                           (self.nameAligners, 'bottom', 0, self.aligners),
                                                           (apply, 'right', 5, seed), (seed, 'right', 5, reset)])

        cmds.showWindow(randWindow)

newWin = Randomizer()