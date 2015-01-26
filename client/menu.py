#! /usr/bin/python

__author__ = 'Kiamehr'

import guiconstvars
import basictypes
from menuinfo import *
from wx import *

#------------------------------------------------------------------------------------
#####################################################################################




class Menu():

        flag = 0

#############
        def __init__(self):
                self.info = MenuInfo()


#############
        def start (self):
                
                Menu.flag = 0
                self.info.host = "localhost"
                self.info.port = int (10000)
                self.info.team = basictypes.Teams.left
                self.info.tanktype = basictypes.TankTypes.attacker
                self.info.isAI = False
                
                def done (event):
                        if host.GetValue() == "" or port.GetValue() == "":
                                wx.MessageBox('PLS ENTER ALL!', '!', wx.OK | wx.ICON_WARNING)
                        else:

                                try:  
                                        self.info.host = str(host.GetValue())
                                        self.info.port = int(port.GetValue())
                                        if team_combobox.GetSelection() == 0:
                                                self.info.team = basictypes.Teams.left
                                        elif team_combobox.GetSelection() == 1:
                                                self.info.team = basictypes.Teams.right

                                        if tanktype_combobox.GetSelection() == 0:
                                                self.info.tanktype = basictypes.TankTypes.attacker
                                        elif tanktype_combobox.GetSelection() == 1:
                                                self.info.tanktype = basictypes.TankTypes.defender

                                        if isAI_combobox.GetSelection() == 0:
                                                self.info.isAI = False
                                        elif isAI_combobox.GetSelection() == 1:
                                                self.info.isAI = True

                                        monitor_rsln = monitor_combobox.GetValue().split('*')
                                        self.info.monitor_width  = int(monitor_rsln[0])
                                        self.info.monitor_height = int(monitor_rsln[1])

                                        wx.MessageBox('Done!', 'Info', wx.OK)
                                        win.Close()
                                        Menu.flag=1
                                except:
                                        wx.MessageBox('host must be string and port must be integer!', 'wrnog type!', wx.OK | wx.ICON_WARNING)  



               
                app = wx.App()
                
                #main window :
                win = wx.Frame(None, style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, title = "pytanks!", size = (280,360))
                win.Show()
                
                #butuns and text boxes and drop lists : 
                host        = wx.TextCtrl(win, value = "localhost", pos = (60,10), size = (180,25))
                port        = wx.TextCtrl(win, value = "10000", pos = (60,50), size = (180,25))
                done_buttun = wx.Button(win, label="Done!", pos=(10,255), size = (260,90))
                done_buttun.Bind(wx.EVT_BUTTON, done)
                team_combobox     = wx.ComboBox(win, value = 'left', choices = ['left', 'right'], style = wx.CB_READONLY, pos = (60, 90))
                tanktype_combobox = wx.ComboBox(win, value = 'attacker', choices = ['attacker', 'defender'], style = wx.CB_READONLY, pos = (60, 130))
                isAI_combobox     = wx.ComboBox(win, value = 'no', choices = ['no', 'yes'], style = wx.CB_READONLY, pos = (60, 170))
                monitor_combobox  = wx.ComboBox(win, value = guiconstvars.resolutions[1], choices = guiconstvars.resolutions, style = wx.CB_READONLY, pos = (60, 210))

                #EVENTs
                done_buttun.Bind(wx.EVT_BUTTON, done)
                
                #labels:
                wx.StaticText(win, 1,'host :', pos = (10,10))
                wx.StaticText(win, 1,'port :', pos = (10,50))
                wx.StaticText(win, 1,'team :', pos = (10,95))
                wx.StaticText(win, 1,'roll :', pos = (10,140))
                wx.StaticText(win, 1,'bot :' , pos = (10,175))
                wx.StaticText(win, 1,'rsln :' , pos = (10,215))
                wx.StaticText(win, 1,'*' , pos = (170,210))

                #EVENT loop:
                app.MainLoop()

##############

        def showMsg(self, txt, title):
                app2=wx.App()
                wx.MessageBox(txt, title, wx.OK | wx.ICON_WARNING)
                
##############

        def getMenuInfo (self):
                return self.info



##############

        def donePressed(self):
                if Menu.flag == 1:
                        return True
                if Menu.flag == 0:
                        return False
                

#---------------------------------------------------------------------------------
##################################################################################


if __name__ == "__main__":
        menu = Menu()
        menu.start()
        print menu.getMenuInfo().host
        print menu.getMenuInfo().port
        print menu.getMenuInfo().tanktype 
        print menu.getMenuInfo().team
        print menu.getMenuInfo().isAI
        menu.showMsg ("test!","test")
        
        if menu.donePressed():
                print "hi!"
        if menu.donePressed() == False:
                print "bye!"
        
