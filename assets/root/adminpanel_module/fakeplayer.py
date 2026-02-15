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
import time
import item
import dbg
import uiToolTip
import uicommon

try:
    _now = time.perf_counter
except AttributeError:
    _now = time.time

IMG_PATH = "d:/ymir work/ui/adminpanel/create_item/"

NORMAL_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
ACTIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)
INACTIVE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)

RACE_NAMES = ["Warrior M", "Ninja F", "Sura M", "Shaman F", "Warrior F", "Ninja M", "Sura F", "Shaman M"]
EMPIRE_NAMES = ["None", "Shinsoo", "Chunjo", "Jinno"]

WEAR_POSITIONS = {
    0: "Body", 1: "Head", 2: "Shoes", 3: "Wristlet",
    4: "Weapon", 5: "Neck", 6: "Ear", 7: "Unique1",
    8: "Unique2", 9: "Arrow", 10: "Shield", 19: "Costume Body",
    20: "Costume Hair", 21: "Costume Mount", 22: "Costume Acce",
    23: "Costume Weapon", 24: "Costume Wing", 25: "Costume Pet"
}

# Slot to item type/subtype mapping for filtering
# Format: slot_position: (item_type, item_subtype or None)
SLOT_TYPE_FILTER = {
    # Equipment slots
    0: (item.ITEM_TYPE_ARMOR, item.ARMOR_BODY),       # Body armor
    1: (item.ITEM_TYPE_ARMOR, item.ARMOR_HEAD),       # Head/Helmet
    2: (item.ITEM_TYPE_ARMOR, item.ARMOR_FOOTS),      # Shoes
    3: (item.ITEM_TYPE_ARMOR, item.ARMOR_WRIST),      # Wristlet
    4: (item.ITEM_TYPE_WEAPON, None),                 # Weapon (any subtype)
    5: (item.ITEM_TYPE_ARMOR, item.ARMOR_NECK),       # Necklace
    6: (item.ITEM_TYPE_ARMOR, item.ARMOR_EAR),        # Earrings
    7: None,                                           # Unique1 - no filtering
    8: None,                                           # Unique2 - no filtering
    9: None,                                           # Arrow - no filtering
    10: (item.ITEM_TYPE_ARMOR, item.ARMOR_SHIELD),    # Shield

    # Costume slots - all require ITEM_TYPE_COSTUME
    19: (item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_BODY),   # Costume Body
    20: (item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_HAIR),   # Costume Hair
    21: (item.ITEM_TYPE_COSTUME, None),               # Costume Mount
    22: (item.ITEM_TYPE_COSTUME, None),               # Costume Acce
    23: (item.ITEM_TYPE_COSTUME, None),               # Costume Weapon
    24: (item.ITEM_TYPE_COSTUME, None),               # Costume Wing
    25: (item.ITEM_TYPE_COSTUME, None),               # Costume Pet
}


class MassLoginController:
    def __init__(self):
        self.loginQueue = []
        self.isRunning = False
        self.loginInterval = 1.0
        self.lastLoginTime = 0
        self.currentIndex = 0
        self.onProgressCallback = None
        self.onCompleteCallback = None

    def StartMassLogin(self, nameList, interval):
        self.loginQueue = list(nameList)
        self.loginInterval = max(0.5, float(interval))
        self.currentIndex = 0
        self.isRunning = True
        self.lastLoginTime = 0

    def StopMassLogin(self):
        self.isRunning = False
        self.loginQueue = []
        self.currentIndex = 0

    def SetProgressCallback(self, callback):
        self.onProgressCallback = callback

    def SetCompleteCallback(self, callback):
        self.onCompleteCallback = callback

    def OnUpdate(self):
        if not self.isRunning:
            return

        currentTime = app.GetTime()
        if currentTime - self.lastLoginTime >= self.loginInterval:
            if self.currentIndex < len(self.loginQueue):
                name = self.loginQueue[self.currentIndex]
                net.SendChatPacket("/adminpanel_fakeplayer_login %s" % name)
                self.lastLoginTime = currentTime
                self.currentIndex += 1

                if self.onProgressCallback:
                    self.onProgressCallback(self.currentIndex, len(self.loginQueue), name)
            else:
                self.isRunning = False
                if self.onCompleteCallback:
                    self.onCompleteCallback(len(self.loginQueue))

    def GetProgress(self):
        if len(self.loginQueue) == 0:
            return 0.0
        return float(self.currentIndex) / float(len(self.loginQueue))

    def IsRunning(self):
        return self.isRunning


