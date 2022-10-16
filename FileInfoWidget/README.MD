# File Info Widget
**This generator uses:** ![maya_icon](https://user-images.githubusercontent.com/44114036/192157730-b543643b-b461-447d-9779-70ba59b347d5.png)
![python_icon](https://user-images.githubusercontent.com/44114036/192157734-130bc0eb-741e-4805-9f56-1a00bc179fc3.png)


**Script category:** *Pipeline*

The tool is created to give a better overwiev on file/version changes when many people are working on the same assets/projects. The widget contains information about the file author, file modification time and image/animated thumbnail if provided while saving the file. The widget uses QtWidgets from PySide2.



This tool is created to handle task to relocate missing texture images with branching subfolders. It is important to give as direct path location as possible otherwise relocating process might become computing-heavy.


## Guides
The tool can work as a stand-alone layout. However joining the widget to the existing layout with the file access code is recommended.

1. Generate the user SID dictionary (instructions in fileDetails.py in the bottom)
2. Edit string to your file paths in FileInforWidget.py line 140.

## Modules
1. PySide2
2. shiboken2
3. os
4. OpenMaya