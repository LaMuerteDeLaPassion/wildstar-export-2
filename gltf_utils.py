import numpy as np
import math
# https://github.com/mrdoob/three.js/blob/dev/build/three.core.js#L3612

def compose(t,r,s):
    x,y,z,w = r
    x2 = x+x
    y2 = y+y
    z2 = z+z
    xx = x*x2
    xy = x*y2
    xz = x*z2
    yy = y*y2
    yz = y*z2
    zz = z*z2
    wx = w*x2
    wy = w*y2
    wz = w*z2
    sx, sy, sz = s
    o = [0]*16
    o[0] = (1 - (yy+zz))*sx
    o[1] = (xy + wz) * sx
    o[2] = (xz - wy) * sx
    o[3] = 0
    o[4] = (xy-wz) * sy
    o[5] = (1 - (xx+zz)) * sy
    o[6] = (yz+wx) * sy
    o[7] = 0
    o[8] = (xz+wy) * sz
    o[9] = (yz-wx) * sz
    o[10] = (1-(xx+yy)) * sz
    o[11] = 0
    o[12] = t[0]
    o[13] = t[1]
    o[14] = t[2]
    o[15] = 1
    return o

def quat_to_mat(m):
    m11 = m[0]
    m12 = m[4]
    m13 = m[8]
    m21 = m[1]
    m22 = m[5]
    m23 = m[9]
    m31 = m[2]
    m32 = m[6]
    m33 = m[10]
    trace = m11 + m22 + m33
    if trace > 0:
        s = 0.5/math.sqrt(trace+1)
        w = 0.25/s
        x = (m32 - m23) * s
        y = (m13 - m31) * s
        z = (m21 - m12) * s
    elif m11 > m22 and m11 > m33:
        s = 2 * math.sqrt(1+m11-m22-m33)
        w = (m32 - m23) / s
        x = 0.25 * s
        y = (m12 + m21) / s
        z = (m13 + m31) / s
    elif m22 > m33:
        s = 2 * math.sqrt(1+m22-m11-m33)
        w = (m13 - m31) / s
        x = (m12 + m21) / s
        y = 0.25 * s
        z = (m23 + m32) / s
    else:
        s = 2 * math.sqrt(1+m33-m11-m22)
        w = (m21 - m12) / s
        x = (m13 + m31) / s
        y = (m23 + m32) / s
        z = 0.25 * s
    return [x,y,z,w]

def derminant(m):
    m11 = m[0]
    m12 = m[1]
    m13 = m[2]
    m14 = m[3]
    m21 = m[4]
    m22 = m[5]
    m23 = m[6]
    m24 = m[7]
    m31 = m[8]
    m32 = m[9]
    m33 = m[10]
    m34 = m[11]
    m41 = m[12]
    m42 = m[13]
    m43 = m[14]
    m44 = m[15]
    return m41 * (m14*m23*m32-m13*m24*m32-m14*m22*m33+m12*m24*m33+m13*m22*m34-m12*m23*m34) + m42 * (m11*m23*m34-m11*m24*m33+m14*m21*m33-m13*m21*m34+m13*m24*m31-m14*m23*m31) + m43 * (m11*m24*m32-m11*m22*m34-m14*m21*m32+m12*m21*m34+m14*m22*m31-m12*m24*m31) + m44 * (-m13*m22*m31-m11*m23*m32+m11*m22*m33+m13*m21*m32-m12*m21*m33+m12*m23*m31)

def decompose(m):
    sx = [m[0], m[1], m[2]]
    sy = [m[4], m[5], m[6]]
    sz = [m[8], m[9], m[10]]
    sx = float(np.linalg.norm(sx))
    sy = float(np.linalg.norm(sy))
    sz = float(np.linalg.norm(sz))
    # if extract_directions:
    #     u_x = v_x / sx
    #     u_y = v_y / sy
    #     u_z = v_z / sz
    #     sign_x = np.sign(np.dot(np.cross(u_y, u_z), u_x))
    #     sign_y = np.sign(np.dot(np.cross(u_z, u_x), u_y))
    #     sign_z = np.sign(np.dot(np.cross(u_x, u_y), u_z))
    #     sx *= sign_x
    #     sy *= sign_y
    #     sz *= sign_z

    det = derminant(m)
    if det < 0:
        sx *= -1
    t = [m[12], m[13], m[14]]
    invsx = 1/sx
    invsy = 1/sy
    invsz = 1/sz
    m[0] *= invsx
    m[1] *= invsx
    m[2] *= invsx
    m[4] *= invsy
    m[5] *= invsy
    m[6] *= invsy
    m[8] *= invsz
    m[9] *= invsz
    m[10] *= invsz

    q = quat_to_mat(m)
    s = [sx, sy, sz]
    return t, q, s

def transform_point(m, p):
    x = p[0] * m[0] + p[1] * m[4] + p[2] * m[8] + 1 * m[12]
    y = p[0] * m[1] + p[1] * m[5] + p[2] * m[9] + 1 * m[13]
    z = p[0] * m[2] + p[1] * m[6] + p[2] * m[10] + 1 * m[14]
    return [x, y, z]