class MainWindow(ui.ScriptWindow):
    def __init__(self):
        self.selectedFakePlayer = None
        self.fakePlayerList = []
        self.fakePlayerData = {}
        self.fakeListPending = []
        self.fakeListCur = 0
        self.fakeListTarget = 0
        self.fakeListLoading = False
        self.fakeListPendingReady = False
        self.fakeListPerFrame = 25
        self.activeList = []
        self.itemData = {}

        self.massLoginController = MassLoginController()
        self.massLoginController.SetProgressCallback(ui.__mem_func__(self.OnMassLoginProgress))
        self.massLoginController.SetCompleteCallback(ui.__mem_func__(self.OnMassLoginComplete))

        self.createDialog = None
        self.itemSelectWindow = None
        self.deleteAllDialog = None

        ui.ScriptWindow.__init__(self)
        self.__LoadWindow()

    def __del__(self):
        self.selectedFakePlayer = None
        self.fakePlayerList = []
        self.fakePlayerData = {}
        self.activeList = []
        self.itemData = {}
        ui.ScriptWindow.__del__(self)

    def Show(self):
        self.RefreshData()
        ui.ScriptWindow.Show(self)

    def Close(self):
        self.Hide()

    def Destroy(self):
        self.Hide()
        self.ClearDictionary()
        if self.deleteAllDialog:
            self.deleteAllDialog.Close()
            self.deleteAllDialog = None

    def __LoadWindow(self):
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "adminpanel_module/uiscript/fakeplayer.py")
        except:
            import exception
            exception.Abort("FakePlayerWindow.LoadWindow.LoadObject")

        try:
            board = self.GetChild("board")
            if hasattr(board, "CloseButtonHide"):
                board.CloseButtonHide()
            elif hasattr(board, "titleBar"):
                title_bar = board.titleBar
                if hasattr(title_bar, "CloseButtonHide"):
                    title_bar.CloseButtonHide()
                elif hasattr(title_bar, "btnClose"):
                    title_bar.btnClose.Hide()

            # Create the list box for fake players
            self.listBoxSearch = ListBoxSearch()
            self.listBoxSearch.SetParent(self.GetChild("list_background"))
            self.listBoxSearch.SetPosition(4, 4)
            self.listBoxSearch.SetSize(200 - 8, 17 * 19)
            self.listBoxSearch.SetEvent(ui.__mem_func__(self.OnSelectFakePlayer))
            self.listBoxSearch.SetMinSearchTextLen(1)
            self.listBoxSearch.SetEditLine(self.GetChild("list_search_editline"))
            self.listBoxSearch.Show()

            # Create race combo box
            self.raceComboBox = ui.ComboBoxEx()
            self.raceComboBox.SetParent(self.GetChild("details_board"))
            self.raceComboBox.AddFlag('float')
            self.raceComboBox.SetPosition(80, 52)
            self.raceComboBox.SetSize(100, 20)
            for i, name in enumerate(RACE_NAMES):
                self.raceComboBox.InsertItem(i, name)
            self.raceComboBox.SetCurrentItem(RACE_NAMES[0])
            self.raceComboBox.Show()

            # Create empire combo box
            self.empireComboBox = ui.ComboBoxEx()
            self.empireComboBox.SetParent(self.GetChild("details_board"))
            self.empireComboBox.AddFlag('float')
            self.empireComboBox.SetPosition(200, 77)
            self.empireComboBox.SetSize(60, 20)
            for i, name in enumerate(EMPIRE_NAMES):
                self.empireComboBox.InsertItem(i, name)
            self.empireComboBox.SetCurrentItem(EMPIRE_NAMES[1])
            self.empireComboBox.Show()

            # Button events
            self.GetChild("btn_refresh").SetEvent(ui.__mem_func__(self.OnClickRefresh))
            self.GetChild("btn_create_new").SetEvent(ui.__mem_func__(self.OnClickCreateNew))
            self.GetChild("btn_save").SetEvent(ui.__mem_func__(self.OnClickSave))
            self.GetChild("btn_delete").SetEvent(ui.__mem_func__(self.OnClickDelete))
            self.GetChild("btn_delete_all").SetEvent(ui.__mem_func__(self.OnClickDeleteAll))
            self.GetChild("btn_login").SetEvent(ui.__mem_func__(self.OnClickLogin))
            self.GetChild("btn_logout").SetEvent(ui.__mem_func__(self.OnClickLogout))
            self.GetChild("btn_login_all").SetEvent(ui.__mem_func__(self.OnClickLoginAll))
            self.GetChild("btn_logout_all").SetEvent(ui.__mem_func__(self.OnClickLogoutAll))
            self.GetChild("btn_stop_mass").SetEvent(ui.__mem_func__(self.OnClickStopMassLogin))
            self.GetChild("btn_create_new_random_one").SetEvent(ui.__mem_func__(self.OnClickCreateRandomOne))
            self.GetChild("btn_create_new_random_multi").SetEvent(ui.__mem_func__(self.OnClickCreateRandomMulti))
            self.editFakePlayersNumber = self.GetChild("edit_fake_players_number")

            # Set default interval
            self.GetChild("edit_interval").SetText("1.0")

            # Create equipment slots
            self.__CreateEquipmentSlots()

            # Create item tooltip
            self.tooltipItem = uiToolTip.ItemToolTip()
            self.tooltipItem.Hide()

            # Initialize progress gauge
            self.progressGauge = self.GetChild("progress_gauge")
            self.progressGauge.MakeGauge(200, "green")

        except:
            import exception
            exception.Abort("FakePlayerWindow.LoadWindow.BindObject")

    def __CreateEquipmentSlots(self):
        self.equipSlots = {}
        self.equipItemData = {}

        # Get equipment slot widgets
        self.wndEquip = self.GetChild("EquipmentSlot")
        self.wndCostume = self.GetChild("CostumeSlot")

        # Equipment slot events
        self.wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptyEquipSlot))
        self.wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.OnSelectEquipSlot))
        self.wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.OnUnselectEquipSlot))
        self.wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OnOverEquipSlot))
        self.wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutEquipSlot))

        # Costume slot events
        self.wndCostume.SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptyEquipSlot))
        self.wndCostume.SetSelectItemSlotEvent(ui.__mem_func__(self.OnSelectEquipSlot))
        self.wndCostume.SetUnselectItemSlotEvent(ui.__mem_func__(self.OnUnselectEquipSlot))
        self.wndCostume.SetOverInItemEvent(ui.__mem_func__(self.OnOverEquipSlot))
        self.wndCostume.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutEquipSlot))

        # Slot positions - equipment: 0-11, costume: 19-23
        # Slot 11 = Belt in UI (maps to wear position 11)
        slotPositions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 19, 20, 21, 22, 23]

        for pos in slotPositions:
            self.equipSlots[pos] = {"vnum": 0, "sockets": [0, 0, 0], "attrs": [[0, 0] for _ in range(7)]}

    def RefreshData(self):
        net.SendChatPacket("/adminpanel_fakeplayer_list")
        net.SendChatPacket("/adminpanel_fakeplayer_active")

    def OnClickRefresh(self):
        self.RefreshData()

    def OnClickCreateNew(self):
        if not self.createDialog:
            self.createDialog = CreateFakePlayerDialog()
            self.createDialog.SetParent(self)

        self.createDialog.Show()

    def OnSelectFakePlayer(self, name, text):
        self.selectedFakePlayer = name
        net.SendChatPacket("/adminpanel_fakeplayer_get %s" % name)
        net.SendChatPacket("/adminpanel_fakeplayer_item_list %s" % name)

    def OnClickSave(self):
        if not self.selectedFakePlayer:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "No fake player selected.")
            return

        # Get values from UI
        level = self.GetChild("edit_level").GetText()
        st = self.GetChild("edit_st").GetText()
        ht = self.GetChild("edit_ht").GetText()
        dx = self.GetChild("edit_dx").GetText()
        iq = self.GetChild("edit_iq").GetText()
        alignment = self.GetChild("edit_alignment").GetText()
        guild_id = self.GetChild("edit_guild_id").GetText()
        language = self.GetChild("edit_language").GetText()

        race = self.raceComboBox.listBox.GetSelectedItem()
        empire = self.empireComboBox.listBox.GetSelectedItem()

        # Send update commands
        if level:
            net.SendChatPacket("/adminpanel_fakeplayer_update %s level %s" % (self.selectedFakePlayer, level))
        if st:
            net.SendChatPacket("/adminpanel_fakeplayer_update %s st %s" % (self.selectedFakePlayer, st))
        if ht:
            net.SendChatPacket("/adminpanel_fakeplayer_update %s ht %s" % (self.selectedFakePlayer, ht))
        if dx:
            net.SendChatPacket("/adminpanel_fakeplayer_update %s dx %s" % (self.selectedFakePlayer, dx))
        if iq:
            net.SendChatPacket("/adminpanel_fakeplayer_update %s iq %s" % (self.selectedFakePlayer, iq))
        if alignment:
            net.SendChatPacket("/adminpanel_fakeplayer_update %s alignment %s" % (self.selectedFakePlayer, alignment))
        if guild_id:
            net.SendChatPacket("/adminpanel_fakeplayer_update %s guild_id %s" % (self.selectedFakePlayer, guild_id))
        if language:
            net.SendChatPacket("/adminpanel_fakeplayer_update %s language %s" % (self.selectedFakePlayer, language))

        net.SendChatPacket("/adminpanel_fakeplayer_update %s race %d" % (self.selectedFakePlayer, race + 1))
        net.SendChatPacket("/adminpanel_fakeplayer_update %s empire %d" % (self.selectedFakePlayer, empire))

        chat.AppendChat(chat.CHAT_TYPE_INFO, "Fake player '%s' saved." % self.selectedFakePlayer)

    def OnClickDelete(self):
        if not self.selectedFakePlayer:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "No fake player selected.")
            return

        net.SendChatPacket("/adminpanel_fakeplayer_delete %s" % self.selectedFakePlayer)

    def OnClickDeleteAll(self):
        self.__OpenDeleteAllDialog()

    def __OpenDeleteAllDialog(self):
        if not self.deleteAllDialog:
            self.deleteAllDialog = uicommon.QuestionDialog()
            self.deleteAllDialog.SetText("Are you sure?")
            self.deleteAllDialog.SetAcceptEvent(ui.__mem_func__(self.__OnDeleteAllAccept))
            self.deleteAllDialog.SetCancelEvent(ui.__mem_func__(self.__OnDeleteAllCancel))
        self.deleteAllDialog.Open()

    def __OnDeleteAllAccept(self):
        if self.deleteAllDialog:
            self.deleteAllDialog.Close()
        net.SendChatPacket("/adminpanel_fakeplayer_delete_all all")

    def __OnDeleteAllCancel(self):
        if self.deleteAllDialog:
            self.deleteAllDialog.Close()

    def OnClickLogin(self):
        if not self.selectedFakePlayer:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "No fake player selected.")
            return

        net.SendChatPacket("/adminpanel_fakeplayer_login %s" % self.selectedFakePlayer)

    def OnClickLogout(self):
        if not self.selectedFakePlayer:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "No fake player selected.")
            return

        net.SendChatPacket("/adminpanel_fakeplayer_logout %s" % self.selectedFakePlayer)

    def OnClickLoginAll(self):
        try:
            interval = float(self.GetChild("edit_interval").GetText())
        except:
            interval = 1.0

        # Get list of inactive fake players
        inactiveList = [name for name in self.fakePlayerList if name not in self.activeList]

        if len(inactiveList) == 0:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "All fake players are already logged in.")
            return

        self.massLoginController.StartMassLogin(inactiveList, interval)
        self.SetMassLoginUIState(True)
        chat.AppendChat(chat.CHAT_TYPE_INFO, "Starting mass login of %d fake players..." % len(inactiveList))

    def OnClickLogoutAll(self):
        net.SendChatPacket("/adminpanel_fakeplayer_logout_all")

    def OnClickCreateRandomOne(self):
        nakedCheckbox = self.GetChild("fake_players_naked_checkbox")
        withEquipment = 0 if nakedCheckbox.IsChecked() else 1
        net.SendChatPacket("/adminpanel_fakeplayer_create_random 1 %d" % withEquipment)
        chat.AppendChat(chat.CHAT_TYPE_INFO, "Creating 1 random fake player...")

    def OnClickCreateRandomMulti(self):
        try:
            count = int(self.editFakePlayersNumber.GetText())
        except:
            count = 1

        if count < 1:
            count = 1
        elif count > 999:
            count = 999

        nakedCheckbox = self.GetChild("fake_players_naked_checkbox")
        withEquipment = 0 if nakedCheckbox.IsChecked() else 1
        net.SendChatPacket("/adminpanel_fakeplayer_create_random %d %d" % (count, withEquipment))
        chat.AppendChat(chat.CHAT_TYPE_INFO, "Creating %d random fake player(s)..." % count)

    def OnClickStopMassLogin(self):
        self.massLoginController.StopMassLogin()
        self.SetMassLoginUIState(False)
        chat.AppendChat(chat.CHAT_TYPE_INFO, "Mass login stopped.")

    def SetMassLoginUIState(self, isRunning):
        self.GetChild("btn_login_all").SetEnable(not isRunning)
        self.GetChild("btn_stop_mass").SetEnable(isRunning)

    def OnMassLoginProgress(self, current, total, name):
        self.GetChild("label_progress_text").SetText("%d/%d - %s" % (current, total, name))
        self.progressGauge.SetPercentage(current, total)

    def OnMassLoginComplete(self, count):
        self.SetMassLoginUIState(False)
        chat.AppendChat(chat.CHAT_TYPE_INFO, "Mass login completed. Logged in %d fake players." % count)
        self.RefreshData()

    def OnSelectEmptyEquipSlot(self, slotIndex):
        if not self.selectedFakePlayer:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "No fake player selected.")
            return

        # Open item select window
        if not self.itemSelectWindow:
            self.itemSelectWindow = ItemSelectWindow()
            self.itemSelectWindow.SetParent(self)
            self.itemSelectWindow.SetItemCallback(ui.__mem_func__(self.OnItemSelected))

        self.itemSelectWindow.SetWearPos(slotIndex)
        self.itemSelectWindow.Show(editMode=False, existingData=None)

    def OnSelectEquipSlot(self, slotIndex):
        # LMB on slot with item = EDIT (not remove)
        if not self.selectedFakePlayer:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "No fake player selected.")
            return

        if slotIndex in self.equipSlots and self.equipSlots[slotIndex]["vnum"] != 0:
            # Open item select window in edit mode with existing data
            if not self.itemSelectWindow:
                self.itemSelectWindow = ItemSelectWindow()
                self.itemSelectWindow.SetParent(self)
                self.itemSelectWindow.SetItemCallback(ui.__mem_func__(self.OnItemSelected))

            existingData = {
                "vnum": self.equipSlots[slotIndex]["vnum"],
                "sockets": self.equipSlots[slotIndex]["sockets"],
            }
            self.itemSelectWindow.SetWearPos(slotIndex)
            self.itemSelectWindow.Show(editMode=True, existingData=existingData)

    def OnUnselectEquipSlot(self, slotIndex):
        # RMB on slot with item = REMOVE
        if not self.selectedFakePlayer:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "No fake player selected.")
            return

        if slotIndex in self.equipSlots and self.equipSlots[slotIndex]["vnum"] != 0:
            net.SendChatPacket("/adminpanel_fakeplayer_item_remove %s %d" % (self.selectedFakePlayer, slotIndex + 1))

    def OnItemSelected(self, wearPos, vnum, sockets, attrs):
        if not self.selectedFakePlayer:
            return

        # Build command string
        cmd = "/adminpanel_fakeplayer_item_add %s %d %d" % (self.selectedFakePlayer, wearPos + 1, vnum)

        # Add sockets
        for i in range(3):
            cmd += " %d" % sockets[i]

        # Add attributes
        for i in range(7):
            cmd += " %d %d" % (attrs[i][0], attrs[i][1])

        net.SendChatPacket(cmd)

    def OnOverEquipSlot(self, slotIndex):
        if slotIndex in self.equipSlots and self.equipSlots[slotIndex]["vnum"] != 0:
            self.tooltipItem.ClearToolTip()
            self.tooltipItem.AddItemData(self.equipSlots[slotIndex]["vnum"], self.equipSlots[slotIndex].get("sockets", [0, 0, 0]))
            self.tooltipItem.ShowToolTip()

    def OnOverOutEquipSlot(self):
        if self.tooltipItem:
            self.tooltipItem.HideToolTip()

    # ---- Server Response Handlers ----

    def RecvFakePlayerList(self, count, data):
        dbg.TraceError("RecvFakePlayerList: count=%d, data_len=%d" % (count, len(data)))

        self.listBoxSearch.ClearItem()
        self.fakePlayerList = []
        self.fakePlayerData = {}
        self.fakeListPending = []
        self.fakeListCur = 0
        self.fakeListTarget = 0
        self.fakeListLoading = False

        if count == 0:
            return

        players = data.split(" ")
        for playerData in players:
            parts = playerData.split("|")
            if len(parts) >= 5:
                name = parts[0]
                race = int(parts[1])
                level = int(parts[2])
                empire = int(parts[3])
                active = int(parts[4])

                self.fakePlayerList.append(name)
                self.fakePlayerData[name] = {
                    "race": race,
                    "level": level,
                    "empire": empire,
                    "active": active
                }

                self.fakeListPending.append((name, level))

        self.fakeListTarget = len(self.fakeListPending)
        self.fakeListLoading = True
        self.__ProcessFakePlayerListBatch()

        # Update active status colors after receiving active list
        self.UpdateListColors()

    def RecvFakePlayerListBegin(self, total):
        if self.listBoxSearch:
            self.listBoxSearch.ClearItem()
        self.fakePlayerList = []
        self.fakePlayerData = {}
        self.fakeListPending = []
        self.fakeListCur = 0
        self.fakeListTarget = 0
        self.fakeListLoading = False
        self.fakeListPendingReady = False

    def RecvFakePlayerListChunk(self, count, data):
        if count <= 0:
            return

        players = data.split(" ") if data else []
        for playerData in players:
            parts = playerData.split("|")
            if len(parts) >= 5:
                name = parts[0]
                race = int(parts[1])
                level = int(parts[2])
                empire = int(parts[3])
                active = int(parts[4])

                self.fakePlayerList.append(name)
                self.fakePlayerData[name] = {
                    "race": race,
                    "level": level,
                    "empire": empire,
                    "active": active
                }

                self.fakeListPending.append((name, level))

        self.fakeListTarget = len(self.fakeListPending)
        if self.listBoxSearch:
            self.fakeListLoading = True
            self.__ProcessFakePlayerListBatch()
        else:
            self.fakeListPendingReady = True

    def RecvFakePlayerListEnd(self):
        self.UpdateListColors()

    def RecvFakePlayerActive(self, count, data):
        self.activeList = []

        if count == 0:
            self.UpdateListColors()
            return

        players = data.split(" ")
        for playerData in players:
            parts = playerData.split("|")
            if len(parts) >= 1:
                name = parts[0]
                self.activeList.append(name)

        self.UpdateListColors()

    def UpdateListColors(self):
        # Update the color in list items based on active status
        for name in self.fakePlayerList:
            if name in self.fakePlayerData:
                self.fakePlayerData[name]["active"] = 1 if name in self.activeList else 0

    def RecvFakePlayerGet(self, data):
        parts = data.split("|")
        if len(parts) < 12:
            return

        name = parts[0]
        race = int(parts[1])
        level = int(parts[2])
        empire = int(parts[3])
        st = int(parts[4])
        ht = int(parts[5])
        dx = int(parts[6])
        iq = int(parts[7])
        alignment = int(parts[8])
        guild_id = int(parts[9])
        language = parts[10]
        block_eq = int(parts[11])

        # Update UI fields
        self.GetChild("edit_name").SetText(name)
        self.GetChild("edit_level").SetText(str(level))
        self.GetChild("edit_st").SetText(str(st))
        self.GetChild("edit_ht").SetText(str(ht))
        self.GetChild("edit_dx").SetText(str(dx))
        self.GetChild("edit_iq").SetText(str(iq))
        self.GetChild("edit_alignment").SetText(str(alignment))
        self.GetChild("edit_guild_id").SetText(str(guild_id))
        self.GetChild("edit_language").SetText(language)

        # Update combo boxes
        if race > 0 and race <= len(RACE_NAMES):
            self.raceComboBox.SetCurrentItem(RACE_NAMES[race - 1])
        if empire >= 0 and empire < len(EMPIRE_NAMES):
            self.empireComboBox.SetCurrentItem(EMPIRE_NAMES[empire])

        # Update status
        isActive = name in self.activeList
        statusText = "Status: ACTIVE" if isActive else "Status: INACTIVE"
        self.GetChild("label_status").SetText(statusText)

    def RecvFakePlayerItemList(self, name, count, data):
        # Clear all equipment slots
        self.__ClearEquipmentSlots()

        if count == 0:
            return

        items = data.split(" ")
        for itemData in items:
            parts = itemData.split("|")
            if len(parts) >= 2:
                wearPos = int(parts[0]) - 1
                vnum = int(parts[1])

                if wearPos in self.equipSlots:
                    self.equipSlots[wearPos]["vnum"] = vnum

                    # Update the slot widget
                    if wearPos <= 11:
                        self.wndEquip.SetItemSlot(wearPos, vnum, 0)
                    else:
                        self.wndCostume.SetItemSlot(wearPos, vnum, 0)

        # Refresh slot display
        self.wndEquip.RefreshSlot()
        self.wndCostume.RefreshSlot()

    def __ClearEquipmentSlots(self):
        for pos in self.equipSlots:
            self.equipSlots[pos]["vnum"] = 0
            if pos <= 11:
                self.wndEquip.ClearSlot(pos)
            else:
                self.wndCostume.ClearSlot(pos)

        self.wndEquip.RefreshSlot()
        self.wndCostume.RefreshSlot()

    def RecvFakePlayerCreated(self, name):
        chat.AppendChat(chat.CHAT_TYPE_INFO, "Fake player '%s' created successfully." % name)
        self.RefreshData()

    def RecvFakePlayerDeleted(self, name):
        chat.AppendChat(chat.CHAT_TYPE_INFO, "Fake player '%s' deleted." % name)
        if self.selectedFakePlayer == name:
            self.selectedFakePlayer = None
            self.ClearDetails()
        self.RefreshData()

    def ClearDetails(self):
        self.GetChild("edit_name").SetText("")
        self.GetChild("edit_level").SetText("")
        self.GetChild("edit_st").SetText("")
        self.GetChild("edit_ht").SetText("")
        self.GetChild("edit_dx").SetText("")
        self.GetChild("edit_iq").SetText("")
        self.GetChild("edit_alignment").SetText("")
        self.GetChild("edit_guild_id").SetText("")
        self.GetChild("edit_language").SetText("")
        self.GetChild("label_status").SetText("Status: -")

        self.__ClearEquipmentSlots()

    def OnUpdate(self):
        self.massLoginController.OnUpdate()
        if self.fakeListPendingReady and self.listBoxSearch and not self.fakeListLoading:
            self.fakeListTarget = len(self.fakeListPending)
            self.fakeListLoading = True
            self.fakeListPendingReady = False
        self.__ProcessFakePlayerListBatch()

    def __ProcessFakePlayerListBatch(self):
        if not self.fakeListLoading:
            return

        step = self.fakeListPerFrame
        while step > 0 and self.fakeListCur < self.fakeListTarget:
            name, level = self.fakeListPending[self.fakeListCur]
            displayText = "%s (Lv.%d)" % (name, level)
            self.listBoxSearch.InsertItem(name, displayText)
            self.fakeListCur += 1
            step -= 1

        if self.fakeListCur >= self.fakeListTarget:
            self.fakeListLoading = False

    def OnRunMouseWheel(self, nLen):
        if self.listBoxSearch.scrollBar.IsShow():
            if nLen > 0:
                self.listBoxSearch.scrollBar.OnUp()
            else:
                self.listBoxSearch.scrollBar.OnDown()

    def OnPressEscapeKey(self):
        self.Close()
        return True


