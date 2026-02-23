import dbg
import ui
import snd
import systemSetting
import net
import chat
import app
import localeInfo
import constInfo
import chrmgr
import player
import musicInfo

import uiSelectMusic
import background

MUSIC_FILENAME_MAX_LEN = 25
TEXTTAIL_RANGE_MIN = 1500
TEXTTAIL_RANGE_MAX = 9000

blockMode = 0

class OptionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print(" -------------------------------------- DELETE SYSTEM OPTION DIALOG")

	def __Initialize(self):
		self.tilingMode = 0
		self.titleBar = 0
		self.changeMusicButton = 0
		self.selectMusicFile = 0
		self.ctrlMusicVolume = 0
		self.ctrlSoundVolume = 0
		self.musicListDlg = 0
		self.tilingApplyButton = 0
		self.cameraModeButtonList = []
		self.fogModeButtonList = []
		self.tilingModeButtonList = []
		self.ctrlShadowQuality = 0
		self.fpsLimitButtonList = []
		self.fpsLimitValues = [60, 90, 120, 0]
		self.vsyncToggle = 0
		self.perfProfileButtonList = []
		self.shadowCadenceButtonList = []
		self.fxAdaptiveToggle = 0
		self.animLodToggle = 0
		self.textTailOptToggle = 0
		self.textTailRangeController = 0
		self.textTailRangeValue = 0
		
	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()
		print(" -------------------------------------- DESTROY SYSTEM OPTION DIALOG")

	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("System.OptionDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			self.selectMusicFile = GetObject("bgm_file")
			self.changeMusicButton = GetObject("bgm_button")
			self.ctrlMusicVolume = GetObject("music_volume_controller")
			self.ctrlSoundVolume = GetObject("sound_volume_controller")			
			self.cameraModeButtonList.append(GetObject("camera_short"))
			self.cameraModeButtonList.append(GetObject("camera_long"))
			self.fogModeButtonList.append(GetObject("fog_level0"))
			self.fogModeButtonList.append(GetObject("fog_level1"))
			self.fogModeButtonList.append(GetObject("fog_level2"))
			self.tilingModeButtonList.append(GetObject("tiling_cpu"))
			self.tilingModeButtonList.append(GetObject("tiling_gpu"))
			self.tilingApplyButton=GetObject("tiling_apply")
			self.fpsLimitButtonList.append(GetObject("fps_60"))
			self.fpsLimitButtonList.append(GetObject("fps_90"))
			self.fpsLimitButtonList.append(GetObject("fps_120"))
			self.fpsLimitButtonList.append(GetObject("fps_unlimited"))
			self.vsyncToggle = GetObject("vsync_toggle")
			self.perfProfileButtonList.append(GetObject("profile_quality"))
			self.perfProfileButtonList.append(GetObject("profile_balanced"))
			self.perfProfileButtonList.append(GetObject("profile_performance"))
			self.fxAdaptiveToggle = GetObject("fx_adaptive_toggle")
			self.animLodToggle = GetObject("anim_lod_toggle")
			self.textTailOptToggle = GetObject("texttail_opt_toggle")
			self.shadowCadenceButtonList.append(GetObject("shadow_cadence_1"))
			self.shadowCadenceButtonList.append(GetObject("shadow_cadence_2"))
			self.shadowCadenceButtonList.append(GetObject("shadow_cadence_3"))
			self.textTailRangeController = GetObject("texttail_range_controller")
			self.textTailRangeValue = GetObject("texttail_range_value")
			#self.ctrlShadowQuality = GetObject("shadow_bar")
		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	def __Load(self):
		self.__Load_LoadScript("uiscript/systemoptiondialog.py")
		self.__Load_BindObject()

		self.SetCenterPosition()
		
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.ctrlMusicVolume.SetSliderPos(float(systemSetting.GetMusicVolume()))
		self.ctrlMusicVolume.SetEvent(ui.__mem_func__(self.OnChangeMusicVolume))

		self.ctrlSoundVolume.SetSliderPos(float(systemSetting.GetSoundVolume()))
		self.ctrlSoundVolume.SetEvent(ui.__mem_func__(self.OnChangeSoundVolume))

#		self.ctrlShadowQuality.SetSliderPos(float(systemSetting.GetShadowLevel()) / 5.0)
#		self.ctrlShadowQuality.SetEvent(ui.__mem_func__(self.OnChangeShadowQuality))

		self.changeMusicButton.SAFE_SetEvent(self.__OnClickChangeMusicButton)

		self.cameraModeButtonList[0].SAFE_SetEvent(self.__OnClickCameraModeShortButton)
		self.cameraModeButtonList[1].SAFE_SetEvent(self.__OnClickCameraModeLongButton)

		self.fogModeButtonList[0].SAFE_SetEvent(self.__OnClickFogModeLevel0Button)
		self.fogModeButtonList[1].SAFE_SetEvent(self.__OnClickFogModeLevel1Button)
		self.fogModeButtonList[2].SAFE_SetEvent(self.__OnClickFogModeLevel2Button)

		self.tilingModeButtonList[0].SAFE_SetEvent(self.__OnClickTilingModeCPUButton)
		self.tilingModeButtonList[1].SAFE_SetEvent(self.__OnClickTilingModeGPUButton)
		self.fpsLimitButtonList[0].SAFE_SetEvent(self.__OnClickFPS60Button)
		self.fpsLimitButtonList[1].SAFE_SetEvent(self.__OnClickFPS90Button)
		self.fpsLimitButtonList[2].SAFE_SetEvent(self.__OnClickFPS120Button)
		self.fpsLimitButtonList[3].SAFE_SetEvent(self.__OnClickFPSUnlimitedButton)
		self.perfProfileButtonList[0].SAFE_SetEvent(self.__OnClickPerfProfileQualityButton)
		self.perfProfileButtonList[1].SAFE_SetEvent(self.__OnClickPerfProfileBalancedButton)
		self.perfProfileButtonList[2].SAFE_SetEvent(self.__OnClickPerfProfilePerformanceButton)
		self.shadowCadenceButtonList[0].SAFE_SetEvent(self.__OnClickShadowCadence1Button)
		self.shadowCadenceButtonList[1].SAFE_SetEvent(self.__OnClickShadowCadence2Button)
		self.shadowCadenceButtonList[2].SAFE_SetEvent(self.__OnClickShadowCadence3Button)

		self.tilingApplyButton.SAFE_SetEvent(self.__OnClickTilingApplyButton)
		self.vsyncToggle.SetToggleDownEvent(self.__OnToggleVSyncOn)
		self.vsyncToggle.SetToggleUpEvent(self.__OnToggleVSyncOff)
		self.fxAdaptiveToggle.SetToggleDownEvent(self.__OnToggleFXAdaptiveOn)
		self.fxAdaptiveToggle.SetToggleUpEvent(self.__OnToggleFXAdaptiveOff)
		self.animLodToggle.SetToggleDownEvent(self.__OnToggleAnimLODOn)
		self.animLodToggle.SetToggleUpEvent(self.__OnToggleAnimLODOff)
		self.textTailOptToggle.SetToggleDownEvent(self.__OnToggleTextTailOptOn)
		self.textTailOptToggle.SetToggleUpEvent(self.__OnToggleTextTailOptOff)
		self.textTailRangeController.SetEvent(ui.__mem_func__(self.OnChangeTextTailOptRange))

		self.__SetCurTilingMode()
		self.__SetCurFPSLimit()
		self.__SetCurVSync()
		self.__SetCurPerfProfile()
		self.__SetCurPerformanceToggles()
		self.__SetCurShadowCadence()
		self.__SetCurTextTailOptRange()

		# MR-14: Fog update by Alaric
		self.__ClickRadioButton(self.fogModeButtonList, systemSetting.GetFogLevel())
		# MR-14: -- END OF -- Fog update by Alaric
		self.__ClickRadioButton(self.cameraModeButtonList, constInfo.GET_CAMERA_MAX_DISTANCE_INDEX())

		if musicInfo.fieldMusic==musicInfo.METIN2THEMA:
			self.selectMusicFile.SetText(uiSelectMusic.DEFAULT_THEMA)
		else:
			self.selectMusicFile.SetText(musicInfo.fieldMusic[:MUSIC_FILENAME_MAX_LEN])

	def __OnClickTilingModeCPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_3)
		self.__SetTilingMode(0)

	def __OnClickTilingModeGPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_3)
		self.__SetTilingMode(1)

	def __OnClickTilingApplyButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_TILING_EXIT)
		if 0==self.tilingMode:
			background.EnableSoftwareTiling(1)
		else:
			background.EnableSoftwareTiling(0)

		net.ExitGame()

	def __OnClickChangeMusicButton(self):
		if not self.musicListDlg:
			
			self.musicListDlg=uiSelectMusic.FileListDialog()
			self.musicListDlg.SAFE_SetSelectEvent(self.__OnChangeMusic)

		self.musicListDlg.Open()

		
	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton=buttonList[buttonIndex]
		except IndexError:
			return

		for eachButton in buttonList:
			eachButton.SetUp()

		selButton.Down()


	def __SetTilingMode(self, index):
		self.__ClickRadioButton(self.tilingModeButtonList, index)
		self.tilingMode=index

	def __SetCameraMode(self, index):
		constInfo.SET_CAMERA_MAX_DISTANCE_INDEX(index)
		self.__ClickRadioButton(self.cameraModeButtonList, index)

	def __SetFogLevel(self, index):
		# MR-14: Fog update by Alaric
		# constInfo.SET_FOG_LEVEL_INDEX(index)
		systemSetting.SetFogLevel(index)
		# MR-14: -- END OF -- Fog update by Alaric

		self.__ClickRadioButton(self.fogModeButtonList, index)

	def __SetFPSLimit(self, index):
		if index < 0 or index >= len(self.fpsLimitValues):
			return

		self.__ClickRadioButton(self.fpsLimitButtonList, index)
		fpsLimit = self.fpsLimitValues[index]
		systemSetting.SetRenderFPSLimit(fpsLimit)

	def __SetCurFPSLimit(self):
		try:
			current = systemSetting.GetRenderFPSLimit()
		except:
			current = 60

		try:
			index = self.fpsLimitValues.index(current)
		except ValueError:
			index = 0

		self.__ClickRadioButton(self.fpsLimitButtonList, index)

	def __SetVSync(self, enabled):
		applyResult = systemSetting.SetVSync(1 if enabled else 0)
		if not applyResult:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "VSync apply failed")

		self.__SetCurVSync()

	def __SetCurVSync(self):
		try:
			isEnabled = systemSetting.GetVSync()
		except:
			isEnabled = 1

		if isEnabled:
			self.vsyncToggle.Down()
		else:
			self.vsyncToggle.SetUp()

	def __SetPerfProfile(self, index):
		if index < 0 or index > 2:
			return

		self.__ClickRadioButton(self.perfProfileButtonList, index)
		systemSetting.SetPerfProfile(index)

	def __SetCurPerfProfile(self):
		try:
			current = systemSetting.GetPerfProfile()
		except:
			current = 1

		if current < 0 or current > 2:
			current = 1

		self.__ClickRadioButton(self.perfProfileButtonList, current)

	def __SetShadowCadence(self, cadence):
		if cadence < 1 or cadence > 3:
			return

		self.__ClickRadioButton(self.shadowCadenceButtonList, cadence - 1)
		systemSetting.SetShadowCadence(cadence)

	def __SetCurShadowCadence(self):
		try:
			cadence = systemSetting.GetShadowCadence()
		except:
			cadence = 2

		if cadence < 1 or cadence > 3:
			cadence = 2

		self.__ClickRadioButton(self.shadowCadenceButtonList, cadence - 1)

	def __SetPerfToggle(self, setter, enabled):
		setter(1 if enabled else 0)
		self.__SetCurPerformanceToggles()

	def __SliderPosToTextTailRange(self, sliderPos):
		if sliderPos < 0.0:
			sliderPos = 0.0
		elif sliderPos > 1.0:
			sliderPos = 1.0

		value = int(TEXTTAIL_RANGE_MIN + (TEXTTAIL_RANGE_MAX - TEXTTAIL_RANGE_MIN) * sliderPos + 0.5)
		value = int((value + 50) / 100) * 100
		if value < TEXTTAIL_RANGE_MIN:
			value = TEXTTAIL_RANGE_MIN
		elif value > TEXTTAIL_RANGE_MAX:
			value = TEXTTAIL_RANGE_MAX
		return value

	def __TextTailRangeToSliderPos(self, value):
		if value < TEXTTAIL_RANGE_MIN:
			value = TEXTTAIL_RANGE_MIN
		elif value > TEXTTAIL_RANGE_MAX:
			value = TEXTTAIL_RANGE_MAX
		return float(value - TEXTTAIL_RANGE_MIN) / float(TEXTTAIL_RANGE_MAX - TEXTTAIL_RANGE_MIN)

	def __SetCurTextTailOptRange(self):
		try:
			value = systemSetting.GetTextTailOptRange()
		except:
			value = 3500

		if value < TEXTTAIL_RANGE_MIN:
			value = TEXTTAIL_RANGE_MIN
		elif value > TEXTTAIL_RANGE_MAX:
			value = TEXTTAIL_RANGE_MAX

		self.textTailRangeController.SetSliderPos(self.__TextTailRangeToSliderPos(value))
		self.textTailRangeValue.SetText(str(value))

	def __SetCurPerformanceToggles(self):
		try:
			fxAdaptive = systemSetting.GetFXAdaptive()
		except:
			fxAdaptive = 1

		try:
			animLod = systemSetting.GetAnimLOD()
		except:
			animLod = 1

		try:
			textTailOpt = systemSetting.GetTextTailOpt()
		except:
			textTailOpt = 1

		if fxAdaptive:
			self.fxAdaptiveToggle.Down()
		else:
			self.fxAdaptiveToggle.SetUp()

		if animLod:
			self.animLodToggle.Down()
		else:
			self.animLodToggle.SetUp()

		if textTailOpt:
			self.textTailOptToggle.Down()
		else:
			self.textTailOptToggle.SetUp()

	def OnChangeTextTailOptRange(self):
		value = self.__SliderPosToTextTailRange(self.textTailRangeController.GetSliderPos())
		self.textTailRangeValue.SetText(str(value))
		systemSetting.SetTextTailOptRange(value)

	def __OnClickCameraModeShortButton(self):
		self.__SetCameraMode(0)

	def __OnClickCameraModeLongButton(self):
		self.__SetCameraMode(1)

	def __OnClickFogModeLevel0Button(self):
		self.__SetFogLevel(0)

	def __OnClickFogModeLevel1Button(self):
		self.__SetFogLevel(1)

	def __OnClickFogModeLevel2Button(self):
		self.__SetFogLevel(2)

	def __OnClickFPS60Button(self):
		self.__SetFPSLimit(0)

	def __OnClickFPS90Button(self):
		self.__SetFPSLimit(1)

	def __OnClickFPS120Button(self):
		self.__SetFPSLimit(2)

	def __OnClickFPSUnlimitedButton(self):
		self.__SetFPSLimit(3)

	def __OnToggleVSyncOn(self):
		self.__SetVSync(True)

	def __OnToggleVSyncOff(self):
		self.__SetVSync(False)

	def __OnClickPerfProfileQualityButton(self):
		self.__SetPerfProfile(0)

	def __OnClickPerfProfileBalancedButton(self):
		self.__SetPerfProfile(1)

	def __OnClickPerfProfilePerformanceButton(self):
		self.__SetPerfProfile(2)

	def __OnToggleFXAdaptiveOn(self):
		self.__SetPerfToggle(systemSetting.SetFXAdaptive, True)

	def __OnToggleFXAdaptiveOff(self):
		self.__SetPerfToggle(systemSetting.SetFXAdaptive, False)

	def __OnToggleAnimLODOn(self):
		self.__SetPerfToggle(systemSetting.SetAnimLOD, True)

	def __OnToggleAnimLODOff(self):
		self.__SetPerfToggle(systemSetting.SetAnimLOD, False)

	def __OnToggleTextTailOptOn(self):
		self.__SetPerfToggle(systemSetting.SetTextTailOpt, True)

	def __OnToggleTextTailOptOff(self):
		self.__SetPerfToggle(systemSetting.SetTextTailOpt, False)

	def __OnClickShadowCadence1Button(self):
		self.__SetShadowCadence(1)

	def __OnClickShadowCadence2Button(self):
		self.__SetShadowCadence(2)

	def __OnClickShadowCadence3Button(self):
		self.__SetShadowCadence(3)

	def __OnChangeMusic(self, fileName):
		self.selectMusicFile.SetText(fileName[:MUSIC_FILENAME_MAX_LEN])

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

		if fileName==uiSelectMusic.DEFAULT_THEMA:
			musicInfo.fieldMusic=musicInfo.METIN2THEMA
		else:
			musicInfo.fieldMusic=fileName

		musicInfo.SaveLastPlayFieldMusic()
		
		if musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	def OnChangeMusicVolume(self):
		pos = self.ctrlMusicVolume.GetSliderPos()
		snd.SetMusicVolume(pos)
		systemSetting.SetMusicVolume(pos)

	def OnChangeSoundVolume(self):
		pos = self.ctrlSoundVolume.GetSliderPos()
		snd.SetSoundVolume(pos)
		systemSetting.SetSoundVolume(pos)

	def OnChangeShadowQuality(self):
		pos = self.ctrlShadowQuality.GetSliderPos()
		systemSetting.SetShadowLevel(int(pos / 0.2))

	def OnCloseInputDialog(self):
		self.inputDialog.Close()
		self.inputDialog = None
		return True

	def OnCloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog = None
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True
	
	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.__SetCurTilingMode()
		self.Hide()

	def __SetCurTilingMode(self):
		if background.IsSoftwareTiling():
			self.__SetTilingMode(0)
		else:
			self.__SetTilingMode(1)	

	def __NotifyChatLine(self, text):
		chat.AppendChat(chat.CHAT_TYPE_INFO, text)
		
