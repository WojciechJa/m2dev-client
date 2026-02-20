# coding=utf-8

import os
import ui
import net
import app
import snd
import chat
import grp
import ime
import wndMgr
import mouseModule
import uiScriptLocale
import localeInfo
import constInfo
import player
import nonplayer
import time
import item
import dbg
import uiToolTip
import miniMap
#import renderTarget

IMG_PATH = "d:/ymir work/ui/adminpanel/create_item/"
#BUTTON_PATH = "d:/ymir work/ui/game/monster_card/button/"

NORMAL_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
POSITIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)
NEGATIVE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)

try:
    _now = time.perf_counter
except AttributeError:
    _now = time.time

try:
    _INTEGER_TYPES = (int, long)
except NameError:
    _INTEGER_TYPES = (int,)

_ADMINPANEL_MOB_VNUM_CACHE = None


class MobSpawnMapWindow(ui.ScriptWindow):

    class IndependentAtlasRenderer(ui.Window):

        def __init__(self):
            ui.Window.__init__(self)
            self.AddFlag("not_pick")
            self.AddFlag("attach")
            self.isAtlasActive = False
            self.wasAtlasVisible = False
            self.hasSavedAtlasState = False

        def OnUpdate(self):
            if self.isAtlasActive:
                miniMap.UpdateAtlas()

        def OnRender(self):
            if self.isAtlasActive:
                (x, y) = self.GetGlobalPosition()
                fx = float(x)
                fy = float(y)
                miniMap.RenderAtlas(fx, fy)

        def ShowIndependentAtlas(self):
            if self.isAtlasActive:
                return
            try:
                if hasattr(miniMap, "isShowAtlas"):
                    self.wasAtlasVisible = bool(miniMap.isShowAtlas())
                    self.hasSavedAtlasState = True
            except:
                self.wasAtlasVisible = False
                self.hasSavedAtlasState = False
            try:
                if hasattr(miniMap, "ShowAtlas"):
                    miniMap.ShowAtlas()
            except:
                pass
            self.isAtlasActive = True

        def HideIndependentAtlas(self):
            if not self.isAtlasActive:
                return
            self.isAtlasActive = False
            try:
                if self.hasSavedAtlasState:
                    if self.wasAtlasVisible:
                        miniMap.ShowAtlas()
                    else:
                        miniMap.HideAtlas()
            except:
                pass
            self.hasSavedAtlasState = False

    def __init__(self, parentWindow):
        self.board = None
        self.instrText = None
        self.coordText = None
        self.AtlasMainWindow = None
        self.confirmButton = None
        self.cancelButton = None

        ui.ScriptWindow.__init__(self)

        self.parentWindow = parentWindow
        self.selectedCoords = (0, 0)
        self.isCoordSelected = False
        self.__LoadWindow()

    def __LoadWindow(self):
        self.board = ui.BoardWithTitleBar()
        self.board.SetParent(self)
        self.board.SetTitleName(localeInfo.ADMINPANEL_SPAWN_MOB_SELECT_COORDS_TITLE)
        self.board.SetCloseEvent(ui.__mem_func__(self.Close))

        self.AddFlag("movable")
        self.AddFlag("float")

        self.board.AddFlag("movable")
        self.board.AddFlag("float")

        self.instrText = ui.TextLine()
        self.instrText.SetParent(self.board)
        self.instrText.SetPosition(10, 35)
        self.instrText.SetText(localeInfo.ADMINPANEL_SPAWN_MOB_SELECT_COORDS_ON_MAP)
        self.instrText.Show()

        # Coordinates display
        self.coordText = ui.TextLine()
        self.coordText.SetParent(self.board)
        self.coordText.SetPosition(10, 55)
        self.coordText.SetText(localeInfo.ADMINPANEL_SPAWN_MOB_NO_CORDS_SELECTED)
        self.coordText.Show()

        self.AtlasMainWindow = self.IndependentAtlasRenderer()
        self.AtlasMainWindow.SetParent(self.board)
        self.AtlasMainWindow.SetPosition(7, 75)

        self.board.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.OnMouseLeftButtonUpEvent))

        try:
            (bGet, iSizeX, iSizeY) = miniMap.GetAtlasSize()
            if bGet:
                self.AtlasMainWindow.SetSize(iSizeX, iSizeY)
                boardWidth = iSizeX + 15
                boardHeight = 75 + iSizeY + 80
                self.board.SetSize(boardWidth, boardHeight)
                self.SetSize(boardWidth, boardHeight)
            else:
                self.AtlasMainWindow.SetSize(400, 300)
                boardWidth = 415
                boardHeight = 75 + 300 + 80  # 455 total
                self.board.SetSize(boardWidth, boardHeight)
                self.SetSize(boardWidth, boardHeight)
        except Exception as e:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "Atlas error: %s" % str(e))
            self.AtlasMainWindow.SetSize(400, 300)
            boardWidth = 415
            boardHeight = 75 + 300 + 80  # 455 total
            self.board.SetSize(boardWidth, boardHeight)
            self.SetSize(boardWidth, boardHeight)

        screenWidth = wndMgr.GetScreenWidth()
        screenHeight = wndMgr.GetScreenHeight()
        windowWidth = self.GetWidth()
        windowHeight = self.GetHeight()

        posX = (screenWidth - windowWidth) // 4  # Left side of screen
        posY = (screenHeight - windowHeight) // 2  # Vertically centered
        self.SetPosition(posX, posY)

        self.AtlasMainWindow.ShowIndependentAtlas()
        self.AtlasMainWindow.Show()
        self.board.Show()


        buttonY = self.board.GetHeight() - 45
        self.confirmButton = ui.Button()
        self.confirmButton.SetParent(self.board)
        self.confirmButton.SetPosition(10, buttonY)
        self.confirmButton.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
        self.confirmButton.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
        self.confirmButton.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
        self.confirmButton.SetText(localeInfo.UI_ACCEPT)
        self.confirmButton.SetEvent(ui.__mem_func__(self.OnConfirm))
        self.confirmButton.Show()

        self.cancelButton = ui.Button()
        self.cancelButton.SetParent(self.board)
        self.cancelButton.SetPosition(140, buttonY)
        self.cancelButton.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
        self.cancelButton.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
        self.cancelButton.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
        self.cancelButton.SetText(localeInfo.UI_CANCEL)
        self.cancelButton.SetEvent(ui.__mem_func__(self.Close))
        self.cancelButton.Show()

        chat.AppendChat(chat.CHAT_TYPE_INFO,
                        "Buttons positioned at Y: %d (Board height: %d)" % (buttonY, self.board.GetHeight()))

    def OnPressEscapeKey(self):
        self.Close()
        return True

    def OnMouseLeftButtonUpEvent(self):
        (mouseX, mouseY) = wndMgr.GetMousePosition()
        (bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID) = miniMap.GetAtlasInfo(mouseX, mouseY)

        if (bFind and iPosX != 0 and iPosY != 0) or (iPosX != 0 or iPosY != 0):
            self.selectedCoords = (iPosX, iPosY)
            self.isCoordSelected = True

            if sName and sName != "":
                displayText = "%s (%d, %d)" % (sName, iPosX, iPosY)
            else:
                displayText = "(%d, %d)" % (iPosX, iPosY)

            self.coordText.SetText(displayText)
            self.coordText.SetPackedFontColor(0xFF00FF00)  # Green
        else:
            self.coordText.SetText(localeInfo.ADMINPANEL_SPAWN_MOB_INVALID_COORDS)
            self.coordText.SetPackedFontColor(0xFFFF0000)  # Red
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMINPANEL_SPAWN_MOB_INVALID_COORDS)

    def OnUpdate(self):
        if not self.board or not self.board.IsIn():
            return

        (mouseX, mouseY) = wndMgr.GetMousePosition()
        try:
            (bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID) = miniMap.GetAtlasInfo(mouseX, mouseY)
            if bFind and (iPosX != 0 or iPosY != 0):
                if sName and sName != "":
                    self.instrText.SetText("%s (%d, %d)" % (sName, iPosX, iPosY))
                else:
                    self.instrText.SetText("(%d, %d)" % (iPosX, iPosY))
            else:
                self.instrText.SetText(localeInfo.ADMINPANEL_SPAWN_MOB_SELECT_COORDS_ON_MAP)
        except:
            self.instrText.SetText(localeInfo.ADMINPANEL_SPAWN_MOB_SELECT_COORDS_ON_MAP)

    def OnConfirm(self):
        if self.isCoordSelected:
            self.parentWindow.SetSelectedCoordinates(self.selectedCoords[0], self.selectedCoords[1])
            self.Close()
        else:
            self.coordText.SetText(localeInfo.ADMINPANEL_SPAWN_MOB_NO_CORDS_SELECTED)
            self.coordText.SetPackedFontColor(0xFFFF0000)
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMINPANEL_SPAWN_MOB_NO_CORDS_SELECTED)

    def Show(self):
        if self.board:
            self.board.Show()
            if self.AtlasMainWindow:
                self.AtlasMainWindow.ShowIndependentAtlas()
        ui.ScriptWindow.Show(self)

    def Close(self):
        if self.parentWindow:
            self.parentWindow.mobSpawnMapWindow = None

        if self.AtlasMainWindow:
            self.AtlasMainWindow.HideIndependentAtlas()
        if self.board:
            self.board.Hide()
        self.Hide()

    def Hide(self):
        if self.parentWindow and hasattr(self.parentWindow, 'mobSpawnMapWindow') and self.parentWindow.mobSpawnMapWindow == self:
            self.parentWindow.mobSpawnMapWindow = None

        if self.board:
            self.board.Hide()
            if self.AtlasMainWindow:
                self.AtlasMainWindow.HideIndependentAtlas()
        ui.ScriptWindow.Hide(self)