class CreateFakePlayerDialog(ui.ScriptWindow):
    def __init__(self):
        self.parent = None
        ui.ScriptWindow.__init__(self)
        self.__LoadWindow()

    def __del__(self):
        self.parent = None
        ui.ScriptWindow.__del__(self)

    def SetParent(self, parent):
        self.parent = parent

    def Show(self):
        self.SetCenterPosition()
        self.SetTop()
        ui.ScriptWindow.Show(self)

    def Close(self):
        self.Hide()

    def __LoadWindow(self):
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "adminpanel_module/uiscript/create_fakeplayer.py")
        except:
            import exception
            exception.Abort("CreateFakePlayerDialog.LoadWindow.LoadObject")

        try:
            self.board = self.GetChild("board")
            self.board.SetCloseEvent(self.Close)

            # Get edit lines from uiscript
            self.nameEditLine = self.GetChild("edit_name")
            self.levelEditLine = self.GetChild("edit_level")
            self.stEditLine = self.GetChild("edit_st")
            self.htEditLine = self.GetChild("edit_ht")
            self.dxEditLine = self.GetChild("edit_dx")
            self.iqEditLine = self.GetChild("edit_iq")
            self.languageEditLine = self.GetChild("edit_language")

            # Create race combo box (not supported in uiscript)
            self.raceComboBox = ui.ComboBoxEx()
            self.raceComboBox.SetParent(self.board)
            self.raceComboBox.AddFlag('float')
            self.raceComboBox.SetPosition(100, 67)
            self.raceComboBox.SetSize(120, 20)
            for i, name in enumerate(RACE_NAMES):
                self.raceComboBox.InsertItem(i, name)
            self.raceComboBox.SetCurrentItem(RACE_NAMES[0])
            self.raceComboBox.Show()

            # Create empire combo box
            self.empireComboBox = ui.ComboBoxEx()
            self.empireComboBox.SetParent(self.board)
            self.empireComboBox.AddFlag('float')
            self.empireComboBox.SetPosition(100, 127)
            self.empireComboBox.SetSize(80, 20)
            for i, name in enumerate(EMPIRE_NAMES[1:], 1):
                self.empireComboBox.InsertItem(i, name)
            self.empireComboBox.SetCurrentItem(EMPIRE_NAMES[1])
            self.empireComboBox.Show()

            # Button events
            self.GetChild("btn_create").SetEvent(ui.__mem_func__(self.OnClickCreate))
            self.GetChild("btn_cancel").SetEvent(ui.__mem_func__(self.Close))

        except:
            import exception
            exception.Abort("CreateFakePlayerDialog.LoadWindow.BindObject")

    def OnClickCreate(self):
        name = self.nameEditLine.GetText()
        if not name:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "Please enter a name.")
            return

        race = self.raceComboBox.listBox.GetSelectedItem() + 1
        level = int(self.levelEditLine.GetText()) if self.levelEditLine.GetText() else 1
        empire = self.empireComboBox.listBox.GetSelectedItem()
        st = int(self.stEditLine.GetText()) if self.stEditLine.GetText() else 10
        ht = int(self.htEditLine.GetText()) if self.htEditLine.GetText() else 10
        dx = int(self.dxEditLine.GetText()) if self.dxEditLine.GetText() else 10
        iq = int(self.iqEditLine.GetText()) if self.iqEditLine.GetText() else 10
        language = self.languageEditLine.GetText() if self.languageEditLine.GetText() else "en"

        cmd = "/adminpanel_fakeplayer_create %s %d %d %d %d %d %d %d 0 0 %s" % (
            name, race, level, empire, st, ht, dx, iq, language)
        net.SendChatPacket(cmd)
        self.Close()

    def OnPressEscapeKey(self):
        self.Close()
        return True


