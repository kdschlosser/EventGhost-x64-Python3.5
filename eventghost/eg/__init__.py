# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import stackless
import sys
import os

_old_stderr = sys.stderr


class StdErrReplacement(object):
    softspace = 0
    _file = None
    _error = None
    _logFilePath = None
    _displayMessage = True
    encoding = "mbcs"

    def __init__(self):
        self._registered = False
        prgName = os.path.splitext(os.path.basename(sys.executable))[0]
        prgAppDataPath = os.path.join(os.environ["APPDATA"], prgName)
        self._logFilePath = os.path.join(prgAppDataPath, "Log.txt")
        if not os.path.exists(prgAppDataPath):
            os.mkdir(prgAppDataPath)

        try:
            self._file = open(self._logFilePath, 'a')

        except Exception as details:
            self._error = details
            self._file = None
            if "-q" not in sys.argv and "-quiet" not in sys.argv:  # NOQA
                import atexit
                import ctypes

                atexit.register(
                    ctypes.windll.user32.MessageBoxA,
                    0,
                    "The logfile '%s' could not be opened:\n %s" % (
                        self._logFilePath,
                        details
                    ),
                    "Error occurred in EventGhost",
                    0
                )

    def write(self, text):
        if self._error is None and not self._registered:
            if "-q" not in sys.argv and "-quiet" not in sys.argv:  # NOQA
                import atexit
                atexit.register(self.__DisplayMessage)
            self._registered = True

        if self._file is not None:
            self._file.write(text)
            self._file.flush()

    def flush(self):
        if self._file is not None:
            self._file.flush()

    def __DisplayMessage(self):
        if not self._displayMessage:
            return
        import ctypes

        message = ctypes.create_unicode_buffer(
            'See the logfile "%s" for details.\n\n'
            'Do you want to open the file now?'
            % self._logFilePath,
        )
        caption = ctypes.create_unicode_buffer(
            'Errors occurred in EventGhost'
        )
        res = ctypes.windll.user32.MessageBoxA(0, message, caption, 4)
        if res == 6:
            import subprocess

            subprocess.Popen('Notepad.exe "%s"' % self._logFilePath)


sys.stderr = StdErrReplacement()
logger = sys.stderr

# the following three import are needed if we are running from source and the
# Python distribution was not installed by the installer. See the following
# link for details:
# http://www.voidspace.org.uk/python/movpy/reference/win32ext.html#id10
import pywintypes # NOQA
import pythoncom # NOQA
import win32api # NOQA

# Local imports
from . import Python3Conversion # NOQA
from . import Cli # NOQA
from .Utils import *  # NOQA
from .Classes.WindowsVersion import WindowsVersion # NOQA


APP_NAME = "EventGhost"


class DynamicModule(object):
    def __init__(self):
        mod = sys.modules[__name__]
        self.__dict__ = mod.__dict__
        self.__orignal_module__ = mod
        sys.modules[__name__] = self

        import builtins

        builtins.eg = self

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        try:
            attr = __import__('eg.' + name, self.__dict__)
        except ImportError:
            mod = __import__("eg.Classes." + name, self.__dict__, {}, [name])
            self.__dict__[name] = attr = getattr(mod, name)
        return attr

    def __repr__(self):
        return "<dynamic-module '%s'>" % self.__name__

    def RaiseAssignments(self):
        """
        After this method is called, creation of new attributes will raise
        AttributeError.

        This is meanly used to find unintended assignments while debugging.
        """
        def __setattr__(self, name, value):
            if name not in self.__dict__:
                try:
                    raise AttributeError(
                        "Assignment to new attribute %s" % name
                    )
                except AttributeError:
                    import traceback
                    eg.PrintWarningNotice(traceback.format_exc())

            object.__setattr__(self, name, value)
        self.__class__.__setattr__ = __setattr__

    def tl(self, *args):
        out = ''
        for arg in args:
            out += repr(arg) + ','
        logger.write(out + '\n')
        # if sys.stdout is not None:
        #     sys.stdout.write(out + '\n')

    def Main(self):
        if Cli.args.install:
            return
        if Cli.args.translate:
            eg.LanguageEditor()
        elif Cli.args.pluginFile:
            eg.PluginInstall.Import(Cli.args.pluginFile)
            return
        else:
            eg.Init.InitGui()
        if eg.debugLevel:
            try:
                eg.Init.ImportAll()
            except:
                eg.PrintDebugNotice(sys.exc_info()[1])
        eg.Tasklet(eg.app.MainLoop)().run()
        stackless.run()


eg = DynamicModule()

__import__('Core', eg.__dict__, level=1)
# from . import Core  # NOQA