class MainWindow(ui.ScriptWindow):

    def __init__(self):
        self.isMoblistLoaded = False
        self.isMoblistLoading = False
        self.deferMobLoad = False
        self.mobList = None
        self.mobDestCount = 0
        self.mobCurCount = 0
        self.lazyMobsPerFrame = 250
        self.scanMobsFallback = False
        self.scanCurrentVnum = 1
        self.scanMaxVnum = 200000
        self.scanEmptyStreak = 0
        self.scanMinStopVnum = 10000
        self.scanEmptyStopThreshold = 25000

        self.selectedMobVnum = 0

        self.animWindowWidth = [490, 490]
        self.curWindowWidth = 490.0
        self.destWindowWidth = 490.0

        self.animConfigWndPos = [225, 225]
        self.curConfigWndPos = 225.0
        self.destConfigWndPos = 225.0

        self.animResetBtnPos = [270, 270]
        self.curResetBtnPos = 270.0
        self.destResetBtnPos = 270.0

        self.MOBS_PER_PAGE = 100
        self.currentPage = 0
        self.totalPages = 0
        self.isPageLoaded = False

        # 3D Model viewing variables
        self.isModelViewEnabled = False
        self.ModelPreviewBoard = None
        self.ModelPreview = None
        self.isRenderTargetActive = False

        self.sortMode = 0

        # COORDINATE SELECTION VARIABLES
        self.selectedSpawnX = 0
        self.selectedSpawnY = 0
        self.isCoordModeSelected = False
        self.mobSpawnMapWindow = None
        self.isCoordMapExpanded = False
        self.coordMapBoard = None
        self.coordMapAtlasWindow = None
        self.coordMapHoverText = None
        self.coordMapSelectedText = None
        self.coordMapAtlasWidth = 400
        self.coordMapAtlasHeight = 300

        ui.ScriptWindow.__init__(self)
        self.__LoadWindow()

    def __del__(self):
        self.isMoblistLoaded = False
        self.isMoblistLoading = False
        self.deferMobLoad = False
        self.mobList = None
        #self.__ModelPreviewClose()
        ui.ScriptWindow.__del__(self)

    def Show(self):
        if not self.isMoblistLoaded and not self.isMoblistLoading:
            self.deferMobLoad = True
        ui.ScriptWindow.Show(self)

    def Close(self):
        self.__HideEmbeddedCoordinateMap()
        #self.__ModelPreviewClose()
        self.Hide()

    def Destroy(self):
        self.__HideEmbeddedCoordinateMap()
        #self.__ModelPreviewClose()
        self.Hide()
        self.ClearDictionary()

    def __LoadWindow(self):
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "adminpanel_module/uiscript/spawn_mob.py")
        except:
            import exception
            exception.Abort("SpawnMobWindow.LoadWindow.LoadObject")

        try:
            self.GetChild("board").CloseButtonHide()

            self.configFields = [self.GetChild("field_set_count"), self.GetChild("field_sort_mode")]
            self.configOverlays = [self.GetChild("field_set_count_overlay"), self.GetChild("field_sort_mode_overlay")]

            for overlay in self.configOverlays:
                overlay.SetAlpha(0.7)

            self.configFields[0].SetStringEvent("MOUSE_LEFT_BUTTON_DOWN", ui.__mem_func__(self.SetEditLineFocus), 0)
            self.GetChild("editline_set_count").SetReturnEvent(ui.__mem_func__(self.OnSpawnMob))
            self.GetChild("coord_select_btn").SetEvent(ui.__mem_func__(self.OnOpenCoordinateMap))
            self.GetChild("prev_page_btn").SetEvent(ui.__mem_func__(self.PrevPage))
            self.GetChild("next_page_btn").SetEvent(ui.__mem_func__(self.NextPage))
            self.pageInfoText = self.GetChild("page_info")

            self.GetChild("mv_up_button").SetEvent(ui.__mem_func__(self.OnMoveUp))
            self.GetChild("mv_down_button").SetEvent(ui.__mem_func__(self.OnMoveDown))
            self.GetChild("left_rotation_button").SetEvent(ui.__mem_func__(self.OnRotateLeft))
            self.GetChild("right_rotation_button").SetEvent(ui.__mem_func__(self.OnRotateRight))
            self.GetChild("mv_reset_button").SetEvent(ui.__mem_func__(self.OnResetView))
            self.GetChild("zoomin_button").SetEvent(ui.__mem_func__(self.OnZoomIn))
            self.GetChild("zoomout_button").SetEvent(ui.__mem_func__(self.OnZoomOut))
            self.GetChild("motion_button").SetEvent(ui.__mem_func__(self.OnChangeMotion))

            # Initialize mob list
            listBoxSearch = ListBoxSearch()
            listBoxSearch.SetParent(self.GetChild("moblist_background"))
            listBoxSearch.SetPosition(4, 4)
            listBoxSearch.SetSize(200 - 4 - 4, 15 * listBoxSearch.stepSize)
            listBoxSearch.SetEvent(ui.__mem_func__(self.OnSelectMob))
            listBoxSearch.SetMinSearchTextLen(1)
            listBoxSearch.SetEditLine(self.GetChild("mobsearch"))
            listBoxSearch.Show()
            self.listBoxSearch = listBoxSearch

            self.spawnModeRadioButtons = []
            self.spawnModeRadioButtons.append(self.GetChild("spawn_mode_point"))
            self.spawnModeRadioButtons.append(self.GetChild("spawn_mode_random"))
            self.spawnModeRadioButtons.append(self.GetChild("spawn_mode_map"))

            self.spawnModeRadioButtonGroup = ui.RadioButtonGroup.Create([
                [self.spawnModeRadioButtons[0], lambda: self.OnSelectSpawnMode(0), None],
                [self.spawnModeRadioButtons[1], lambda: self.OnSelectSpawnMode(1), None],
                [self.spawnModeRadioButtons[2], lambda: self.OnSelectSpawnMode(2), None]
            ])

            # Set default selection (Random mode = index 1)
            self.spawnMode = 1
            self.spawnModeRadioButtonGroup.OnClick(1)

            # Sort mode selection
            self.selectSortMode = ui.ComboBoxEx()
            self.selectSortMode.SetParent(self)
            self.selectSortMode.SetPosition(18, 438)
            self.selectSortMode.SetSize(188, 15)
            self.selectSortMode.SetEvent(ui.__mem_func__(self.OnSelectSortMode))

            self.selectSortMode.InsertItem(0, localeInfo.ADMINPANEL_SPAWN_MOB_SORT_VNUM)
            self.selectSortMode.InsertItem(1, localeInfo.ADMINPANEL_SPAWN_MOB_SORT_NAME)
            self.selectSortMode.InsertItem(2, localeInfo.ADMINPANEL_SPAWN_MOB_SORT_TYPE)

            self.selectSortMode.SetCurrentItem(localeInfo.ADMINPANEL_SPAWN_MOB_SORT_VNUM)
            self.sortMode = 0
            self.selectSortMode.Show()
            self.selectSortMode.SetTop()

            self.GetChild("SpawnButton").SetEvent(ui.__mem_func__(self.OnSpawnMob))
            self.GetChild("ResetButton").SetEvent(ui.__mem_func__(self.OnResetMob))

            self.tooltipItem = uiToolTip.ItemToolTip()
            self.tooltipItem.Hide()
            self.__CreateEmbeddedCoordinateMap()

        except:
            self.pageInfoText = None
            import exception
            exception.Abort("SpawnMobWindow.LoadWindow.BindObject")

    def SetEditLineFocus(self, index):
        self.GetChild("editline_set_count").SetFocus()

    def OnSelectSpawnMode(self, mode):
        self.spawnMode = mode

        coord_btn = self.GetChild("coord_select_btn")
        if mode == 0:
            coord_btn.Show()
            self.__ShowEmbeddedCoordinateMap()
        else:  # Random or Map mode - hide coordinate selection
            coord_btn.Hide()
            self.isCoordModeSelected = False
            self.__HideEmbeddedCoordinateMap()

    def OnOpenCoordinateMap(self):
        try:
            if self.spawnMode != 0:
                return

            if self.isCoordMapExpanded:
                self.__HideEmbeddedCoordinateMap()
            else:
                self.__ShowEmbeddedCoordinateMap()
        except Exception as e:
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMINPANEL_SPAWN_MOB_COORD_ERROR % str(e))

    def SetSelectedCoordinates(self, x, y):
        self.selectedSpawnX = x
        self.selectedSpawnY = y
        self.isCoordModeSelected = True
        if self.coordMapSelectedText:
            self.coordMapSelectedText.SetText("(%d, %d)" % (x, y))
            self.coordMapSelectedText.SetPackedFontColor(0xFF00FF00)

    def __CreateEmbeddedCoordinateMap(self):
        try:
            (bGet, iSizeX, iSizeY) = miniMap.GetAtlasSize()
            if bGet and iSizeX > 0 and iSizeY > 0:
                self.coordMapAtlasWidth = iSizeX
                self.coordMapAtlasHeight = iSizeY
        except:
            pass

        self.animWindowWidth = [490, 490 + self.coordMapAtlasWidth + 25]
        self.curWindowWidth = float(self.animWindowWidth[0])
        self.destWindowWidth = float(self.animWindowWidth[0])

        board = self.GetChild("board")

        self.coordMapBoard = ui.ThinBoardCircle()
        self.coordMapBoard.SetParent(board)
        self.coordMapBoard.SetPosition(490, 40)
        self.coordMapBoard.SetSize(self.coordMapAtlasWidth + 10, self.coordMapAtlasHeight + 42)
        self.coordMapBoard.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.OnCoordinateMapClick))
        self.coordMapBoard.Hide()

        self.coordMapAtlasWindow = MobSpawnMapWindow.IndependentAtlasRenderer()
        self.coordMapAtlasWindow.SetParent(self.coordMapBoard)
        self.coordMapAtlasWindow.SetPosition(5, 5)
        self.coordMapAtlasWindow.SetSize(self.coordMapAtlasWidth, self.coordMapAtlasHeight)
        self.coordMapAtlasWindow.Hide()

        self.coordMapHoverText = ui.TextLine()
        self.coordMapHoverText.SetParent(self.coordMapBoard)
        self.coordMapHoverText.SetPosition(6, self.coordMapAtlasHeight + 9)
        self.coordMapHoverText.SetText(localeInfo.ADMINPANEL_SPAWN_MOB_SELECT_COORDS_ON_MAP)
        self.coordMapHoverText.Show()

        self.coordMapSelectedText = ui.TextLine()
        self.coordMapSelectedText.SetParent(self.coordMapBoard)
        self.coordMapSelectedText.SetPosition(6, self.coordMapAtlasHeight + 23)
        self.coordMapSelectedText.SetText(localeInfo.ADMINPANEL_SPAWN_MOB_NO_CORDS_SELECTED)
        self.coordMapSelectedText.Show()

    def __ShowEmbeddedCoordinateMap(self):
        if not self.coordMapBoard or not self.coordMapAtlasWindow:
            return
        self.isCoordMapExpanded = True
        self.destWindowWidth = float(self.animWindowWidth[1])
        self.coordMapBoard.Show()
        self.coordMapAtlasWindow.ShowIndependentAtlas()
        self.coordMapAtlasWindow.Show()

    def __HideEmbeddedCoordinateMap(self):
        self.isCoordMapExpanded = False
        self.destWindowWidth = float(self.animWindowWidth[0])
        if self.coordMapAtlasWindow:
            self.coordMapAtlasWindow.HideIndependentAtlas()
            self.coordMapAtlasWindow.Hide()
        if self.coordMapBoard:
            self.coordMapBoard.Hide()

    def OnCoordinateMapClick(self):
        (mouseX, mouseY) = wndMgr.GetMousePosition()
        (bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID) = miniMap.GetAtlasInfo(mouseX, mouseY)

        if (bFind and iPosX != 0 and iPosY != 0) or (iPosX != 0 or iPosY != 0):
            self.SetSelectedCoordinates(iPosX, iPosY)
        else:
            if self.coordMapSelectedText:
                self.coordMapSelectedText.SetText(localeInfo.ADMINPANEL_SPAWN_MOB_INVALID_COORDS)
                self.coordMapSelectedText.SetPackedFontColor(0xFFFF0000)
            self.isCoordModeSelected = False

    def OnSelectSortMode(self, mode):
        self.sortMode = mode
        sort_names = [localeInfo.ADMINPANEL_SPAWN_MOB_SORT_VNUM, localeInfo.ADMINPANEL_SPAWN_MOB_SORT_NAME, localeInfo.ADMINPANEL_SPAWN_MOB_SORT_TYPE]
        self.selectSortMode.SetCurrentItem(sort_names[mode])
        self.SortMobList()
        self.LoadCurrentPage()

    def GetMobRaceFlag(self, vnum):
        try:
            if hasattr(nonplayer, 'GetMonsterRaceFlag'):
                race_flag = nonplayer.GetMonsterRaceFlag(vnum)
                # Map race flag bits to names
                if race_flag & (1 << 0):
                    return localeInfo.ADMINPANEL_SPAWN_MOB_RACE_ANIMAL
                elif race_flag & (1 << 1):
                    return localeInfo.ADMINPANEL_SPAWN_MOB_RACE_UNDEAD
                elif race_flag & (1 << 2):
                    return localeInfo.ADMINPANEL_SPAWN_MOB_RACE_DEVIL
                elif race_flag & (1 << 3):
                    return localeInfo.ADMINPANEL_SPAWN_MOB_RACE_HUMAN
                elif race_flag & (1 << 4):
                    return localeInfo.ADMINPANEL_SPAWN_MOB_RACE_ORC
                elif race_flag & (1 << 5):
                    return localeInfo.ADMINPANEL_SPAWN_MOB_RACE_MILGYO
                elif race_flag & (1 << 6):
                    return localeInfo.ADMINPANEL_SPAWN_MOB_RACE_INSECT
                elif race_flag & (1 << 7):
                    return localeInfo.ADMINPANEL_SPAWN_MOB_RACE_FIRE
                elif race_flag & (1 << 8):
                    return localeInfo.ADMINPANEL_SPAWN_MOB_RACE_ICE
                elif race_flag & (1 << 9):
                    return localeInfo.ADMINPANEL_SPAWN_MOB_RACE_DESERT
                elif race_flag & (1 << 10):
                    return localeInfo.ADMINPANEL_SPAWN_MOB_RACE_TREE
                else:
                    return localeInfo.ADMINPANEL_SPAWN_MOB_RACE_OTHER
            else:
                return localeInfo.ADMINPANEL_SPAWN_MOB_RACE_UNKNOWN
        except Exception as e:
            return localeInfo.ADMINPANEL_SPAWN_MOB_RACE_ERROR

    def SortMobList(self):
        if not self.mobList:
            self.totalPages = 0
            self.currentPage = 0
            self.UpdatePageInfo()
            return

        if self.sortMode == 0:  # Sort by vnum
            self.mobList.sort()
        elif self.sortMode == 1:  # Sort by name
            mob_name_pairs = []
            for vnum in self.mobList:
                try:
                    name = nonplayer.GetMonsterName(vnum)
                    if name and name != "":
                        mob_name_pairs.append((name.lower(), vnum))
                    else:
                        mob_name_pairs.append((localeInfo.ADMINPANEL_SPAWN_MOB_UNNAMED, vnum))
                except:
                    mob_name_pairs.append((localeInfo.ADMINPANEL_SPAWN_MOB_NAME_ERROR, vnum))
            mob_name_pairs.sort(key=lambda x: x[0])
            self.mobList = [pair[1] for pair in mob_name_pairs]
        elif self.sortMode == 2:  # Sort by race flag
            mob_race_pairs = []
            race_priority = {
                localeInfo.ADMINPANEL_SPAWN_MOB_RACE_ANIMAL: 1,
                localeInfo.ADMINPANEL_SPAWN_MOB_RACE_UNDEAD: 2,
                localeInfo.ADMINPANEL_SPAWN_MOB_RACE_DEVIL: 3,
                localeInfo.ADMINPANEL_SPAWN_MOB_RACE_HUMAN: 4,
                localeInfo.ADMINPANEL_SPAWN_MOB_RACE_ORC: 5,
                localeInfo.ADMINPANEL_SPAWN_MOB_RACE_MILGYO: 6,
                localeInfo.ADMINPANEL_SPAWN_MOB_RACE_INSECT: 7,
                localeInfo.ADMINPANEL_SPAWN_MOB_RACE_FIRE: 8,
                localeInfo.ADMINPANEL_SPAWN_MOB_RACE_ICE: 9,
                localeInfo.ADMINPANEL_SPAWN_MOB_RACE_DESERT: 10,
                localeInfo.ADMINPANEL_SPAWN_MOB_RACE_TREE: 11,
                localeInfo.ADMINPANEL_SPAWN_MOB_RACE_OTHER: 98,
                localeInfo.ADMINPANEL_SPAWN_MOB_RACE_UNKNOWN: 99,
                localeInfo.ADMINPANEL_SPAWN_MOB_RACE_ERROR: 100
            }
            for vnum in self.mobList:
                race_name = self.GetMobRaceFlag(vnum)
                priority = race_priority.get(race_name, 99)
                mob_race_pairs.append((priority, race_name, vnum))
            mob_race_pairs.sort(key=lambda x: (x[0], x[2]))
            self.mobList = [pair[2] for pair in mob_race_pairs]

        self.totalPages = (len(self.mobList) + self.MOBS_PER_PAGE - 1) // self.MOBS_PER_PAGE
        self.currentPage = 0
        self.UpdatePageInfo()

    def OnResetMob(self):
        self.selectedMobVnum = 0
        self.GetChild("editline_set_count").SetText("1")
        self.spawnMode = 1
        self.spawnModeRadioButtonGroup.OnClick(1)
        self.selectSortMode.SetCurrentItem(localeInfo.ADMINPANEL_SPAWN_MOB_SORT_VNUM)
        self.sortMode = 0

        # RESET COORDINATE SELECTION
        self.selectedSpawnX = 0
        self.selectedSpawnY = 0
        self.isCoordModeSelected = False
        self.__HideEmbeddedCoordinateMap()
        if self.coordMapSelectedText:
            self.coordMapSelectedText.SetText(localeInfo.ADMINPANEL_SPAWN_MOB_NO_CORDS_SELECTED)
            self.coordMapSelectedText.SetPackedFontColor(0xFFFFFFFF)

        #self.__ModelPreviewClose()

        # Reset button text
        try:
            self.GetChild("coord_select_btn").SetText("")
        except:
            pass

        self.SortMobList()
        self.LoadCurrentPage()
        for overlay in self.configOverlays:
            overlay.Show()

    def OnSpawnMob(self):
        # Get mob vnum
        mob_vnum = self.selectedMobVnum
        if mob_vnum <= 0:
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMINPANEL_SPAWN_MOB_NO_MOB_SELECTED)
            return

        # Get count
        try:
            count_text = self.GetChild("editline_set_count").GetText()
            count = int(count_text) if count_text else 1
            if count <= 0:
                count = 1
        except ValueError:
            count = 1
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMINPANEL_SPAWN_MOB_INVALID_COUNT)

        # Coordinate validation
        if self.spawnMode == 0 and self.isCoordModeSelected:
            if self.selectedSpawnX <= 0 or self.selectedSpawnY <= 0:
                chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMINPANEL_SPAWN_MOB_INVALID_COORDS)
                return
            else:
                chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMINPANEL_SPAWN_MOB_COORDS_OK)

        # BUILD COMMAND BASED ON MODE (existing server commands only)
        if self.spawnMode == 0 and self.isCoordModeSelected:
            cmd_string = "/m %d %d %d %d" % (mob_vnum, count, self.selectedSpawnX, self.selectedSpawnY)
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMINPANEL_SPAWN_MOB_COORD_CMD % cmd_string)
            net.SendChatPacket(cmd_string)
        elif self.spawnMode == 0:
            # Point mode without selected coordinates behaves like regular /mob around player.
            cmd_string = "/mob %d %d" % (mob_vnum, count)
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMINPANEL_SPAWN_MOB_POINT_CMD % cmd_string)
            net.SendChatPacket(cmd_string)
        elif self.spawnMode == 1:
            # Random mode around player also uses /mob.
            cmd_string = "/mob %d %d" % (mob_vnum, count)
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMINPANEL_SPAWN_MOB_RANDOM_CMD % cmd_string)
            net.SendChatPacket(cmd_string)
        elif self.spawnMode == 2:
            # /mob_map has no count argument, so send it multiple times.
            cmd_string = "/mob_map %d" % mob_vnum
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMINPANEL_SPAWN_MOB_MAP_CMD % cmd_string)
            for _ in range(count):
                net.SendChatPacket(cmd_string)

        # Success message
        try:
            mob_name = nonplayer.GetMonsterName(mob_vnum)
            if self.spawnMode == 0 and self.isCoordModeSelected:
                chat.AppendChat(chat.CHAT_TYPE_INFO,
                                localeInfo.ADMINPANEL_SPAWN_MOB_SUCCESS_COORDS % (count, mob_name, self.selectedSpawnX, self.selectedSpawnY))
            else:
                mode_names = [localeInfo.ADMINPANEL_SPAWN_MOB_MODE_POINT, localeInfo.ADMINPANEL_SPAWN_MOB_MODE_RANDOM, localeInfo.ADMINPANEL_SPAWN_MOB_MODE_MAP]
                chat.AppendChat(chat.CHAT_TYPE_INFO,
                                localeInfo.ADMINPANEL_SPAWN_MOB_SUCCESS_MODE % (count, mob_name, mode_names[self.spawnMode]))
        except Exception as e:
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMINPANEL_SPAWN_MOB_CMD_SENT)

    def _NormalizeMobList(self, mob_list):
        normalized = []
        for vnum in mob_list:
            if isinstance(vnum, _INTEGER_TYPES):
                if vnum > 0:
                    normalized.append(vnum)
                continue

            try:
                parsed = int(vnum)
            except:
                continue

            if parsed > 0:
                normalized.append(parsed)

        return normalized

    def _FinalizeMobLoad(self):
        self.isMoblistLoading = False
        self.scanMobsFallback = False
        self.deferMobLoad = False
        self.mobCurCount = 0
        self.mobDestCount = len(self.mobList) if self.mobList else 0
        self.SortMobList()
        self.LoadCurrentPage()
        self.isMoblistLoaded = True

    def _StartFallbackMobScan(self):
        self.mobList = []
        self.mobCurCount = 0
        self.mobDestCount = self.scanMaxVnum
        self.totalPages = 0
        self.currentPage = 0
        self.isPageLoaded = False
        self.scanCurrentVnum = 1
        self.scanEmptyStreak = 0
        self.scanMobsFallback = True
        self.isMoblistLoading = True
        self.isMoblistLoaded = False
        self.deferMobLoad = False
        self.UpdatePageInfo()

    def _UpdateFallbackMobScan(self):
        if not self.scanMobsFallback:
            return

        step = self.lazyMobsPerFrame
        loaded = 0

        while loaded < step and self.scanCurrentVnum <= self.scanMaxVnum:
            vnum = self.scanCurrentVnum
            self.scanCurrentVnum += 1
            loaded += 1

            try:
                mob_name = nonplayer.GetMonsterName(vnum)
            except:
                mob_name = ""

            if mob_name and len(mob_name) > 1:
                self.mobList.append(vnum)
                self.scanEmptyStreak = 0
            else:
                self.scanEmptyStreak += 1

            if self.scanCurrentVnum > self.scanMinStopVnum and self.scanEmptyStreak >= self.scanEmptyStopThreshold:
                self.scanCurrentVnum = self.scanMaxVnum + 1
                break

        self.mobCurCount = min(self.scanCurrentVnum, self.scanMaxVnum) - 1

        if self.scanCurrentVnum > self.scanMaxVnum:
            global _ADMINPANEL_MOB_VNUM_CACHE
            _ADMINPANEL_MOB_VNUM_CACHE = list(self.mobList)
            self._FinalizeMobLoad()
            return

        if self.mobCurCount % 2000 < step:
            self.UpdatePageInfo()

    def LoadMobList(self):
        global _ADMINPANEL_MOB_VNUM_CACHE

        if self.isMoblistLoading:
            return

        if _ADMINPANEL_MOB_VNUM_CACHE:
            self.mobList = list(_ADMINPANEL_MOB_VNUM_CACHE)
            self._FinalizeMobLoad()
            return

        self.deferMobLoad = False
        self.isMoblistLoading = True
        self.isMoblistLoaded = False

        try:
            if hasattr(nonplayer, "AdminPanelGetMobList"):
                mob_list = nonplayer.AdminPanelGetMobList()
                normalized = self._NormalizeMobList(mob_list)
                if normalized:
                    self.mobList = normalized
                    _ADMINPANEL_MOB_VNUM_CACHE = list(normalized)
                    self._FinalizeMobLoad()
                    return
                dbg.TraceError("SpawnMobWindow: AdminPanelGetMobList returned empty list, switching to fallback scan.")
            else:
                dbg.TraceError("SpawnMobWindow: nonplayer.AdminPanelGetMobList is not available, switching to fallback scan.")
        except Exception as e:
            dbg.TraceError("SpawnMobWindow: AdminPanelGetMobList failed: %s" % str(e))

        self.isMoblistLoading = False
        self._StartFallbackMobScan()

    def LoadCurrentPage(self):
        """Load mobs from current page"""
        self.listBoxSearch.ClearItem()
        if not self.mobList:
            return

        start_idx = self.currentPage * self.MOBS_PER_PAGE
        end_idx = min(start_idx + self.MOBS_PER_PAGE, len(self.mobList))

        for i in range(start_idx, end_idx):
            mobvnum = self.mobList[i]
            if mobvnum <= 0 or mobvnum > 99999:
                continue
            try:
                mob_name = nonplayer.GetMonsterName(mobvnum)
                if mob_name and mob_name != "" and len(mob_name) > 1:
                    self.listBoxSearch.InsertItem(mobvnum, "%s (%d)" % (mob_name, mobvnum))
            except:
                continue

        self.isPageLoaded = True
        self.UpdatePageInfo()

    def UpdatePageInfo(self):
        """Update page information"""
        if self.pageInfoText:
            if self.isMoblistLoading:
                progress = int((float(self.mobCurCount) / float(max(1, self.mobDestCount))) * 100.0)
                if progress > 99:
                    progress = 99
                page_text = "Loading... %d%%" % progress
            else:
                page_text = "%d/%d" % (self.currentPage + 1, max(1, self.totalPages))
            self.pageInfoText.SetText(page_text)

        try:
            if self.isMoblistLoading:
                self.GetChild("prev_page_btn").Disable()
                self.GetChild("next_page_btn").Disable()
                return

            if self.currentPage <= 0:
                self.GetChild("prev_page_btn").Disable()
            else:
                self.GetChild("prev_page_btn").Enable()

            if self.currentPage >= self.totalPages - 1:
                self.GetChild("next_page_btn").Disable()
            else:
                self.GetChild("next_page_btn").Enable()
        except:
            pass

    def NextPage(self):
        if self.currentPage < self.totalPages - 1:
            self.currentPage += 1
            self.LoadCurrentPage()

    def PrevPage(self):
        if self.currentPage > 0:
            self.currentPage -= 1
            self.LoadCurrentPage()

    def OnSelectMob(self, vnum, text):
        self.configOverlays[0].Hide()
        self.configOverlays[1].Hide()
        self.GetChild("editline_set_count").SetText("1")
        self.selectedMobVnum = vnum

        self.GetChild("editline_set_count").SetText("1")
        self.GetChild("editline_set_count").SetFocus()
        self.GetChild("editline_set_count").SetEndPosition()

        #self.__ModelPreviewShow()

    def OnRunMouseWheel(self, nLen):
        if nLen > 0:
            self.listBoxSearch.scrollBar.OnUp()
        else:
            self.listBoxSearch.scrollBar.OnDown()

    """def __ModelPreviewShow(self):
        if self.selectedMobVnum == 0:
            return

        if constInfo.DISABLE_MODEL_PREVIEW == 1:
            return

        RENDER_TARGET_INDEX = 1  # POPRAWIONE na 1

        try:
            renderTarget.SetVisibility(RENDER_TARGET_INDEX, False)

            self.ModelPreviewBoard = self.GetChild("model_preview_background")
            self.ModelPreviewBoard.Show()

            self.ModelPreview = ui.RenderTarget()
            self.ModelPreview.SetParent(self.ModelPreviewBoard)
            self.ModelPreview.SetSize(230, 270)
            self.ModelPreview.SetPosition(10, 10)
            self.ModelPreview.SetRenderTarget(RENDER_TARGET_INDEX)
            self.ModelPreview.Show()

            renderTarget.SetBackground(RENDER_TARGET_INDEX, "d:/ymir work/ui/game/myshop_deco/render_bg.png")
            renderTarget.SetVisibility(RENDER_TARGET_INDEX, True)
            renderTarget.SelectModel(RENDER_TARGET_INDEX, self.selectedMobVnum)

            self.isRenderTargetActive = True

        except Exception as e:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "Błąd 3D preview: %s" % str(e))

    def __ModelPreviewClose(self):
        RENDER_TARGET_INDEX = 1

        try:
            if self.isRenderTargetActive:
                renderTarget.SetVisibility(RENDER_TARGET_INDEX, False)
                self.isRenderTargetActive = False

            if self.ModelPreviewBoard:
                self.ModelPreviewBoard.Hide()
                self.ModelPreviewBoard = None

            if self.ModelPreview:
                self.ModelPreview.Hide()
                self.ModelPreview = None

        except Exception as e:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "Błąd zamykania 3D preview: %s" % str(e))"""

    def OnMoveUp(self):
        renderTarget.MoveCamera(1, 1)

    def OnMoveDown(self):
        renderTarget.MoveCamera(1, -1)

    def OnRotateLeft(self):
        renderTarget.RotateCamera(1, -1)

    def OnRotateRight(self):
        renderTarget.RotateCamera(1, 1)

    def OnResetView(self):
        renderTarget.ResetCamera(1)

    def OnZoomIn(self):
        renderTarget.Zoom(1, -1)

    def OnZoomOut(self):
        renderTarget.Zoom(1, 1)

    def OnChangeMotion(self):
        renderTarget.ChangeMotion(1)

    def OnUpdate(self):
        if self.deferMobLoad:
            self.LoadMobList()

        if self.isMoblistLoading and self.scanMobsFallback:
            self._UpdateFallbackMobScan()


        if self.GetChild("editline_set_count").GetText() != "":
            try:
                count = int(self.GetChild("editline_set_count").GetText())
                max_count = 20
                if count > max_count:
                    self.GetChild("editline_set_count").SetText(str(max_count))
            except:
                pass

        if self.destWindowWidth != self.curWindowWidth:
            self.curWindowWidth += (self.destWindowWidth - self.curWindowWidth) / 3.0
            if abs(self.curWindowWidth - self.destWindowWidth) < 0.003:
                self.curWindowWidth = self.destWindowWidth
            self.GetChild("board").SetSize(int(self.curWindowWidth), 510)
            self.SetSize(int(self.curWindowWidth), 510)

        if self.isCoordMapExpanded and self.coordMapHoverText:
            (mouseX, mouseY) = wndMgr.GetMousePosition()
            try:
                (bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID) = miniMap.GetAtlasInfo(mouseX, mouseY)
                if bFind and (iPosX != 0 or iPosY != 0):
                    if sName and sName != "":
                        self.coordMapHoverText.SetText("%s (%d, %d)" % (sName, iPosX, iPosY))
                    else:
                        self.coordMapHoverText.SetText("(%d, %d)" % (iPosX, iPosY))
                else:
                    self.coordMapHoverText.SetText(localeInfo.ADMINPANEL_SPAWN_MOB_SELECT_COORDS_ON_MAP)
            except:
                self.coordMapHoverText.SetText(localeInfo.ADMINPANEL_SPAWN_MOB_SELECT_COORDS_ON_MAP)

    def OnPressEscapeKey(self):
        self.Close()
        return True