_ADMINPANEL_ITEM_VNUM_CACHE = None

class ItemSelectWindow(ui.ScriptWindow):
    # Race filter constants
    RACE_TAB_ALL = 0
    RACE_TAB_WARRIOR = 1
    RACE_TAB_NINJA = 2
    RACE_TAB_SURA = 3
    RACE_TAB_SHAMAN = 4

    def __init__(self):
        self.parent = None
        self.wearPos = 0
        self.selectedVnum = 0
        self.baseVnum = 0
        self.selectedRefine = 0
        self.itemCallback = None
        self.editMode = False
        self.existingData = None

        self.sockets = [0, 0, 0]
        self.attrs = [[0, 0] for _ in range(7)]

        # Race tab state
        self.currentRaceTab = self.RACE_TAB_ALL
        self.tabButtons = {}
        self.tabButtonGroup = None

        # Item list loading
        self.listBoxSearch = None
        self.isItemlistLoaded = False
        self.itemList = None
        self.itemDestCount = 0
        self.itemCurCount = 0
        self.isItemlistLoading = False
        self.deferItemLoad = False
        self.lazyBatchSize = 200
        self.lazyTargetCount = 0
        self.lazyItemsPerFrame = 8

        # Race filter cache
        self.itemRaceCache = {}

        ui.ScriptWindow.__init__(self)
        self.__LoadWindow()

    def __del__(self):
        self.parent = None
        self.listBoxSearch = None
        self.tabButtons = {}
        self.tabButtonGroup = None
        ui.ScriptWindow.__del__(self)

    def SetParent(self, parent):
        self.parent = parent

    def SetWearPos(self, wearPos):
        self.wearPos = wearPos
        if self.listBoxSearch:
            self.listBoxSearch.SetSlotFilter(wearPos)

    def SetItemCallback(self, callback):
        self.itemCallback = callback

    def Show(self, editMode=False, existingData=None):
        self.editMode = editMode
        self.existingData = existingData

        # Update title and button text based on mode
        if editMode:
            self.board.SetTitleName("Edit Item")
            self.GetChild("btn_add").SetText("Edit")
        else:
            self.board.SetTitleName("Add Item")
            self.GetChild("btn_add").SetText("Add")

        # Reset state
        self.selectedVnum = 0
        self.baseVnum = 0
        self.selectedRefine = 0
        self.GetChild("label_selected").SetText("Selected: None")

        # Reset socket fields
        self.socket0EditLine.SetText("0")
        self.socket1EditLine.SetText("0")
        self.socket2EditLine.SetText("0")

        # Reset refine combo
        if hasattr(self, 'refineCombo'):
            self.refineCombo.ClearItem()
            self.refineCombo.Hide()

        # If editing, populate with existing data
        if editMode and existingData:
            self.selectedVnum = existingData.get("vnum", 0)
            self.baseVnum = self.selectedVnum
            sockets = existingData.get("sockets", [0, 0, 0])
            self.socket0EditLine.SetText(str(sockets[0]) if len(sockets) > 0 else "0")
            self.socket1EditLine.SetText(str(sockets[1]) if len(sockets) > 1 else "0")
            self.socket2EditLine.SetText(str(sockets[2]) if len(sockets) > 2 else "0")

            # Update selected label
            if self.selectedVnum > 0:
                item.SelectItem(self.selectedVnum)
                itemName = item.GetItemName()
                self.GetChild("label_selected").SetText("Selected: %s (%d)" % (itemName, self.selectedVnum))

        # Trigger item list loading if needed
        if not self.isItemlistLoaded and not self.isItemlistLoading:
            self.deferItemLoad = True

        # Reset race filter to "All" and re-filter
        self.currentRaceTab = self.RACE_TAB_ALL
        if self.tabButtonGroup:
            self.tabButtonGroup.OnClick(0)
        if self.listBoxSearch:
            self.listBoxSearch.SetRaceFilter(self.RACE_TAB_ALL)
            self.listBoxSearch.SetSlotFilter(self.wearPos)
            if self.isItemlistLoaded:
                self.listBoxSearch.ReSearchItems()

        self.SetCenterPosition()
        self.SetTop()
        ui.ScriptWindow.Show(self)
        self.searchEditLine.SetFocus()

    def Close(self):
        self.Hide()

    def __LoadWindow(self):
        try:
            pyScrLoader = ui.PythonScriptLoader()
            pyScrLoader.LoadScriptFile(self, "adminpanel_module/uiscript/item_select.py")
        except:
            import exception
            exception.Abort("ItemSelectWindow.LoadWindow.LoadObject")

        try:
            self.board = self.GetChild("board")
            self.board.SetCloseEvent(self.Close)

            self.searchEditLine = self.GetChild("search_editline")
            self.socket0EditLine = self.GetChild("edit_socket0")
            self.socket1EditLine = self.GetChild("edit_socket1")
            self.socket2EditLine = self.GetChild("edit_socket2")

            # Create ListBoxSearch for items
            self.listBoxSearch = ListBoxSearchWithRaceFilter()
            self.listBoxSearch.SetParent(self.GetChild("itemlist_background"))
            self.listBoxSearch.SetPosition(4, 4)
            self.listBoxSearch.SetSize(410 - 8, 12 * 17)
            self.listBoxSearch.SetEvent(ui.__mem_func__(self.OnSelectItem))
            self.listBoxSearch.SetMinSearchTextLen(1)
            self.listBoxSearch.SetEditLine(self.searchEditLine)
            self.listBoxSearch.Show()

            # Bind tab buttons
            self.__BindTabButtons()

            self.GetChild("btn_add").SetEvent(ui.__mem_func__(self.OnClickAdd))
            self.GetChild("btn_cancel").SetEvent(ui.__mem_func__(self.Close))

            # Create refine combo box
            self.refineCombo = ui.ComboBoxEx()
            self.refineCombo.SetParent(self.board)
            self.refineCombo.AddFlag('float')
            self.refineCombo.SetPosition(300, 352)
            self.refineCombo.SetSize(80, 20)
            self.refineCombo.SetEvent(ui.__mem_func__(self.OnSelectRefine))
            self.refineCombo.Hide()
        except:
            import exception
            exception.Abort("ItemSelectWindow.LoadWindow.BindObject")

    def __BindTabButtons(self):
        tabNames = ["tab_all", "tab_warrior", "tab_ninja", "tab_sura", "tab_shaman"]
        tabKeys = [self.RACE_TAB_ALL, self.RACE_TAB_WARRIOR, self.RACE_TAB_NINJA, self.RACE_TAB_SURA, self.RACE_TAB_SHAMAN]

        self.tabButtonGroup = ui.RadioButtonGroup.Create(
            [
                [self.GetChild(tabNames[0]), lambda: self.__OnClickTabButton(self.RACE_TAB_ALL), None],
                [self.GetChild(tabNames[1]), lambda: self.__OnClickTabButton(self.RACE_TAB_WARRIOR), None],
                [self.GetChild(tabNames[2]), lambda: self.__OnClickTabButton(self.RACE_TAB_NINJA), None],
                [self.GetChild(tabNames[3]), lambda: self.__OnClickTabButton(self.RACE_TAB_SURA), None],
                [self.GetChild(tabNames[4]), lambda: self.__OnClickTabButton(self.RACE_TAB_SHAMAN), None],
            ]
        )

        for i, name in enumerate(tabNames):
            self.tabButtons[tabKeys[i]] = self.GetChild(name)

        # Select "All" tab by default
        self.tabButtonGroup.OnClick(0)

    def __OnClickTabButton(self, tabKey):
        if self.currentRaceTab == tabKey:
            return

        self.currentRaceTab = tabKey
        self.__FilterItemList()

    def __FilterItemList(self):
        if not self.listBoxSearch:
            return

        self.listBoxSearch.SetRaceFilter(self.currentRaceTab)
        self.listBoxSearch.ReSearchItems()

    def __ItemMatchesRaceFilter(self, vnum):
        if self.currentRaceTab == self.RACE_TAB_ALL:
            return True

        # Check cache first
        if vnum in self.itemRaceCache:
            return self.itemRaceCache[vnum].get(self.currentRaceTab, True)

        item.SelectItem(vnum)

        # Build race cache for this item
        self.itemRaceCache[vnum] = {
            self.RACE_TAB_WARRIOR: not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
            self.RACE_TAB_NINJA: not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
            self.RACE_TAB_SURA: not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
            self.RACE_TAB_SHAMAN: not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN),
        }

        return self.itemRaceCache[vnum].get(self.currentRaceTab, True)

    def LoadItemList(self):
        global _ADMINPANEL_ITEM_VNUM_CACHE
        if _ADMINPANEL_ITEM_VNUM_CACHE is None:
            _ADMINPANEL_ITEM_VNUM_CACHE = item.AdminPanelGetItemList()
        self.itemList = _ADMINPANEL_ITEM_VNUM_CACHE
        self.itemCurCount = 0
        self.itemDestCount = len(self.itemList)
        self.lazyTargetCount = min(self.lazyBatchSize, self.itemDestCount)
        self.isItemlistLoading = True
        self.deferItemLoad = False

    def OnUpdate(self):
        if self.deferItemLoad:
            self.LoadItemList()

        if self.isItemlistLoading and self.itemCurCount < self.itemDestCount:
            # Check if user is searching, load all items
            if self.listBoxSearch and self.listBoxSearch.editLine:
                search_text = self.listBoxSearch.editLine.GetText()
                if search_text and len(search_text) >= self.listBoxSearch.minSearchTextLen:
                    self.lazyTargetCount = self.itemDestCount

            # Lazy load more items when scrolling near the end
            if self.lazyTargetCount < self.itemDestCount:
                view_count = self.listBoxSearch.GetViewItemCount()
                if self.listBoxSearch.basePos + view_count >= self.itemCurCount - 5:
                    self.lazyTargetCount = min(self.lazyTargetCount + self.lazyBatchSize, self.itemDestCount)

            load_target = min(self.lazyTargetCount, self.itemDestCount)
            step = self.lazyItemsPerFrame
            count = 0
            while count < step and self.itemCurCount < load_target:
                itemvnum = self.itemList[self.itemCurCount]
                item.SelectItem(itemvnum)
                self.itemCurCount += 1
                itemName = item.GetItemName()
                if itemName != "":
                    self.listBoxSearch.InsertItem(itemvnum, "%s (%d)" % (itemName, itemvnum))
                count += 1

            if self.itemCurCount >= self.itemDestCount:
                self.isItemlistLoaded = True
                self.isItemlistLoading = False

    def OnSelectItem(self, vnum, text):
        self.baseVnum = vnum
        self.selectedVnum = vnum
        self.selectedRefine = 0

        # Update selected label
        self.GetChild("label_selected").SetText("Selected: %s" % text)

        # Load refine variants (+0 to +9)
        if hasattr(self, 'refineCombo'):
            self.refineCombo.ClearItem()
            variantCount = 0

            for i in range(10):
                testVnum = vnum + i
                item.SelectItem(testVnum)
                itemName = item.GetItemName()
                if itemName and itemName != "":
                    self.refineCombo.InsertItem(i, "+%d" % i)
                    variantCount += 1
                else:
                    break

            if variantCount > 1:
                self.refineCombo.SetCurrentItem("+0")
                self.refineCombo.Show()
            else:
                self.refineCombo.Hide()

    def OnSelectRefine(self, args):
        refineLevel = self.refineCombo.listBox.GetSelectedItem()
        self.selectedRefine = refineLevel
        self.selectedVnum = self.baseVnum + refineLevel

        # Update selected label
        item.SelectItem(self.selectedVnum)
        itemName = item.GetItemName()
        self.GetChild("label_selected").SetText("Selected: %s (%d)" % (itemName, self.selectedVnum))

    def OnClickAdd(self):
        if self.selectedVnum <= 0:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "Please select an item from the list.")
            return

        try:
            sockets = [
                int(self.socket0EditLine.GetText()) if self.socket0EditLine.GetText() else 0,
                int(self.socket1EditLine.GetText()) if self.socket1EditLine.GetText() else 0,
                int(self.socket2EditLine.GetText()) if self.socket2EditLine.GetText() else 0,
            ]
        except:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "Invalid socket values.")
            return

        attrs = [[0, 0] for _ in range(7)]

        if self.itemCallback:
            self.itemCallback(self.wearPos, self.selectedVnum, sockets, attrs)

        self.Close()

    def OnRunMouseWheel(self, nLen):
        if self.listBoxSearch and self.listBoxSearch.scrollBar.IsShow():
            if nLen > 0:
                self.listBoxSearch.scrollBar.OnUp()
            else:
                self.listBoxSearch.scrollBar.OnDown()

    def OnPressEscapeKey(self):
        self.Close()
        return True


