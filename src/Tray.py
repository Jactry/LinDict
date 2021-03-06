#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################################################
#  Copyright (C) 2012 by Jactry Zeng                                     #
#                                                                        #
#  This program is free software: you can redistribute it and/or modify  #
#  it under the terms of the GNU General Public License as published by  #
#  the Free Software Foundation, either version 3 of the License, or     #
#  (at your option) any later version.                                   #
#                                                                        #
#  This program is distributed in the hope that it will be useful,       #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#  GNU General Public License for more details.                          #
#                                                                        #
#  You should have received a copy of the GNU General Public License     #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>. #
##########################################################################

from PyQt4 import QtGui


class LinTray(QtGui.QSystemTrayIcon):
    def __init__(self, parent):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        self.icon = QtGui.QIcon("./youdao.png")
        self.setIcon(self.icon)
        self.Tray_Menu = QtGui.QMenu()
        self.setContextMenu(self.Tray_Menu)
