import math as mt
import numpy as np

def sides_len(pt_1, pt_2, pt_3):
    '''Len of sides of traingle'''
    a = mt.sqrt((pt_2[1] - pt_1[1])**2 + (pt_2[0] - pt_1[0])**2)
    b = mt.sqrt((pt_3[1] - pt_2[1])**2 + (pt_3[0] - pt_2[0])**2)
    c = mt.sqrt((pt_1[1] - pt_3[1])**2 + (pt_1[0] - pt_3[0])**2)

    return a, b, c

def triangle_square(a, b, c):
    '''Square of traingle'''
    print(a, b, c)
    p = (a + b + c) / 2

    return ((p * (p - a) * (p - b) * (p - c))**(1/2))

def find_radius_in_circle(points_array):
    '''Radius of inscribed circle'''
    a, b, c = sides_len(points_array[0], points_array[1], points_array[2])
    tr_square = triangle_square(a, b, c)

    return ((2 * tr_square) / (a + b + c))

def center_in_circle(points_array):
    '''Center of inscribed circle'''
    a, b, c = sides_len(points_array[0], points_array[1], points_array[2])

    xa = points_array[0][0]
    ya = points_array[0][1]
    xb = points_array[1][0]
    yb = points_array[1][1]
    xc = points_array[2][0]
    yc = points_array[2][1]

    v_ab = [xb - xa, yb - ya]
    v_ac = [xc - xa, yc - ya]

    v_a = [v_ab[0] / a, v_ab[1] / a]
    v_b = [v_ac[0] / c, v_ac[1] / c]

    v_ak = [v_a[0] + v_b[0], v_a[1] + v_b[1]]

    v_bc = [xc - xb, yc - yb]
    v_ba = [xa - xb, ya - yb]

    v_a = [v_bc[0] / b, v_bc[1] / b]
    v_b = [v_ba[0] / a, v_ba[1] / a]

    v_bk = [v_a[0] + v_b[0], v_a[1] + v_b[1]]

    M1 = np.array([[v_ak[1], -v_ak[0]],
                   [v_bk[1], -v_bk[0]]])

    v1 = np.array([[v_ak[1] * xa - v_ak[0] * ya], [v_bk[1] * xb - v_bk[0] * yb]])
    res = np.linalg.solve(M1, v1)

    return res

def square_in_circle(pt_1, pt_2, pt_3):
    '''Square of inscribed circle'''
    points_array = []
    points_array.append(pt_1)
    points_array.append(pt_2)
    points_array.append(pt_3)

    radius = find_radius_in_circle(points_array)

    return (mt.pi * radius**2)


def check_triangle(pt_1, pt_2, pt_3):
    '''Check triangle for degeneracy'''
    points_array = []
    points_array.append(pt_1)
    points_array.append(pt_2)
    points_array.append(pt_3)

    a, b, c = sides_len(points_array[0], points_array[1], points_array[2])
    tr_square = triangle_square(a, b, c)

    if tr_square != 0:
        return 0, tr_square
    else:
        return 1, tr_square

def find_answer(points_array):
    '''Find min difference between square of triangle and inscribed circle'''
    pts_of_min = [0, 0, 0]
    min_square = 1000000

    for i in range(len(points_array)):
        for j in range(len(points_array)):
            for k in range(len(points_array)):
                if (i != j) and (i != k) and (j != k):
                    check, tr_square = check_triangle(points_array[i], points_array[j], points_array[k])
                    if(check == 0):
                        #tr_square = triangle_square(points_array[i], points_array[j], points_array[k])
                        inscribed_circle = square_in_circle(points_array[i], points_array[j], points_array[k])

                        if(abs(tr_square - inscribed_circle) < min_square):
                            print()
                            print(tr_square, inscribed_circle, tr_square - inscribed_circle)
                            print()
                            min_square = abs(tr_square - inscribed_circle)
                            pts_of_min[0] = points_array[i]
                            pts_of_min[1] = points_array[j]
                            pts_of_min[2] = points_array[k]

    return pts_of_min, tr_square
