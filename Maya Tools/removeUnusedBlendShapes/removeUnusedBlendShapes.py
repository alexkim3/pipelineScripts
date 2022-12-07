import re

def removeUnusedBlendShapes():
    blendShapeNodeList = cmds.ls(type='blendShape')
    inputTargetGroupRegex = re.compile('inputTarget\[\d+\]\.inputTargetGroup\[(\d+)\]$')
    cmds.select(d=True)
    
    for bs in blendShapeNodeList:
        multiAttrList = cmds.listAttr(bs, multi=True)
        weightIndexToInputTargetGroupDict = {inputTargetGroupRegex.match(attr).group(1): attr for attr in multiAttrList if inputTargetGroupRegex.match(attr)}
        for targetIndexNum in weightIndexToInputTargetGroupDict.keys():
            if not cmds.listConnections(bs + ".w[{}]".format(targetIndexNum)):
                cmds.removeMultiInstance(bs + ".weight[{}]".format(targetIndexNum), b=True)  
                inputTargetGroupAttr = weightIndexToInputTargetGroupDict[targetIndexNum]
                cmds.removeMultiInstance(bs + "." + inputTargetGroupAttr, b=True)

removeUnusedBlendShapes()