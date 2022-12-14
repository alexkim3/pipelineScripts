# Relink Missing Material Paths Tool
**This generator uses:** ![maya_icon](https://user-images.githubusercontent.com/44114036/192157730-b543643b-b461-447d-9779-70ba59b347d5.png)
![python_icon](https://user-images.githubusercontent.com/44114036/192157734-130bc0eb-741e-4805-9f56-1a00bc179fc3.png)


**Script category:** *Modeling, Texturing*

Relocating missing textures manually might become time consuming for big scenes and in many cases moving files in working directory can't be fully avoided. 

![missingPaths](https://user-images.githubusercontent.com/44114036/192157654-83b61e5f-90e9-4db1-b897-105ef378a759.png)

This tool is created to handle task to relocate missing texture images with branching subfolders. It is important to give as direct path location as possible otherwise relocating process might become computing-heavy.

https://user-images.githubusercontent.com/44114036/192157370-6485e9a6-7b9a-4dfe-ac3d-9cdd44600038.mp4


## Guides
1. Run the script without selection (the relocation works for the whole scene)
2. Browse the file location or enter the path manually
3. Hit Apply to relocate the materials in the specified location

It is recommended to run the tool several times from the closest location level and relocate from multiple locations rather than input the higher level containing a big amount of files.
