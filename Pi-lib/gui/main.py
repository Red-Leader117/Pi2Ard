from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from pi2ard.link import Link
from kivy.factory import Factory
from os.path import join, isfile
from kivy.garden.graph import LinePlot
from random import random

from datetime import timedelta

from kivy.config import Config
Config.set('graphics', 'minimum_width', 250)
Config.set('graphics', 'minimum_height', 250)

red = [1, 0, 0, 1]
orange = [1, 0.65, 0, 1]
green = [0, 1, 0, 1]
genericIndex = 0

class WarningDialog(BoxLayout):
    warningDlg = ObjectProperty(None)

    def __init__(self, path, **kwargs):
        self.register_event_type('on_answer')
        super(WarningDialog, self).__init__(**kwargs)
        self.warningDlg.text = "[i]{}[/i] already exists. Recording will overwrite any data in that file. To preserve data, select a different file.".format(path)

    def on_answer(self, *args):
        pass

class FilePickDialog(FloatLayout):
    saveBtn = ObjectProperty(None)
    textInput = ObjectProperty(None)
    cancelBtn = ObjectProperty(None)

    def __init__(self, save, cancel, **kwargs):
        super(FilePickDialog, self).__init__(**kwargs)
        self.save = save
        self.cancel = cancel

class Pi2ArdWidget(BoxLayout):
    statusLbl = ObjectProperty(None)
    fileLbl = ObjectProperty(None)
    timeLbl = ObjectProperty(None)
    graph = ObjectProperty(None)
    connectBtn = ObjectProperty(None)
    fileBtn = ObjectProperty(None)
    playBtn = ObjectProperty(None)
    stopBtn = ObjectProperty(None)

    def __init__(self, link, app, **kwargs):
        super(Pi2ArdWidget, self).__init__(**kwargs)
        self.link = link
        self.app = app
        self.savePath = "D:\\Documents\\Python\\pi2ard\\data\\"
        self.warningDialog = Popup(
            title = "Warning!",
            title_color = (1, 1, 0, 1),
            auto_dismiss = False,
            size_hint = (None, None),
            height = 200,
            width = 300)

    def toggleConnection(self):
        if self.app.linkState == 2:
            self.link.disconnect()
            self.app._updateStatus(0)
        else:
            self.link.connect()
            self.app._updateStatus(0)

    def openFilePick(self):
        self.filePickPopup = Popup(title = "Choose in what file to save the data",
            content = FilePickDialog(save = self.save, cancel = self.cancel),
            size_hint = (0.5, 0.9))
        self.filePickPopup.open()

    def play(self):
        self.app.startRec()
        self.elapsedSec = 0;
        self.loop = Clock.schedule_interval(self._updateTime, 1)
        self.playBtn.disabled = True
        self.fileBtn.disabled = True
        self.stopBtn.disabled = False
        self.timeLbl.text = "Recording time: 00:00:00"

    def stop(self):
        self.app.stopRec()
        self.fileBtn.disabled = False
        self.playBtn.disabled = False
        self.stopBtn.disabled = True
        self.loop.cancel()

    def changeStaus(self, new_state):
        if new_state == 0:
            self.statusLbl.color = red
            self.statusLbl.text = "Disconnected"
            self.connectBtn.disabled = True
            self.playBtn.disabled = True
        elif new_state == 1:
            self.statusLbl.color = orange
            self.statusLbl.text = "Device available"
            self.connectBtn.disabled = False
            self.playBtn.disabled = True
            self.connectBtn.text = "Connect"
        else:
            self.statusLbl.color = green
            self.statusLbl.text = "Connected"
            self.connectBtn.text = "Disconnect"
            self.playBtn.disabled = False

    def save(self, path, filename):
        self.savePath = self.fileLbl.text = join(path, filename)
        self.app._setPath(self.savePath)
        self.filePickPopup.dismiss()
        content = WarningDialog(path = self.savePath)
        content.bind(on_answer = self.dismiss_warning)
        
        if isfile(self.savePath):
            self.warningDialog.content = content
            self.warningDialog.open()

    def cancel(self):
        self.filePickPopup.dismiss()
        
    def dismiss_warning(self, instance):
        self.warningDialog.dismiss()

    def _updateTime(self, dt):
        self.elapsedSec += 1
        self.timeLbl.text = "Recording time: {}".format(timedelta(seconds = self.elapsedSec))

