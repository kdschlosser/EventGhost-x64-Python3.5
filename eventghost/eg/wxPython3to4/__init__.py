# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

import sys
import wx
import wx.html
import wx.lib
import wx.lib.agw.buttonpanel
import wx.lib.agw.customtreectrl
import wx.lib.agw.flatnotebook
import wx.lib.agw.foldpanelbar
import wx.lib.agw.hyperlink
import wx.adv
import wx.dataview


class ModuleRedirect(object):

    def __init__(self, srcs, dst):
        self.__original_mods__ = []
        for src in srcs:
            mod = sys.modules[src]
            self.__dict__.update(mod.__dict__)
            self.__original_mods__ += [mod]

        sys.modules[dst] = self

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        for mod in self.__original_mods__:
            if hasattr(mod, item):
                return getattr(mod, item)

        raise AttributeError(item)


def checked(self):
    return self.IsChecked()


wx.CommandEvent.Checked = checked
wx.THICK_FRAME = wx.RESIZE_BORDER
wx.AboutBox = wx.adv.AboutBox
wx.AboutDialogInfo = wx.adv.AboutDialogInfo
# wx.AcceleratorEntry_Create 	MISSING
# wx.ANIHandler 	MISSING
wx.ArtProvider_Delete = wx.ArtProvider.Delete
wx.ArtProvider_GetBitmap = wx.ArtProvider.GetBitmap
wx.ArtProvider_GetIcon = wx.ArtProvider.GetIcon
wx.ArtProvider_GetIconBundle = wx.ArtProvider.GetIconBundle
wx.ArtProvider_GetMessageBoxIcon = wx.ArtProvider.GetMessageBoxIcon
wx.ArtProvider_GetMessageBoxIconId = wx.ArtProvider.GetMessageBoxIconId
wx.ArtProvider_GetNativeSizeHint = wx.ArtProvider.GetNativeSizeHint
wx.ArtProvider_GetSizeHint = wx.ArtProvider.GetSizeHint
wx.ArtProvider_HasNativeProvider = wx.ArtProvider.HasNativeProvider
wx.ArtProvider_Insert = wx.ArtProvider.Insert
wx.ArtProvider_Pop = wx.ArtProvider.Pop
wx.ArtProvider_Push = wx.ArtProvider.Push
wx.ArtProvider_PushBack = wx.ArtProvider.PushBack
wx.BitmapButton.SetBitmapSelected = wx.BitmapButton.SetBitmapPressed
wx.BitmapFromBits = wx.Bitmap
wx.BitmapFromIcon = wx.Bitmap
wx.BitmapFromImage = wx.Bitmap
wx.BitmapFromXPMData = wx.Bitmap
# wx.BMPHandler 	MISSING
wx.BookCtrlBase_GetClassDefaultAttributes = wx.BookCtrl.GetClassDefaultAttributes
wx.BrushFromBitmap = wx.Brush
wx.Button_GetClassDefaultAttributes = wx.Button.GetClassDefaultAttributes
wx.Button_GetDefaultSize = wx.Button.GetDefaultSize
wx.CalculateLayoutEvent = wx.adv.CalculateLayoutEvent
wx.Caret_GetBlinkTime = wx.Caret.GetBlinkTime
wx.Caret_SetBlinkTime = wx.Caret.SetBlinkTime
wx.CheckBox_GetClassDefaultAttributes = wx.CheckBox.GetClassDefaultAttributes
wx.Choice_GetClassDefaultAttributes = wx.Choice.GetClassDefaultAttributes
wx.ChoicebookEvent = wx.BookCtrlEvent
wx.Clipboard_Get = wx.Clipboard.Get
wx.ClipboardEvent = wx.ClipboardTextEvent
# wx.ClipboardLocker 	MISSING
wx.Colour.SetFromString = wx.Colour.Set
wx.ColourRGB = wx.Colour
wx.ComboBox_GetClassDefaultAttributes = wx.ComboBox.GetClassDefaultAttributes
wx.CommandLinkButton = wx.adv.CommandLinkButton
wx.ConfigBase_Create = wx.ConfigBase.Create
wx.ConfigBase_DontCreateOnDemand = wx.ConfigBase.DontCreateOnDemand
wx.ConfigBase_Get = wx.ConfigBase.Get
wx.ConfigBase_Set = wx.ConfigBase.Set
wx.Control_Ellipsize = wx.Control.Ellipsize
wx.Control_EscapeMnemonics = wx.Control.EscapeMnemonics
# wx.Control_FindAccelIndex = MISSING
wx.Control_GetClassDefaultAttributes = wx.Control.GetClassDefaultAttributes
# wx.Control_GetCompositeControlsDefaultAttributes = MISSING
wx.Control_RemoveMnemonics = wx.Control.RemoveMnemonics
# wx.CPPFileSystemHandler = REMOVED
wx.CreateFileTipProvider = wx.adv.CreateFileTipProvider
# wx.CURHandler = MISSING
wx.CursorFromImage = wx.Cursor
wx.CustomDataFormat = wx.DataFormat
wx.DateEvent = wx.adv.DateEvent
wx.DatePickerCtrl = wx.adv.DatePickerCtrl
wx.DatePickerCtrlBase = wx.adv.DatePickerCtrl
wx.DateSpan_Day = wx.DateSpan.Day
wx.DateSpan_Days = wx.DateSpan.Days
wx.DateSpan_Month = wx.DateSpan.Month
wx.DateSpan_Months = wx.DateSpan.Months
wx.DateSpan_Week = wx.DateSpan.Week
wx.DateSpan_Weeks = wx.DateSpan.Weeks
wx.DateSpan_Year = wx.DateSpan.Year
wx.DateSpan_Years = wx.DateSpan.Years
wx.DateTime_ConvertYearToBC = wx.DateTime.ConvertYearToBC
wx.DateTime_GetAmPmStrings = wx.DateTime.GetAmPmStrings
wx.DateTime_GetBeginDST = wx.DateTime.GetBeginDST
wx.DateTime_GetCentury = wx.DateTime.GetCentury
wx.DateTime_GetCountry = wx.DateTime.GetCountry
wx.DateTime_GetCurrentMonth = wx.DateTime.GetCurrentMonth
wx.DateTime_GetCurrentYear = wx.DateTime.GetCurrentYear
wx.DateTime_GetEndDST = wx.DateTime.GetEndDST
wx.DateTime_GetEnglishMonthName = wx.DateTime.GetEnglishMonthName
wx.DateTime_GetEnglishWeekDayName = wx.DateTime.GetEnglishWeekDayName
wx.DateTime_GetMonthName = wx.DateTime.GetMonthName
# wx.DateTime_GetNumberOfDaysInMonth = MISSING
# wx.DateTime_GetNumberOfDaysinYear = MISSING
wx.DateTime_GetWeekDayName = wx.DateTime.GetWeekDayName
wx.DateTime_IsDSTApplicable = wx.DateTime.IsDSTApplicable
wx.DateTime_IsLeapYear = wx.DateTime.IsLeapYear
wx.DateTime_IsWestEuropeanCountry = wx.DateTime.IsWestEuropeanCountry
wx.DateTime_Now = wx.DateTime.Now
wx.DateTime_SetCountry = wx.DateTime.SetCountry
wx.DateTime_SetToWeekOfYear = wx.DateTime.SetToWeekOfYear
wx.DateTime_Today = wx.DateTime.Today
wx.DateTime_UNow = wx.DateTime.UNow
wx.DateTimeFromDateTime = wx.DateTime
wx.Dialog_EnableLayoutAdaptation = wx.Dialog.EnableLayoutAdaptation
wx.Dialog_GetClassDefaultAttributes = wx.Dialog.GetClassDefaultAttributes
wx.Dialog_GetLayoutAdapter = wx.Dialog.GetLayoutAdapter
wx.Dialog_IsLayoutAdaptationEnabled = wx.Dialog.IsLayoutAdaptationEnabled
wx.Dialog_SetLayoutAdapter = wx.Dialog.SetLayoutAdapter
# wx.DirItemData = MISSING
wx.Display_GetCount = wx.Display.GetCount
wx.Display_GetFromPoint = wx.Display.GetFromPoint
wx.Display_GetFromWindow = wx.Display.GetFromWindow
# wx.DragIcon = MISSING
# wx.DragListItem = MISSING
# wx.DragString = MISSING
# wx.DragTreeItem = MISSING
# wx.DROP_ICON = MISSING
wx.EmptyBitmap = wx.Bitmap
wx.EmptyIcon = wx.Icon
wx.EmptyImage = wx.Image
# wx.EncodingConverter = MISSING
# wx.EncodingConverter_CanConvert = MISSING
# wx.EncodingConverter_GetAllEquivalents = MISSING
# wx.EncodingConverter_GetPlatformEquivalents = MISSING
wx.EventLoopBase_GetActive = wx.EventLoopBase.GetActive
wx.EventLoopBase_SetActive = wx.EventLoopBase.SetActive
# wx.EventProcessInHandlerOnly = MISSING
# wx.EVT_COMMAND = MISSING
# wx.EVT_COMMAND_RANGE = MISSING
# wx.ExpandEnvVars = MISSING
wx.FFontFromPixelSize = wx.Font
wx.FileConfig_GetGlobalFileName = wx.FileConfig.GetGlobalFileName
wx.FileConfig_GetLocalFileName = wx.FileConfig.GetLocalFileName
wx.FileSystem_AddHandler = wx.FileSystem.AddHandler
# wx.FileSystem_CleanUpHandlers = MISSING
wx.FileSystem_FileNameToURL = wx.FileSystem.FileNameToURL
wx.FileSystem_RemoveHandler = wx.FileSystem.RemoveHandler
wx.FileSystem_URLToFileName = wx.FileSystem.URLToFileName
# wx.FileSystemHandler_GetAnchor = MISSING
# wx.FileSystemHandler_GetLeftLocation = MISSING
wx.FileSystemHandler_GetMimeTypeFromExt = wx.FileSystemHandler.GetMimeTypeFromExt
# wx.FileSystemHandler_GetProtocol = MISSING
# wx.FileSystemHandler_GetRightLocation = MISSING
wx.FileType_ExpandCommand = wx.FileType.ExpandCommand
# wx.FileTypeInfoSequence = MISSING
wx.FindWindowById = wx.Window.FindWindowById
wx.Font2 = wx.Font
# wx.Font_AdjustToSymbolicSize = MISSING
wx.Font_GetDefaultEncoding = wx.Font.GetDefaultEncoding
wx.Font_SetDefaultEncoding = wx.Font.SetDefaultEncoding
wx.FontEnumerator_GetEncodings = wx.FontEnumerator.GetEncodings
wx.FontEnumerator_GetFacenames = wx.FontEnumerator.GetFacenames
wx.FontEnumerator_IsValidFacename = wx.FontEnumerator.IsValidFacename
wx.FontFromNativeInfo = wx.Font
wx.FontFromNativeInfoString = wx.Font
wx.FontFromPixelSize = wx.Font
wx.FontMapper_Get = wx.FontMapper.Get
# wx.FontMapper_GetDefaultConfigPath = MISSING
wx.FontMapper_GetEncoding = wx.FontMapper.GetEncoding
wx.FontMapper_GetEncodingDescription = wx.FontMapper.GetEncodingDescription
wx.FontMapper_GetEncodingFromName = wx.FontMapper.GetEncodingFromName
wx.FontMapper_GetEncodingName = wx.FontMapper.GetEncodingName
wx.FontMapper_GetSupportedEncodingsCount = wx.FontMapper.GetSupportedEncodingsCount
wx.FontMapper_Set = wx.FontMapper.Set
wx.Frame_GetClassDefaultAttributes = wx.Frame.GetClassDefaultAttributes
wx.FutureCall = wx.CallLater
wx.Gauge_GetClassDefaultAttributes = wx.Gauge.GetClassDefaultAttributes
wx.GBSizerItemSizer = wx.GBSizerItem
wx.GBSizerItemSpacer = wx.GBSizerItem
wx.GBSizerItemWindow = wx.GBSizerItem
# wx.GDIObjListBase = MISSING
wx.GenericFindWindowAtPoint = wx.FindWindowAtPoint
# wx.GetAccelFromString = MISSING
# wx.GetCurrentId = MISSING
# wx.GetCurrentTime = MISSING
# wx.GetDefaultPyEncoding = REMOVED
wx.GetDisplayDepth = wx.DisplayDepth
# wx.GetFreeMemory = MISSING
# wx.GetLocale = MISSING
# wx.GetLocalTime = MISSING
# wx.GetLocalTimeMillis = MISSING
# wx.GetNativeFontEncoding = MISSING
# wx.GetNumberFromUser = MISSING
# wx.GetPasswordFromUser = MISSING
# wx.GetSingleChoiceIndex = MISSING
# wx.GetStockHelpString = MISSING
# wx.GetStockLabel = MISSING
# wx.GetTextFromUser = MISSING
# wx.GetUTCTime = MISSING
# wx.GetXDisplay = MISSING
# wx.GIFHandler = MISSING
wx.GraphicsContext_Create = wx.GraphicsContext.Create
wx.GraphicsContext_CreateFromNative = wx.GraphicsContext.CreateFromNative
wx.GraphicsContext_CreateFromNativeWindow = wx.GraphicsContext.CreateFromNativeWindow
wx.GraphicsContext_CreateMeasuringContext = wx.GraphicsContext.Create
wx.GraphicsRenderer_GetCairoRenderer = wx.GraphicsRenderer.GetCairoRenderer
wx.GraphicsRenderer_GetDefaultRenderer = wx.GraphicsRenderer.GetDefaultRenderer
wx.HelpProvider_Get = wx.HelpProvider.Get
wx.HelpProvider_Set = wx.HelpProvider.Set
# wx.HtmlListBox = MISSING
wx.HyperlinkCtrl = wx.adv.HyperlinkCtrl
wx.HyperlinkEvent = wx.adv.HyperlinkEvent
# wx.ICOHandler = MISSING
wx.IconBundleFromFile = wx.IconBundle
wx.IconBundleFromIcon = wx.IconBundle
wx.IconBundleFromStream = wx.IconBundle
wx.IconFromBitmap = wx.Icon
wx.IconFromLocation = wx.Icon
wx.IconFromXPMData = wx.Icon
wx.IdleEvent_GetMode = wx.IdleEvent.GetMode
wx.IdleEvent_SetMode = wx.IdleEvent.SetMode
wx.Image_AddHandler = wx.Image.AddHandler
wx.Image_CanRead = wx.Image.CanRead
wx.Image_CanReadStream = wx.Image.CanRead
# wx.Image_GetHandlers = MISSING
wx.Image_GetImageCount = wx.Image.GetImageCount
wx.Image_GetImageExtWildcard = wx.Image.GetImageExtWildcard
wx.Image_HSVtoRGB = wx.Image.HSVtoRGB
wx.Image_HSVValue = wx.Image.HSVValue
wx.Image_InsertHandler = wx.Image.InsertHandler
wx.Image_RemoveHandler = wx.Image.RemoveHandler
wx.Image_RGBtoHSV = wx.Image.RGBtoHSV
wx.Image_RGBValue = wx.Image.RGBValue
wx.ImageFromMime = wx.Image
wx.ImageFromStream = wx.Image
wx.ImageFromStreamMime = wx.Image
wx.ImageHistogram_MakeKey = wx.ImageHistogram.MakeKey
# wx.IsStockID = MISSING
# wx.IsStockLabel = MISSING
wx.Joystick = wx.adv.Joystick

