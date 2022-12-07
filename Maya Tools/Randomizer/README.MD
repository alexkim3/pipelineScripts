# Randomizer
**This generator uses:** ![maya_icon](https://user-images.githubusercontent.com/44114036/192157730-b543643b-b461-447d-9779-70ba59b347d5.png)
![python_icon](https://user-images.githubusercontent.com/44114036/192157734-130bc0eb-741e-4805-9f56-1a00bc179fc3.png)


**Script category:** *Modeling, Layout*

Randomizer currently provides a possibilty to randomize main channels (translation, rotation and scale) for a large amount of objects. Using randomizer provides a realtime change reflection so its possible to have a quick overview and absolute control of the randomized result.

https://user-images.githubusercontent.com/44114036/196045130-96e3b30c-0d40-4ff8-9a79-e3642b719c60.mp4

## Features:

- **Add:** builds the channel randomization additionally from the lowest value object to the given destination value.
- **Fit:** The range is re-created and scaled between the given min-max range in UI.

    - Step: Aligns all the numbers into the step iterations
    - Align/Compress - compress the existing numbers into step in non-repeating way. So there are not 2 objects on the same position/rotation/scale and there is not a left number before the last iterated object.

The difference between add and fit aligners are mainly in the way of controlling placement. Add aligners works with the already existing placement of min and max, while Fit aligners controls placements with the controllers.



![Add_align](https://user-images.githubusercontent.com/44114036/196045144-db63da4c-7592-407e-84c3-1f4f102243c3.png)


![Fit_align](https://user-images.githubusercontent.com/44114036/196045146-f1c9e653-75fb-4ca7-ab39-560e0f5bba9d.png)



## Guides
1. Select gemetries to modify
2. Select channels to modify
3. Choose modify options from randomizer
4. Apply stores the values, seed changes the random variaton, reset reverts the values to the initial state

## Modules used:
1. Random
2. Functools
