#!/usr/bin/env python

import os, sys
from time import sleep
import re
from threading import Thread
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
from glib import markup_escape_text

def Monitor(path, gui):
    oldmtime = None
    while 1:
        sleep(0.1)
        newmtime = os.stat(path+'/out')[8]
        if newmtime != oldmtime:
            try:
                f = open(path+'/out', 'r')
                text = f.read()
                text = markup_escape_text(text)
                name = re.compile('(....-..-..) (..:..) &lt;(.*?)&gt;', re.M)
                event = re.compile('(....-..-..) (..:..) -!- (.*)', re.M)
                url = re.compile('(http://[^ |\n]*)', re.M)
                text = re.sub(name,  r'<span foreground="grey">\2</span> <span foreground="darkgreen">\3:</span>', text)
                text = re.sub(event, r'<span foreground="grey">\2 -!- \3</span>', text)
                text = re.sub(url,   r'<a href="\1">\1</a>', text)
                gui.mainlabel.set_markup(text)
                f.close()
                gui.scrolltoend()
                gui.window.set_urgency_hint(True)
            except Exception as e:
                print e
        oldmtime = newmtime

class GUI():
    def __init__(self, path):
        self.path = path

        self.tree           = gtk.glade.XML('chan.glade')
        self.window         = self.tree.get_widget("mainWindow")
        self.scrolledwindow = self.tree.get_widget("mainScrolledWindow")
        self.mainlabel      = self.tree.get_widget("mainLabel")
        self.mainentry      = self.tree.get_widget("mainEntry")
        self.sendbutton     = self.tree.get_widget("sendButton")

        self.window.set_title(path.split('/')[-1:][0])
        self.mainentry.set_activates_default(True)

        self.window.connect("destroy", self.on_destroy)
        self.window.connect("visibility-notify-event", self.on_focus)
        self.window.connect("window-state-event", self.on_focus)
        self.window.connect("focus-in-event", self.on_focus)
        self.mainentry.connect("activate", self.on_send)
        self.sendbutton.connect("clicked", self.on_send)

        self.window.show_all()

    def on_destroy(self, widget, data=None):
        gtk.main_quit()

    def on_focus(self, widget, data=None):
        self.window.set_urgency_hint(False)

    def on_send(self, widget, data=None):
        message = self.mainentry.get_text()
        self.send_message(message)
        self.mainentry.set_text('')

    def send_message(self, message):
        f = open(path+'/in', 'w')
        f.write(message+'\n')
        f.close()

    def scrolltoend(self):
        adjustment = self.scrolledwindow.get_vadjustment()
        upper = adjustment.get_upper()
        adjustment.set_value(upper)

    def main(self):
        gtk.gdk.threads_init()
        gtk.gdk.threads_leave()
        gtk.main()
        gtk.gdk.threads_enter()
        gtk.gdk.flush()

if __name__ == '__main__':
    path = sys.argv[1]
    gui = GUI(path)
    guithread     = Thread(None, gui.main, None, (),          {})
    monitorthread = Thread(None, Monitor,  None, (path, gui), {})
    monitorthread.start()
    guithread.start()