# wx.JPEGHandler = MISSING


def m_alt_down(self, *args, **kwargs):
    return self.GetModifiers(*args, **kwargs)


def m_control_down(self, *args, **kwargs):
    return self.GetModifiers(*args, **kwargs)


def m_meta_down(self, *args, **kwargs):
    return self.GetModifiers(*args, **kwargs)


def m_shift_down(self, *args, **kwargs):
    return self.GetModifiers(*args, **kwargs)


wx.KeyEvent.m_altDown = m_alt_down
wx.KeyEvent.m_controlDown = m_control_down
wx.KeyEvent.m_metaDown = m_meta_down
wx.KeyEvent.m_shiftDown = m_shift_down


wx.KeyEvent.m_keyCode = wx.KeyEvent.__dict__['KeyCode']


wx.KeyEvent.m_metaDown = wx.KeyboardState.GetModifiers
wx.KeyEvent.m_shiftDown = wx.KeyboardState.GetModifiers


wx.KeyEvent.m_x = wx.KeyEvent.__dict__['X']
wx.KeyEvent.m_y = wx.KeyEvent.__dict__['Y']
wx.LayoutAlgorithm = wx.adv.LayoutAlgorithm
wx.ListbookEvent = wx.BookCtrlEvent
wx.ListBox_GetClassDefaultAttributes = wx.ListBox.GetClassDefaultAttributes
wx.ListCtrl_GetClassDefaultAttributes = wx.ListCtrl.GetClassDefaultAttributes
wx.ListCtrl_HasColumnOrderSupport = wx.ListCtrl.HasColumnOrderSupport
wx.ListEvent.m_code = wx.ListEvent.__dict__['KeyCode']
wx.ListEvent.m_col = wx.ListEvent.__dict__['Column']
wx.ListEvent.m_item = wx.ListEvent.__dict__['Item']
wx.ListEvent.m_itemIndex = wx.ListEvent.__dict__['Index']
wx.ListEvent.m_oldItemIndex = wx.ListEvent.__dict__['CacheFrom']
wx.ListEvent.m_pointDrag = wx.ListEvent.__dict__['Point']
wx.ListItem.m_col = wx.ListItem.__dict__['Column']
wx.ListItem.m_data = wx.ListItem.__dict__['Data']
wx.ListItem.m_format = wx.ListItem.__dict__['Align']
wx.ListItem.m_image = wx.ListItem.__dict__['Image']
wx.ListItem.m_itemId = wx.ListItem.__dict__['Id']
wx.ListItem.m_mask = wx.ListItem.__dict__['Mask']
wx.ListItem.m_state = wx.ListItem.__dict__['State']
wx.ListItem.m_stateMask = wx.ListItem.__dict__['State']
wx.ListItem.m_text = wx.ListItem.__dict__['Text']
wx.ListItem.m_width = wx.ListItem.__dict__['Width']
wx.Locale_AddCatalogLookupPathPrefix = wx.Locale.AddCatalogLookupPathPrefix
wx.Locale_AddLanguage = wx.Locale.AddLanguage
wx.Locale_FindLanguageInfo = wx.Locale.FindLanguageInfo
wx.Locale_GetInfo = wx.Locale.GetInfo
wx.Locale_GetLanguageCanonicalName = wx.Locale.GetLanguageCanonicalName
wx.Locale_GetLanguageInfo = wx.Locale.GetLanguageInfo
wx.Locale_GetLanguageName = wx.Locale.GetLanguageName
wx.Locale_GetSystemEncoding = wx.Locale.GetSystemEncoding
wx.Locale_GetSystemEncodingName = wx.Locale.GetSystemEncodingName
wx.Locale_GetSystemLanguage = wx.Locale.GetSystemLanguage
wx.Locale_IsAvailable = wx.Locale.IsAvailable
wx.Log_AddTraceMask = wx.Log.AddTraceMask
wx.Log_ClearTraceMasks = wx.Log.ClearTraceMasks
# Log_DoCreateOnDemand = MISSING
wx.Log_DontCreateOnDemand = wx.Log.DontCreateOnDemand
wx.Log_EnableLogging = wx.Log.EnableLogging
wx.Log_FlushActive = wx.Log.FlushActive
wx.Log_GetActiveTarget = wx.Log.GetActiveTarget
# wx.Log_GetComponentLevel = MISSING
wx.Log_GetLogLevel = wx.Log.GetLogLevel
wx.Log_GetRepetitionCounting = wx.Log.GetRepetitionCounting
wx.Log_GetTimestamp = wx.Log.GetTimestamp
# wx.Log_GetTraceMask = MISSING
wx.Log_GetTraceMasks = wx.Log.GetTraceMasks
wx.Log_GetVerbose = wx.Log.GetVerbose
wx.Log_IsAllowedTraceMask = wx.Log.IsAllowedTraceMask
wx.Log_IsEnabled = wx.Log.IsEnabled
wx.Log_IsLevelEnabled = wx.Log.IsLevelEnabled
wx.Log_RemoveTraceMask = wx.Log.RemoveTraceMask
wx.Log_Resume = wx.Log.Resume
wx.Log_SetActiveTarget = wx.Log.SetActiveTarget
wx.Log_SetComponentLevel = wx.Log.SetComponentLevel
wx.Log_SetLogLevel = wx.Log.SetLogLevel
wx.Log_SetRepetitionCounting = wx.Log.SetRepetitionCounting
wx.Log_SetTimestamp = wx.Log.SetTimestamp
# wx.Log_SetTraceMask = MISSING
wx.Log_SetVerbose = wx.Log.SetVerbose
wx.Log_Suspend = wx.Log.Suspend
# wx.Log_TimeStamp = MISSING
wx.LogInfo = wx.LogMessage
wx.LogStatusFrame = wx.LogStatus
# wx.LogTrace = MISSING
wx.MaskColour = wx.Colour
wx.MemoryDCFromDC = wx.MemoryDC
wx.MemoryFSHandler_AddFile = wx.MemoryFSHandler.AddFile
wx.MemoryFSHandler_AddFileWithMimeType = wx.MemoryFSHandler.AddFileWithMimeType
wx.MemoryFSHandler_RemoveFile = wx.MemoryFSHandler.RemoveFile
# wx.MenuBar_GetAutoWindowMenu = MISSING
wx.MenuBar_MacSetCommonMenuBar = wx.MenuBar.MacSetCommonMenuBar
# wx.MenuBar_SetAutoWindowMenu = MISSING
# wx.MenuItem_GetDefaultMarginWidth = MISSING
wx.MenuItem_GetLabelText = wx.MenuItem.GetLabelText
wx.MetaFile = wx.MemoryDC
# wx.MetafileDataObject = MISSING
wx.MetaFileDC = wx.MetafileDC
wx.MimeTypesManager_IsOfType = wx.MimeTypesManager.IsOfType
# wx.ModalEventLoop = MISSING
# wx.MutexGuiEnter = MISSING
# wx.MutexGuiLeave = MISSING
# wx.MutexGuiLocker = MISSING
wx.NamedColour = wx.Colour
# wx.NativeEncodingInfo = MISSING
# wx.NcPaintEvent = MISSING
wx.Notebook_GetClassDefaultAttributes = wx.Notebook.GetClassDefaultAttributes
wx.NotebookEvent = wx.BookCtrlEvent
# wx.NotebookPage = MISSING
wx.NotificationMessage = wx.adv.NotificationMessage
# wx.NullFileTypeInfo = MISSING
wx.Panel_GetClassDefaultAttributes = wx.Panel.GetClassDefaultAttributes
# wx.PCXHandler = MISSING
wx.PlatformInformation_GetOperatingSystemDirectory = wx.PlatformInformation.GetOperatingSystemDirectory
# wx.PNGHandler = MISSING
# wx.PNMHandler = MISSING
wx.Point2DCopy = wx.Point2D
wx.Point2DFromPoint = wx.Point2D
wx.PreBitmapButton = wx.BitmapButton
wx.PreButton = wx.Button
wx.PreCheckBox = wx.CheckBox
wx.PreCheckListBox = wx.CheckListBox
wx.PreChoice = wx.Choice
wx.PreChoicebook = wx.Choicebook
wx.PreCollapsiblePane = wx.CollapsiblePane
wx.PreColourPickerCtrl = wx.ColourPickerCtrl
wx.PreComboBox = wx.ComboBox
wx.PreCommandLinkButton = wx.adv.CommandLinkButton
wx.PreControl = wx.Control
wx.PreDatePickerCtrl = wx.adv.DatePickerCtrl
wx.PreDialog = wx.Dialog
wx.PreDirFilterListCtrl = wx.DirFilterListCtrl
wx.PreDirPickerCtrl = wx.DirPickerCtrl
wx.PreFileCtrl = wx.FileCtrl
wx.PreFilePickerCtrl = wx.FilePickerCtrl
wx.PreFindReplaceDialog = wx.FindReplaceDialog
wx.PreFontPickerCtrl = wx.FontPickerCtrl
wx.PreFrame = wx.Frame
wx.PreGauge = wx.Gauge
wx.PreGenericDirCtrl = wx.GenericDirCtrl
wx.PreHScrolledWindow = wx.HScrolledWindow
# wx.PreHtmlListBox = MISSING
wx.PreHVScrolledWindow = wx.HVScrolledWindow
wx.PreHyperlinkCtrl = wx.adv.HyperlinkCtrl
wx.PreInfoBar = wx.InfoBar
wx.PreListbook = wx.Listbook
wx.PreListBox = wx.ListBox
wx.PreListCtrl = wx.ListCtrl
wx.PreListView = wx.ListView
wx.PreMDIChildFrame = wx.MDIChildFrame
wx.PreMDIClientWindow = wx.MDIClientWindow
wx.PreMDIParentFrame = wx.MDIParentFrame
wx.PreMiniFrame = wx.MiniFrame
wx.PreNotebook = wx.Notebook
wx.PrePanel = wx.Panel
wx.PrePopupTransientWindow = wx.PopupTransientWindow
wx.PrePopupWindow = wx.PopupWindow
# wx.PrePyAxBaseWindow = MISSING
wx.PrePyControl = wx.Control
wx.PrePyPanel = wx.Panel
wx.PrePyPickerBase = wx.PickerBase
wx.PrePyScrolledWindow = wx.ScrolledWindow
wx.PrePyWindow = wx.Window
wx.PreRadioBox = wx.RadioBox
wx.PreRadioButton = wx.RadioButton
wx.PreSashLayoutWindow = wx.adv.SashLayoutWindow
wx.PreSashWindow = wx.adv.SashWindow
wx.PreScrollBar = wx.ScrollBar
wx.PreScrolledWindow = wx.ScrolledWindow
wx.PreSearchCtrl = wx.SearchCtrl
# wx.PreSimpleHtmlListBox = MISSING
wx.PreSingleInstanceChecker = wx.SingleInstanceChecker
wx.PreSlider = wx.Slider
wx.PreSpinButton = wx.SpinButton
wx.PreSpinCtrl = wx.SpinCtrl
wx.PreSpinCtrlDouble = wx.SpinCtrlDouble
wx.PreSplitterWindow = wx.SplitterWindow
wx.PreStaticBitmap = wx.StaticBitmap
wx.PreStaticBox = wx.StaticBox
wx.PreStaticLine = wx.StaticLine
wx.PreStaticText = wx.StaticText
wx.PreStatusBar = wx.StatusBar
wx.PreTextCtrl = wx.TextCtrl
wx.PreToggleButton = wx.ToggleButton
wx.PreToolBar = wx.ToolBar
wx.PreToolbook = wx.Toolbook
wx.PreTreebook = wx.Treebook
wx.PreTreeCtrl = wx.TreeCtrl
wx.PreVListBox = wx.VListBox
wx.PreVScrolledWindow = wx.VScrolledWindow
wx.PreWindow = wx.Window
wx.Printer_GetLastError = wx.Printer.GetLastError
wx.Process_Exists = wx.Process.Exists
wx.Process_Kill = wx.Process.Kill
wx.Process_Open = wx.Process.Open
wx.PseudoDC = wx.adv.PseudoDC
wx.PyApp_GetComCtl32Version = wx.PyApp.GetComCtl32Version
# wx.PyApp_GetMacSupportPCMenuShortcuts = MISSING
wx.PyApp_GetShell32Version = wx.PyApp.GetShell32Version
# wx.PyApp_GetTraitsIfExists = MISSING
wx.PyApp_IsDisplayAvailable = wx.PyApp.IsDisplayAvailable
wx.PyApp_IsMainLoopRunning = wx.PyApp.IsMainLoopRunning
# wx.PyApp_SetMacSupportPCMenuShortcuts = MISSING
# wx.PyAxBaseWindow_FromHWND = MISSING
wx.PyBitmapDataObject = wx.BitmapDataObject
wx.PyControl = wx.Control
wx.PyDataObjectSimple = wx.DataObjectSimple
wx.PyDeadObjectError = RuntimeError
wx.PyDropTarget = wx.DropTarget
wx.PyEvtHandler = wx.EvtHandler
wx.PyImageHandler = wx.ImageHandler
wx.PyLocale = wx.Locale
wx.PyLog = wx.Log
wx.PyPanel = wx.Panel
wx.PyPickerBase = wx.PickerBase
wx.PyPreviewControlBar = wx.PreviewControlBar
wx.PyPreviewFrame = wx.PreviewFrame
wx.PyPrintPreview = wx.PrintPreview
wx.PyScrolledWindow = wx.ScrolledWindow
wx.PySimpleApp = wx.App
wx.PyTextDataObject = wx.TextDataObject
wx.PyTimer = wx.Timer
wx.PyTipProvider = wx.adv.TipProvider
wx.PyValidator = wx.Validator
wx.PyWindow = wx.Window
# wx.Quantize = MISSING
# wx.Quantize_Quantize = MISSING
wx.QueryLayoutInfoEvent = wx.adv.QueryLayoutInfoEvent
wx.RadioBox_GetClassDefaultAttributes = wx.RadioBox.GetClassDefaultAttributes
wx.RadioButton_GetClassDefaultAttributes = wx.RadioButton.GetClassDefaultAttributes
wx.RectPP = wx.Rect
wx.RectPS = wx.Rect
wx.RectS = wx.Rect
wx.Rect.OffsetXY = wx.Rect.Offset
wx.RegionFromBitmap = wx.Region
wx.RegionFromBitmapColour = wx.Region
wx.RegionFromPoints = wx.Region
wx.RendererNative_Get = wx.RendererNative.Get
wx.RendererNative_GetDefault = wx.RendererNative.GetDefault
wx.RendererNative_GetGeneric = wx.RendererNative.GetGeneric
wx.RendererNative_Set = wx.RendererNative.Set
wx.RendererVersion_IsCompatible = wx.RendererVersion.IsCompatible
wx.SashEvent = wx.adv.SashEvent
wx.SashLayoutWindow = wx.adv.SashLayoutWindow
wx.SashWindow = wx.adv.SashWindow
wx.ScrollBar_GetClassDefaultAttributes = wx.ScrollBar.GetClassDefaultAttributes
wx.ScrolledWindow_GetClassDefaultAttributes = wx.ScrolledWindow.GetClassDefaultAttributes
wx.ScrollHelper = wx.VarHVScrollHelper
wx.SearchCtrlBase = wx.SearchCtrl
# wx.SetCursor = MISSING
# wx.SetDefaultPyEncoding = REMOVED
wx.SetBitmapSelected = wx.AnyButton.SetBitmapPressed
wx.ShowTip = wx.adv.ShowTip
# wx.SimpleHtmlListBox = MISSING
wx.SizerFlags_GetDefaultBorder = wx.SizerFlags.GetDefaultBorder
wx.SizerItemSizer = wx.SizerItem
wx.SizerItemSpacer = wx.SizerItem
wx.SizerItemWindow = wx.SizerItem
wx.Slider_GetClassDefaultAttributes = wx.Slider.GetClassDefaultAttributes
wx.Sound = wx.adv.Sound
wx.Sound_PlaySound = wx.adv.Sound.PlaySound
wx.Sound_Stop = wx.adv.Sound.Stop
wx.SoundFromData = wx.adv.Sound
wx.SpinButton_GetClassDefaultAttributes = wx.SpinButton.GetClassDefaultAttributes
wx.SpinCtrl_GetClassDefaultAttributes = wx.SpinCtrl.GetClassDefaultAttributes
wx.SplashScreen = wx.adv.SplashScreen
# wx.SplashScreenWindow = MISSING
wx.SplitterWindow_GetClassDefaultAttributes = wx.SplitterWindow.GetClassDefaultAttributes
# wx.StandardDialogLayoutAdapter = MISSING
# wx.StandardDialogLayoutAdapter_DoFitWithScrolling = MISSING
# wx.StandardDialogLayoutAdapter_DoMustScroll = MISSING
# wx.StandardDialogLayoutAdapter_DoReparentControls = MISSING
wx.StandardPaths_Get = wx.StandardPaths.Get
wx.StaticBitmap_GetClassDefaultAttributes = wx.StaticBitmap.GetClassDefaultAttributes
wx.StaticBox_GetClassDefaultAttributes = wx.StaticBox.GetClassDefaultAttributes
wx.StaticLine_GetClassDefaultAttributes = wx.StaticLine.GetClassDefaultAttributes
wx.StaticLine_GetDefaultSize = wx.StaticLine.GetDefaultSize
wx.StaticText_GetClassDefaultAttributes = wx.StaticText.GetClassDefaultAttributes
wx.StatusBar_GetClassDefaultAttributes = wx.StatusBar.GetClassDefaultAttributes
wx.StockCursor = wx.Cursor
# wx.StockGDI_DeleteAll = wx.StockGDI.DeleteAll
# wx.StockGDI_GetBrush = wx.StockGDI.GetBrush
# wx.StockGDI_GetColour = wx.StockGDI.GetColour
# wx.StockGDI_GetCursor = wx.StockGDI.GetCursor
# wx.StockGDI_GetPen = wx.StockGDI.GetPen
# wx.StockGDI_instance = wx.StockGDI.instance
# wx.StyledTextCtrl.SetUseAntiAliasing = REMOVED
wx.SystemOptions_GetOption = wx.SystemOptions.GetOption
wx.SystemOptions_GetOptionInt = wx.SystemOptions.GetOptionInt
wx.SystemOptions_HasOption = wx.SystemOptions.HasOption
wx.SystemOptions_IsFalse = wx.SystemOptions.IsFalse
wx.SystemOptions_SetOption = wx.SystemOptions.SetOption
wx.SystemOptions_SetOptionInt = wx.SystemOptions.SetOption
wx.SystemSettings_GetColour = wx.SystemSettings.GetColour
wx.SystemSettings_GetFont = wx.SystemSettings.GetFont
wx.SystemSettings_GetMetric = wx.SystemSettings.GetMetric
wx.SystemSettings_GetScreenType = wx.SystemSettings.GetScreenType
wx.SystemSettings_HasFeature = wx.SystemSettings.HasFeature
# wx.SystemSettings_SetScreenType = MISSING
wx.TaskBarIcon = wx.adv.TaskBarIcon
wx.TaskBarIcon_IsAvailable = wx.adv.TaskBarIcon.IsAvailable
wx.TaskBarIconEvent = wx.adv.TaskBarIconEvent
# wx.TestFontEncoding = MISSING
wx.TextAreaBase = wx.TextEntry
# wx.TextAttr_BitlistsEqPartial = MISSING
# wx.TextAttr_Combine = MISSING
# wx.TextAttr_CombineBitlists = MISSING
# wx.TextAttr_RemoveStyle = MISSING
# wx.TextAttr_SplitParaCharStyles = MISSING
# wx.TextAttr_TabsEq = MISSING
wx.TextCtrl_GetClassDefaultAttributes = wx.TextCtrl.GetClassDefaultAttributes
wx.TextCtrlBase = wx.TextCtrl
# wx.TextCtrlIface = NONE
wx.TextEntryBase = wx.TextEntry
# wx.TextUrlEvent = MISSING
# wx.TGAHandler = MISSING
wx.Thread_IsMain = wx.IsMainThread
# wx.ThreadEvent = MISSING
# wx.TIFFHandler = MISSING
wx.TimeSpan_Day = wx.TimeSpan.Day
wx.TimeSpan_Days = wx.TimeSpan.Days
wx.TimeSpan_Hour = wx.TimeSpan.Hour
wx.TimeSpan_Hours = wx.TimeSpan.Hours
wx.TimeSpan_Millisecond = wx.TimeSpan.Millisecond
wx.TimeSpan_Milliseconds = wx.TimeSpan.Milliseconds
wx.TimeSpan_Minute = wx.TimeSpan.Minute
wx.TimeSpan_Minutes = wx.TimeSpan.Minutes
wx.TimeSpan_Second = wx.TimeSpan.Second
wx.TimeSpan_Seconds = wx.TimeSpan.Seconds
wx.TimeSpan_Week = wx.TimeSpan.Week
wx.TimeSpan_Weeks = wx.TimeSpan.Weeks
wx.TipProvider = wx.adv.TipProvider
wx.ToggleButton_GetClassDefaultAttributes = wx.ToggleButton.GetClassDefaultAttributes
wx.ToolBar_GetClassDefaultAttributes = wx.ToolBar.GetClassDefaultAttributes
wx.ToolbookEvent = wx.BookCtrlEvent
wx.ToolTip_Enable = wx.ToolTip.Enable
wx.ToolTip_SetAutoPop = wx.ToolTip.SetAutoPop
wx.ToolTip_SetDelay = wx.ToolTip.SetDelay
wx.ToolTip_SetMaxWidth = wx.ToolTip.SetMaxWidth
wx.ToolTip_SetReshow = wx.ToolTip.SetReshow
wx.TopLevelWindow_GetDefaultSize = wx.TopLevelWindow.GetDefaultSize
# wx.Trap = MISSING
wx.TreebookEvent = wx.BookCtrlEvent
wx.TreeCtrl_GetClassDefaultAttributes = wx.TreeCtrl.GetClassDefaultAttributes
wx.UpdateUIEvent_CanUpdate = wx.UpdateUIEvent.CanUpdate
wx.UpdateUIEvent_GetMode = wx.UpdateUIEvent.GetMode
wx.UpdateUIEvent_GetUpdateInterval = wx.UpdateUIEvent.GetUpdateInterval
wx.UpdateUIEvent_ResetUpdateTime = wx.UpdateUIEvent.ResetUpdateTime
wx.UpdateUIEvent_SetMode = wx.UpdateUIEvent.SetMode
wx.UpdateUIEvent_SetUpdateInterval = wx.UpdateUIEvent.SetUpdateInterval
wx.Validator_IsSilent = wx.Validator.IsSilent
# wx.Validator_SetBellOnError = REMOVED
wx.Validator_SuppressBellOnError = wx.Validator.SuppressBellOnError
wx.Window_FindFocus = wx.Window.FindFocus
# wx.Window_FromHWND = MISSING
wx.Window_GetCapture = wx.Window.GetCapture
wx.Window_GetClassDefaultAttributes = wx.Window.GetClassDefaultAttributes
wx.Window_NewControlId = wx.Window.NewControlId
wx.Window_UnreserveControlId = wx.Window.UnreserveControlId
# wx.XPMHandler = MISSING


