import vtk


def create_camera(position=(0, 0, 0), focal_point=(1, 0, 0),
                  view_up=(0, 0, 1), zoom=1):
    camera = vtk.vtkCamera()
    camera.SetPosition(*position)
    camera.SetFocalPoint(*focal_point)
    camera.SetViewUp(*view_up)
    camera.Zoom(zoom)

    return camera


def create_render(window_size, window_name, bg_color=(1, 1, 1)):
    ren = vtk.vtkRenderer()
    ren_win = vtk.vtkRenderWindow()

    ren_win.AddRenderer(ren)
    ren_win.SetWindowName(window_name)
    ren_win.SetSize(*window_size)

    ren.SetBackground(bg_color)

    return ren, renWin
