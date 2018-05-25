'''
Created on 2018/5/19

@author: Lulumi5129
'''
from LocalizationSystem.LocalizationAlg.L3M_System import L3M_Sys, L3M_Config
from LocalizationSystem.Node.node import node_Config
from mpl_toolkits.mplot3d import Axes3D, axes3d
from itertools import cycle
import matplotlib.pyplot as plt
import numpy as np
nodeConfigFilePath = './config/node_config.cfg'
L3MSysConfigFilePath = './config/L3M_System_config_3D.cfg'

#Get Node config params
node_cfg = node_Config(nodeConfigFilePath)
        
#print config params
print(node_cfg)

#Get L3M config params
L3M_cfg = L3M_Config(L3MSysConfigFilePath)
        
#print config params
print(L3M_cfg)

(anchorNodeList, targetNodeList, realRSSIDict, noiseDict, L3M_CoordinateDict, anchorCombDict, L3M_Comb_CoordinateDict) = L3M_Sys.L3M_Sys_main()

L3M_Sys.printTargetNode(targetNodeList)
L3M_Sys.printAnchorNode(anchorNodeList)
L3M_Sys.printRealRSSI(realRSSIDict, noiseDict)
L3M_Sys.printL3M_Coordinate(L3M_CoordinateDict)
L3M_Sys.printL3M_Comb_Coordinate(L3M_Comb_CoordinateDict, anchorCombDict)

# plot
fig = plt.figure(figsize=(8,6), dpi=120)
ax = fig.add_subplot(111, projection='3d')
cycol=cycle('bgrcmk')

for anchor in anchorNodeList :
    # center and radius
    center = anchor.coordinate
    radius,b = anchor.getChannelDistance(targetNodeList[0])

    # data
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
    y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]

    ax.plot_wireframe(x, y, z, rstride=10, cstride=10, color=next(cycol))
    #ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b')



x_anchor=[]
y_anchor=[]
z_anchor=[]
target=targetNodeList[0]
    
# get anchor coordinate
for anchor in anchorNodeList :
    x_anchor.append(anchor.x)
    y_anchor.append(anchor.y)
    z_anchor.append(anchor.z)
            
# plot
ax.scatter(x_anchor, y_anchor, z_anchor, c='b', s=100, marker='^', label='Anchor')
ax.scatter(target.x, target.y, target.z, c='r', s=100, marker='o', label=target.nodeName)
legend = ax.legend(loc='center right', fontsize='x-small', shadow=True)
legend.get_frame().set_facecolor('#00FFCC')
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')

# show
plt.show()