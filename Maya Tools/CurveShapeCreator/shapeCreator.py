def copyCurve(pCurves, pIndx, pName, pSeparateList, curveFormIndex):
    oldPos = cmds.getAttr( pCurves + '.cv[*]' )
    newPos = oldPos
    if curveFormIndex == 2:
        newPos.append( oldPos[0] )
        newPos.append( oldPos[1] )
        newPos.append( oldPos[2] )
        
    for vec in newPos:
        print('{}{}.append( ( {}, {}, {} ) )' .format(pSeparateList, pIndx, vec[0], vec[1], vec[2] ) )

    #if curve is periodic
    if curveFormIndex == 2:
        
        #############  get the knots  #################
        cmds.createNode( 'curveInfo', name = "curveInfo" + str(pIndx) )
        cmds.connectAttr( pCurves + '.worldSpace', "curveInfo" + str(pIndx) + '.inputCurve' )
        knot = cmds.getAttr( "curveInfo" + str(pIndx) + '.knots[*]' )
        print('knot = {}'.format(knot))
    
        ############  create a curve  #################
        cmds.delete("curveInfo" + str(pIndx))
        print('{}_crv{} = cmds.curve( per=True, p={}{}, name=\'{}_crv{}\', k=knot )'.format( pName, pIndx, pSeparateList, pIndx, pName, pIndx ))
        
    else:
        ############# the curve is open ###############
        print('{}_crv{} = cmds.curve( p={}{}, name=\'{}_crv{}\')'.format( pName, pIndx, pSeparateList, pIndx, pName, pIndx )) 

def getCurveHierarchy(objectList):
    if not objectList:
        print 'no curve selected'
    else:
        pSepListPrefix = 'piece'
        for curveShape in objectList:
            
            ############  check shape children ###########
            listChildren = cmds.listRelatives(curveShape, shapes = True, children=True, path=True)
            print(curveShape + 'List' + ' = []\n')
            for indx, curves in enumerate(listChildren):
                formIndex = cmds.getAttr(curves + '.form')
                print("\n{}{} = [] \n".format(pSepListPrefix, indx))
                copyCurve(curves, indx, curveShape, pSepListPrefix, formIndex)

            # get the strings from the shapeList without quotes ''
            strShapeList = [pSepListPrefix + str(posMem) for posMem in range(len(listChildren))]
            print('\n' + curveShape + 'List' + '= [{}]'.format(', '.join(map(str, strShapeList))) )
        
############  get the selection   ############
selList = cmds.ls(selection=True)
getCurveHierarchy(selList)
cmds.select(selList)