def blit_point_size(self, *args, **kwargs):
    return self.Blit(*args, **kwargs)


def calc_bounding_box_point(self, *args, **kwargs):
    return self.CalcBoundingBox(*args, **kwargs)


def cross_hair_point(self, *args, **kwargs):
    return self.CrossHair(*args, **kwargs)


def draw_arc_point(self, *args, **kwargs):
    return self.DrawArc(*args, **kwargs)


def draw_bitmap_point(self, *args, **kwargs):
    return self.DrawBitmap(*args, **kwargs)


def draw_check_mark_rect(self, *args, **kwargs):
    return self.DrawCheckMark(*args, **kwargs)


def draw_circle_point(self, *args, **kwargs):
    return self.DrawCircle(*args, **kwargs)


def draw_ellipse_point_size(self, *args, **kwargs):
    return self.DrawEllipse(*args, **kwargs)


def draw_ellipse_rect(self, *args, **kwargs):
    return self.DrawEllipse(*args, **kwargs)


def draw_elliptic_arc_point_size(self, *args, **kwargs):
    return self.DrawEllipticArc(*args, **kwargs)


def draw_icon_point(self, *args, **kwargs):
    return self.DrawIcon(*args, **kwargs)


def draw_line_point(self, *args, **kwargs):
    return self.DrawLine(*args, **kwargs)


