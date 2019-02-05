"""
The module defines all print and draw function for showing the result

Author: Xu Zhang
"""

import numpy as np

def frame2ellipse(f):
    if f is None or f.shape[0] == 0:
        return np.array([])

    frame_dim = f.shape[1]
    g = np.zeros((f.shape[0],6),dtype = np.float32)
    if frame_dim == 2:
        g[0,:] = f[0,:]
        g[1,:] = f[1,:]
        g[2,:] = 1
        g[4,:] = 1
    elif frame_dim==3 or frame_dim==4:
        g[0,:] = f[0,:]
        g[1,:] = f[1,:]
        g[2,:] = np.power(f[2,:],2)
        g[4,:] = np.power(f[2,:],2)
    elif frame_dim == 5:
        g = f.copy()
    elif frame_dim == 6:
        g[0,:] = f[0,:]
        g[1,:] = f[1,:]
        for k in range(f.shape[0]):
            A = np.reshape(f[2:6,k], 2, 2)
            E = np.matmul(A.transpose(),A)
            g[2] = E[0,0]
            g[3] = E[0,1]
            g[4] = E[1,1]
    else:
        print('Unknown Frame Type')
        return np.array([])
    return g

def ellipse_warp(H, ell, method = 'linearise'):
    transformed_ell = np.zeros(ell.shape,dtype = np.float32)

    for i in range(ell.shape[0]):
        if method == 'standard':
            S = np.array([[ell(2,i),ell(3,i),0],\
                    [ell(3,i), ell(4,i), 0],
                    [0,0,-1]])
            T = [[1, 0, ell(0,i)],
                [0,1,ell(1,i)],
                [0,0,1]]
            
            #M = H * T * S * T' * H' ;
            M =np.matmul(np.matmul(np.matmul(np.matmul(H,T),S),\
                    T.transpose()), H.transpose())

            #M = - M / M(3,3) ;
            M = -1*M/M[2,2]
            
            #t_ = - M(1:2,3) ;
            t_ = -1*M[0:1,2]
            #S_ = M(1:2,1:2) + t_*t_' ;
            S_ = M[0:1,0:1] + np.matmul(t_,t_.transpose())

            #transformed_ell[:,i] = [t_ ; S_([1;2;4])] ;
            transformed_ell[i,0:3] = t_
            transformed_ell[i,3:6] = [S_[0],S_[1],S_[3]] 
        elif method == 'linearise':

