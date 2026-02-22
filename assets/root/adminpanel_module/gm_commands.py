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

			self.pageName = {
				"TAB1": "Commands",
				"TAB2": "Players",
				"TAB3": "World",
				"TAB4": "Misc 1",
				"TAB5": "Misc 2",
				"TAB6": "Misc 3",
				"TAB7": "Misc 4",
			}
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

			self.tabButtonDict["TAB1"].SetText("Cmd")
			self.tabButtonDict["TAB2"].SetText("Ply")
			self.tabButtonDict["TAB3"].SetText("World")
			self.tabButtonDict["TAB4"].SetText("Misc1")
			self.tabButtonDict["TAB5"].SetText("Misc2")
			self.tabButtonDict["TAB6"].SetText("Misc3")
			self.tabButtonDict["TAB7"].SetText("Misc4")

			self.tabButtonDict["TAB1"].SetText("Ogolne")

			page1 = self.pageWindow["TAB1"]
			self.privEmpireValue = page1.GetChild("PrivEmpire_ValueValue")
			self.privEmpireDuration = page1.GetChild("PrivEmpire_DurationValue")
			self.privEmpireApply = page1.GetChild("PrivEmpire_Apply")
			self.privEmpireApply.SetEvent(self.OnPrivEmpire)

			self._InitPrivEmpireButtons()

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
		# Board has no titlebar; keep page switch without title update.

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

	def _InitPrivEmpireButtons(self):
		page1 = self.pageWindow["TAB1"]

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

		cmd = "/priv_empire %d %d %d %d" % (self.empireValue, self.typeValue, value, duration)
		net.SendChatPacket(cmd)
