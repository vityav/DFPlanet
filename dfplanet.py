import numpy as np
from matplotlib._png import read_png
import scipy.ndimage as ndimage
import visvis as vv

#Imports for matplotlib version
#import imageio
#import matplotlib.pyplot as plt
#from matplotlib.cbook import get_sample_data
#from mpl_toolkits.mplot3d import Axes3D
#from mayavi import mlab

#Smoothing function in case map edges are too sharp
def SmoothX(I,by):
    (width,height,colors)=np.shape(I)
    K=np.roll(I,by,axis=1)
    K[width-by:width,:,:]=ndimage.gaussian_filter(K[width-by:width,:,:],sigma=(by,by,0),order=0)
    K=np.roll(I,-1*by,axis=1)
    return K

#Control rotation of sphere
def onTimer(event):
    Rot.angle += 10
    if Rot.angle > 360:
        timer.Stop()
        Rot.angle = 0
    axes.Draw()


# Control parameters

# Flag and Gaussian kernel size for smoothing
Smooth=0
SmoothBy=250

# Scale factor for elevation. Scales grayscale value of pixel
scalefactor=1.0

# Image with surface features to draw
pngfile = 'region3_map.png'
img = read_png(pngfile)

# Image with underlying elevation map
pngfile = 'region3_el.png'
elev = read_png(pngfile)
if Smooth:
    img = SmoothX(img,SmoothBy)  #If you want to smooth the surface features
    elev = SmoothX(elev,SmoothBy)  #If you want to smooth the elevation map

# Can either use grayscale combination of all three color channels for elevation, or just pick one
#gray = 0.2989 * elev[:,:,0] + 0.5870 * elev[:,:,1] + 0.1140 * elev[:,:,2]
gray = elev[:,:,2]


pi = np.pi
cos = np.cos
sin = np.sin
sqrt = np.sqrt

(width,height,colors)=np.shape(elev)

# Create grid to match the image shape
phi, theta = np.mgrid[0:pi:width*1j, 0:2*pi:height*1j]


# Set radius as scaled version of grayscale values.
r = 5 + (np.sqrt((gray+1))-1) * scalefactor

# Equirectangular parametric equations to convert 2D map to 3D projection
x = r * sin(phi) * cos(theta)
y = r * sin(phi) * sin(theta)
z = r * cos(phi) #+ 0.5* sin(sqrt(x**2 + y**2)) * cos(2*theta)

#  ____  _       _
# |  _ \| | ___ | |_
# | |_) | |/ _ \| __|
# |  __/| | (_) | |_
# |_|   |_|\___/ \__|


vv.figure()
vv.axis('off')
k = vv.surf(x,y,z,img)

# If you turn on edge shading, things get weird
k.faceShading='smooth'
k.edgeShading=None
Rot = vv.Transform_Rotate(1)
k.transformations.insert(0,Rot)
axes = vv.gca()

# Zoom
axes.SetLimits(margin=0.0)
axes.SetLimits(margin=0.0,rangeX=(-1,1))

# Control lighting
#axes.bgcolor='k'
# axes.light0.ambient = 0.0 # 0.2 is default for light 0
# axes.light0.diffuse = 0.0 # 1.0 is default
axes.light0.Off()
light1 = axes.lights[1]
light1.On()
light1.ambient = 0.8
light1.diffuse = 1.0
light1.isDirectional = True
light1.position = (2,-4,2,0)
rec = vv.record(vv.gcf())

# Timer for controlling rotation speed
timer = vv.Timer(axes, 100, False)
timer.Bind(onTimer)
timer.Start(interval=1)
app = vv.use()
app.Run()

# Output movie to gif
rec.Stop()
rec.Export('movie.gif')


# Old code that used matplotlib, which is like 10 times slower, but left in
# since visvis is discontinued

# grayimg = 0.2989 * img[:,:,0] + 0.5870 * img[:,:,1] + 0.1140 * img[:,:,2]
# mlab.figure(bgcolor=(1,1,1))
# #mlab.mesh(x,y,z,scalars=grayimg,colormap='gist_earth')
# mlab.mesh(x,y,z,color=img)
# mlab.show()

# fig = plt.figure()
# fig.set_size_inches(9, 9)
# ax = fig.add_subplot(111, projection='3d', label='axes1')
#
# # Drape the image (img) on the globe's surface
# sp = ax.plot_surface(x, y, z, \
#                 rstride=2, cstride=2, \
#                 facecolors=img)
#
# ax.set_aspect(1)
#
# plt.show()
