#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Nghia Ho (https://nghiaho.com/?page_id=671, online 12.3.2019)
# Can I use and modify for research? -> Sure! ( https://web.archive.org/web/20190313135843/https://nghiaho.com/?page_id=671#comment-890748 )

from numpy import *
from math import sqrt

# Input: expects Nx3 matrix of points
# Returns R,t (B = R*A + t)
# R = 3x3 rotation matrix
# t = 3x1 column vector

def rigid_transform_3D(A, B):
    assert len(A) == len(B)

    N = A.shape[0]; # total points

    centroid_A = mean(A, axis=0)
    centroid_B = mean(B, axis=0)
    
    # centre the points
    AA = A - tile(centroid_A, (N, 1))
    BB = B - tile(centroid_B, (N, 1))

    H = dot(transpose(AA), BB)

    U, S, Vt = linalg.svd(H)

    R = dot(Vt.T, U.T)

    # special reflection case
    if linalg.det(R) < 0:
       #print "Reflection detected"
       Vt[2,:] *= -1
       R = dot(Vt.T, U.T)

    t = -dot(R, centroid_A.T) + centroid_B.T

    #print t

    return R, t
    
"""
# CAM
A=array([array([0.01841625, 0.03528079, 0.18800001]), array([0.02974893, 0.01900213, 0.19475001]), array([0.02502723, 0.03071728, 0.32000001]), array([0.05301977, 0.05059613, 0.26725002]), array([-0.01741662,  0.04898024,  0.33175001])])

# ROBOT
B=array([array([ 0.04137775, -0.10228969,  0.31572101]), array([ 0.1103007 , -0.09618147,  0.29017541]), array([ 0.1546393 , -0.07542561,  0.24978575]), array([ 0.11474095, -0.12544958,  0.26818195]), array([ 0.14834657, -0.01945851,  0.22522159])])

print(rigid_transform_3D(A, B))
"""