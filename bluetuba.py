#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import sal

class AboutBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About <<project>>",
            style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(400,200))
        vers = {}
        vers["python"] = sys.version.split()[0]
        vers["wxpy"] = wx.VERSION_STRING
        hwin.SetPage(aboutText % vers)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, pos=(150,150), size=(350,200))

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        menuBar.Append(menu, "&File")
        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)

        self.statusbar = self.CreateStatusBar()

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        m_text = wx.StaticText(panel, -1, "Hello World!")
        m_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        m_text.SetSize(m_text.GetBestSize())
        box.Add(m_text, 0, wx.ALL, 10)

        img = wx.Image("./resource/ic_play_arrow_black_48dp.png")
        img.Rescale(36, 36)
        bmp = wx.BitmapFromImage(img)
        #m_close = wx.Button(panel, wx.ID_CLOSE, "Close")
        m_close = wx.BitmapButton(panel, id = wx.ID_ANY, bitmap = bmp, size = (bmp.GetWidth()+10, bmp.GetHeight()+10))
        box.Add(m_close, 0, wx.ALL, 10)

        panel.SetSizer(box)
        panel.Layout()

    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()

    def onConnected(self, device):
        self.SetTitle("bluetuba - {}".format(device))

    def onDisconnected(self, device):
        self.SetTitle("bluetuba")

if __name__ == '__main__':
    app = wx.App(False)
    Sal = sal.sal()
    frame = Frame("bluetuba")
    Sal.regConnectCB(frame.onConnected)
    Sal.regDisconnectCB(frame.onDisconnected)
    frame.Show(True)
    app.MainLoop()
