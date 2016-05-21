import cv2  # OpenCV namespace
import numpy as np
import vtk


class Background(object):
    """
    This class captures the image from the video camera by means of OpenCV
    and renders it as the deepest layer of a VTK RenderWindow in order to
    overlap other content.
    """
    def __init__(self):
        """ Class constructor """

        # Initialize the OpenCV object responsible for acquire the images
        self.capture = cv2.VideoCapture(0)

        # Initialize the VTK object that is going to translate the image
        self.image = vtk.vtkImageImport()
        self.image.SetDataScalarTypeToUnsignedChar()

        # Three color layers
        self.image.SetNumberOfScalarComponents(3)

        # Image dimensions
        width, height = self.size
        self.image.SetDataExtent(0, width-1, 0, height-1, 0, 0)
        self.image.SetWholeExtent(0, width-1, 0, height-1, 0, 0)
        self.update()

        # Initialize render and assign the deepest layer
        self.render = vtk.vtkRenderer()
        self.render.SetLayer(0)
        self.render.InteractiveOff()

        # In VTK renders objects are shown through actors, like in a movie
        self.image_actor = vtk.vtkImageActor()
        image_port = self.image.GetOutputPort()
        self.image_actor.GetMapper().SetInputConnection(image_port)

        # Place actor into action
        self.render.AddActor(self.image_actor)

    def get_frame(self):
        return self.capture.read()[1]

    @property
    def size(self):
        """
        Get camera image width and height in pixels
        """

        frame = self.get_frame()

        # Unpack array dimensions
        height, width, layers = np.array(frame).shape

        return width, height

    def update(self):
        # Get what the camera is seeing
        frame = self.get_frame()

        # This step is a bit tricky. For a curious reason, OpenCV handels
        # images in BGR instead of the most common RGB color layer order.
        # In addition, pixels are sorted top-down rows and left-right columns.
        # Meanwhile, VTK shows images in RGB and dows it bottom-up.
        # That's why there's a need of rearranging pixels in order to visualize
        # images properly.
        # After translating the image into a Numpy array, a switch is done in:
        # * First index => changes rows.
        # * Second is left as it is, otherwise a specular image would be shown.
        # * Third index => BGR to RGB.
        image = np.array(frame)[::-1, :, ::-1]

        # I don't really like this step, but I haven't found a nicer way to
        # pass the image information to VTK. I consider it too obscure because
        # it is done translating the Numpy array into a string and then passing
        # it to the VTK image importer with its length.
        # If you know a more natural approach to this step, please let me know.
        image_str = image.tostring()
        self.image.CopyImportVoidPointer(image_str, len(image_str))


def test_background():
    """
    Unit test of Background class.
    Test is passed by means of visualization, this is, getting on screen the
    image that the camera is capturing in real time.
    """

    # Create a Background instance
    test_background = Background()

    # Create a VTK Render Window to display the video capture
    renWin = vtk.vtkRenderWindow()

    # Set Window Size with the camera actual resolution
    renWin.SetSize(*test_background.size)

    # Link the Render to the Window
    renWin.AddRenderer(test_background.render)

    while True:
        test_background.update()
        renWin.Render()


if __name__ == '__main__':
    test_background()