def draw_point_point(self, *args, **kwargs):
    return self.DrawPoint(*args, **kwargs)


def draw_rectangle_point_size(self, *args, **kwargs):
    return self.DrawRectangle(*args, **kwargs)


def draw_rectangle_rect(self, *args, **kwargs):
    return self.DrawRectangle(*args, **kwargs)


def draw_rotated_text_point(self, *args, **kwargs):
    return self.DrawRotatedText(*args, **kwargs)


def draw_rounded_rectangle_point_size(self, *args, **kwargs):
    return self.DrawRoundedRectangle(*args, **kwargs)


def draw_rounded_rectangle_rect(self, *args, **kwargs):
    return self.DrawRoundedRectangle(*args, **kwargs)


def draw_text_point(self, *args, **kwargs):
    return self.DrawText(*args, **kwargs)


def flood_fill_point(self, *args, **kwargs):
    return self.FloodFill(*args, **kwargs)


def get_device_origin_tuple(self, *args, **kwargs):
    return self.GetDeviceOrigin(*args, **kwargs)


# wx.DC.GetImpl = REMOVED


def get_logical_origin_tuple(self, *args, **kwargs):
    return self.GetLogicalOrigin(*args, **kwargs)


def get_multi_line_text_extent(self, *args, **kwargs):
    return self.GetFullMultiLineTextExtent(*args, **kwargs)


