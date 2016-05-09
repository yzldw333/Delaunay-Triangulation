# Delaunay Triangulation
***
### 数据结构
point_set:点集合  
edge_buffer:边的缓冲域  
temp_triangles:临时三角形  
triangles:分割好的三角形  
***
### 算法描述
    input: 顶点列表(vertices)                       //vertices为外部生成的随机或乱序顶点列表
    output:已确定的三角形列表(triangles)
      初始化顶点列表
      创建索引列表(indices = new Array(vertices.length))    //indices数组中的值为0,1,2,3,......,vertices.length-1
      基于vertices中的顶点x坐标对indices进行sort           //sort后的indices值顺序为顶点坐标x从小到大排序（也可对y坐标，本例中针对x坐标）
      确定超级三角形
      将超级三角形保存至未确定三角形列表（temp triangles）
      将超级三角形push到triangles列表
      遍历基于indices顺序的vertices中每一个点            //基于indices后，则顶点则是由x从小到大出现
        初始化边缓存数组（edge buffer）
        遍历temp triangles中的每一个三角形
          计算该三角形的圆心和半径
          如果该点在外接圆的右侧
            则该三角形为Delaunay三角形，保存到triangles
            并在temp里去除掉
            跳过
          如果该点在外接圆外（即也不是外接圆右侧）
            则该三角形为不确定                      //后面会在问题中讨论
            跳过
          如果该点在外接圆内
            则该三角形不为Delaunay三角形
            将三边保存至edge buffer
            在temp中去除掉该三角形
        对edge buffer进行去重
        将edge buffer中的边与当前的点进行组合成若干三角形并保存至temp triangles中
      将triangles与temp triangles进行合并
      除去与超级三角形有关的三角形
    end
#### 补充说明
边的去重：
找的是唯一边，即如果有两个或以上的边存在，无需将边添加入集合，只有唯一的出现一次的边才会被添加入集合，相关算法代码如下。  

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
        # 这里我将三角形的生成和边的添加进行合并了。
    i+=1
