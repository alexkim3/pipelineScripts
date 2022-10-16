# Randomizer
**This generator uses:** ![maya_icon](https://user-images.githubusercontent.com/44114036/192157730-b543643b-b461-447d-9779-70ba59b347d5.png)
![python_icon](https://user-images.githubusercontent.com/44114036/192157734-130bc0eb-741e-4805-9f56-1a00bc179fc3.png)


**Script category:** *Modeling, Layout*

Randomizer currently provides a possibilty to randomize main channels (translation, rotation and scale) for a large amount of objects. Using randomizer provides a realtime change reflection so its possible to have a quick overview and absolute control of the randomized result.

## Features:

- **Add:** builds the channel randomization additionally from the lowest value object to the given destination value.
- **Fit:** The range is re-created and scaled between the given min-max range in UI.

    - Step: Aligns all the numbers into the step iterations
    - Align/Compress - compress the existing numbers into step in non-repeating way. So there are not 2 objects on the same position/rotation/scale and there is not a left number before the last iterated object.

The difference between add and fit aligners are mainly in the way of controlling placement. Add aligners works with the already existing placement of min and max, while Fit aligners controls placements with the controllers.




## Guides
1. Select gemetries to modify
2. Select channels to modify
3. Choose modify options from randomizer
4. Apply stores the values, seed changes the random variaton, reset reverts the values to the initial state

## Modules used:
1. Random
2. Functools