# wx.DC.GetOptimization = REMOVED


def get_pixel_point(self, *args, **kwargs):
    return self.GetPixel(*args, **kwargs)


def get_resolution(self, *args, **kwargs):
    return self.GetPPI(*args, **kwargs)


def get_size_m_m_tuple(self, *args, **kwargs):
    return self.GetSizeMM(*args, **kwargs)


def ok(self, *args, **kwargs):
    return self.IsOk(*args, **kwargs)


def set_clipping_rect(self, *args, **kwargs):
    return self.SetClippingRegion(*args, **kwargs)


def set_clipping_region_as_region(self, *args, **kwargs):
    return self.SetClippingRegion(*args, **kwargs)


def set_clipping_region_point_size(self, *args, **kwargs):
    return self.SetClippingRegion(*args, **kwargs)


def set_device_origin_point(self, *args, **kwargs):
    return self.SetDeviceOrigin(*args, **kwargs)


def set_logical_origin_point(self, *args, **kwargs):
    return self.SetLogicalOrigin(*args, **kwargs)


def stretch_blit_point_size(self, *args, **kwargs):
    return self.StretchBlit(*args, **kwargs)


wx.DC.BlitPointSize = blit_point_size
wx.DC.CalcBoundingBoxPoint = calc_bounding_box_point
wx.DC.CrossHairPoint = cross_hair_point
wx.DC.DrawArcPoint = draw_arc_point
wx.DC.DrawBitmapPoint = draw_bitmap_point
wx.DC.DrawCheckMarkRect = draw_check_mark_rect
wx.DC.DrawCirclePoint = draw_circle_point
wx.DC.DrawEllipsePointSize = draw_ellipse_point_size
wx.DC.DrawEllipseRect = draw_ellipse_rect
wx.DC.DrawEllipticArcPointSize = draw_elliptic_arc_point_size
wx.DC.DrawIconPoint = draw_icon_point
wx.DC.DrawLinePoint = draw_line_point
wx.DC.DrawPointPoint = draw_point_point
wx.DC.DrawRectanglePointSize = draw_rectangle_point_size
wx.DC.DrawRectangleRect = draw_rectangle_rect
wx.DC.DrawRotatedTextPoint = draw_rotated_text_point
wx.DC.DrawRoundedRectanglePointSize = draw_rounded_rectangle_point_size
wx.DC.DrawRoundedRectangleRect = draw_rounded_rectangle_rect
wx.DC.DrawTextPoint = draw_text_point
wx.DC.FloodFillPoint = flood_fill_point
wx.DC.GetDeviceOriginTuple = get_device_origin_tuple
wx.DC.GetLogicalOriginTuple = get_logical_origin_tuple
wx.DC.GetMultiLineTextExtent = get_multi_line_text_extent
wx.DC.GetPixelPoint = get_pixel_point
wx.DC.GetResolution = get_resolution
wx.DC.GetSizeMMTuple = get_size_m_m_tuple
wx.DC.Ok = ok
wx.DC.SetClippingRect = set_clipping_rect
wx.DC.SetClippingRegionAsRegion = set_clipping_region_as_region
wx.DC.SetClippingRegionPointSize = set_clipping_region_point_size
wx.DC.SetDeviceOriginPoint = set_device_origin_point
wx.DC.SetLogicalOriginPoint = set_logical_origin_point
wx.DC.StretchBlitPointSize = stretch_blit_point_size