class Pi2ArdApp(App):
    def build(self):
        self.reset = False
        self.ymin = 0
        self.ymax = 0
        self.first = True
        self.path = ""
        self.file = None
        self.recording = False
        self.recordingDelta = 0.1
        self.linkState = 0  # 0 = unconnected, none detected (red)
                            # 1 = unconnected, detected (yellow)
                            # 2 = connected (green)
        self.link = Link()
        self.link.setOnReceive(self._onReceive)
        self.loop = Clock.schedule_interval(self._updateStatus, 0.5)
        self.recordingLoop = None
        self.widget = Pi2ArdWidget(link = self.link, app = self)
        return self.widget

    def _updateStatus(self, dt):
        avail = self.link.checkAvailable()
        if self.linkState == 0 and avail == True:
            self.linkState = 1
            self.widget.changeStaus(1)
        elif self.linkState == 1 and avail == False:
            self.linkState = 0
            self.widget.changeStaus(0)
        elif self.linkState == 1 and avail == True and self.link.isOpen() == True:
            self.linkState = 2
            self.widget.changeStaus(2)
        elif self.linkState == 2 and avail == True and self.link.isOpen() == False:
            self.linkState = 1
            self.widget.changeStaus(1)
        elif self.linkState == 2 and avail == False:
            self.linkState = 0
            self.widget.changeStaus(0)

    def _dataUpdate(self, dt):
        self.link.receive()

    def _setPath(self, path):
        self.path = path

    def on_stop(self):
        self.link.disconnect()
        if not self.recordingLoop is None:
            self.recordingLoop.cancel()

    def startRec(self):
        self.first = True
        genericIndex = 0
        if self.reset:
            for genericIndex in range(0, self.nPlots):
                self.widget.graph.remove_plot(self.plotsList[genericIndex])
        self.plotsList = []
        self.link.clearBuffer()
        self.file = open(self.path, "w")
        self.file.truncate(0)
        genericIndex = 0
        self.recordingLoop = Clock.schedule_interval(self._dataUpdate, self.recordingDelta)

    def stopRec(self):
        self.recordingLoop.cancel()
        self.file.close()
        self.reset = True

    def _onReceive(self, data):
        genericIndex = 0
        data = data.decode('utf-8').rstrip()
        if self.first:
            self.first = False
            self.plotsList = []
            self.nPlots = len(data.split(','))
            for genericIndex in range(0, self.nPlots):
                newPlot = LinePlot(line_width = 2, color=[random(), random(), random(), 1])
                self.widget.graph.add_plot(newPlot)
                self.plotsList.append(newPlot)
            self.file.write("Time,")
            for genericIndex in range(0, self.nPlots):
                if (genericIndex == self.nPlots - 1):
                    self.file.write("Plot {}\n".format(genericIndex + 1))
                else:
                    self.file.write("Plot {},".format(genericIndex + 1))
        
        self.addData(data)
        self.file.write("{}, {}\n".format(self.widget.elapsedSec, data))
        
    def addData(self, data):
        data = data.split(',')
        genericIndex = 0
        for genericIndex in range(0, self.nPlots):
            t = self.widget.elapsedSec
            self.widget.graph.xmax = t + 10
            self.widget.graph.xmin = t - 50
            self.plotsList[genericIndex].points.append((t, float(data[genericIndex])))
        genericIndex = 0
        for genericIndex in data:
            self.ymax = max(self.ymax, float(genericIndex))
            self.ymin = min(self.ymin, float(genericIndex))
            self.widget.graph.ymin = self.ymin - 2
            self.widget.graph.ymax = self.ymax + 2

if __name__ == "__main__":
    Pi2ArdApp().run()
