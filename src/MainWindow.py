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

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import *
from PyQt4 import QtGui

from ui_main import Ui_Form
from Tray import LinTray
from CloseWindow import CloseDialog

#from Xlib import X, XK, display
#from Xlib.ext import record
#from Xlib.protocol import rq

import Lookup
import sys
import Configure


class MainWindow(QWidget, Ui_Form):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.translate)
        self.pushButton.setAutoDefault(True)

        self.word_completer = QCompleter()
        self.lineEdit.setCompleter(self.word_completer)
        self.word_completer.setCaseSensitivity(Qt.CaseInsensitive)
        model = QStringListModel()
        self.word_completer.setModel(model)
        self.get_word_list(model)

        self.real_time_status = True
        self.move_to_center()
        self.creat_menu()
        #self.hotkey()
        htmlfile = open("./template/index.html", 'r')
        self.textEdit.setText(self.tr(htmlfile.read()))
        htmlfile.close()

    def get_word_list(self, model):
        file = open('./word.ldc', "r")
        word_list = []
        for eachline in file:
            word_list.append(eachline.strip())
        file.close()

        model.setStringList(word_list)

    def hide_or_display(self):
        if self.isVisible():
            self.hide()
        else:
            self.setVisible(True)

    def about_lindict(self):
        QtGui.QMessageBox.about(self, u'关于 LinDict', u'LinDict by Jactry Zeng')

    def creat_menu(self):
        self.hide_action = QtGui.QAction(u'显示/隐藏窗口', self, triggered=self.hide_or_display)
        self.real_time_action = QtGui.QAction(u'划词翻译', self, checkable=True, triggered=self.change_real_time_status)
        #self.real_time_action.setShortcut(QKeySequence('X'))
        #self.real_time_action.setShortcutContext(Qt.ApplicationShortcut)
        self.about_action = QtGui.QAction(u'关于 Lindict', self, triggered=self.about_lindict)
        self.quit_action = QtGui.QAction(u'退出', self, triggered=QtGui.qApp.quit)
        self.real_time_action.setChecked(True)
        self.tray = LinTray(self)
        self.tray_menu = QtGui.QMenu()
        self.tray_menu.addAction(self.hide_action)
        self.tray_menu.addAction(self.real_time_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.about_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.quit_action)
        self.tray.setContextMenu(self.tray_menu)
        self.tray.show()

    def change_real_time_status(self):
        if self.real_time_status:
            self.real_time_action.setChecked(False)
            self.real_time_status = False
        else:
            self.real_time_action.setChecked(True)
            self.real_time_status = True

    def translate(self):
        res = Lookup.look_up(self.lineEdit.text())
        if not res:
            htmlfile = open("./template/404.html", 'r')
            self.textEdit.setText(self.tr(htmlfile.read()))
            htmlfile.close()
        else:
            reload(sys)
            sys.setdefaultencoding('utf-8')
            res = unicode(res)
            self.textEdit.setText(res)

    def move_to_center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and self.lineEdit.text() != "":
            self.translate()
        #elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_S:
        #    self.change_real_time_status()

    def closeEvent(self, event):
        event.ignore()
        close_state = Configure.read_config()
        if close_state == '0':
            self.hide_or_display()
        elif close_state == '2':
            QtGui.qApp.quit()
        else:
            self.close_dialog = CloseDialog(self)
            self.close_dialog.setModal(False)
            self.jiajia = self.close_dialog.exec_()
            Configure.write_config(self.jiajia)
            if self.jiajia == 0:
                self.hide_or_display()
                #self.ask_next_time = False
            elif self.jiajia == 1:
                self.hide_or_display()
                #self.ask_next_time = True
            elif self.jiajia == 2:
                self.ask_next_time = False
                QtGui.qApp.quit()
            elif self.jiajia == 3:
                self.ask_next_time = True
                QtGui.qApp.quit()
       # delete self.close_dialog
            #self.close_dialog.exec()
            #self.setEnabled(False)
    """
    def hotkey(self):

        self.record_dpy = display.Display()
        self.ctx = self.record_dpy.record_create_context(
            0,
            [record.AllClients],
            [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.KeyPress, X.MotionNotify),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
            }])

        def lookup_keysym(keysym):

            for name in dir(XK):
                if name[:3] == "XK_" and getattr(XK, name) == keysym:
                    return name[3:]
            return "[%d]" % keysym

        def record_callback(reply):
            if reply.category != record.FromServer:
                return
            if reply.client_swapped:
                print "* received swapped protocol data, cowardly ignored"
                return
            if not len(reply.data) or ord(reply.data[0]) < 2:
                # not an event
                return

            data = reply.data
            while len(data):
                event, data = rq.EventField(None).parse_binary_value(data, self.record_dpy.display, None, None)
                keysym = self.record_dpy.keycode_to_keysym(event.detail, 0)
                if lookup_keysym(keysym) == "F8":
                    self.change_real_time_status
                    print "Jactry"

        self.record_dpy.record_enable_context(self.ctx, record_callback) """