class ListBoxSearch(ui.ListBox):
    SEARCH_UPDATE_TIME = 0.1

    def __init__(self):
        ui.ListBox.__init__(self)
        self.visibleDict = {}
        self.textDictLower = {}
        self.lastSearchText = ""
        self.lastSearchTime = 0
        self.minSearchTextLen = 3
        self.realSelectedLine = -1
        self.editLine = None
        self.scrollBar = ui.ScrollBar()
        self.scrollBar.SetParent(self)
        self.scrollBar.SetScrollEvent(self.__OnScroll)
        self.scrollBar.SetScrollStep(0.01)
        self.scrollBar.Hide()

    def SetMinSearchTextLen(self, minSearchTextLen):
        self.minSearchTextLen = minSearchTextLen

    def SetEditLine(self, editLine):
        self.editLine = editLine

    def SetSize(self, width, height):
        ui.ListBox.SetSize(self, width - ui.ScrollBar.SCROLLBAR_WIDTH, height)
        ui.Window.SetSize(self, width, height)
        self.scrollBar.SetPosition(width - ui.ScrollBar.SCROLLBAR_WIDTH, 0)
        self.scrollBar.SetScrollBarSize(height)

    def ClearItem(self):
        ui.ListBox.ClearItem(self)
        self.visibleDict = {}
        self.textDictLower = {}
        self.lastSearchText = ""
        self.lastSearchTime = 0
        self.realSelectedLine = -1
        self.scrollBar.SetPos(0)

    def SelectItem(self, line):
        lineDict = []
        for key in range(len(self.itemList)):
            if not self.visibleDict[key]:
                continue
            lineDict.append(key)

        if line >= len(lineDict):
            return

        realLine = lineDict[line]
        if realLine not in self.keyDict:
            return
        if line == self.selectedLine:
            return

        self.selectedLine = line
        self.realSelectedLine = realLine
        self.event(self.keyDict.get(realLine, 0), self.textDict.get(realLine, "None"))

    def GetSelectedItem(self):
        return self.keyDict.get(self.realSelectedLine, 0)

    def InsertItem(self, number, text, doLocate=True):
        self.keyDict[len(self.itemList)] = number
        self.textDict[len(self.itemList)] = text
        self.textDictLower[len(self.itemList)] = text.lower()
        self.visibleDict[len(self.itemList)] = True

        textLine = ui.TextLine()
        textLine.SetParent(self)
        textLine.SetText(text)
        textLine.Show()

        if self.itemCenterAlign:
            textLine.SetWindowHorizontalAlignCenter()
            textLine.SetHorizontalAlignCenter()

        self.itemList.append(textLine)
        if doLocate:
            self._LocateItem()

    def LocateItem(self):
        self._LocateItem()

    def _LocateItem(self):
        self.selectedLine = -1
        self.realSelectedLine = -1
        skipCount = self.basePos
        yPos = 0
        self.showLineCount = 0

        for key, value in list(self.keyDict.items()):
            textLine = self.itemList[key]
            textLine.Hide()

            if not self.visibleDict[key]:
                continue

            if skipCount > 0:
                skipCount -= 1
                continue

            textLine.SetPosition(0, yPos + 3)
            yPos += self.stepSize

            if yPos <= self.GetHeight():
                self.showLineCount += 1
                textLine.Show()

        if self.showLineCount < self.GetItemCount():
            self.scrollBar.SetMiddleBarSize(float(self.GetViewItemCount()) / self.GetItemCount())
            self.scrollBar.Show()
        else:
            self.scrollBar.Hide()

    def __OnScroll(self):
        scrollLen = self.GetItemCount() - self.GetViewItemCount()
        if scrollLen < 0:
            scrollLen = 0
        self.SetBasePos(int(self.scrollBar.GetPos() * scrollLen))

    def GetItemCount(self):
        return sum(1 for key, value in list(self.keyDict.items()) if self.visibleDict[key])

    def ReSearchItems(self):
        self._SearchItems(self.editLine.GetText())

    def _SearchItems(self, text):
        if len(text) < self.minSearchTextLen and len(text) != 0:
            return

        text = text.lower()
        for key, value in list(self.keyDict.items()):
            textLineText = self.textDictLower[key]
            self.visibleDict[key] = False
            if textLineText.find(text) != -1:
                self.visibleDict[key] = True

        self.scrollBar.SetPos(0)
        self.SetBasePos(0)

    def OnUpdate(self):
        self.overLine = -1
        if self.scrollBar.IsShow():
            min_number = 1.00 / float(self.GetItemCount()) * 5
            if min_number < 0.005:
                min_number = 0.005
            self.scrollBar.SetScrollStep(min_number)

        if self.IsIn():
            x, y = self.GetGlobalPosition()
            height = self.GetHeight()
            xMouse, yMouse = wndMgr.GetMousePosition()

            if yMouse - y < height - 1:
                self.overLine = (yMouse - y) // self.stepSize
                if self.overLine < 0:
                    self.overLine = -1
                if self.overLine >= self.GetItemCount():
                    self.overLine = -1

        if self.lastSearchTime < _now():
            searchText = self.editLine.GetText() if self.editLine else ""
            if self.lastSearchText != searchText:
                self.lastSearchText = searchText
                self._SearchItems(searchText)
            self.lastSearchTime = _now() + self.SEARCH_UPDATE_TIME
