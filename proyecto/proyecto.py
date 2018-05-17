def model():
    """
    Draws a cube at an angle so it is more interesting
    """
    r = Render(800, 600)
    t = Texture('./models/model.bmp')
    r.load('./models/model.obj', (1, 1, 1), (300, 300, 300), texture=t)
    r.display('out.bmp')