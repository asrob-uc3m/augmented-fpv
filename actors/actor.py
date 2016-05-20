import numpy as np
import vtk


class Actor(object):
    def __init__(self, vtk_src, position=(0, 0, 0), direction=(0, 0, 1),
                 speed=(0, 0, 0), angular_speed=(0, 0, 0),
                 acceleration=(0, 0, 0), angular_acceleration=(0, 0, 0)):

        self.vtk_src = vtk_src
        self.transform = vtk.vtkTransform()
        self.transform_filter = vtk.vtkTransformPolyDataFilter()
        self.transform_filter.SetInputConnection(vtk_src.GetOutputPort())
        self.transform_filter.SetTransform(self.transform)
        self.transform_filter.Update()
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.transform_filter.GetOutputPort())
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)

        self.position = np.array(position)
        self.direction = np.array(direction)
        self.speed = np.array(speed)
        self.angular_speed = np.array(angular_speed)
        self.acceleration = np.array(acceleration)
        self.angular_acceleration = np.array(angular_acceleration)

    def update(self, dt):
        self.speed = self.speed + self.acceleration * dt
        self.position = self.position + self.speed * dt

        self.angular_speed = self.angular_speed + self.angular_acceleration * dt
        theta = self.angular_speed * dt
        theta_norm = np.linalg.norm(theta)
        if not np.isclose(theta_norm, 0):
            theta_unit = theta / theta_norm
            normal = np.cross(theta_unit, self.direction)
            # TODO: continue developoing turn

        self.update_vtk_data()

    def update_vtk_data(self):
        self.transform.Translate(*self.position)
        self.transform_filter.Update()
        # TODO: continue developing transformation