try:
    wx.PyApp_GetMacAboutMenuItemId = wx.PyApp.__dict__['GetMacAboutMenuItemId']
    wx.PyApp_GetMacExitMenuItemId = wx.PyApp.__dict__['GetMacExitMenuItemId']
    wx.PyApp_GetMacHelpMenuTitleName = wx.PyApp.__dict__['GetMacHelpMenuTitleName']
    wx.PyApp_GetMacPreferencesMenuItemId = wx.PyApp.__dict__['GetMacPreferencesMenuItemId']
    wx.PyApp_SetMacAboutMenuItemId = wx.PyApp.__dict__['SetMacAboutMenuItemId']
    wx.PyApp_SetMacExitMenuItemId = wx.PyApp.__dict__['SetMacExitMenuItemId']
    wx.PyApp_SetMacHelpMenuTitleName = wx.PyApp.__dict__['SetMacHelpMenuTitleName']
    wx.PyApp_SetMacPreferencesMenuItemId = wx.PyApp.__dict__['SetMacPreferencesMenuItemId']
except KeyError:
    pass


def yield_if_needed():
    return wx.GetApp().Yield(onlyIfNeeded=True)


def tree_item_data(data):
    return data


def do_nothing_func(*_, **__):
    pass


wx.TreeItemData = tree_item_data
wx.YieldIfNeeded = yield_if_needed
wx.DC.BeginDrawing = do_nothing_func
wx.DC.EndDrawing = do_nothing_func
wx.DC.SetOptimization = do_nothing_func
wx.App_CleanUp = do_nothing_func
wx.WakeUpMainThread = do_nothing_func


