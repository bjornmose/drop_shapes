"""
Version 1.0
2018_12_20
JOW
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
zero_eps = 0.0000001

class ylsolver():
 
 def __init__(self):
  self.beta = zero_eps

 def yl_derivs(self,y,s):
  """
	Young Laplace .. Adams Bashford system
  """
  dx_dPhi = np.cos(y[2])
  dz_dPhi = np.sin(y[2])
  dPhi_ds = 2 - self.beta*y[1] - np.sin(y[2])/y[0]
  dS_ds = 1.
  dV_ds = np.abs(dx_dPhi * dx_dPhi) * (dz_dPhi) * np.pi
  return [dx_dPhi, dz_dPhi, dPhi_ds,dS_ds,dV_ds]
 
 def solve(self):
  s = np.arange(0, 8 * 3.142, 0.01)
  y0 = [zero_eps,zero_eps , 0.,0.,0.]
  y = odeint(self.yl_derivs,y0,s)
  return(y)

class yl_plotrange():
 def __init__(self):
  self.scn = 0.25
  self.k   = 0.1
  self.nC = 10
  self.vx = 0
  self.vy = 1

 def plot(self):
  solv = ylsolver()
  for n in range(1,self.nC):
   sn = n * self.scn
   solv.beta = self.k / (sn*sn)
   p = solv.solve()
   plt.plot(p[:,self.vx], p[:,self.vy])
   del p # clean up 
  del solv # clean up

shape = 0.01
jow_dist=0.05

plt.title('Volume , Lenght of Arc')
plt.ylabel('Volume')
plt.xlabel('ArcLen')


g1 =  yl_plotrange()
g1.k = shape
g1.scn = jow_dist
g1.vx=3
g1.vy=4
g1.plot()
del g1

plt.axis([0 ,16, 0,16])
plt.show()

plt.title('Shapes')
plt.ylabel('Z')
plt.xlabel('X')

g2 =  yl_plotrange()
g2.k = shape
g2.scn = jow_dist
g2.vx=0
g2.vy=1
g2.plot()
del g2



plt.axis([0 ,16, 0,16])
plt.show()
 


