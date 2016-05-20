import cv2
import numpy as np
import vtk


class Background(object):
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.image = vtk.vtkImageImport()
        self.update()

        self.render = vtk.vtkRenderer()
        self.render.SetLayer(0)

        self.image_actor = vtk.vtkImageActor()
        image_port = self.image.GetOutputPort()
        self.image_actor.GetMapper().SetInputConnection(image_port)
        self.render.AddActor(self.image_actor)

    def update(self):
        ret, frame = self.capture.read()

        image = np.array(frame)[::-1, ::-1, ::-1]
        height, width, channels = image.shape

        image_str = image.tostring()
        self.image.CopyImportVoidPointer(image_str, len(image_str))

        self.image.SetDataScalarTypeToUnsignedChar()
        self.image.SetNumberOfScalarComponents(3)

        self.image.SetDataExtent(0, width-1, 0, height-1, 0, 0)
        self.image.SetWholeExtent(0, width-1, 0, height-1, 0, 0)


if __name__ == '__main__':
    b = Background()
    ret, cap = b.capture.read()
    print np.array(cap).shape

    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(640, 480)
    renWin.AddRenderer(b.render)
    while True:
        b.update()
        renWin.Render()