def client_to_screen_x_y(self, *args, **kwargs):
    return self.ClientToScreen(*args, **kwargs)


def convert_dialog_point_to_pixels(self, *args, **kwargs):
    return self.ConvertDialogToPixels(*args, **kwargs)


def convert_dialog_size_to_pixels(self, *args, **kwargs):
    return self.ConvertDialogToPixels(*args, **kwargs)


def get_adjusted_best_size(self, *args, **kwargs):
    return self.GetEffectiveMinSize(*args, **kwargs)


def get_best_fitting_size(self, *args, **kwargs):
    return self.GetEffectiveMinSize(*args, **kwargs)


def get_best_size_tuple(self, *args, **kwargs):
    return self.GetBestSize(*args, **kwargs)


def get_client_size_tuple(self, *args, **kwargs):
    return self.GetClientSize(*args, **kwargs)


def get_screen_position_tuple(self, *args, **kwargs):
    return self.GetScreenPosition(*args, **kwargs)


def get_size_tuple(self, *args, **kwargs):
    return self.GetSize(*args, **kwargs)


def get_tool_tip_string(self, *args, **kwargs):
    return self.GetToolTipText(*args, **kwargs)


def hit_test_x_y(self, *args, **kwargs):
    return self.HitTest(*args, **kwargs)


def is_exposed_point(self, *args, **kwargs):
    return self.IsExposed(*args, **kwargs)


def is_exposed_rect(self, *args, **kwargs):
    return self.IsExposed(*args, **kwargs)


# wx.Window.MakeModal = REMOVED


def popup_menu_x_y(self, *args, **kwargs):
    return self.PopupMenu(*args, **kwargs)


def screen_to_client_x_y(self, *args, **kwargs):
    return self.ScreenToClient(*args, **kwargs)


def set_best_fitting_size(self, *args, **kwargs):
    return self.SetInitialSize(*args, **kwargs)


def set_client_size_w_h(self, *args, **kwargs):
    return self.SetClientSize(*args, **kwargs)


def set_dimensions(self, *args, **kwargs):
    return self.SetSize(*args, **kwargs)


def set_help_text_for_id(self, *args, **kwargs):
    return self.SetHelpText(*args, **kwargs)


def set_size_hints_sz(self, *args, **kwargs):
    return self.SetSizeHints(*args, **kwargs)


def set_tool_tip_string(self, *args, **kwargs):
    return self.SetToolTip(*args, **kwargs)


# wx.Window.SetVirtualSizeHints = REMOVED
# wx.Window.SetVirtualSizeHintsSz = REMOVED


def add_f(self, *args, **kwargs):
    return self.Add(*args, **kwargs)


def add_item(self, *args, **kwargs):
    return self.Add(*args, **kwargs)


def add_sizer(self, *args, **kwargs):
    return self.Add(*args, **kwargs)


def add_window(self, *args, **kwargs):
    return self.Add(*args, **kwargs)


def delete_windows(self, *args, **kwargs):
    return self.Clear(*args, **kwargs)


def get_item_index(self, *args, **kwargs):
    return self.GetItem(*args, **kwargs)


def get_min_size_tuple(self, *args, **kwargs):
    return self.GetMinSize(*args, **kwargs)


def get_position_tuple(self, *args, **kwargs):
    return self.GetPosition(*args, **kwargs)


def insert_f(self, *args, **kwargs):
    return self.Insert(*args, **kwargs)


def insert_item(self, *args, **kwargs):
    return self.Insert(*args, **kwargs)


def insert_sizer(self, *args, **kwargs):
    return self.Insert(*args, **kwargs)


def insert_window(self, *args, **kwargs):
    return self.Insert(*args, **kwargs)


def prepend_f(self, *args, **kwargs):
    return self.Prepend(*args, **kwargs)


def prepend_item(self, *args, **kwargs):
    return self.Prepend(*args, **kwargs)


def prepend_sizer(self, *args, **kwargs):
    return self.Prepend(*args, **kwargs)


def prepend_window(self, *args, **kwargs):
    return self.Prepend(*args, **kwargs)


def remove_pos(self, *args, **kwargs):
    return self.Remove(*args, **kwargs)


def remove_sizer(self, *args, **kwargs):
    return self.Remove(*args, **kwargs)


def remove_window(self, *args, **kwargs):
    return self.Remove(*args, **kwargs)


