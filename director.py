from time import time, sleep

import numpy as np
import vtk

from actors.cube import Cube
from background import Background


class Director(object):
    """
    This class controls the whole scene
    """
    def __init__(self, dt=0.1, auto_dt=False):
        """
        Class constructor
        """

        self.background = Background()
        # check width and height
        ret, cap = self.background.capture.read()
        height, width, channels = np.array(cap).shape

        self.render = vtk.vtkRenderer()
        self.render.SetLayer(2)

        # self.camera = vtk.vtkCamera()
        # self.camera.SetPosition(-10, 0, 0)
        # self.camera.SetFocalPoint(0, 0, 0)
        # self.render.SetActiveCamera(self.camera)
        # self.render.ResetCamera()

        self.render_window = vtk.vtkRenderWindow()
        self.render_window.SetSize(width, height)
        self.render_window.AddRenderer(self.background.render)
        self.render_window.AddRenderer(self.render)

        self.t = 0
        self.dt = dt
        self.auto_dt = auto_dt

        self.actors = []

    def add_actor(self, actor):
        self.actors.append(actor)
        self.render.AddActor(actor.actor)

    def pause(self):
        self.keep_playing = False

    def play(self):
        self.keep_playing = True
        t0 = time()

        self.run_events()

        # update
        self.update()

        self.render_window.Render()

        dt = time() - t0
        if dt < self.dt:
            sleep(self.dt - dt)

        if self.keep_playing:
            self.play()

    def run_events(self):
        pass

    def stop(self):
        self.keep_playing = False
        self.render_window.Finalize()

    def update(self):
        self.background.update()
        for actor in self.actors:
            actor.update(dt=self.dt)


if __name__ == '__main__':

    cube = Cube(length=1)

    render = Director(dt=1)
    render.add_actor(cube)
    render.play()