class ListBoxSearchWithRaceFilter(ui.ListBox):
    SEARCH_UPDATE_TIME = 0.1

    # Race filter constants (must match ItemSelectWindow)
    RACE_TAB_ALL = 0
    RACE_TAB_WARRIOR = 1
    RACE_TAB_NINJA = 2
    RACE_TAB_SURA = 3
    RACE_TAB_SHAMAN = 4

    def __init__(self):
        ui.ListBox.__init__(self)
        self.visibleDict = {}
        self.textDictLower = {}
        self.lastSearchText = ""
        self.lastSearchTime = 0
        self.minSearchTextLen = 1
        self.realSelectedLine = -1
        self.editLine = None
        self.currentRaceFilter = self.RACE_TAB_ALL
        self.itemRaceCache = {}
        self.currentSlotFilter = None  # None means no slot filtering
        self.itemSlotCache = {}        # Cache for item type/subtype lookups

        self.scrollBar = ui.ScrollBar()
        self.scrollBar.SetParent(self)
        self.scrollBar.SetScrollEvent(self.__OnScroll)
        self.scrollBar.SetScrollStep(0.01)
        self.scrollBar.Hide()

    def SetMinSearchTextLen(self, minSearchTextLen):
        self.minSearchTextLen = minSearchTextLen

    def SetEditLine(self, editLine):
        self.editLine = editLine

    def SetRaceFilter(self, raceFilter):
        self.currentRaceFilter = raceFilter

    def SetSlotFilter(self, wearPos):
        """Set the current slot position for filtering items by type."""
        self.currentSlotFilter = wearPos

    def __CacheItemSlotInfo(self, vnum):
        """Cache item type and subtype for a given vnum."""
        if vnum in self.itemSlotCache:
            return

        item.SelectItem(vnum)
        self.itemSlotCache[vnum] = (item.GetItemType(), item.GetItemSubType())

    def __ItemMatchesSlotFilter(self, vnum):
        """Check if an item matches the current slot filter."""
        if self.currentSlotFilter is None:
            return True

        filterConfig = SLOT_TYPE_FILTER.get(self.currentSlotFilter)

        if filterConfig is None:
            return True

        requiredType, requiredSubType = filterConfig

        if vnum not in self.itemSlotCache:
            self.__CacheItemSlotInfo(vnum)

        itemType, itemSubType = self.itemSlotCache.get(vnum, (None, None))

        if itemType != requiredType:
            return False

        if requiredSubType is None:
            return True

        return itemSubType == requiredSubType

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
        self.itemRaceCache = {}
        self.itemSlotCache = {}
        self.scrollBar.SetPos(0)

    def SelectItem(self, line):
        lineDict = []
        for key in range(len(self.itemList)):
            if not self.visibleDict.get(key, True):
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

    def InsertItem(self, vnum, text, doLocate=True):
        idx = len(self.itemList)
        self.keyDict[idx] = vnum
        self.textDict[idx] = text
        self.textDictLower[idx] = text.lower()
        self.visibleDict[idx] = True

        # Cache race info for this item
        self.__CacheItemRace(vnum)

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

    def __CacheItemRace(self, vnum):
        if vnum in self.itemRaceCache:
            return

        item.SelectItem(vnum)
        self.itemRaceCache[vnum] = {
            self.RACE_TAB_WARRIOR: not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
            self.RACE_TAB_NINJA: not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
            self.RACE_TAB_SURA: not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
            self.RACE_TAB_SHAMAN: not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN),
        }

    def __ItemMatchesRaceFilter(self, vnum):
        if self.currentRaceFilter == self.RACE_TAB_ALL:
            return True

        if vnum not in self.itemRaceCache:
            self.__CacheItemRace(vnum)

        return self.itemRaceCache.get(vnum, {}).get(self.currentRaceFilter, True)

    def LocateItem(self):
        self._LocateItem()

    def _LocateItem(self):
        self.selectedLine = -1
        self.realSelectedLine = -1
        skipCount = self.basePos
        yPos = 0
        self.showLineCount = 0

        for key, value in self.keyDict.items():
            textLine = self.itemList[key]
            textLine.Hide()

            if not self.visibleDict.get(key, True):
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
        return sum(1 for key in self.keyDict if self.visibleDict.get(key, True))

    def ReSearchItems(self):
        searchText = ""
        if self.editLine:
            searchText = self.editLine.GetText()
        self._SearchItems(searchText)

    def _SearchItems(self, text):
        if len(text) < self.minSearchTextLen and len(text) != 0:
            return

        text = text.lower()

        for key in self.keyDict:
            vnum = self.keyDict[key]
            textLineText = self.textDictLower.get(key, "")

            # Check text match
            textMatch = textLineText.find(text) != -1

            # Check race filter match
            raceMatch = self.__ItemMatchesRaceFilter(vnum)

            # Check slot filter match (item type/subtype)
            slotMatch = self.__ItemMatchesSlotFilter(vnum)

            self.visibleDict[key] = textMatch and raceMatch and slotMatch

        self.scrollBar.SetPos(0)
        self.SetBasePos(0)

    def OnUpdate(self):
        self.overLine = -1
        if self.scrollBar.IsShow():
            itemCount = self.GetItemCount()
            if itemCount > 0:
                min_number = 1.00 / float(itemCount) * 5
                if min_number < 0.005:
                    min_number = 0.005
                self.scrollBar.SetScrollStep(min_number)

        if self.IsIn():
            x, y = self.GetGlobalPosition()
            height = self.GetHeight()
            xMouse, yMouse = wndMgr.GetMousePosition()

            if yMouse - y < height - 1:
                self.overLine = (yMouse - y) / self.stepSize

                if self.overLine < 0:
                    self.overLine = -1
                if self.overLine >= self.GetItemCount():
                    self.overLine = -1

        if self.editLine and self.lastSearchTime < _now():
            searchText = self.editLine.GetText()
            if self.lastSearchText != searchText:
                self.lastSearchText = searchText
                self._SearchItems(searchText)
            self.lastSearchTime = _now() + self.SEARCH_UPDATE_TIME