wx.Window.ClientToScreenXY = client_to_screen_x_y
wx.Window.ConvertDialogPointToPixels = convert_dialog_point_to_pixels
wx.Window.ConvertDialogSizeToPixels = convert_dialog_size_to_pixels
wx.Window.GetAdjustedBestSize = get_adjusted_best_size
wx.Window.GetBestFittingSize = get_best_fitting_size
wx.Window.GetBestSizeTuple = get_best_size_tuple
wx.Window.GetClientSizeTuple = get_client_size_tuple
wx.Window.GetScreenPositionTuple = get_screen_position_tuple
wx.Window.GetSizeTuple = get_size_tuple
wx.Window.GetToolTipString = get_tool_tip_string
wx.Window.HitTestXY = hit_test_x_y
wx.Window.IsExposedPoint = is_exposed_point
wx.Window.IsExposedRect = is_exposed_rect
wx.Window.PopupMenuXY = popup_menu_x_y
wx.Window.ScreenToClientXY = screen_to_client_x_y
wx.Window.SetBestFittingSize = set_best_fitting_size
wx.Window.SetClientSizeWH = set_client_size_w_h
wx.Window.SetDimensions = set_dimensions
wx.Window.SetHelpTextForId = set_help_text_for_id
wx.Window.SetSizeHintsSz = set_size_hints_sz
wx.Window.SetToolTipString = set_tool_tip_string
wx.Sizer.AddF = add_f
wx.Sizer.AddItem = add_item
wx.Sizer.AddSizer = add_sizer
wx.Sizer.AddWindow = add_window
wx.Sizer.DeleteWindows = delete_windows
wx.Sizer.GetItemIndex = get_item_index
wx.Sizer.GetMinSizeTuple = get_min_size_tuple
wx.Sizer.GetPositionTuple = get_position_tuple
wx.Sizer.InsertF = insert_f
wx.Sizer.InsertItem = insert_item
wx.Sizer.InsertSizer = insert_sizer
wx.Sizer.InsertWindow = insert_window
wx.Sizer.PrependF = prepend_f
wx.Sizer.PrependItem = prepend_item
wx.Sizer.PrependSizer = prepend_sizer
wx.Sizer.PrependWindow = prepend_window
wx.Sizer.RemovePos = remove_pos
wx.Sizer.RemoveSizer = remove_sizer
wx.Sizer.RemoveWindow = remove_window


def append_menu(self, *args, **kwargs):
    args = list(args)
    if 'id' in kwargs:
        del kwargs['id']
    else:
        args.pop(0)

    if 'text' not in kwargs:
        kwargs['text'] = args.pop(0)
    if 'submenu' not in kwargs:
        kwargs['submenu'] = args.pop(0)
    if 'help' not in kwargs and len(args):
        kwargs['help'] = args.pop(0)

    return self.AppendSubMenu(**kwargs)


_original_append = wx.Menu.Append


def append(self, *args, **kwargs):
    if 'subMenu' in kwargs:
        args = list(args)
        kwargs['submenu'] = kwargs.pop('subMenu')
        if 'id' not in kwargs:
            kwargs['id'] = args.pop(0)

        if 'item' in kwargs:
            kwargs['text'] = kwargs.pop('item')
        else:
            kwargs['text'] = args.pop(0)

        if 'helpString' in kwargs:
            kwargs['help'] = kwargs.pop('helpString')

        return append_menu(self, **kwargs)

    return _original_append(self, *args, **kwargs)

#
# def append_item(self, *args, **kwargs):
#     if 'item' in kwargs:
#         kwargs['menuItem'] = kwargs.pop('item')
#     else:
#         kwargs['menuItem'] = args[0]
#
#     return self.Append(**kwargs)

wx.Menu.AppendMenu = append_menu
wx.Menu.Append = append
# wx.Menu.AppendItem = append_item
#
# def add_simple_tool(self, *args, **kwargs):
#     args = list(args)
#
#     if 'id' in kwargs:
#         kwargs['toolId'] = kwargs.pop('id')
#     else:
#         kwargs['toolId'] = args.pop(0)
#
#     if 'bitmap' not in kwargs:
#         kwargs['bitmap'] = args.pop(0)
#     if 'shortHelp' not in kwargs and len(args):
#         kwargs['shortHelp'] = args.pop(0)
#     if 'longHelp' not in kwargs and len(args):
#         kwargs['longHelp'] = args.pop(0)
#     if 'kind' not in kwargs and len(args):
#         kwargs['kind'] = args.pop(0)
#
#     return self.AddTool(**kwargs)
#
#
# wx.ToolBar.AddSimpleTool = add_simple_tool


wx.DECORATIVE = wx.FONTFAMILY_DECORATIVE
wx.ROMAN = wx.FONTFAMILY_ROMAN
wx.SCRIPT = wx.FONTFAMILY_SCRIPT
wx.SWISS = wx.FONTFAMILY_SWISS
wx.MODERN = wx.FONTFAMILY_MODERN
wx.TELETYPE = wx.FONTFAMILY_TELETYPE
wx.NORMAL = wx.FONTSTYLE_NORMAL
wx.ITALIC = wx.FONTSTYLE_ITALIC
wx.SLANT = wx.FONTSTYLE_SLANT

wx.EVT_TASKBAR_MOVE = wx.adv.EVT_TASKBAR_MOVE
wx.EVT_TASKBAR_LEFT_DOWN = wx.adv.EVT_TASKBAR_LEFT_DOWN
wx.EVT_TASKBAR_LEFT_UP = wx.adv.EVT_TASKBAR_LEFT_UP
wx.EVT_TASKBAR_RIGHT_DOWN = wx.adv.EVT_TASKBAR_RIGHT_DOWN
wx.EVT_TASKBAR_RIGHT_UP = wx.adv.EVT_TASKBAR_RIGHT_UP
wx.EVT_TASKBAR_LEFT_DCLICK = wx.adv.EVT_TASKBAR_LEFT_DCLICK
wx.EVT_TASKBAR_RIGHT_DCLICK = wx.adv.EVT_TASKBAR_RIGHT_DCLICK
wx.EVT_TASKBAR_CLICK = wx.adv.EVT_TASKBAR_CLICK

wx.OPEN = wx.FD_OPEN
wx.SAVE = wx.FD_SAVE
wx.OVERWRITE_PROMPT = wx.FD_OVERWRITE_PROMPT
wx.FILE_MUST_EXIST = wx.FD_FILE_MUST_EXIST
wx.MULTIPLE = wx.FD_MULTIPLE
wx.CHANGE_DIR = wx.FD_CHANGE_DIR
wx.PREVIEW = wx.FD_PREVIEW


wx.BitmapFromBufferRGBA = wx.Bitmap.FromBufferRGBA
wx.NewId = wx.NewIdRef

# wx.lib.grids = REMOVED
# wx.lib.pyshell = REMOVED
# wx.lib.rightalign = REMOVED
# wx.lib.shell = REMOVED
# wx.lib.splashscreen = REMOVED
# wx.lib.wxPlotCanvas = REMOVED

ModuleRedirect(['wx.lib.agw.buttonpanel'], 'wx.lib.buttonpanel')
ModuleRedirect(['wx.lib.agw.customtreectrl'], 'wx.lib.customtreectrl')
ModuleRedirect(['wx.lib.agw.flatnotebook'], 'wx.lib.flatnotebook')
ModuleRedirect(['wx.lib.agw.foldpanelbar'], 'wx.lib.foldpanelbar')
ModuleRedirect(['wx.lib.agw.hyperlink'], 'wx.lib.hyperlink')
ModuleRedirect(['wx.adv'], 'wx.calendar')
ModuleRedirect(['wx.adv'], 'wx.animate')
ModuleRedirect(['wx.adv'], 'wx.combo')
ModuleRedirect(['wx.dataview', 'wx.adv'], 'wx.gizmos')
ModuleRedirect(['wx.adv'], 'wx.wizard')
ModuleRedirect(['wx.html'], 'wx.html')
ModuleRedirect(['wx.adv', 'wx'], 'wx')

sys.modules['wx'] = wx

