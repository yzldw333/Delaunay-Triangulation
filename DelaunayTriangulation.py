import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve

class Edge:
    p1 = None
    p2 = None

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


class Triangle:

    p1 = None
    p2 = None
    p3 = None
    edge1 = None
    edge2 = None
    edge3 = None
    centerx = 0
    centery = 0
    radius = 0
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.edge1 = Edge(p1,p2)
        self.edge2 = Edge(p2,p3)
        self.edge3 = Edge(p3,p1)


    def get_outer_circle(self):
        if self.radius!=0:
            return (self.centerx, self.centery, self.radius)
        xa, ya = self.p1[0], self.p1[1]
        xb, yb = self.p2[0], self.p2[1]
        xc, yc = self.p3[0], self.p3[1]

        # 两条边的中点
        x1, y1 = (xa + xb) / 2.0, (ya + yb) / 2.0
        x2, y2 = (xb + xc) / 2.0, (yb + yc) / 2.0

        # 两条线的斜率
        ka = (yb - ya) / (xb - xa) if xb != xa else None
        kb = (yc - yb) / (xc - xb) if xc != xb else None

        alpha = np.arctan(ka) if ka != None else np.pi / 2
        beta  = np.arctan(kb) if kb != None else np.pi / 2

        # 两条垂直平分线的斜率
        k1 = np.tan(alpha + np.pi / 2)
        k2 = np.tan(beta + np.pi / 2)

        # 圆心
        y, x = solve([[1.0, -k1], [1.0, -k2]], [y1 - k1 * x1, y2 - k2 * x2])
        # 半径
        r1 = np.sqrt((x - xa)**2 + (y - ya)**2)
        self.centerx = x
        self.centery = y
        self.radius = r1
        return (x, y, r1)


    def plot(self):
        '''
            Call this function, you need to use plt.show() to see the image.
        :return:None
        '''
        plt.plot([self.p1[0],self.p2[0],self.p3[0],self.p1[0]],[self.p1[1],self.p2[1],self.p3[1],self.p1[1]],linewidth=2)

class DelaunayTriangulation:
    point_set = []
    edge_buffer = []
    temp_triangles = []
    triangles = []
    super_triangle = None

    def point_plot(self):
        '''
            Call this function, you need to use plt.show() to see the image.
        :return:None
        '''
        plt.plot(self.point_set[:,0],self.point_set[:,1],linewidth=0,marker='o')

    def set_point(self,point_set):
        num = len(point_set)
        self.point_set = point_set
        self.point_set.sort(key=lambda x: x[0])
        self.point_set = np.array(self.point_set).reshape(num,2)

    def build_super_triangle(self):
        max_loc = np.max(self.point_set,0)
        min_loc = np.min(self.point_set,0)
        centerx = (max_loc[0]+min_loc[0])/2.0
        top = np.array([centerx,(max_loc[1]-min_loc[1])*2+min_loc[1]-10])
        width = (max_loc[0]-centerx)*2+25
        if width<max_loc[1]-min_loc[1]+10:
            width = max_loc[1]-min_loc[1]+25 # extension to satisfy ground > height
        right = np.array([centerx+width,min_loc[1]-10])
        left = np.array([centerx-width,min_loc[1]-10])
        self.super_triangle = Triangle(top,left,right)
        self.temp_triangles.append(self.super_triangle)
        self.super_triangle.plot()
        self.point_plot()
        plt.show()
    def draw_tmp_triangle(self):
        for triangle in self.temp_triangles:
            triangle.plot()
        self.point_plot()
        plt.show()
    def draw_result(self):
        for triangle in self.triangles:
            triangle.plot()
        self.point_plot()
        plt.show()
    def iteration(self):
        epsilon = 1e-5
        point_set = list(self.point_set) # change point_set from numpy array to list of (x,y)
        for point in point_set:
            print(point)
            self.edge_buffer = []
            tmp_triangles = []
            for triangle in self.temp_triangles:
                (x,y,radius) = triangle.get_outer_circle()
                # judge: if the point is on the right of the circle.
                if point[0]>x+radius+epsilon:
                    self.triangles.append(triangle)
                    continue
                # judge: if the point is outside of the circle.
                if (point[0]-x)**2+(point[1]-y)**2 > radius**2:
                    tmp_triangles.append(triangle)
                    continue
                else:
                    # judge: if the point is inside of the circle:
                    self.edge_buffer.append(triangle.edge1)
                    self.edge_buffer.append(triangle.edge2)
                    self.edge_buffer.append(triangle.edge3)
                    continue
            self.temp_triangles = tmp_triangles
            # clean duplicate edge in edge_buffer
            i = 0
            for edge in self.edge_buffer:
                ifadd = True
                j=0
                for edgee in self.edge_buffer:
                    if (i!=j)and ((edge.p1==edgee.p1).all() and (edge.p2==edgee.p2).all() \
                        or (edge.p1 == edgee.p2).all() and (edge.p2==edgee.p1).all()):
                        ifadd = False
                        break
                    j+=1
                if ifadd:
                    self.temp_triangles.append(Triangle(edge.p1,edge.p2,point))
                i+=1
            # generate new temp triangle with the point and the edge in the buffer
            #for edge in self.edge_buffer:
            #    self.temp_triangles.append(Triangle(edge.p1,edge.p2,point))
            #self.draw_result()

        # combine triangles and temp_triangles
        for add_triangle in self.temp_triangles:
             self.triangles.append(add_triangle)
        # remove the triangles which are related to the super triangle.
        self.temp_triangles = self.triangles
        self.triangles = []

        for triangle in self.temp_triangles:
            if (triangle.p1 == self.super_triangle.p1).all() or (triangle.p1 == self.super_triangle.p2).all() or (triangle.p1 == self.super_triangle.p3).all() \
                or (triangle.p2 == self.super_triangle.p1).all() or (triangle.p2 == self.super_triangle.p2).all() or (triangle.p2 == self.super_triangle.p3).all() \
                or (triangle.p3 == self.super_triangle.p1).all() or (triangle.p3 == self.super_triangle.p2).all() or (triangle.p3 == self.super_triangle.p3).all():
                pass
            else:
                self.triangles.append(triangle)


if __name__ == '__main__':
    n = 100
    delaunay_triangulation = DelaunayTriangulation()
    points = np.random.rand(n,2)*200-100
    point_set = list(points)
    delaunay_triangulation.set_point(point_set)
    delaunay_triangulation.build_super_triangle()
    delaunay_triangulation.iteration()
    delaunay_triangulation.draw_result()
