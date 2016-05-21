import vtk

from actors.actor import Actor


class Cube(Actor):
    def __init__(self, length, position=(0, 0, 0), **kwargs):
        cube = vtk.vtkCubeSource()
        cube.SetXLength(length)
        cube.SetYLength(length)
        cube.SetZLength(length)
        cube.SetCenter(position)
        cube.Update()

        super(Cube, self).__init__(cube, position, **kwargs)
