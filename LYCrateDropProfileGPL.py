# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
import math
from math import sin, cos, radians
import mathutils
import bmesh
import numpy as np
from scipy.integrate import odeint
"""
Name: This Script
Purpose:
Generate 2 Objects in Blender
1 YLProfile
2 YLDrop
by using ODE Solver odeint of the scipy package and some blender python voodoo
naming the objects includes shape parameter beta and Scriptversion
Young - Laplace
Sessile Drop .. Pendant Drop ..Adams Bashford .. Andreas .. Gauss .. Capillary Interaction
"""

"""
Set Parameters
"""

Scriptversion = 0.01
def beta():
	return(5.)

#set to zero to use default
def segments():
	return(16)




"""
Run
"""


"""
Math part .. should work in any python
"""



def yl_ds(y,s):
    """
	simlpe Young Laplace Integrator
    """
    lB = beta()
    dy0 = np.cos(y[2])
    dy1 = np.sin(y[2])
    dy2 = 2 - lB*y[1] - np.sin(y[2])/y[0]
    return [dy0, dy1, dy2]
n_verts = 120

"""
Define reasonable ranges for s and solve
"""

zero_eps = 0.0000001
if beta() > 0. :
    if segments() > 0 : 
        n_verts = segments() 
    else : 
        n_verts = 50
    s = np.arange(0, 5 * math.pi, 0.1)
    y0 = [zero_eps,zero_eps , 0.]
    y = odeint(yl_ds, y0, s)

if beta() < 0. :
    if segments() > 0 : 
        n_verts = segments() 
    else : 
        n_verts = 35
    s = np.arange(0, 2. * math.pi, 0.1)
    y0 = [zero_eps,zero_eps , 0.]
    y = odeint(yl_ds, y0, s)
    
    
#calculate volume
Volume = 0
#VolArr =[0]
#step over Y
#a = 0

for n in range(n_verts ):
    #cylinder volume
    h = y[ n+1,1]-y[n,1] #thickness of the slice
    r = (y[n+1,0]+y[n,0])/2. # av x see trapezregel
    voc = r*r*h *math.pi
    Volume +=voc
    #VolArr.append(voc)
#return Vol
# debug print
#print(VolArr)

print(Volume)


# debug print
#print(y)




"""
Blender part .. creates a meshes and objects
"""



#building  vertex array
z_float = 0.0
Verts = []
Edges = []

for i in range(n_verts):
    x_float = y[i,0]
    y_float = y[i,1]
    Verts.append((x_float, y_float, z_float))
    

#building  edge array
for i in range(n_verts-1):
#   close poloygan if you want
#   if i == n_verts-1:
#       Edges.append([i, 0])
#       break
    Edges.append([i, i+1])

# build Profile
name = 'YLProfilefileMeshData:B {:.2}V{:}_'.format(beta(),Scriptversion)
profile_mesh = bpy.data.meshes.new(name)
profile_mesh.from_pydata(Verts, Edges, [])
profile_mesh.update()


name = 'YLProfilefile:B {:.2}V{:}_'.format(beta(),Scriptversion)
profile_object = bpy.data.objects.new(name, profile_mesh)
profile_object.data = profile_mesh

scene = bpy.context.scene
scene.objects.link(profile_object)
profile_object.select = True

# build surface eith spin function
# Make a new BMesh
bm = bmesh.new()
bm.from_mesh(profile_mesh)   # fill it in from a Mesh)


# Spin and deal with geometry on side 'a
edges_start_a = bm.edges[:]
geom_start_a = bm.verts[:] + edges_start_a
ret = bmesh.ops.spin(
        bm,
        geom=geom_start_a,
        angle=math.radians(360.0),
        steps=36,
        axis=(0.0, 1.0, 0.0),
        cent=(0.0, 0.0, 0.0))
edges_end_a = [ele for ele in ret["geom_last"]
               if isinstance(ele, bmesh.types.BMEdge)]
del ret
del profile_object 

# Finish up, write the bmesh into a new mesh
name = 'YLDropMesh:Beta {:.2}V_'.format(beta())
me = bpy.data.meshes.new(name)
bm.to_mesh(me)
bm.free()

name = 'YLDrop:Beta {:.2}Vol{:.4}_'.format(beta(),Volume)
# Add the mesh to the scene
scene = bpy.context.scene
obj = bpy.data.objects.new(name, me)
obj['Volume']=Volume
obj['beta']=beta()
obj['ScrVer']=Scriptversion 
scene.objects.link(obj)

# Select and make active
scene.objects.active = obj
obj.select = True