class ListBoxSearch(ui.ListBox):
    SEARCH_UPDATE_TIME = 0.1

    def __init__(self):
        ui.ListBox.__init__(self)
        self.visibleDict = {}
        self.textDictLower = {}
        self.lastSearchText = ""
        self.lastSearchTime = 0
        self.minSearchTextLen = 1
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
            if not self.visibleDict.get(key, True):
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
        self.event(self.keyDict.get(realLine, ""), self.textDict.get(realLine, "None"))

    def GetSelectedItem(self):
        return self.keyDict.get(self.realSelectedLine, "")

    def InsertItem(self, key, text, doLocate=True):
        idx = len(self.itemList)
        self.keyDict[idx] = key
        self.textDict[idx] = text
        self.textDictLower[idx] = text.lower()
        self.visibleDict[idx] = True

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

        for key, value in self.keyDict.items():
            textLine = self.itemList[key]
            textLine.Hide()

            if not self.visibleDict.get(key, True):
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
        return sum(1 for key in self.keyDict if self.visibleDict.get(key, True))

    def ReSearchItems(self):
        self._SearchItems(self.editLine.GetText())

    def _SearchItems(self, text):
        if len(text) < self.minSearchTextLen and len(text) != 0:
            return

        text = text.lower()

        for key in self.keyDict:
            textLineText = self.textDictLower.get(key, "")
            self.visibleDict[key] = False
            if textLineText.find(text) != -1:
                self.visibleDict[key] = True

        self.scrollBar.SetPos(0)
        self.SetBasePos(0)

    def OnUpdate(self):
        self.overLine = -1
        if self.scrollBar.IsShow():
            itemCount = self.GetItemCount()
            if itemCount > 0:
                min_number = 1.00 / float(itemCount) * 5
                if min_number < 0.005:
                    min_number = 0.005
                self.scrollBar.SetScrollStep(min_number)

        if self.IsIn():
            x, y = self.GetGlobalPosition()
            height = self.GetHeight()
            xMouse, yMouse = wndMgr.GetMousePosition()

            if yMouse - y < height - 1:
                self.overLine = (yMouse - y) / self.stepSize

                if self.overLine < 0:
                    self.overLine = -1
                if self.overLine >= self.GetItemCount():
                    self.overLine = -1

        if self.editLine and self.lastSearchTime < _now():
            searchText = self.editLine.GetText()
            if self.lastSearchText != searchText:
                self.lastSearchText = searchText
                self._SearchItems(searchText)
            self.lastSearchTime = _now() + self.SEARCH_UPDATE_TIME
