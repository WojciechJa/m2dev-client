import ui
import uiScriptLocale
import net
import chat

UI_SCRIPT_FILE = "adminpanel_module/uiscript/gm_commands.py"


class MainWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, UI_SCRIPT_FILE)
		except:
			import exception
			exception.Abort("GMCommandsWindow.LoadWindow.LoadObject")

		try:
			self.board = self.GetChild("board")

			self.pageWindow = {
				"TAB1": self.GetChild("Page_01"),
				"TAB2": self.GetChild("Page_02"),
				"TAB3": self.GetChild("Page_03"),
				"TAB4": self.GetChild("Page_04"),
				"TAB5": self.GetChild("Page_05"),
				"TAB6": self.GetChild("Page_06"),
				"TAB7": self.GetChild("Page_07"),
			}
			self._LoadTabScripts()
			self.tabDict = {
				"TAB1": self.GetChild("Tab_01"),
				"TAB2": self.GetChild("Tab_02"),
				"TAB3": self.GetChild("Tab_03"),
				"TAB4": self.GetChild("Tab_04"),
				"TAB5": self.GetChild("Tab_05"),
				"TAB6": self.GetChild("Tab_06"),
				"TAB7": self.GetChild("Tab_07"),
			}
			self.tabButtonDict = {
				"TAB1": self.GetChild("Tab_Button_01"),
				"TAB2": self.GetChild("Tab_Button_02"),
				"TAB3": self.GetChild("Tab_Button_03"),
				"TAB4": self.GetChild("Tab_Button_04"),
				"TAB5": self.GetChild("Tab_Button_05"),
				"TAB6": self.GetChild("Tab_Button_06"),
				"TAB7": self.GetChild("Tab_Button_07"),
			}

			for key, btn in self.tabButtonDict.items():
				btn.SetEvent(self.SelectPage, key)

			self.tabButtonDict["TAB1"].SetText("Ogolne")
			self.tabButtonDict["TAB2"].SetText("Gracze")
			self.tabButtonDict["TAB3"].SetText("World")
			self.tabButtonDict["TAB4"].SetText("Quest")
			self.tabButtonDict["TAB5"].SetText("Guild")
			self.tabButtonDict["TAB6"].SetText("Horse")
			self.tabButtonDict["TAB7"].SetText("Custom")

			self._InitTab1PrivEmpire()
			self._InitTab2Players()
			self._InitTab3World()
			self._InitTab4QuestEvent()
			self._InitTab5Guild()
			self._InitTab6HorseMisc()
			self._InitTab7Custom()

			self.SelectPage("TAB1")
		except:
			import exception
			exception.Abort("GMCommandsWindow.LoadWindow.BindObject")

	def SelectPage(self, arg):
		for key, btn in self.tabButtonDict.items():
			if arg != key:
				btn.SetUp()
		for key, img in self.tabDict.items():
			if arg == key:
				img.Show()
			else:
				img.Hide()
		for key, page in self.pageWindow.items():
			if arg == key:
				page.Show()
			else:
				page.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def _GetInt(self, edit, name, min_val=None, max_val=None):
		text = edit.GetText().strip()
		if not text:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Missing value: %s" % name)
			return None
		try:
			value = int(text)
		except:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Invalid number: %s" % name)
			return None
		if min_val is not None and value < min_val:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "%s too low (min %d)" % (name, min_val))
			return None
		if max_val is not None and value > max_val:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "%s too high (max %d)" % (name, max_val))
			return None
		return value

	def _GetText(self, edit, name, required=True):
		text = edit.GetText().strip()
		if required and not text:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Missing value: %s" % name)
			return None
		return text

	def _SendCommand(self, cmd):
		if not cmd:
			return
		if cmd[0] != "/":
			cmd = "/" + cmd
		net.SendChatPacket(cmd)

	def _GetChildOrNone(self, parent, name):
		try:
			return parent.GetChild(name)
		except:
			return None

	def _BindIfExists(self, parent, name, event):
		child = self._GetChildOrNone(parent, name)
		if child:
			child.SetEvent(event)

	def _LoadTabScripts(self):
		tabScripts = {
			"TAB1": "adminpanel_module/uiscript/gm_tabs/tab1.py",
			"TAB2": "adminpanel_module/uiscript/gm_tabs/tab2.py",
			"TAB3": "adminpanel_module/uiscript/gm_tabs/tab3.py",
			"TAB4": "adminpanel_module/uiscript/gm_tabs/tab4.py",
			"TAB5": "adminpanel_module/uiscript/gm_tabs/tab5.py",
			"TAB6": "adminpanel_module/uiscript/gm_tabs/tab6.py",
			"TAB7": "adminpanel_module/uiscript/gm_tabs/tab7.py",
		}
		for key, page in self.pageWindow.items():
			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(page, tabScripts[key])
			except:
				import exception
				exception.Abort("GMCommandsWindow.LoadWindow.TabScript %s" % key)

	def _InitTab1PrivEmpire(self):
		page1 = self.pageWindow["TAB1"]
		self.privEmpireValue = page1.GetChild("PrivEmpire_ValueValue")
		self.privEmpireDuration = page1.GetChild("PrivEmpire_DurationValue")
		self.privEmpireApply = page1.GetChild("PrivEmpire_Apply")
		self.privEmpireApply.SetEvent(self.OnPrivEmpire)

		self.empireButtons = {
			0: page1.GetChild("Empire_All"),
			1: page1.GetChild("Empire_Shinsoo"),
			2: page1.GetChild("Empire_Chunjo"),
			3: page1.GetChild("Empire_Jinno"),
		}
		for value, btn in self.empireButtons.items():
			btn.SetToggleDownEvent(lambda value=value: self.SelectEmpire(value))
			btn.SetToggleUpEvent(lambda value=value: self.SelectEmpire(value))
			btn.SetEvent(self.SelectEmpire, value)

		self.typeButtons = {
			1: page1.GetChild("Type_Item"),
			2: page1.GetChild("Type_Gold"),
			3: page1.GetChild("Type_Gold10"),
			4: page1.GetChild("Type_Exp"),
		}
		for value, btn in self.typeButtons.items():
			btn.SetToggleDownEvent(lambda value=value: self.SelectType(value))
			btn.SetToggleUpEvent(lambda value=value: self.SelectType(value))
			btn.SetEvent(self.SelectType, value)

		self.SelectEmpire(0)
		self.SelectType(1)

	def SelectEmpire(self, value):
		self.empireValue = value
		for v, btn in self.empireButtons.items():
			if v == value:
				btn.Down()
			else:
				btn.SetUp()

	def SelectType(self, value):
		self.typeValue = value
		for v, btn in self.typeButtons.items():
			if v == value:
				btn.Down()
			else:
				btn.SetUp()

	def OnPrivEmpire(self):
		value = self._GetInt(self.privEmpireValue, "value", 0, 1000)
		if value is None:
			return
		duration = self._GetInt(self.privEmpireDuration, "duration", 0, None)
		if duration is None:
			return
		self._SendCommand("priv_empire %d %d %d %d" % (self.empireValue, self.typeValue, value, duration))

	def _InitTab2Players(self):
		page = self.pageWindow["TAB2"]
		self.plyName = page.GetChild("Ply_NameValue")
		self.plyLevel = page.GetChild("Ply_LevelValue")
		self.plyBlockMins = page.GetChild("Ply_BlockMinsValue")
		self.plySetField = page.GetChild("Ply_SetFieldValue")
		self.plySetValue = page.GetChild("Ply_SetValueValue")
		self.plySkill = page.GetChild("Ply_SkillValue")
		self.plySkillLevel = page.GetChild("Ply_SkillLevelValue")

		page.GetChild("Ply_DC").SetEvent(self.OnPlayerDC)
		page.GetChild("Ply_Kill").SetEvent(self.OnPlayerKill)
		page.GetChild("Ply_Transfer").SetEvent(self.OnPlayerTransfer)
		page.GetChild("Ply_Stun").SetEvent(self.OnPlayerStun)
		page.GetChild("Ply_Slow").SetEvent(self.OnPlayerSlow)
		page.GetChild("Ply_LevelSelf").SetEvent(self.OnPlayerLevelSelf)
		page.GetChild("Ply_Advance").SetEvent(self.OnPlayerAdvance)
		page.GetChild("Ply_BlockChat").SetEvent(self.OnPlayerBlockChat)
		page.GetChild("Ply_SetApply").SetEvent(self.OnPlayerSet)
		page.GetChild("Ply_SetSkillOther").SetEvent(self.OnPlayerSetSkillOther)
		page.GetChild("Ply_ResetSubskill").SetEvent(self.OnPlayerResetSubskill)
		page.GetChild("Ply_ResetSelf").SetEvent(lambda: self._SendCommand("reset"))
		page.GetChild("Ply_Cooltime").SetEvent(lambda: self._SendCommand("cooltime"))
		page.GetChild("Ply_AllSkill").SetEvent(lambda: self._SendCommand("all_skill_master"))

	def _GetPlayerName(self):
		return self._GetText(self.plyName, "player")

	def OnPlayerDC(self):
		name = self._GetPlayerName()
		if name:
			self._SendCommand("dc %s" % name)

	def OnPlayerKill(self):
		name = self._GetPlayerName()
		if name:
			self._SendCommand("kill %s" % name)

	def OnPlayerTransfer(self):
		name = self._GetPlayerName()
		if name:
			self._SendCommand("transfer %s" % name)

	def OnPlayerStun(self):
		name = self._GetPlayerName()
		if name:
			self._SendCommand("stun %s" % name)

	def OnPlayerSlow(self):
		name = self._GetPlayerName()
		if name:
			self._SendCommand("slow %s" % name)

	def OnPlayerLevelSelf(self):
		level = self._GetInt(self.plyLevel, "level", 1, 250)
		if level is not None:
			self._SendCommand("level %d" % level)

	def OnPlayerAdvance(self):
		name = self._GetPlayerName()
		if not name:
			return
		level = self._GetInt(self.plyLevel, "advance level", 1, 250)
		if level is None:
			return
		self._SendCommand("advance %s %d" % (name, level))

	def OnPlayerBlockChat(self):
		name = self._GetPlayerName()
		if not name:
			return
		mins = self._GetInt(self.plyBlockMins, "block minutes", 0, 100000)
		if mins is None:
			return
		self._SendCommand("block_chat %s %d" % (name, mins))

	def OnPlayerSet(self):
		name = self._GetPlayerName()
		if not name:
			return
		field = self._GetText(self.plySetField, "set field")
		if not field:
			return
		value = self._GetText(self.plySetValue, "set value")
		if value is None:
			return
		self._SendCommand("set %s %s %s" % (name, field, value))

	def OnPlayerSetSkillOther(self):
		name = self._GetPlayerName()
		if not name:
			return
		skill = self._GetText(self.plySkill, "skill id/name")
		if not skill:
			return
		lvl = self._GetInt(self.plySkillLevel, "skill level", 0, 59)
		if lvl is None:
			return
		self._SendCommand("setskillother %s %s %d" % (name, skill, lvl))

	def OnPlayerResetSubskill(self):
		name = self._GetPlayerName()
		if name:
			self._SendCommand("reset_subskill %s" % name)

	def _InitTab3World(self):
		page = self.pageWindow["TAB3"]
		self.worldTarget = self._GetChildOrNone(page, "World_TargetValue")
		self.worldX = self._GetChildOrNone(page, "World_XValue")
		self.worldY = self._GetChildOrNone(page, "World_YValue")

		self._BindIfExists(page, "World_WarpPlayer", self.OnWorldWarpPlayer)
		self._BindIfExists(page, "World_TransferPlayer", self.OnWorldTransferPlayer)
		self._BindIfExists(page, "World_GotoXY", self.OnWorldGotoXY)
		self._BindIfExists(page, "World_WarpXY", self.OnWorldWarpXY)
		self._BindIfExists(page, "World_WeakenNear", lambda: self._SendCommand("weaken"))
		self._BindIfExists(page, "World_WeakenAll", lambda: self._SendCommand("weaken all"))

	def OnWorldWarpPlayer(self):
		if not self.worldTarget:
			return
		target = self._GetText(self.worldTarget, "warp target")
		if target:
			self._SendCommand("warp %s" % target)

	def OnWorldTransferPlayer(self):
		if not self.worldTarget:
			return
		target = self._GetText(self.worldTarget, "transfer target")
		if target:
			self._SendCommand("transfer %s" % target)

	def OnWorldGotoXY(self):
		if not self.worldX or not self.worldY:
			return
		x = self._GetInt(self.worldX, "x", 0, None)
		y = self._GetInt(self.worldY, "y", 0, None)
		if x is None or y is None:
			return
		self._SendCommand("goto %d %d" % (x, y))

	def OnWorldWarpXY(self):
		if not self.worldX or not self.worldY:
			return
		x = self._GetInt(self.worldX, "x", 0, None)
		y = self._GetInt(self.worldY, "y", 0, None)
		if x is None or y is None:
			return
		self._SendCommand("warp %d %d" % (x, y))

	def _InitTab4QuestEvent(self):
		page = self.pageWindow["TAB4"]
		self.eventFlagName = page.GetChild("Ev_FlagNameValue")
		self.eventFlagValue = page.GetChild("Ev_FlagValueValue")
		self.questFlagName = page.GetChild("Ev_QFlagNameValue")
		self.questFlagValue = page.GetChild("Ev_QFlagValueValue")
		self.questTarget = page.GetChild("Ev_QTargetValue")
		self.questStateQuest = page.GetChild("Ev_StateQuestValue")
		self.questStateName = page.GetChild("Ev_StateNameValue")
		self.clearQuestName = page.GetChild("Ev_ClearQuestValue")

		page.GetChild("Ev_SetEventFlag").SetEvent(self.OnSetEventFlag)
		page.GetChild("Ev_GetEventFlag").SetEvent(lambda: self._SendCommand("geteventflag"))
		page.GetChild("Ev_SetQf").SetEvent(self.OnSetQf)
		page.GetChild("Ev_GetQf").SetEvent(self.OnGetQf)
		page.GetChild("Ev_DelQf").SetEvent(self.OnDelQf)
		page.GetChild("Ev_SetState").SetEvent(self.OnSetState)
		page.GetChild("Ev_ClearQuest").SetEvent(self.OnClearQuest)

	def OnSetEventFlag(self):
		name = self._GetText(self.eventFlagName, "event flag")
		if not name:
			return
		value = self._GetInt(self.eventFlagValue, "event value", 0, None)
		if value is None:
			return
		self._SendCommand("eventflag %s %d" % (name, value))

	def OnSetQf(self):
		flag = self._GetText(self.questFlagName, "quest flag")
		if not flag:
			return
		value = self._GetInt(self.questFlagValue, "quest value", -2147483648, 2147483647)
		if value is None:
			return
		target = self._GetText(self.questTarget, "quest target", False)
		if target:
			self._SendCommand("setqf %s %d %s" % (flag, value, target))
		else:
			self._SendCommand("setqf %s %d" % (flag, value))

	def OnGetQf(self):
		target = self._GetText(self.questTarget, "quest target", False)
		if target:
			self._SendCommand("getqf %s" % target)
		else:
			self._SendCommand("getqf")

	def OnDelQf(self):
		flag = self._GetText(self.questFlagName, "quest flag")
		if not flag:
			return
		target = self._GetText(self.questTarget, "quest target", False)
		if target:
			self._SendCommand("delqf %s %s" % (flag, target))
		else:
			self._SendCommand("delqf %s" % flag)

	def OnSetState(self):
		quest = self._GetText(self.questStateQuest, "quest name")
		state = self._GetText(self.questStateName, "state")
		if quest and state:
			self._SendCommand("set_state %s %s" % (quest, state))

	def OnClearQuest(self):
		quest = self._GetText(self.clearQuestName, "clear_quest name")
		if quest:
			self._SendCommand("clear_quest %s" % quest)

	def _InitTab5Guild(self):
		page = self.pageWindow["TAB5"]
		self.guildId1 = page.GetChild("Guild_Id1Value")
		self.guildId2 = page.GetChild("Guild_Id2Value")
		self.guildName = page.GetChild("Guild_NameValue")

		page.GetChild("Guild_GwList").SetEvent(lambda: self._SendCommand("gwlist"))
		page.GetChild("Guild_GwStop").SetEvent(self.OnGuildWarStop)
		page.GetChild("Guild_GwCancel").SetEvent(self.OnGuildWarCancel)
		page.GetChild("Guild_State").SetEvent(self.OnGuildState)
		page.GetChild("Guild_Priv").SetEvent(self.OnGuildPriv)

	def OnGuildWarStop(self):
		id1 = self._GetInt(self.guildId1, "guild id1", 1, None)
		id2 = self._GetInt(self.guildId2, "guild id2", 1, None)
		if id1 is None or id2 is None:
			return
		self._SendCommand("gwstop %d %d" % (id1, id2))

	def OnGuildWarCancel(self):
		id1 = self._GetInt(self.guildId1, "guild id1", 1, None)
		id2 = self._GetInt(self.guildId2, "guild id2", 1, None)
		if id1 is None or id2 is None:
			return
		self._SendCommand("gwcancel %d %d" % (id1, id2))

	def OnGuildState(self):
		name = self._GetText(self.guildName, "guild name")
		if name:
			self._SendCommand("gstate %s" % name)

	def OnGuildPriv(self):
		name_or_id = self._GetText(self.guildName, "guild name/id")
		if name_or_id:
			self._SendCommand("priv_guild %s" % name_or_id)

	def _InitTab6HorseMisc(self):
		page = self.pageWindow["TAB6"]
		self.horseName = page.GetChild("Horse_NameValue")
		self.horseLevel = page.GetChild("Horse_LevelValue")
		self.horseHP = page.GetChild("Horse_HPValue")
		self.horseStam = page.GetChild("Horse_StamValue")

		page.GetChild("Horse_State").SetEvent(lambda: self._SendCommand("horse_state"))
		page.GetChild("Horse_Summon").SetEvent(lambda: self._SendCommand("horse_summon"))
		page.GetChild("Horse_Unsummon").SetEvent(lambda: self._SendCommand("horse_unsummon"))
		page.GetChild("Horse_LevelApply").SetEvent(self.OnHorseLevel)
		page.GetChild("Horse_SetStat").SetEvent(self.OnHorseSetStat)

		page.GetChild("Misc_XmasSnow").SetEvent(lambda: self._SendCommand("xmas_snow"))
		page.GetChild("Misc_XmasSanta").SetEvent(lambda: self._SendCommand("xmas_santa"))
		page.GetChild("Misc_XmasBoom").SetEvent(lambda: self._SendCommand("xmas_boom"))
		page.GetChild("Misc_Eclipse").SetEvent(lambda: self._SendCommand("eclipse"))
		page.GetChild("Misc_Weekly").SetEvent(lambda: self._SendCommand("weeklyevent"))
		page.GetChild("Misc_EventHelper").SetEvent(lambda: self._SendCommand("eventhelper"))
		page.GetChild("Misc_Siege").SetEvent(lambda: self._SendCommand("siege"))
		page.GetChild("Misc_Temp").SetEvent(lambda: self._SendCommand("temp"))
		page.GetChild("Misc_Frog").SetEvent(lambda: self._SendCommand("frog"))

	def OnHorseLevel(self):
		name = self._GetText(self.horseName, "player")
		if not name:
			return
		level = self._GetInt(self.horseLevel, "horse level", 0, 30)
		if level is None:
			return
		self._SendCommand("horse_level %s %d" % (name, level))

	def OnHorseSetStat(self):
		hp = self._GetInt(self.horseHP, "horse hp", 0, None)
		stam = self._GetInt(self.horseStam, "horse stamina", 0, None)
		if hp is None or stam is None:
			return
		self._SendCommand("horse_set_stat %d %d" % (hp, stam))

	def _InitTab7Custom(self):
		page = self.pageWindow["TAB7"]
		self.customCmd = page.GetChild("Custom_CmdValue")
		page.GetChild("Custom_Send").SetEvent(self.OnCustomSend)

	def OnCustomSend(self):
		cmd = self._GetText(self.customCmd, "custom command")
		if cmd:
			self._SendCommand(cmd)
