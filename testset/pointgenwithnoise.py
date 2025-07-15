# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 13:34:18 2022

@author: Peter Szutor
"""

import numpy as np
import open3d as o3d
import pandas as pd

#10 000 000 * 10 000 000 tér
xext=10000000
yext=10000000
magpontdarab=3
minpontszam=600
alaptav=(xext/(magpontdarab*1.1))
def magpontgen(darab,alaptav):
    kipontok=[]
    c=0
    while c<darab:
        ujpontx=np.random.randint(0,xext,(1),dtype='int64')[0]
        ujponty=np.random.randint(0,yext,(1),dtype='int64')[0]
        tulkozel=False
        ujpont=np.array([ujpontx,ujponty])
        for egy in kipontok:
            tav=np.linalg.norm(egy-ujpont)
            if tav<alaptav:
                tulkozel=True
                break
        if not tulkozel:
            kipontok.append(ujpont)
            c+=1
    return np.array(kipontok)


def belsopontgen(pont,darab,maxtav):
    kipontok=[]
    minx=pont[0]-maxtav
    maxx=pont[0]+maxtav
    miny=pont[1]-maxtav
    maxy=pont[1]+maxtav
    if maxx>xext:
        maxx=xext
    if maxy>yext:
        maxy=yext
    if minx<0:
        minx=0
    if miny<0:
        miny=0
    c=0
    pontokx=np.random.normal((maxx-minx)/2,maxtav/2.5,(minpontszam if darab*2<minpontszam else darab*2))
    pontoky=np.random.normal((maxy-miny)/2,maxtav/2.5,(minpontszam if darab*2<minpontszam else darab*2))
    while c<(minpontszam if darab*2<minpontszam else darab*2):
        ujpontx=np.random.choice(pontokx,size=1)[0]+minx
        ujponty=np.random.choice(pontoky,size=1)[0]+miny
        # ujpontx=np.random.randint(int(minx),int(maxx),(1),dtype='int64')[0]
        # ujponty=np.random.randint(int(miny),int(maxy),(1),dtype='int64')[0]
        ujpont=np.array([ujpontx,ujponty])
        tav=np.linalg.norm(ujpont-pont)
        if tav<maxtav:
            kipontok.append(ujpont)
            c+=1
    return np.array(kipontok)

def zajpontgen(magpontok,darab,maxtav):
    kipontok=[]
    minx=0
    maxx=xext
    miny=0
    maxy=yext
    if maxx>xext:
        maxx=xext
    if maxy>yext:
        maxy=yext
    if minx<0:
        minx=0
    if miny<0:
        miny=0
    c=0
    while c<(120 if darab*2<120 else darab*2):
        ujpontx=np.random.randint(int(minx),int(maxx),(1),dtype='int64')[0]
        ujponty=np.random.randint(int(miny),int(maxy),(1),dtype='int64')[0]
        ujpont=np.array([ujpontx,ujponty])
        jopont=True
        for mp in magpontok:
            tav=np.linalg.norm(ujpont-mp)
            if tav<maxtav:
                jopont=False
        if jopont:
            kipontok.append(ujpont)
            c+=1
    return np.array(kipontok)


magpontok=(magpontgen(magpontdarab,alaptav))
osszpont=[np.array([0,0],dtype='int64')]
for egymag in magpontok:
    osszpont=np.concatenate((osszpont,belsopontgen(egymag,magpontdarab,alaptav/2)),axis=0)
osszpont=np.concatenate((osszpont,zajpontgen(magpontok,magpontdarab,alaptav/1.8)),axis=0)
np.savetxt('clustesztmintazajos'+str(magpontdarab)+'.csv',osszpont,fmt='%10.0f')
import matplotlib.pyplot as plt
plt.scatter(osszpont[:,0], osszpont[:,1], alpha=0.8)
plt.show()
plt.scatter(magpontok[:,0], magpontok[:,1], alpha=0.8)
plt.show()
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(osszpont)
# o3d.io.write_point_cloud("tesztrandom1.pcd", pcd)
