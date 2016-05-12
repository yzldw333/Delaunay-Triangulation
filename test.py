import wx
import numpy as np
from Homework8.DelaunayTriangulation.DelaunayTriangulation import *
class DrawPanel(wx.Panel):
    def __init__(self,parent):
        super().__init__(parent,  -1, name="DrawPanel", size=(1024,718))
        self.Bind(wx.EVT_PAINT,self.OnPaint)
        self.parent = parent
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)
        self.SetPosition((0,50))
        self.SetBackgroundColour('white')
        self.point_set = []
        self.delaunay_triangulation = DelaunayTriangulation()
    def init(self):
        dc = wx.ClientDC(self)
        dc.Clear()
        self.point_set = []
    def OnPaint(self, event):
        dc = wx.ClientDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK,4))
        for triangle in self.delaunay_triangulation.triangles:
            dc.DrawLine(triangle.edge1.p1[0],triangle.edge1.p1[1],triangle.edge1.p2[0],triangle.edge1.p2[1])
            dc.DrawLine(triangle.edge2.p1[0],triangle.edge2.p1[1],triangle.edge2.p2[0],triangle.edge2.p2[1])
            dc.DrawLine(triangle.edge3.p1[0],triangle.edge3.p1[1],triangle.edge3.p2[0],triangle.edge3.p2[1])
    def PaintWithNum(self,num):
        width, height = self.GetSize()
        x_array = np.random.rand(num,1)*width
        y_array = np.random.rand(num,1)*height
        point_set = np.hstack((x_array,y_array))
        point_set = np.array(point_set,dtype=np.float64)
        self.point_set = list(point_set)
        if len(self.point_set)>=3:
            # Draw Triangle
            self.delaunay_triangulation.set_point(self.point_set)
            self.delaunay_triangulation.build_super_triangle()
            self.delaunay_triangulation.iteration()
            self.OnPaint(None)
    def OnClick(self, event):
        pos = event.GetPosition()
        print((pos))
        self.parent.ShowPos(pos)
        # 导入DelaunayTriangulation
        self.point_set.append(np.array([pos.x,pos.y],dtype=np.float64))
        if len(self.point_set)>=3:
            # Draw Triangle
            self.delaunay_triangulation.set_point(self.point_set)
            self.delaunay_triangulation.build_super_triangle()
            self.delaunay_triangulation.iteration()
            self.OnPaint(None)



class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None,  -1, "Delaunay Triangulation", size = (1024, 768))
        self.panel = DrawPanel(self)
        self.button = wx.Button(self,label="Clear",pos=(180,10),style=0)
        self.button.Bind(wx.EVT_BUTTON,self.OnButtonClick)
        wx.StaticText(self, -1, "Pos:", pos = (10, 12))
        self.posCtrl = wx.TextCtrl(self, -1, "", pos = (40, 10))
        menu_bar = wx.MenuBar()
        random_menu = wx.Menu()
        random_points = random_menu.Append(wx.ID_ANY,'&Random Points','Generate the points randomly.')
        self.Bind(wx.EVT_MENU,self.OnRandomPoints,random_points)
        menu_bar.Append(random_menu,'&Option')
        system_menu = wx.Menu()
        about = system_menu.Append(wx.ID_ABOUT,'&About')
        exit = system_menu.Append(wx.ID_EXIT,'&Exit')
        self.Bind(wx.EVT_MENU,self.OnExit,exit)
        self.Bind(wx.EVT_MENU,self.OnAbout,about)
        menu_bar.Append(system_menu,'&Help')
        self.SetMenuBar(menu_bar)

    def OnRandomPoints(self,event):
        dialog = wx.TextEntryDialog(parent=self, message="Set points' num")
        dialog.SetMaxLength(4)
        dialog.Bind(wx.EVT_WINDOW_MODAL_DIALOG_CLOSED, self.OnDialogCallback)
        dialog.ShowWindowModal()
    def OnDialogCallback(self,event):
        str = event.GetEventObject().GetValue()
        if str.isdigit():
            self.panel.PaintWithNum(int(str))
    def OnAbout(self,event):
        message = wx.MessageBox("Delaunay Triangulation")

    def OnExit(self,event):
        self.Close()
    def OnButtonClick(self, event):
        self.panel.init()
    def ShowPos(self,pos):
        self.posCtrl.SetValue("%s, %s" %(pos.x, pos.y))



if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()