# this is here to make an IDE properly populate the AutoComplete
if "EventGhost.exe" not in sys.executable and not sys.argv[0].endswith('setup.py'):

    def RaiseAssignments():
        pass

    from .Init import ImportAll
    ImportAll()

    from .Core import (
        _CommandEvent,
        Exception,
        GetCurrentProcessId,
        StopException,
        HiddenAction,
        Bind,
        CallWait,
        DummyFunc,
        Exit,
        HasActiveHandler,
        MessageBox,
        Notify,
        RegisterPlugin,
        RestartAsyncore,
        RunProgram,
        Unbind,
        Wait,
        Icons,
        TracebackHook
    )

    from .Classes.AboutDialog import AboutDialog
    from .Classes.ActionBase import ActionBase
    from .Classes.ActionGroup import ActionGroup
    from .Classes.ActionItem import ActionItem
    from .Classes.ActionSelectButton import ActionSelectButton
    from .Classes.ActionThread import ActionThread
    from .Classes.ActionWithStringParameter import ActionWithStringParameter
    from .Classes.AddActionDialog import AddActionDialog
    from .Classes.AddActionGroupDialog import AddActionGroupDialog
    from .Classes.AddEventDialog import AddEventDialog
    from .Classes.AddPluginDialog import AddPluginDialog
    from .Classes.AnimatedWindow import AnimatedWindow
    from .Classes.App import App
    from .Classes.AutostartItem import AutostartItem
    from .Classes.BoxedGroup import BoxedGroup
    from .Classes.ButtonRow import ButtonRow
    from .Classes.CheckBoxGrid import CheckBoxGrid
    from .Classes.CheckUpdate import CheckUpdate
    from .Classes.Choice import Choice
    from .Classes.Colour import Colour
    from .Classes.ColourSelectButton import ColourSelectButton
    from .Classes.Config import Config
    from .Classes.ConfigDialog import ConfigDialog
    from .Classes.ConfigPanel import ConfigPanel
    from .Classes.ContainerItem import ContainerItem
    from .Classes.ControlProviderMixin import ControlProviderMixin
    from .Classes.Dialog import Dialog
    from .Classes.DigitOnlyValidator import DigitOnlyValidator
    from .Classes.DirBrowseButton import DirBrowseButton
    from .Classes.DisplayChoice import DisplayChoice
    from .Classes.Document import Document
    from .Classes.Environment import Environment
    from .Classes.EventGhostEvent import EventGhostEvent
    from .Classes.EventItem import EventItem
    from .Classes.EventRemapDialog import EventRemapDialog
    from .Classes.EventThread import EventThread
    from .Classes.Exceptions import Exceptions
    from .Classes.ExceptionsProvider import ExceptionsProvider
    from .Classes.ExportDialog import ExportDialog
    from .Classes.FileBrowseButton import FileBrowseButton
    from .Classes.FindDialog import FindDialog
    from .Classes.FolderItem import FolderItem
    from .Classes.FolderPath import FolderPath
    from .Classes.FontSelectButton import FontSelectButton
    from .Classes.GUID import GUID
    from .Classes.HeaderBox import HeaderBox
    from .Classes.HtmlDialog import HtmlDialog
    from .Classes.HtmlWindow import HtmlWindow
    from .Classes.HyperLinkCtrl import HyperLinkCtrl
    from .Classes.ImagePicker import ImagePicker
    from .Classes.IrDecoderPlugin import IrDecoderPlugin
    from .Classes.LanguageEditor import LanguageEditor
    from .Classes.License import License
    from .Classes.Log import Log
    from .Classes.MacroItem import MacroItem
    from .Classes.MacroSelectButton import MacroSelectButton
    from .Classes.MainMessageReceiver import MainMessageReceiver
    from .Classes.MessageDialog import MessageDialog
    from .Classes.MessageReceiver import MessageReceiver
    from .Classes.MonitorsCtrl import MonitorsCtrl
    from .Classes.NamespaceTree import NamespaceTree
    from .Classes.NetworkSend import NetworkSend
    from .Classes.OptionsDialog import OptionsDialog
    from .Classes.Panel import Panel
    from .Classes.Password import Password
    from .Classes.PasswordCtrl import PasswordCtrl
    from .Classes.PersistentData import PersistentData
    from .Classes.PluginBase import PluginBase
    from .Classes.PluginInstall import PluginInstall
    from .Classes.PluginInstanceInfo import PluginInstanceInfo
    from .Classes.PluginItem import PluginItem
    from .Classes.PluginManager import PluginManager
    from .Classes.PluginMetaClass import PluginMetaClass
    from .Classes.PluginModuleInfo import PluginModuleInfo
    from .Classes.PythonEditorCtrl import PythonEditorCtrl
    from .Classes.RadioBox import RadioBox
    from .Classes.RadioButtonGrid import RadioButtonGrid
    from .Classes.RawReceiverPlugin import RawReceiverPlugin
    from .Classes.ResettableTimer import ResettableTimer
    from .Classes.RootItem import RootItem
    from .Classes.Scheduler import Scheduler
    from .Classes.SerialPort import SerialPort
    from .Classes.SerialPortChoice import SerialPortChoice
    from .Classes.SerialThread import SerialThread
    from .Classes.Shortcut import Shortcut
    from .Classes.SimpleInputDialog import SimpleInputDialog
    from .Classes.SizeGrip import SizeGrip
    from .Classes.Slider import Slider
    from .Classes.SmartSpinIntCtrl import SmartSpinIntCtrl
    from .Classes.SmartSpinNumCtrl import SmartSpinNumCtrl
    from .Classes.SoundMixerTree import SoundMixerTree
    from .Classes.SpinIntCtrl import SpinIntCtrl
    from .Classes.SpinNumCtrl import SpinNumCtrl
    from .Classes.StaticTextBox import StaticTextBox
    from .Classes.StdLib import StdLib
    from .Classes.TaskBarIcon import TaskBarIcon
    from .Classes.Tasklet import Tasklet
    from .Classes.TaskletDialog import TaskletDialog
    from .Classes.Text import Text
    from .Classes.ThreadWorker import ThreadWorker
    from .Classes.TimeCtrl import TimeCtrl
    from .Classes.TimeCtrl_Duration import TimeCtrl_Duration
    from .Classes.TransferDialog import TransferDialog
    from .Classes.TranslatableStrings import TranslatableStrings
    from .Classes.Translation import Translation
    from .Classes.TreeItem import TreeItem
    from .Classes.TreeItemBrowseCtrl import TreeItemBrowseCtrl
    from .Classes.TreeItemBrowseDialog import TreeItemBrowseDialog
    from .Classes.TreeLink import TreeLink
    from .Classes.TreePosition import TreePosition
    from .Classes.Version import Version
    from .Classes.WindowDragFinder import WindowDragFinder
    from .Classes.WindowList import WindowList
    from .Classes.WindowMatcher import WindowMatcher
    from .Classes.WindowsVersion import WindowsVersion
    from .Classes.WindowTree import WindowTree
    from .Classes.WinUsb import WinUsb
    from .Classes.WinUsbRemote import WinUsbRemote
    from .Classes.MainFrame import MainFrame
    from .Classes.UndoHandler import UndoHandler
    from .Classes.IrDecoder import IrDecoder

    from .WinApi.SendKeys import SendKeysParser

    useTreeItemGUID = Core.eg.useTreeItemGUID
    CORE_PLUGIN_GUIDS = Core.eg.CORE_PLUGIN_GUIDS

    from . import NamedPipe

    namedPipe = NamedPipe.Server()
    ID_TEST = eg.ID_TEST
    revision = eg.revision
    startupArguments = Cli.args
    systemEncoding = eg.systemEncoding
    result = eg.result
    globals = Bunch()
    globals.eg = eg
    event = eg.event
    eventTable = eg.eventTable
    eventString = eg.eventString
    notificationHandlers = eg.notificationHandlers
    programCounter = eg.programCounter
    programReturnStack = eg.programReturnStack
    indent = Core.eg.indent
    pluginList = eg.pluginList
    mainThread = eg.mainThread
    stopExecutionFlag = eg.stopExecutionFlag
    lastFoundWindows = eg.lastFoundWindows
    currentItem = eg.currentItem
    actionGroup = Bunch()
    actionGroup.items = []
    GUID = GUID()
    CommandEvent = _CommandEvent
    ValueChangedEvent, EVT_VALUE_CHANGED = eg.CommandEvent()
    pyCrustFrame = eg.pyCrustFrame
    dummyAsyncoreDispatcher = eg.dummyAsyncoreDispatcher
    processId = eg.GetCurrentProcessId()

    messageReceiver = MainMessageReceiver()
    app = App()
    log = Log()


    def Print(*args, **kwargs):
        pass


    def PrintDebugNotice(*args):
        pass


    def PrintWarningNotice(*args):
        pass


    def PrintError(*args, **kwargs):
        pass


    def PrintNotice(*args, **kwargs):
        pass


    def PrintStack(skip=0):
        pass


    def PrintTraceback(msg=None, skip=0, source=None, excInfo=None):
        pass


    config = Config()
    debugLevel = config.logDebug
    colour = Colour()
    text = Text('en_US')
    actionThread = ActionThread()
    eventThread = EventThread()
    pluginManager = PluginManager()
    scheduler = Scheduler()


    def TriggerEvent(
        suffix,
        payload=None,
        prefix="Main",
        source=eg
    ):
        pass


    def TriggerEnduringEvent(
        suffix,
        payload=None,
        prefix="Main",
        source=Core.eg
    ):
        pass


    SendKeys = SendKeysParser()
    PluginClass = PluginBase
    ActionClass = ActionBase
    taskBarIcon = TaskBarIcon(False)


    def SetProcessingState(state, event):
        pass


    wit = False
    document = Document()
    mainFrame = MainFrame(document)
    folderPath = FolderPath()
    mainDir = folderPath.mainDir
    configDir = folderPath.configDir
    corePluginDir = folderPath.corePluginDir
    localPluginDir = folderPath.localPluginDir
    imagesDir = folderPath.imagesDir
    languagesDir = folderPath.languagesDir
    sitePackagesDir = folderPath.sitePackagesDir
    pluginDirs = [corePluginDir, localPluginDir]

    cFunctions = __import__('cFunctions')

    from types import ModuleType

    UserPluginModule = ModuleType("eg.UserPluginModule")
    UserPluginModule.__path__ = [localPluginDir]

    from .CorePluginModule import AIRT
    from .CorePluginModule import AsusPsr2000
    from .CorePluginModule import AtiRemoteWonder2WinUsb
    from .CorePluginModule import Auvisio
    from .CorePluginModule import BSPlayer
    from .CorePluginModule import BT8x8
    from .CorePluginModule import Barco
    from .CorePluginModule import Billy
    from .CorePluginModule import Broadcaster
    from .CorePluginModule import CM11A
    from .CorePluginModule import CambridgeAudioSerial
    from .CorePluginModule import Conceptronic
    from .CorePluginModule import CyberlinkUniversalRemote
    from .CorePluginModule import DBox2
    from .CorePluginModule import DScaler4
    from .CorePluginModule import DVBDream
    from .CorePluginModule import DVBViewer
    from .CorePluginModule import DenonSerial
    from .CorePluginModule import DesktopRemote
    from .CorePluginModule import DirectoryWatcher
    from .CorePluginModule import DynamicWebserver
    E_mail = __import__('.CorePluginModule.E-mail')
    from .CorePluginModule import EventGhost
    from .CorePluginModule import EventPhone
    from .CorePluginModule import FS20PCE
    from .CorePluginModule import FS20PCS
    from .CorePluginModule import Fhz1000Pc
    from .CorePluginModule import FileOperations
    from .CorePluginModule import Foobar2000
    from .CorePluginModule import GOMPlayer
    from .CorePluginModule import GameVoice
    from .CorePluginModule import H79Serial
    from .CorePluginModule import HID
    from .CorePluginModule import HarmanKardon
    from .CorePluginModule import HauppaugeIR
    from .CorePluginModule import Homeseer
    from .CorePluginModule import IgorPlugUDP
    from .CorePluginModule import IgorPlugUSB
    from .CorePluginModule import IrfanView
    from .CorePluginModule import JVCHD1Serial
    from .CorePluginModule import Joystick
    from .CorePluginModule import JvcDlaSerial
    from .CorePluginModule import KIRA
    from .CorePluginModule import Keyboard
    from .CorePluginModule import Lirc
    from .CorePluginModule import LogitechUltraX
    from .CorePluginModule import MCE
    from .CorePluginModule import MarantzSerial
    from .CorePluginModule import MceRemote
    from .CorePluginModule import MceRemote_Vista
    from .CorePluginModule import MediaMonkey
    from .CorePluginModule import MediaPlayerClassic
    from .CorePluginModule import MediaPortal
    from .CorePluginModule import Meedio
    from .CorePluginModule import Mouse
    from .CorePluginModule import Multitap
    from .CorePluginModule import MyTheatre
    from .CorePluginModule import NetworkReceiver
    from .CorePluginModule import NetworkSender
    from .CorePluginModule import OOo_Impress
    from .CorePluginModule import OSE
    from .CorePluginModule import OSM
    from .CorePluginModule import Onkyo
    from .CorePluginModule import OnkyoISCP
    PC_Remote_Controller = __import__('.CorePluginModule.PC Remote Controller')
    from .CorePluginModule import PHX01RN
    from .CorePluginModule import PS3
    from .CorePluginModule import Phoner
    from .CorePluginModule import Ping
    from .CorePluginModule import PowerDVD
    from .CorePluginModule import ProcessWatcher
    from .CorePluginModule import RFXcom_xPL
    from .CorePluginModule import RadioSure
    from .CorePluginModule import RawInput
    from .CorePluginModule import RemoteEventMapper
    from .CorePluginModule import SageTV
    from .CorePluginModule import SamsungTV
    from .CorePluginModule import SchedulGhost
    from .CorePluginModule import Scheduler
    from .CorePluginModule import ScreamerRadio
    from .CorePluginModule import Serial
    from .CorePluginModule import SmallPcRemote
    from .CorePluginModule import SoundMixerEx
    from .CorePluginModule import Speech
    from .CorePluginModule import Speedlink6399
    from .CorePluginModule import SplashLite
    from .CorePluginModule import Streamzap
    from .CorePluginModule import SunTracker
    from .CorePluginModule import SysTrayMenu
    from .CorePluginModule import System
    from .CorePluginModule import TVcentral
    from .CorePluginModule import Task
    from .CorePluginModule import TechniSatUsb
    from .CorePluginModule import TechnoTrendIr
    from .CorePluginModule import TechnoTrendIrBda
    from .CorePluginModule import TellStick
    from .CorePluginModule import TerratecUsb
    from .CorePluginModule import Test
    from .CorePluginModule import TestPatterns
    from .CorePluginModule import TheaterTek
    from .CorePluginModule import Timer
    from .CorePluginModule import Tira
    from .CorePluginModule import UIR
    from .CorePluginModule import UIRT2
    USB_RFID = __import__('.CorePluginModule.USB-RFID')
    USB_UIRT = __import__('.CorePluginModule.USB-UIRT')
    from .CorePluginModule import VLC
    from .CorePluginModule import WMPlayer
    from .CorePluginModule import Weather
    from .CorePluginModule import Webserver
    from .CorePluginModule import WinUsbTest
    from .CorePluginModule import Winamp
    from .CorePluginModule import Window
    from .CorePluginModule import X10
    from .CorePluginModule import XBCDRC
    from .CorePluginModule import XBMCEventReceiver
    from .CorePluginModule import XBMCRepeat
    from .CorePluginModule import YARD
    from .CorePluginModule import YamahaSerial
    from .CorePluginModule import ZoomPlayer
    from .CorePluginModule import ffdshow
    from .CorePluginModule import xPL

    from .CorePluginModule.System.Command import Command
    from .CorePluginModule.System.Execute import Execute

    from . import CorePluginModule as _CorePluginModule
    from importlib.machinery import ModuleSpec

    class CorePluginModule(object):
        __cached__ = _CorePluginModule.__cached__
        __file__ = _CorePluginModule.__file__
        __path__ = _CorePluginModule.__path__
        __loader__ = _CorePluginModule.__loader__
        __name__ = 'eg.' + _CorePluginModule.__name__
        __package__ = 'eg.' + _CorePluginModule.__package__
        __spec__ = ModuleSpec(
            name='eg.' + _CorePluginModule.__name__,
            loader=_CorePluginModule.__loader__,
            origin=_CorePluginModule.__file__,
            is_package=True
        )
        __spec__.submodule_search_locations = _CorePluginModule.__path__

        class AIRT(object):
            plugin = AIRT.AIRT()


        class AsusPsr2000(object):
            plugin = AsusPsr2000.AsusPsr2000()


        class AtiRemoteWonder2(object):
            plugin = AtiRemoteWonder2WinUsb.AtiRemoteWonder2()


        class Auvisio(object):
            plugin = Auvisio.Auvisio()


        class BSPlayer(object):
            plugin = BSPlayer.BSPlayer()


        class BtRemote(object):
            plugin = BT8x8.BtRemote()


        class Barco(object):
            plugin = Barco.Barco()
            ActionBase = Barco.ActionBase()
            SendCustom = Barco.SendCustom()
            SetText = Barco.SetText()
            ReadTime = Barco.ReadTime()
            ReadStatus = Barco.ReadStatus()
            ReadVersion = Barco.ReadVersion()
            ReadSerialNumber = Barco.ReadSerialNumber()
            GetInfo = Barco.GetInfo()
            RequestShape = Barco.RequestShape()
            LockIr = Barco.LockIr()
            ReadPotentiometer = Barco.ReadPotentiometer()
            WritePotentiometer = Barco.WritePotentiometer()


        class Billy(object):
            plugin = Billy.Billy()


        class BroadcastListener(object):
            plugin = Broadcaster.BroadcastListener()
            Broadcast = Broadcaster.Broadcast()


        class CM11A(object):
            plugin = CM11A.CM11A()


        class CambridgeAudioSerial(object):
            plugin = CambridgeAudioSerial.CambridgeAudioSerial()
            ValueAction = CambridgeAudioSerial.ValueAction()
            Raw = CambridgeAudioSerial.Raw()


        class Conceptronic(object):
            plugin = Conceptronic.Conceptronic()


        class CyberlinkUniversalRemote(object):
            plugin = CyberlinkUniversalRemote.CyberlinkUniversalRemote()


        class DBox2(object):
            plugin = DBox2.DBox2()
            ActionPrototype = DBox2.ActionPrototype()


        class Dscaler(object):
            plugin = DScaler4.Dscaler()


        class DVBDream(object):
            plugin = DVBDream.DVBDream()


        class DVBViewer(object):
            plugin = DVBViewer.DVBViewer()


        class DenonSerial(object):
            plugin = DenonSerial.DenonSerial()
            ValueAction = DenonSerial.ValueAction()
            MasterFade = DenonSerial.MasterFade()
            Raw = DenonSerial.Raw()


        class DesktopRemote(object):
            plugin = DesktopRemote.DesktopRemote()
            CreateNew = DesktopRemote.CreateNew()
            AddButton = DesktopRemote.AddButton()
            StartNewLine = DesktopRemote.StartNewLine()
            Show = DesktopRemote.Show()
            Close = DesktopRemote.Close()


        class DirectoryWatcher(object):
            plugin = DirectoryWatcher.DirectoryWatcher()


        class DynamicWebserver(object):
            plugin = DynamicWebserver.DynamicWebserver()


        class E_mail(object):
            plugin = E_mail.E_mail()


        class EventGhost(object):
            plugin = EventGhost.EventGhost()
            EnableItem = EventGhost.EnableItem()
            AutoRepeat = EventGhost.AutoRepeat()
            Comment = EventGhost.Comment()
            DisableItem = EventGhost.DisableItem()
            DumpResult = EventGhost.DumpResult()
            EnableExclusive = EventGhost.EnableExclusive()
            FlushEvents = EventGhost.FlushEvents()
            GetItemState = EventGhost.GetItemState()
            JumpIfDoubleEvent = EventGhost.JumpIfDoubleEvent()
            JumpIfLongPress = EventGhost.JumpIfLongPress()
            OpenConfig = EventGhost.OpenConfig()
            OpenEventGhost = EventGhost.OpenEventGhost()
            PythonCommand = EventGhost.PythonCommand()
            StopProcessing = EventGhost.StopProcessing()
            TriggerEvent = EventGhost.TriggerEvent()
            Wait = EventGhost.Wait()


        class EventPhone(object):
            plugin = EventPhone.EventPhone()


        class FS20PCE(object):
            plugin = FS20PCE.FS20PCE()


        class FS20PCS(object):
            plugin = FS20PCS.FS20PCS()
            ActionBase = FS20PCS.ActionBase()
            SimpleAction = FS20PCS.SimpleAction()
            RepeatAction = FS20PCS.RepeatAction()
            RepeatTimerValueAction = FS20PCS.RepeatTimerValueAction()
            TimerValueAction = FS20PCS.TimerValueAction()
            Dim = FS20PCS.Dim()
            DimTimer = FS20PCS.DimTimer()


        class Fhz1000Pc(object):
            plugin = Fhz1000Pc.Fhz1000Pc()
            ActionBase = Fhz1000Pc.ActionBase()
            Dim = Fhz1000Pc.Dim()
            Off = Fhz1000Pc.Off()
            On = Fhz1000Pc.On()
            ToggleDim = Fhz1000Pc.ToggleDim()
            DimUp = Fhz1000Pc.DimUp()
            DimDown = Fhz1000Pc.DimDown()
            Toggle = Fhz1000Pc.Toggle()
            StartProgramTimer = Fhz1000Pc.StartProgramTimer()
            ResetToFactoryDefaults = Fhz1000Pc.ResetToFactoryDefaults()


        class FileOperations(object):
            plugin = FileOperations.FileOperations()


        class Foobar2000(object):
            plugin = Foobar2000.Foobar2000()


        class GOMPlayer(object):
            plugin = GOMPlayer.GOMPlayer()


        class GameVoice(object):
            plugin = GameVoice.GameVoice()


        class H79Serial(object):
            plugin = H79Serial.H79Serial()


        class HID(object):
            plugin = HID.HID()


        class HarmanKardon(object):
            plugin = HarmanKardon.HarmanKardon()


        class HauppaugeIR(object):
            plugin = HauppaugeIR.HauppaugeIR()


        class HomeseerPlugin(object):
            plugin = Homeseer.HomeseerPlugin()


        class IgorPlugUDP(object):
            plugin = IgorPlugUDP.IgorPlugUDP()


        class IgorPlugUSB(object):
            plugin = IgorPlugUSB.IgorPlugUSB()


        class IrfanView(object):
            plugin = IrfanView.IrfanView()


        class JVCHD1Serial(object):
            plugin = JVCHD1Serial.JVCHD1Serial()


        class Joystick(object):
            plugin = Joystick.Joystick()


        class JvcDlaSerial(object):
            plugin = JvcDlaSerial.JvcDlaSerial()


        class KIRA(object):
            plugin = KIRA.KIRA()


        class Keyboard(object):
            plugin = Keyboard.Keyboard()


        class Lirc(object):
            plugin = Lirc.Lirc()


        class UltraX(object):
            plugin = LogitechUltraX.UltraX()


        class MCE(object):
            plugin = MCE.MCE()


        class MarantzSerial(object):
            plugin = MarantzSerial.MarantzSerial()
            MarantzSerialSetVolumeAbsolute = MarantzSerial.MarantzSerialSetVolumeAbsolute()
            MarantzSerialSetVolumeRelative = MarantzSerial.MarantzSerialSetVolumeRelative()


        class MceRemote(object):
            plugin = MceRemote.MceRemote()
            TransmitIr = MceRemote.TransmitIr()


        class MCE_Vista(object):
            plugin = MceRemote_Vista.MCE_Vista()
            GetIR = MceRemote_Vista.GetIR()
            TransmitIR = MceRemote_Vista.TransmitIR()
            GetDeviceInfo = MceRemote_Vista.GetDeviceInfo()
            TestIR = MceRemote_Vista.TestIR()
            SetLearnMode = MceRemote_Vista.SetLearnMode()
            SetNormalMode = MceRemote_Vista.SetNormalMode()


        class MediaMonkey(object):
            plugin = MediaMonkey.MediaMonkey()
            Start = MediaMonkey.Start()
            Exit = MediaMonkey.Exit()
            Play = MediaMonkey.Play()
            TogglePlay = MediaMonkey.TogglePlay()
            DiscretePause = MediaMonkey.DiscretePause()
            Stop = MediaMonkey.Stop()
            StopAfterCurrent = MediaMonkey.StopAfterCurrent()
            Next = MediaMonkey.Next()
            Previous = MediaMonkey.Previous()
            ToggleMute = MediaMonkey.ToggleMute()
            SetVolume = MediaMonkey.SetVolume()
            VolumeUp = MediaMonkey.VolumeUp()
            VolumeDown = MediaMonkey.VolumeDown()
            SetBalance = MediaMonkey.SetBalance()
            SetShuffle = MediaMonkey.SetShuffle()
            SetRepeat = MediaMonkey.SetRepeat()
            SetAutoDJ = MediaMonkey.SetAutoDJ()
            SetCrossfade = MediaMonkey.SetCrossfade()
            BalanceRight = MediaMonkey.BalanceRight()
            BalanceLeft = MediaMonkey.BalanceLeft()
            Seek = MediaMonkey.Seek()
            GetPlaylists = MediaMonkey.GetPlaylists()
            GetBasicStatistics = MediaMonkey.GetBasicStatistics()
            GetNotAccessibleTracks = MediaMonkey.GetNotAccessibleTracks()
            GetSomeInfo = MediaMonkey.GetSomeInfo()
            GetIsRunning = MediaMonkey.GetIsRunning()
            GetShuffle = MediaMonkey.GetShuffle()
            GetStatus = MediaMonkey.GetStatus()
            GetSongInfo = MediaMonkey.GetSongInfo()
            GetDetailSongInfo = MediaMonkey.GetDetailSongInfo()
            GetClassificationInfo = MediaMonkey.GetClassificationInfo()
            GetTechnicalSongInfo = MediaMonkey.GetTechnicalSongInfo()
            GetUniversal = MediaMonkey.GetUniversal()
            WritingToMM = MediaMonkey.WritingToMM()
            LoadPlaylist = MediaMonkey.LoadPlaylist()
            AddCurrentSongToPlaylist = MediaMonkey.AddCurrentSongToPlaylist()
            RemoveCurrentSongFromPlaylist = MediaMonkey.RemoveCurrentSongFromPlaylist()
            RemoveCurrentSongFromNowPlaying = MediaMonkey.RemoveCurrentSongFromNowPlaying()
            LoadPlaylistByFilter = MediaMonkey.LoadPlaylistByFilter()
            LoadPlaylistBySql = MediaMonkey.LoadPlaylistBySql()
            Jukebox = MediaMonkey.Jukebox()
            SongJukebox = MediaMonkey.SongJukebox()
            SendKeys = MediaMonkey.SendKeys()


        class MediaPlayerClassic(object):
            plugin = MediaPlayerClassic.MediaPlayerClassic()
            ActionPrototype = MediaPlayerClassic.ActionPrototype()
            GetWindowState = MediaPlayerClassic.GetWindowState()
            GetPlayState = MediaPlayerClassic.GetPlayState()
            GetNowPlaying = MediaPlayerClassic.GetNowPlaying()
            GetTimes = MediaPlayerClassic.GetTimes()
            GoTo_OSD = MediaPlayerClassic.GoTo_OSD()
            Run = MediaPlayerClassic.Run()
            SendCmd = MediaPlayerClassic.SendCmd()
            GetInfo = MediaPlayerClassic.GetInfo()
            OpenFile = MediaPlayerClassic.OpenFile()
            GetPosition = MediaPlayerClassic.GetPosition()
            SetInteger = MediaPlayerClassic.SetInteger()
            SendOSD = MediaPlayerClassic.SendOSD()


        class MediaPortal(object):
            plugin = MediaPortal.MediaPortal()
            ActionPrototype = MediaPortal.ActionPrototype()


        class MeedioPlugin(object):
            plugin = Meedio.MeedioPlugin()


        class Mouse(object):
            plugin = Mouse.Mouse()
            GoDirection = Mouse.GoDirection()
            LeftButton = Mouse.LeftButton()
            LeftDoubleClick = Mouse.LeftDoubleClick()
            MiddleButton = Mouse.MiddleButton()
            MouseWheel = Mouse.MouseWheel()
            MoveAbsolute = Mouse.MoveAbsolute()
            MoveRelative = Mouse.MoveRelative()
            RightButton = Mouse.RightButton()
            RightDoubleClick = Mouse.RightDoubleClick()
            ToggleLeftButton = Mouse.ToggleLeftButton()


        class Multitap(object):
            plugin = Multitap.Multitap()


        class MyTheatre(object):
            plugin = MyTheatre.MyTheatre()


        class NetworkReceiver(object):
            plugin = NetworkReceiver.NetworkReceiver()


        class NetworkSender(object):
            plugin = NetworkSender.NetworkSender()
            Map = NetworkSender.Map()


        class Impress(object):
            plugin = OOo_Impress.Impress()


        class OSE(object):
            plugin = OSE.OSE()
            ShowMenu = OSE.ShowMenu()
            MoveCursor = OSE.MoveCursor()
            PageUpDown = OSE.PageUpDown()
            Cancel = OSE.Cancel()
            GoToParent = OSE.GoToParent()
            GoBack = OSE.GoBack()
            GetValue = OSE.GetValue()
            Execute = OSE.Execute()


        class OSM(object):
            plugin = OSM.OSM()
            ShowMenu = OSM.ShowMenu()
            CreateMenuFromList = OSM.CreateMenuFromList()
            MoveCursor = OSM.MoveCursor()
            PageUpDown = OSM.PageUpDown()
            OK_Btn = OSM.OK_Btn()
            Num_Btn = OSM.Num_Btn()
            Cancel_Btn = OSM.Cancel_Btn()
            Get_Btn = OSM.Get_Btn()


        class OnkyoSerial(object):
            plugin = Onkyo.OnkyoSerial()
            ValueAction = Onkyo.ValueAction()
            Raw = Onkyo.Raw()


        class OnkyoISCP(object):
            plugin = OnkyoISCP.OnkyoISCP()
            SendCommand = OnkyoISCP.SendCommand()


        class PcRemoteController(object):
            plugin = PC_Remote_Controller.PcRemoteController()


        class PHX01RN(object):
            plugin = PHX01RN.PHX01RN()


        class HIDPS3(object):
            plugin = PS3.HIDPS3()


        class Phoner(object):
            plugin = Phoner.Phoner()
            Start = Phoner.Start()
            Exit = Phoner.Exit()
            MakeCall = Phoner.MakeCall()
            MakeCallOver = Phoner.MakeCallOver()
            Transfer = Phoner.Transfer()
            Conference = Phoner.Conference()
            SendDTMF = Phoner.SendDTMF()
            SendWAVE = Phoner.SendWAVE()
            SendTTS = Phoner.SendTTS()
            SendSMS = Phoner.SendSMS()
            SendSMSService = Phoner.SendSMSService()
            DisconnectReason = Phoner.DisconnectReason()
            CallFunction = Phoner.CallFunction()
            NumberOfCalls = Phoner.NumberOfCalls()
            GetInfo2 = Phoner.GetInfo2()
            SetState = Phoner.SetState()
            ToggleRecording = Phoner.ToggleRecording()
            GetInfo = Phoner.GetInfo()


        class PingPlugin(object):
            plugin = Ping.PingPlugin()
            OnePing = Ping.OnePing()
            AddHost = Ping.AddHost()
            RemoveHost = Ping.RemoveHost()
            GetHostsStatus = Ping.GetHostsStatus()


        class PowerDvd(object):
            plugin = PowerDVD.PowerDvd()
            ActionPrototype = PowerDVD.ActionPrototype()


        class Process(object):
            plugin = ProcessWatcher.Process()


        class RFXcom(object):
            plugin = RFXcom_xPL.RFXcom()


        class RadioSure(object):
            plugin = RadioSure.RadioSure()
            Run = RadioSure.Run()
            WindowControl = RadioSure.WindowControl()
            SendMessageActions = RadioSure.SendMessageActions()
            MinimRest = RadioSure.MinimRest()
            CheckAndChange = RadioSure.CheckAndChange()
            GetStatus = RadioSure.GetStatus()
            GetMenuItem = RadioSure.GetMenuItem()
            SetVolume = RadioSure.SetVolume()
            GetVolume = RadioSure.GetVolume()
            SelectFav = RadioSure.SelectFav()
            NextPrevFav = RadioSure.NextPrevFav()
            RandomFav = RadioSure.RandomFav()
            GetPlayingTitle = RadioSure.GetPlayingTitle()
            StartTitlebarObservation = RadioSure.StartTitlebarObservation()
            StopTitlebarObservation = RadioSure.StopTitlebarObservation()
            OpenManager = RadioSure.OpenManager()
            HideManager = RadioSure.HideManager()
            GetFavorites = RadioSure.GetFavorites()
            OpenScheduler = RadioSure.OpenScheduler()
            HideScheduler = RadioSure.HideScheduler()
            EnableSchedule = RadioSure.EnableSchedule()
            EnableAll = RadioSure.EnableAll()
            DeleteSchedule = RadioSure.DeleteSchedule()
            RunScheduleImmediately = RadioSure.RunScheduleImmediately()
            AddSchedule = RadioSure.AddSchedule()


        class RawInput(object):
            plugin = RawInput.RawInput()


        class RemoteEventMapper(object):
            plugin = RemoteEventMapper.RemoteEventMapper()


        class SageTV(object):
            plugin = SageTV.SageTV()


        class SamsungSerial(object):
            plugin = SamsungTV.SamsungSerial()
            ValueAction = SamsungTV.ValueAction()
            Raw = SamsungTV.Raw()


        class SchedulGhost(object):
            plugin = SchedulGhost.SchedulGhost()
            ShowSchedulGhost = SchedulGhost.ShowSchedulGhost()
            HideSchedulGhost = SchedulGhost.HideSchedulGhost()
            EnableSchedule = SchedulGhost.EnableSchedule()
            EnableAll = SchedulGhost.EnableAll()
            DeleteSchedule = SchedulGhost.DeleteSchedule()
            RunScheduleImmediately = SchedulGhost.RunScheduleImmediately()
            AddSchedule = SchedulGhost.AddSchedule()
            SetEggTimer = SchedulGhost.SetEggTimer()
            ShowRunningEggTimers = SchedulGhost.ShowRunningEggTimers()
            AbortEggTimers = SchedulGhost.AbortEggTimers()
            DataToXML = SchedulGhost.DataToXML()
            ReloadXML = SchedulGhost.ReloadXML()
            AbortEggTimer = SchedulGhost.AbortEggTimer()


        class Scheduler(object):
            plugin = Scheduler.Scheduler()


        class ScreamerRadio(object):
            plugin = ScreamerRadio.ScreamerRadio()


        class Serial(object):
            plugin = Serial.Serial()
            Write = Serial.Write()
            Read = Serial.Read()


        class SmallPcRemote(object):
            plugin = SmallPcRemote.SmallPcRemote()


        class SoundMixerEx(object):
            plugin = SoundMixerEx.SoundMixerEx()


        class Speech(object):
            plugin = Speech.Speech()


        class Speedlink(object):
            plugin = Speedlink6399.Speedlink()


        class SplashLite(object):
            plugin = SplashLite.SplashLite()
            Run = SplashLite.Run()
            HotKeyAction = SplashLite.HotKeyAction()
            OpenFile = SplashLite.OpenFile()


        class Streamzap(object):
            plugin = Streamzap.Streamzap()


        class Suntracker(object):
            plugin = SunTracker.Suntracker()


        class SysTrayMenu(object):
            plugin = SysTrayMenu.SysTrayMenu()
            Enable = SysTrayMenu.Enable()
            Disable = SysTrayMenu.Disable()


        class System(object):
            plugin = System.System()
            GetBootTimestamp = System.GetBootTimestamp()
            GetUpTime = System.GetUpTime()
            OpenDriveTray = System.OpenDriveTray()
            RefreshEnvironment = System.RefreshEnvironment()
            ResetIdleTimer = System.ResetIdleTimer()
            SetClipboard = System.SetClipboard()
            SetIdleTime = System.SetIdleTime()
            WakeOnLan = System.WakeOnLan()
            Command = Command()
            Execute = Execute()
            MonitorPowerOff = System.MonitorPowerOff()
            MonitorPowerOn = System.MonitorPowerOn()
            MonitorStandby = System.MonitorStandby()
            SetDisplayPreset = System.SetDisplayPreset()
            SetWallpaper = System.SetWallpaper()
            StartScreenSaver = System.StartScreenSaver()
            DisplayImage = System.DisplayImage()
            HideImage = System.HideImage()
            ShowPicture = System.ShowPicture()
            ShowQRcode = System.ShowQRcode()
            __ComputerPowerAction = System.__ComputerPowerAction()
            Hibernate = System.Hibernate()
            LockWorkstation = System.LockWorkstation()
            LogOff = System.LogOff()
            PowerDown = System.PowerDown()
            Reboot = System.Reboot()
            SetSystemIdleTimer = System.SetSystemIdleTimer()
            Standby = System.Standby()
            ChangeMasterVolumeBy = System.ChangeMasterVolumeBy()
            GetMute = System.GetMute()
            MuteOff = System.MuteOff()
            MuteOn = System.MuteOn()
            PlaySound = System.PlaySound()
            SetMasterVolume = System.SetMasterVolume()
            ToggleMute = System.ToggleMute()


        class TVcentral(object):
            plugin = TVcentral.TVcentral()


        class Task(object):
            plugin = Task.Task()


        class TechniSatUsb(object):
            plugin = TechniSatUsb.TechniSatUsb()


        class TTIR(object):
            plugin = TechnoTrendIr.TTIR()


        class TTIRBDA(object):
            plugin = TechnoTrendIrBda.TTIRBDA()


        class TellStick(object):
            plugin = TellStick.TellStick()


        class TerratecUsb(object):
            plugin = TerratecUsb.TerratecUsb()


        class Test(object):
            plugin = Test.Test()
            TestAction = Test.TestAction()


        class TestPatterns(object):
            plugin = TestPatterns.TestPatterns()
            TestPatternAction = TestPatterns.TestPatternAction()
            SetDisplay = TestPatterns.SetDisplay()
            Focus = TestPatterns.Focus()
            IreWindow = TestPatterns.IreWindow()
            Checkerboard = TestPatterns.Checkerboard()
            Grid = TestPatterns.Grid()
            Dots = TestPatterns.Dots()
            ZonePlate = TestPatterns.ZonePlate()
            Lines = TestPatterns.Lines()
            Bars = TestPatterns.Bars()
            SiemensStar = TestPatterns.SiemensStar()
            Burst = TestPatterns.Burst()
            Geometry = TestPatterns.Geometry()
            PixelCropping = TestPatterns.PixelCropping()
            Readability = TestPatterns.Readability()
            Close = TestPatterns.Close()


        class TheaterTek(object):
            plugin = TheaterTek.TheaterTek()
            stdActionWithStringParameter = TheaterTek.stdActionWithStringParameter()


        class Timer(object):
            plugin = Timer.Timer()


        class Tira(object):
            plugin = Tira.Tira()
            TransmitIR = Tira.TransmitIR()


        class UIR(object):
            plugin = UIR.UIR()


        class UIRT2(object):
            plugin = UIRT2.UIRT2()
            TransmitIR = UIRT2.TransmitIR()


        class USB_RFID(object):
            plugin = USB_RFID.USB_RFID()
            ActionBase = USB_RFID.ActionBase()


        class USB_UIRT(object):
            plugin = USB_UIRT.USB_UIRT()


        class VLC(object):
            plugin = VLC.VLC()
            ActionPrototype = VLC.ActionPrototype()
            Start = VLC.Start()
            GetSomeInfo = VLC.GetSomeInfo()
            SimulateKey = VLC.SimulateKey()
            SimulKey = VLC.SimulKey()
            GetHotkeys = VLC.GetHotkeys()
            GetTime = VLC.GetTime()
            GetLength = VLC.GetLength()
            SwitchTrack = VLC.SwitchTrack()
            MyCommand = VLC.MyCommand()
            Seek = VLC.Seek()


        class WMPlayer(object):
            plugin = WMPlayer.WMPlayer()


        class Weather(object):
            plugin = Weather.Weather()


        class Webserver(object):
            plugin = Webserver.Webserver()
            WsBroadcastMessage = Webserver.WsBroadcastMessage()
            WsBroadcastValue = Webserver.WsBroadcastValue()
            WsBroadcastAllValues = Webserver.WsBroadcastAllValues()
            WsBroadcastData = Webserver.WsBroadcastData()
            WsBroadcastCommand = Webserver.WsBroadcastCommand()
            WsBroadcastUniversal = Webserver.WsBroadcastUniversal()
            WsSendMessage = Webserver.WsSendMessage()
            WsSendValue = Webserver.WsSendValue()
            WsSendAllValues = Webserver.WsSendAllValues()
            WsSendData = Webserver.WsSendData()
            WsSendCommand = Webserver.WsSendCommand()
            WsSendUniversal = Webserver.WsSendUniversal()
            WsStopClientPeriodicTasks = Webserver.WsStopClientPeriodicTasks()
            WsStopPeriodicTasks = Webserver.WsStopPeriodicTasks()
            SetClientsFlags = Webserver.SetClientsFlags()
            GetValue = Webserver.GetValue()
            GetPersistentValue = Webserver.GetPersistentValue()
            SetValue = Webserver.SetValue()
            SetPersistentValue = Webserver.SetPersistentValue()
            SendEvent = Webserver.SendEvent()
            SendEventExt = Webserver.SendEventExt()
            StartClient = Webserver.StartClient()
            StopClient = Webserver.StopClient()
            StopAllClients = Webserver.StopAllClients()
            ClSendMessage = Webserver.ClSendMessage()
            ClSendValue = Webserver.ClSendValue()
            ClSendAllValues = Webserver.ClSendAllValues()
            ClSendData = Webserver.ClSendData()
            ClSendCommand = Webserver.ClSendCommand()
            ClSendUniversal = Webserver.ClSendUniversal()
            JumpIf = Webserver.JumpIf()

        class WinUsbTest(object):
            plugin = WinUsbTest.WinUsbTest()


        class Winamp(object):
            plugin = Winamp.Winamp()


        class Window(object):
            plugin = Window.Window()
            BringToFront = Window.BringToFront()
            Close = Window.Close()
            DockWindow = Window.DockWindow()
            GrabText = Window.GrabText()
            Maximize = Window.Maximize()
            Minimize = Window.Minimize()
            MinimizeToTray = Window.MinimizeToTray()
            MoveTo = Window.MoveTo()
            Resize = Window.Resize()
            Restore = Window.Restore()
            SendMessage = Window.SendMessage()
            SetAlwaysOnTop = Window.SetAlwaysOnTop()


        class X10(object):
            plugin = X10.X10()


        class XBCDRC(object):
            plugin = XBCDRC.XBCDRC()


        class XbmceventbroadcastListener(object):
            plugin = XBMCEventReceiver.XbmceventbroadcastListener()


        class XBMC2(object):
            plugin = XBMCRepeat.XBMC2()
            UpdateLibrary = XBMCRepeat.UpdateLibrary()
            BuiltInFunctions = XBMCRepeat.BuiltInFunctions()


        class YARD(object):
            plugin = YARD.YARD()
            SendRemoteKey = YARD.SendRemoteKey()
            ClearScreen = YARD.ClearScreen()
            Print = YARD.Print()


        class YamahaSerial(object):
            plugin = YamahaSerial.YamahaSerial()


        class ZoomPlayer(object):
            plugin = ZoomPlayer.ZoomPlayer()
            NvAction = ZoomPlayer.NvAction()
            FnAction = ZoomPlayer.FnAction()
            ExAction = ZoomPlayer.ExAction()


        class Ffdshow(object):
            plugin = ffdshow.Ffdshow()
            SetPreset = ffdshow.SetPreset()


        class xPL(object):
            plugin = xPL.xPL()


    plugins = CorePluginModule
    del CorePluginModule
    del _CorePluginModule
    del ModuleSpec
    del ModuleType
    del AIRT
    del AsusPsr2000
    del AtiRemoteWonder2WinUsb
    del Auvisio
    del BSPlayer
    del BT8x8
    del Barco
    del Billy
    del Broadcaster
    del CM11A
    del CambridgeAudioSerial
    del Conceptronic
    del CyberlinkUniversalRemote
    del DBox2
    del DScaler4
    del DVBDream
    del DVBViewer
    del DenonSerial
    del DesktopRemote
    del DirectoryWatcher
    del DynamicWebserver
    del E_mail
    del EventGhost
    del EventPhone
    del FS20PCE
    del FS20PCS
    del Fhz1000Pc
    del FileOperations
    del Foobar2000
    del GOMPlayer
    del GameVoice
    del H79Serial
    del HID
    del HarmanKardon
    del HauppaugeIR
    del Homeseer
    del IgorPlugUDP
    del IgorPlugUSB
    del IrfanView
    del JVCHD1Serial
    del Joystick
    del JvcDlaSerial
    del KIRA
    del Keyboard
    del Lirc
    del LogitechUltraX
    del MCE
    del MarantzSerial
    del MceRemote
    del MceRemote_Vista
    del MediaMonkey
    del MediaPlayerClassic
    del MediaPortal
    del Meedio
    del Mouse
    del Multitap
    del MyTheatre
    del NetworkReceiver
    del NetworkSender
    del OOo_Impress
    del OSE
    del OSM
    del Onkyo
    del OnkyoISCP
    del PC_Remote_Controller
    del PHX01RN
    del PS3
    del Phoner
    del Ping
    del PowerDVD
    del ProcessWatcher
    del RFXcom_xPL
    del RadioSure
    del RawInput
    del RemoteEventMapper
    del SageTV
    del SamsungTV
    del SchedulGhost
    del Scheduler
    del ScreamerRadio
    del Serial
    del SmallPcRemote
    del SoundMixerEx
    del Speech
    del Speedlink6399
    del SplashLite
    del Streamzap
    del SunTracker
    del SysTrayMenu
    del System
    del TVcentral
    del Task
    del TechniSatUsb
    del TechnoTrendIr
    del TechnoTrendIrBda
    del TellStick
    del TerratecUsb
    del Test
    del TestPatterns
    del TheaterTek
    del Timer
    del Tira
    del UIR
    del UIRT2
    del USB_RFID
    del USB_UIRT
    del VLC
    del WMPlayer
    del Weather
    del Webserver
    del WinUsbTest
    del Winamp
    del Window
    del X10
    del XBCDRC
    del XBMCEventReceiver
    del XBMCRepeat
    del YARD
    del YamahaSerial
    del ZoomPlayer
    del ffdshow
    del xPL

    from . import CorePluginModule
    from . import Icons as _Icons

    sys.modules["eg.UserPluginModule"] = UserPluginModule
    sys.modules['eg.cFunctions'] = cFunctions
    cFunctions = eg.cFunctions

if eg.debugLevel:
    eg.RaiseAssignments()
