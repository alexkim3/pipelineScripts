# Shape script creator

**This generator uses:** ![maya_icon](https://user-images.githubusercontent.com/44114036/192157730-b543643b-b461-447d-9779-70ba59b347d5.png)
![python_icon](https://user-images.githubusercontent.com/44114036/192157734-130bc0eb-741e-4805-9f56-1a00bc179fc3.png)


**Script category:** *Modeling, Rigging*

This shape script creator is a generator of python code, which can duplicate and write a new curve.

This tool works for EP and CV curves. Applying to the selected curve the code generates a new python coordinates script list. When the printed script is run, a new duplicated curve is created in the Maya scene.

The reason why the code is creating a next code as a sub-step is to create a shape library for which the generator was created for. The new shape library can be then stored and serve as a tool for creating new curves e.g. for rigging controllers.

It is important to have no more parent levels than 1 (1st level of children), to have EP or CV curves selected (doesn't work for bezier curves) and to not have namespaces in the applied curve.

https://user-images.githubusercontent.com/44114036/192155535-d413363e-c6f1-4136-b324-0adddc42ea14.mov

## Guides

1. Select a curve in a scene. More than 1 curve can be selected, but the hierarchy can not be bigger than 1 branch (ungroup the grouped curves first)
2. Run the script shapeCreator.py
3. Select the generated code
4. Add the code to your shape library or run the generated code to duplicate the curve directly



