import urllib
import dbg
import app
import net
import ui
import ime
import snd
import wndMgr
import musicInfo
import serverInfo
import systemSetting
import ServerStateChecker
import locale
import constInfo
import uiCommon
import time
import ServerCommandParser
import ime
import uiScriptLocale
import chat
import sys
import md5
import background
import string

##INTROLOGIN VON DASKUCHEN##

DEINEIP = "185.5.173.22"
CHANNELAZ = 4
CH1PORT = 13070
CH2PORT = 14070
CH3PORT = 99999
CH4PORT = 99999
AUTHPORT = 11002

##FRAGEN = 1 nicht verändern
FRAGEN = 1

#########################

RUNUP_MATRIX_AUTH = FALSE
NEWCIBN_PASSPOD_AUTH = FALSE

LOGIN_DELAY_SEC = 0.0
SKIP_LOGIN_PHASE = FALSE
SKIP_LOGIN_PHASE_SUPPORT_CHANNEL = FALSE
FULL_BACK_IMAGE = TRUE

PASSPOD_MSG_DICT = {}

VIRTUAL_KEYBOARD_NUM_KEYS = 46
VIRTUAL_KEYBOARD_RAND_KEY = FALSE

def Suffle(src):
	if VIRTUAL_KEYBOARD_RAND_KEY:
		items = [item for item in src]

		itemCount = len(items)
		for oldPos in xrange(itemCount):
			newPos = app.GetRandom(0, itemCount-1)
			items[newPos], items[oldPos] = items[oldPos], items[newPos]

		return "".join(items)
	else:
		return src

if locale.IsNEWCIBN() or locale.IsCIBN10():
	LOGIN_DELAY_SEC = 20.0
	FULL_BACK_IMAGE = TRUE
	NEWCIBN_PASSPOD_AUTH = TRUE
	PASSPOD_MSG_DICT = {
		"PASERR1"	: locale.LOGIN_FAILURE_PASERR1,
		"PASERR2"	: locale.LOGIN_FAILURE_PASERR2,
		"PASERR3"	: locale.LOGIN_FAILURE_PASERR3,
		"PASERR4"	: locale.LOGIN_FAILURE_PASERR4,
		"PASERR5"	: locale.LOGIN_FAILURE_PASERR5,
	}

elif locale.IsYMIR() or locale.IsCHEONMA():
	FULL_BACK_IMAGE = TRUE

elif locale.IsHONGKONG():
	FULL_BACK_IMAGE = TRUE
	RUNUP_MATRIX_AUTH = TRUE 
	PASSPOD_MSG_DICT = {
		"NOTELE"	: locale.LOGIN_FAILURE_NOTELEBLOCK,
	}

elif locale.IsJAPAN():
	FULL_BACK_IMAGE = TRUE

def IsFullBackImage():
	global FULL_BACK_IMAGE
	return FULL_BACK_IMAGE

def IsLoginDelay():
	global LOGIN_DELAY_SEC
	if LOGIN_DELAY_SEC > 0.0:
		return TRUE
	else:
		return FALSE

def IsRunupMatrixAuth():
	global RUNUP_MATRIX_AUTH
	return RUNUP_MATRIX_AUTH	

def IsNEWCIBNPassPodAuth():
	global NEWCIBN_PASSPOD_AUTH
	return NEWCIBN_PASSPOD_AUTH

def GetLoginDelay():
	global LOGIN_DELAY_SEC
	return LOGIN_DELAY_SEC

app.SetGuildMarkPath("test")

class ConnectingDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.eventTimeOver = lambda *arg: None
		self.eventExit = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/ConnectingDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.countdownMessage = self.GetChild("countdown_message")

		except:
			import exception
			exception.Abort("ConnectingDialog.LoadDialog.BindObject")

	def Open(self, waitTime):
		curTime = time.clock()
		self.endTime = curTime + waitTime

		self.Lock()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()		

	def Close(self):
		self.onPressKeyDict = None
		self.Unlock()
		self.Hide()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

	def SetText(self, text):
		self.message.SetText(text)

	def SetCountDownMessage(self, waitTime):
		self.countdownMessage.SetText("%.0f%s" % (waitTime, locale.SECOND))

	def SAFE_SetTimeOverEvent(self, event):
		self.eventTimeOver = ui.__mem_func__(event)

	def SAFE_SetExitEvent(self, event):
		self.eventExit = ui.__mem_func__(event)

	def OnUpdate(self):
		lastTime = max(0, self.endTime - time.clock())
		if 0 == lastTime:
			self.Close()
			self.eventTimeOver()
		else:
			self.SetCountDownMessage(self.endTime - time.clock())

	def OnPressExitKey(self):
		#self.eventExit()
		return TRUE

class LoginWindow(ui.ScriptWindow):

	IS_TEST = net.IsTest()

	def __init__(self, stream):
		print "NEW LOGIN WINDOW  ----------------------------------------------------------------------------"
		ui.ScriptWindow.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(self)

		self.matrixInputChanceCount = 0
		self.lastLoginTime = 0
		self.inputDialog = None
		self.connectingDialog = None
		self.stream=stream
		self.isNowCountDown=FALSE
		self.isStartError=FALSE

		self.xServerBoard = 0
		self.yServerBoard = 0
		
		self.loadingImage = None


		
	def __del__(self):
		net.ClearPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(0)
		ui.ScriptWindow.__del__(self)
		print "---------------------------------------------------------------------------- DELETE LOGIN WINDOW"

	def Open(self):
		ServerStateChecker.Create(self)

		print "LOGIN WINDOW OPEN ----------------------------------------------------------------------------"

		self.loginFailureMsgDict={
			#"DEFAULT" : locale.LOGIN_FAILURE_UNKNOWN,

			"ALREADY"	: locale.LOGIN_FAILURE_ALREAY,
			"NOID"		: locale.LOGIN_FAILURE_NOT_EXIST_ID,
			"WRONGPWD"	: locale.LOGIN_FAILURE_WRONG_PASSWORD,
			"FULL"		: locale.LOGIN_FAILURE_TOO_MANY_USER,
			"SHUTDOWN"	: locale.LOGIN_FAILURE_SHUTDOWN,
			"REPAIR"	: locale.LOGIN_FAILURE_REPAIR_ID,
			"BLOCK"		: locale.LOGIN_FAILURE_BLOCK_ID,
			"WRONGMAT"	: locale.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER,
			"QUIT"		: locale.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER_TRIPLE,
			"BESAMEKEY"	: locale.LOGIN_FAILURE_BE_SAME_KEY,
			"NOTAVAIL"	: locale.LOGIN_FAILURE_NOT_AVAIL,
			"NOBILL"	: locale.LOGIN_FAILURE_NOBILL,
			"BLKLOGIN"	: locale.LOGIN_FAILURE_BLOCK_LOGIN,
			"WEBBLK"	: locale.LOGIN_FAILURE_WEB_BLOCK,
			
			"HACK"		: "Du wurdest wegen hacken gesperrt.",
			"BOT"		: "Du wurdest wegen benutzung von Bots gesperrt.",
			"SCAM"		: "Du wurdest wegen Betrug gesperrt.",
			"INSULT"	: "Du wurdest wegen Beleidigung gesperrt.",
			"FAKE"		: "Du wurdest aufgrund deiner Namensgebung gesperrt.",
			"NAME"		: "Du wurdest aufgrund deiner Namensgebung gesperrt.",
			"BUG"		: "Du wurdest wegen Bugusing gesperrt.",
			"DK"		: "Du wurdest wegen Dauerkill gesperrt.",
			"OTHER"		: "Du wurdest von der Serverleitung gesperrt.",
		}

		self.loginFailureFuncDict = {
			"WRONGPWD"	: self.__DisconnectAndInputPassword,
			"WRONGMAT"	: self.__DisconnectAndInputMatrix,
			"QUIT"		: app.Exit,
		}

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("LoginWindow")

		if not self.__LoadScript(uiScriptLocale.LOCALE_UISCRIPT_PATH + "LoginWindow.py"):
			dbg.TraceError("LoginWindow.Open - __LoadScript Error")
			return
		
		self.__LoadLoginInfo("loginInfo.py")
		
		if app.loggined:
			self.loginFailureFuncDict = {
			"WRONGPWD"	: app.Exit,
			"WRONGMAT"	: app.Exit,
			"QUIT"		: app.Exit,
			}

		if musicInfo.loginMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/"+musicInfo.loginMusic)

		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		# pevent key "[" "]"
		ime.AddExceptKey(91)
		ime.AddExceptKey(93)
			
		self.Show()

		global SKIP_LOGIN_PHASE
		if SKIP_LOGIN_PHASE:
			if self.isStartError:
				self.connectBoard.Hide()
				self.loginBoard.Hide()
				self.serverBoard.Hide()
				self.PopupNotifyMessage(locale.LOGIN_CONNECT_FAILURE, self.__ExitGame)
				return

			if self.loginInfo:
				self.serverBoard.Hide()
			else:
				self.__RefreshServerList()
				self.__OpenServerBoard()
		else:
			connectingIP = self.stream.GetConnectAddr()
			if connectingIP:
				self.__OpenLoginBoard()
				if IsFullBackImage():
					self.GetChild("bg1").Show()
					self.GetChild("bg2").Hide()

			else:
				self.__RefreshServerList()
				self.__OpenServerBoard()

		app.ShowCursor()


	def Close(self):

		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		ServerStateChecker.Destroy(self)

		print "---------------------------------------------------------------------------- CLOSE LOGIN WINDOW "
		#
		# selectMusicÀÌ ŸøÀžžé BGMÀÌ ²÷±â¹Ç·Î µÎ°³ ŽÙ ÃŒÅ©ÇÑŽÙ. 
		#
		if musicInfo.loginMusic != "" and musicInfo.selectMusic != "":
			snd.FadeOutMusic("BGM/"+musicInfo.loginMusic)

		## NOTE : idEditLine¿Í pwdEditLineÀº ÀÌº¥Æ®°¡ Œ­·Î ¿¬°á µÇŸîÀÖŸîŒ­
		##        EventžŠ °­ÁŠ·Î ÃÊ±âÈ­ ÇØÁÖŸîŸßžž ÇÕŽÏŽÙ - [levites]
		self.idEditLine.SetTabEvent(0)
		self.idEditLine.SetReturnEvent(0)
		self.pwdEditLine.SetReturnEvent(0)
		self.pwdEditLine.SetTabEvent(0)

		self.connectBoard = None
		self.loginBoard = None
		self.BGBoard = None
		self.idEditLine = None
		self.pwdEditLine = None
		self.inputDialog = None
		self.connectingDialog = None
		self.loadingImage = None

		self.serverBoard				= None
		self.serverList					= None
		self.channelList				= None

		# RUNUP_MATRIX_AUTH
		self.matrixQuizBoard	= None
		self.matrixAnswerInput	= None
		self.matrixAnswerOK	= None
		self.matrixAnswerCancel	= None
		# RUNUP_MATRIX_AUTH_END

		# NEWCIBN_PASSPOD_AUTH
		self.passpodBoard	= None
		self.passpodAnswerInput	= None
		self.passpodAnswerOK	= None
		self.passpodAnswerCancel = None
		# NEWCIBN_PASSPOD_AUTH_END

		self.VIRTUAL_KEY_ALPHABET_LOWERS = None
		self.VIRTUAL_KEY_ALPHABET_UPPERS = None
		self.VIRTUAL_KEY_SYMBOLS = None
		self.VIRTUAL_KEY_NUMBERS = None

		# VIRTUAL_KEYBOARD_BUG_FIX
		

		self.KillFocus()
		self.Hide()

		self.stream.popupWindow.Close()
		self.loginFailureFuncDict=None

		ime.ClearExceptKey()

		app.HideCursor()

	def __SaveChannelInfo(self):
		try:
			file=open("channel.inf", "w")
			file.write("%d %d %d" % (self.__GetServerID(), self.__GetChannelID(), self.__GetRegionID()))
		except:
			print "LoginWindow.__SaveChannelInfo - SaveError"

	def __LoadChannelInfo(self):
		try:
			file=open("channel.inf")
			lines=file.readlines()
			
			if len(lines)>0:
				tokens=lines[0].split()

				selServerID=int(tokens[0])
				selChannelID=int(tokens[1])
				
				if len(tokens) == 3:
					regionID = int(tokens[2])

				return regionID, selServerID, selChannelID

		except:
			print "LoginWindow.__LoadChannelInfo - OpenError"
			return -1, -1, -1

	def __ExitGame(self):
		app.Exit()

	def SetIDEditLineFocus(self):
		if self.idEditLine != None:
			self.idEditLine.SetFocus()

	def SetPasswordEditLineFocus(self):
		if locale.IsEUROPE():
			if self.idEditLine != None: #0000862: [M2EU] ·Î±×ÀÎÃ¢ ÆËŸ÷ ¿¡·¯: ÁŸ·áœÃ žÕÀú None Œ³Á€µÊ
				self.idEditLine.SetText("")
				self.idEditLine.SetFocus() #0000685: [M2EU] ŸÆÀÌµð/ºñ¹Ð¹øÈ£ À¯Ãß °¡ŽÉ ¹ö±× ŒöÁ€: ¹«Á¶°Ç ŸÆÀÌµð·Î Æ÷Ä¿œº°¡ °¡°Ô žžµçŽÙ

			if self.pwdEditLine != None: #0000862: [M2EU] ·Î±×ÀÎÃ¢ ÆËŸ÷ ¿¡·¯: ÁŸ·áœÃ žÕÀú None Œ³Á€µÊ
				self.pwdEditLine.SetText("")
		else:
			if self.pwdEditLine != None:
				self.pwdEditLine.SetFocus()								

	def OnEndCountDown(self):
		self.isNowCountDown = FALSE
		self.OnConnectFailure()

	def OnConnectFailure(self):

		if self.isNowCountDown:
			return

		snd.PlaySound("sound/ui/loginfail.wav")

		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		if app.loggined:
			self.PopupNotifyMessage(locale.LOGIN_CONNECT_FAILURE, self.__ExitGame)
		else:
			self.PopupNotifyMessage(locale.LOGIN_CONNECT_FAILURE, self.SetPasswordEditLineFocus)

	def OnHandShake(self):
		if not IsLoginDelay():
			snd.PlaySound("sound/ui/loginok.wav")
			self.PopupDisplayMessage(locale.LOGIN_CONNECT_SUCCESS)

	def OnLoginStart(self):
		if not IsLoginDelay():
			self.PopupDisplayMessage(locale.LOGIN_PROCESSING)

	def OnLoginFailure(self, error):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		try:
			loginFailureMsg = self.loginFailureMsgDict[error]
		except KeyError:
			if PASSPOD_MSG_DICT:
				try:
					loginFailureMsg = PASSPOD_MSG_DICT[error]
				except KeyError:
					loginFailureMsg = locale.LOGIN_FAILURE_UNKNOWN + error
			else:
				loginFailureMsg = locale.LOGIN_FAILURE_UNKNOWN  + error


		#0000685: [M2EU] ŸÆÀÌµð/ºñ¹Ð¹øÈ£ À¯Ãß °¡ŽÉ ¹ö±× ŒöÁ€: ¹«Á¶°Ç ÆÐœº¿öµå·Î Æ÷Ä¿œº°¡ °¡°Ô žžµçŽÙ
		loginFailureFunc=self.loginFailureFuncDict.get(error, self.SetPasswordEditLineFocus)

		if app.loggined:
			self.PopupNotifyMessage(loginFailureMsg, self.__ExitGame)
		else:
			self.PopupNotifyMessage(loginFailureMsg, loginFailureFunc)

		snd.PlaySound("sound/ui/loginfail.wav")

	def __DisconnectAndInputID(self):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		self.SetIDEditLineFocus()
		net.Disconnect()

	def __DisconnectAndInputPassword(self):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		self.SetPasswordEditLineFocus()
		net.Disconnect()

	def __DisconnectAndInputMatrix(self):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		self.stream.popupWindow.Close()
		self.matrixInputChanceCount -= 1

		if self.matrixInputChanceCount <= 0:
			self.__OnCloseInputDialog()

		elif self.inputDialog:
			self.inputDialog.Show()

	def __LoadScript(self, fileName):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("LoginWindow.__LoadScript.LoadObject")

		try:
			GetObject=self.GetChild
			self.serverBoard			= GetObject("ServerBoard")
			self.serverList				= GetObject("ServerList")
			self.channelList			= GetObject("ChannelList")
			self.serverSelectButton		= GetObject("ServerSelectButton")			
			self.serverExitButton		= GetObject("ServerExitButton")
			self.connectBoard			= GetObject("ConnectBoard")
			self.loginBoard				= GetObject("LoginBoard")
			self.BGBoard				= GetObject("BGBoard")
			self.idEditLine				= GetObject("ID_EditLine")
			self.pwdEditLine			= GetObject("Password_EditLine")
			self.Channel1Button	= GetObject("Channel1Button")
			self.Channel2Button	= GetObject("Channel2Button")
			self.Channel3Button	= GetObject("Channel3Button")
			self.Channel4Button	= GetObject("Channel4Button")			
			self.loginButton			= GetObject("LoginButton")
			self.loginExitButton		= GetObject("LoginExitButton")
			
			## ACCMANAGER
			
			self.acc1loginButton		= GetObject("Acc1Login")
			self.acc2loginButton		= GetObject("Acc2Login")
			self.acc3loginButton		= GetObject("Acc3Login")
			self.LoginSaveButton		= GetObject("LoginSaveButton")
			self.ACC1_LABEL		= GetObject("ACC1_LABEL")
			self.ACC2_LABEL		= GetObject("ACC2_LABEL")
			self.ACC3_LABEL		= GetObject("ACC3_LABEL")
			self.ACC1__LABEL		= GetObject("ACC1__LABEL")
			self.ACC2__LABEL		= GetObject("ACC2__LABEL")
			self.ACC3__LABEL		= GetObject("ACC3__LABEL")
			self.serverInfo				= GetObject("ConnectName")
			
			self.Acc1Del		= GetObject("Acc1Del")
			self.Acc2Del		= GetObject("Acc2Del")
			self.Acc3Del		= GetObject("Acc3Del")
			
			# RUNUP_MATRIX_AUTH
			if IsRunupMatrixAuth():
				self.matrixQuizBoard	= GetObject("RunupMatrixQuizBoard")
				self.matrixAnswerInput	= GetObject("RunupMatrixAnswerInput")
				self.matrixAnswerOK	= GetObject("RunupMatrixAnswerOK")
				self.matrixAnswerCancel	= GetObject("RunupMatrixAnswerCancel")
			# RUNUP_MATRIX_AUTH_END

			# NEWCIBN_PASSPOD_AUTH
			if IsNEWCIBNPassPodAuth():
				self.passpodBoard	= GetObject("NEWCIBN_PASSPOD_BOARD")
				self.passpodAnswerInput	= GetObject("NEWCIBN_PASSPOD_INPUT")
				self.passpodAnswerOK	= GetObject("NEWCIBN_PASSPOD_OK")
				self.passpodAnswerCancel= GetObject("NEWCIBN_PASSPOD_CANCEL")
			# NEWCIBN_PASSPOD_AUTH_END

			self.virtualKeyboard		= self.GetChild2("VirtualKeyboard")
			self.AccountBoard		= self.GetChild2("AccountBoard")
			self.AccEditBoard		= self.GetChild2("AccEditBoard")


		except:
			import exception
			exception.Abort("LoginWindow.__LoadScript.BindObject")

		if self.IS_TEST:
			self.Channel1Button.Hide()
		else:
			self.Channel1Button.SetEvent(ui.__mem_func__(self.__OnClickChannel1Button))

		self.serverBoard.OnKeyUp = ui.__mem_func__(self.__ServerBoard_OnKeyUp)
		self.xServerBoard, self.yServerBoard = self.serverBoard.GetLocalPosition()

		self.serverSelectButton.SetEvent(ui.__mem_func__(self.__OnClickSelectServerButton))
		self.serverExitButton.SetEvent(ui.__mem_func__(self.__OnClickExitButton))

		self.loginButton.SetEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.loginExitButton.SetEvent(ui.__mem_func__(self.__OnClickExitButton))
		
		## ACCMANAGER
		
		self.acc1loginButton.SetEvent(ui.__mem_func__(self.__OnClickACC1LoginButton))
		self.acc2loginButton.SetEvent(ui.__mem_func__(self.__OnClickACC2LoginButton))
		self.acc3loginButton.SetEvent(ui.__mem_func__(self.__OnClickACC3LoginButton))
		self.LoginSaveButton.SetEvent(ui.__mem_func__(self.__OnClickLoginSaveButton))
		
		self.Acc1Del.SetEvent(ui.__mem_func__(self.__OnClickAcc1DelButton))
		self.Acc2Del.SetEvent(ui.__mem_func__(self.__OnClickAcc2DelButton))
		self.Acc3Del.SetEvent(ui.__mem_func__(self.__OnClickAcc3DelButton))
		
		#self.Frage.SetEvent(ui.__mem_func__(self.__OnClickFrageLABEL))

		## END ACCMANAGER
		
		self.serverList.SetEvent(ui.__mem_func__(self.__OnSelectServer))
		
		self.idEditLine.SetReturnEvent(ui.__mem_func__(self.pwdEditLine.SetFocus))
		self.idEditLine.SetTabEvent(ui.__mem_func__(self.pwdEditLine.SetFocus))

		self.pwdEditLine.SetReturnEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.pwdEditLine.SetTabEvent(ui.__mem_func__(self.idEditLine.SetFocus))

		# RUNUP_MATRIX_AUTH
		if IsRunupMatrixAuth():			
			self.matrixAnswerOK.SAFE_SetEvent(self.__OnClickMatrixAnswerOK)
			self.matrixAnswerCancel.SAFE_SetEvent(self.__OnClickMatrixAnswerCancel)
			self.matrixAnswerInput.SAFE_SetReturnEvent(self.__OnClickMatrixAnswerOK)
		# RUNUP_MATRIX_AUTH_END

		# NEWCIBN_PASSPOD_AUTH
		if IsNEWCIBNPassPodAuth():
			self.passpodAnswerOK.SAFE_SetEvent(self.__OnClickNEWCIBNPasspodAnswerOK)
			self.passpodAnswerCancel.SAFE_SetEvent(self.__OnClickNEWCIBNPasspodAnswerCancel)
			self.passpodAnswerInput.SAFE_SetReturnEvent(self.__OnClickNEWCIBNPasspodAnswerOK)

		# NEWCIBN_PASSPOD_AUTH_END


		if IsFullBackImage():
			self.GetChild("bg1").Show()
			self.GetChild("bg2").Hide()
		return 1

				
	def Connect(self, id, pwd):
		if constInfo.SEQUENCE_PACKET_ENABLE:
			net.SetPacketSequenceMode()

		if IsLoginDelay():
			loginDelay = GetLoginDelay()
			self.connectingDialog = ConnectingDialog()
			self.connectingDialog.Open(loginDelay)
			self.connectingDialog.SAFE_SetTimeOverEvent(self.OnEndCountDown)
			self.connectingDialog.SAFE_SetExitEvent(self.OnPressExitKey)
			self.isNowCountDown = TRUE

		else:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(locale.LOGIN_CONNETING, self.SetPasswordEditLineFocus, locale.UI_CANCEL)

		self.stream.SetLoginInfo(id, pwd)
		self.stream.Connect()

	## ACCMANAGER			
	def __LoadACCNames(self):

		fd = open( "Settings/loginsetting1.cfg" )
		login1 = fd.readline()
		login1.replace( "\n", "" )
		fd.close()

		fd = open( "Settings/loginsetting2.cfg" )
		login2 = fd.readline()
		login2.replace( "\n", "" )
		fd.close()

		fd = open( "Settings/loginsetting3.cfg" )
		login3 = fd.readline()
		login3.replace( "\n", "" )
		fd.close()

		fd = open( "Settings/loginsetting4.cfg" )
		login4 = fd.readline()
		login4.replace( "\n", "" )
		fd.close()
	
		if login1 != "":
			self.ACC1__LABEL.SetText(login1)
			self.ACC1_LABEL.SetText(login1)
		if login2 != "":
			self.ACC2__LABEL.SetText(login2)
			self.ACC2_LABEL.SetText(login2)
		if login3 != "":
			self.ACC3__LABEL.SetText(login3)
			self.ACC3_LABEL.SetText(login3)
	
	def __LoadACCInfos(self, accid):
		import linecache
		login = linecache.getline("Settings/loginsetting" + str(accid) + ".cfg", 1)
		password = linecache.getline("Settings/loginsetting" + str(accid) + ".cfg", 2)
		login = login.replace('\n', '')
		self.Connect(login, password)
	
	def __OnClickACC1LoginButton(self):
		self.__LoadACCInfos(1)
	
	def __OnClickACC2LoginButton(self):
		self.__LoadACCInfos(2)
	
	def __OnClickACC3LoginButton(self):
		self.__LoadACCInfos(3)
	
	def __OnClickLoginSaveButton(self):
		id = self.idEditLine.GetText()
		pwd = self.pwdEditLine.GetText()
		
		fd = open( "Settings/loginsetting1.cfg" )
		login1 = fd.readline()
		login1.replace( "\n", "" )
		fd.close()

		fd = open( "Settings/loginsetting2.cfg" )
		login2 = fd.readline()
		login2.replace( "\n", "" )
		fd.close()

		fd = open( "Settings/loginsetting3.cfg" )
		login3 = fd.readline()
		login3.replace( "\n", "" )
		fd.close()

		fd = open( "Settings/loginsetting4.cfg" )
		login4 = fd.readline()
		login4.replace( "\n", "" )
		fd.close()
		
		if login1 == "":
			slot = 1
		elif login2 == "":
			slot = 2
		elif login3 == "":
			slot = 3
		elif login4 == "":
			slot = 4
		else:
			self.PopupNotifyMessage("Es ist kein Slot zum speichern frei!")
			return
		
		
		f = open("Settings/loginsetting" + str(slot) + ".cfg", "w")
		f.write (id +"\n")
		f.write (pwd)
		f.close()
		
		self.PopupNotifyMessage("Deine Login-Daten wurden gespeichert!")
		self.__LoadACCNames()
	
	def __OnClickAcc1DelButton(self):
		f = open("Settings/loginsetting1.cfg", "w")
		f.write ("")
		f.close()
		self.ACC1__LABEL.SetText("-")
		self.ACC1_LABEL.SetText("-")
		self.__LoadACCNames()
		
	def __OnClickAcc2DelButton(self):
		f = open("Settings/loginsetting2.cfg", "w")
		f.write ("")
		f.close()
		self.ACC2__LABEL.SetText("-")
		self.ACC2_LABEL.SetText("-")
		self.__LoadACCNames()
	def __OnClickAcc3DelButton(self):
		f = open("Settings/loginsetting3.cfg", "w")
		f.write ("")
		f.close()
		self.ACC3__LABEL.SetText("-")
		self.ACC3_LABEL.SetText("-")
		self.__LoadACCNames()
	
	def __OnClickExitButton(self):
		self.stream.SetPhaseWindow(0)

	def __SetServerInfo(self, name):
		net.SetServerInfo(name.strip())

	def __LoadLoginInfo(self, loginInfoFileName):

		try:
			loginInfo={}
			execfile(loginInfoFileName, loginInfo)
		except IOError:
			print(\
				"ÀÚµ¿ ·Î±×ÀÎÀ» ÇÏœÃ·Ážé" + loginInfoFileName + "ÆÄÀÏÀ» ÀÛŒºÇØÁÖŒŒ¿ä\n"\
				"\n"\
				"³»¿ë:\n"\
				"================================================================\n"\
				"addr=ÁÖŒÒ\n"\
				"port=Æ÷Æ®\n"\
				"id=ŸÆÀÌµð\n"\
				"pwd=ºñ¹Ð¹øÈ£\n"\
				"slot=Ä³ž¯ÅÍ Œ±ÅÃ ÀÎµŠœº (Ÿø°Å³ª -1ÀÌžé ÀÚµ¿ Œ±ÅÃ ŸÈÇÔ)\n"\
				"autoLogin=ÀÚµ¿ Á¢ŒÓ ¿©ºÎ\n"
				"autoSelect=ÀÚµ¿ Á¢ŒÓ ¿©ºÎ\n"
				"locale=(ymir) LC_Ymir ÀÏ°æ¿ì ymir·Î ÀÛµ¿. ÁöÁ€ÇÏÁö ŸÊÀžžé korea·Î ÀÛµ¿\n"
			);

		id=loginInfo.get("id", "")
		pwd=loginInfo.get("pwd", "")

		if self.IS_TEST:
			try:
				addr=loginInfo["addr"]
				port=loginInfo["port"]
				account_addr=addr
				account_port=port

				net.SetMarkServer(addr, port)
				self.__SetServerInfo(locale.CHANNEL_TEST_SERVER_ADDR % (addr, port))
			except:
				try:
					addr=serverInfo.TESTADDR["ip"]
					port=serverInfo.TESTADDR["tcp_port"]

					net.SetMarkServer(addr, port)
					self.__SetServerInfo(locale.CHANNEL_TEST_SERVER)
				except:
					import exception
					exception.Abort("LoginWindow.__LoadLoginInfo - Å×œºÆ®Œ­¹ö ÁÖŒÒ°¡ ŸøœÀŽÏŽÙ")

		else:
			addr=loginInfo.get("addr", "")
			port=loginInfo.get("port", 0)
			account_addr=loginInfo.get("account_addr", addr)
			account_port=loginInfo.get("account_port", port)

			locale = loginInfo.get("locale", "")

			if addr and port:
				net.SetMarkServer(addr, port)

				if locale == "ymir" :
					net.SetServerInfo("Ãµž¶ Œ­¹ö")
				else:
					net.SetServerInfo(addr+":"+str(port))

		slot=loginInfo.get("slot", 0)
		isAutoLogin=loginInfo.get("auto", 0)
		isAutoLogin=loginInfo.get("autoLogin", 0)
		isAutoSelect=loginInfo.get("autoSelect", 0)

		self.stream.SetCharacterSlot(slot)
		self.stream.SetConnectInfo(addr, port, account_addr, account_port)
		self.stream.isAutoLogin=isAutoLogin
		self.stream.isAutoSelect=isAutoSelect

		self.id = None
		self.pwd = None		
		self.loginnedServer = None
		self.loginnedChannel = None			
		app.loggined = FALSE

		self.loginInfo = loginInfo

		if self.id and self.pwd:
			app.loggined = TRUE

		if isAutoLogin:
			self.Connect(id, pwd)
			
			print "=================================================================================="
			print "ÀÚµ¿ ·Î±×ÀÎ: %s - %s:%d %s" % (loginInfoFileName, addr, port, id)
			print "=================================================================================="

		
	def PopupDisplayMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg)

	def PopupNotifyMessage(self, msg, func=0):
		if not func:
			func=self.EmptyFunc

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, locale.UI_OK)

	# RUNUP_MATRIX_AUTH
	def BINARY_OnRunupMatrixQuiz(self, quiz):
		if not IsRunupMatrixAuth():
			return

		id		= self.GetChild("RunupMatrixID")
		id.SetText(self.idEditLine.GetText())
		
		code	= self.GetChild("RunupMatrixCode")
		
		code.SetText("".join(["[%c,%c]" % (quiz[i], quiz[i+1]) for i in xrange(0, len(quiz), 2)]))

		self.stream.popupWindow.Close()
		self.serverBoard.Hide()
		self.connectBoard.Hide()
		self.loginBoard.Hide()
		self.BGBoard.Hide()
		self.matrixQuizBoard.Show()
		self.matrixAnswerInput.SetFocus()

	def __OnClickMatrixAnswerOK(self):
		answer = self.matrixAnswerInput.GetText()

		print "matrix_quiz.ok"
		net.SendRunupMatrixCardPacket(answer)
		self.matrixQuizBoard.Hide()	

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open("WAITING FOR MATRIX AUTHENTICATION", 
			self.__OnClickMatrixAnswerCancel, 
			locale.UI_CANCEL)

	def __OnClickMatrixAnswerCancel(self):
		print "matrix_quiz.cancel"

		if self.matrixQuizBoard:
			self.matrixQuizBoard.Hide()	

		if self.connectBoard:
			self.connectBoard.Show()	

		if self.loginBoard:
			self.loginBoard.Show()

	# RUNUP_MATRIX_AUTH_END

	# NEWCIBN_PASSPOD_AUTH
	def BINARY_OnNEWCIBNPasspodRequest(self):
		if not IsNEWCIBNPassPodAuth():
			return

		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		self.stream.popupWindow.Close()
		self.serverBoard.Hide()
		self.connectBoard.Hide()
		self.loginBoard.Hide()
		self.passpodBoard.Show()
		self.passpodAnswerInput.SetFocus()

	def BINARY_OnNEWCIBNPasspodFailure(self):
		if not IsNEWCIBNPassPodAuth():
			return

	def __OnClickNEWCIBNPasspodAnswerOK(self):
		answer = self.passpodAnswerInput.GetText()

		print "passpod.ok"
		net.SendNEWCIBNPasspodAnswerPacket(answer)
		self.passpodAnswerInput.SetText("")
		self.passpodBoard.Hide()	

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(locale.WAIT_FOR_PASSPOD, 
			self.__OnClickNEWCIBNPasspodAnswerCancel, 
			locale.UI_CANCEL)

	def __OnClickNEWCIBNPasspodAnswerCancel(self):
		print "passpod.cancel"

		if self.passpodBoard:
			self.passpodBoard.Hide()	

		if self.connectBoard:
			self.connectBoard.Show()	

		if self.loginBoard:
			self.loginBoard.Show()

	# NEWCIBN_PASSPOD_AUTH_END


	def OnMatrixCard(self, row1, row2, row3, row4, col1, col2, col3, col4):

		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		self.matrixInputChanceCount = 3

		self.stream.popupWindow.Close()

		# CHINA_MATRIX_CARD_BUG_FIX
		## A~Z ±îÁö 26 ÀÌ³»ÀÇ °ªÀÌ µéŸîÀÖŸîŸßžž ÇÑŽÙ.
		## Python Exception Log ¿¡Œ­ ±× ÀÌ»óÀÇ °ªÀÌ µéŸîÀÖŸîŒ­ ¿¡·¯ ¹æÁö
		## Çåµ¥ ¿Ö ÇÑ±¹ÂÊ ·Î±×¿¡Œ­ ÀÌ°Ô È°¿ëµÇŽÂÁöŽÂ žðž£°ÚÀœ
		row1 = min(30, row1)
		row2 = min(30, row2)
		row3 = min(30, row3)
		row4 = min(30, row4)
		# END_OF_CHINA_MATRIX_CARD_BUG_FIX

		row1 = chr(row1 + ord('A'))
		row2 = chr(row2 + ord('A'))
		row3 = chr(row3 + ord('A'))
		row4 = chr(row4 + ord('A'))
		col1 = col1 + 1
		col2 = col2 + 1
		col3 = col3 + 1
		col4 = col4 + 1

		inputDialog = uiCommon.InputDialogWithDescription2()
		inputDialog.SetMaxLength(8)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.__OnAcceptMatrixCardData))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.__OnCancelMatrixCardData))
		inputDialog.SetTitle(locale.INPUT_MATRIX_CARD_TITLE)
		inputDialog.SetDescription1(locale.INPUT_MATRIX_CARD_NUMBER)
		inputDialog.SetDescription2("%c%d %c%d %c%d %c%d" % (row1, col1,
															row2, col2,
															row3, col3,
															row4, col4))

		inputDialog.Open()
		self.inputDialog = inputDialog

	def __OnAcceptMatrixCardData(self):
		text = self.inputDialog.GetText()
		net.SendChinaMatrixCardPacket(text)
		if self.inputDialog:
			self.inputDialog.Hide()
		self.PopupNotifyMessage(locale.LOGIN_PROCESSING)
		return TRUE

	def __OnCancelMatrixCardData(self):
		self.SetPasswordEditLineFocus()
		self.__OnCloseInputDialog()
		self.__DisconnectAndInputPassword()
		return TRUE

	def __OnCloseInputDialog(self):
		if self.inputDialog:
			self.inputDialog.Close()
		self.inputDialog = None
		return TRUE

	def OnPressExitKey(self):
		self.stream.popupWindow.Close()
		self.stream.SetPhaseWindow(0)
		return TRUE

	def OnExit(self):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(locale.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER_TRIPLE, app.Exit, locale.UI_OK)

	def OnUpdate(self):
		ServerStateChecker.Update()

	def EmptyFunc(self):
		pass

	#####################################################################################

	def __ServerBoard_OnKeyUp(self, key):
		if self.serverBoard.IsShow():
			if app.DIK_RETURN==key:
				self.__OnClickSelectServerButton()
		return TRUE

	def __GetRegionID(self):
		return 0

	def __GetServerID(self):
		return self.serverList.GetSelectedItem()

	def __GetChannelID(self):
		return self.channelList.GetSelectedItem()

	# SEVER_LIST_BUG_FIX
	def __ServerIDToServerIndex(self, regionID, targetServerID):
		try:
			regionDict = serverInfo.REGION_DICT[regionID]
		except KeyError:
			return -1

		retServerIndex = 0
		for eachServerID, regionDataDict in regionDict.items():
			if eachServerID == targetServerID:
				return retServerIndex

			retServerIndex += 1		
		
		return -1

	def __ChannelIDToChannelIndex(self, channelID):
		return channelID - 1
	# END_OF_SEVER_LIST_BUG_FIX

	def __OpenServerBoard(self):
		global DEINEIP
		global CH1PORT
		global AUTHPORT
		global CH2PORT
		global CHANNELAZ
		self.stream.SetConnectInfo(DEINEIP, CH1PORT, DEINEIP ,AUTHPORT)
		net.SetServerInfo("Channel 1")
		net.SetMarkServer(DEINEIP, CH1PORT)
		self.serverInfo.SetText("Channel 1")
		app.SetGuildMarkPath("10.tga")
		app.SetGuildSymbolPath("10")

		self.Channel1Button.SetEvent(ui.__mem_func__(self.__OnClickChannel1Button))
		self.Channel2Button.SetEvent(ui.__mem_func__(self.__OnClickChannel2Button))
		self.Channel3Button.SetEvent(ui.__mem_func__(self.__OnClickChannel3Button))
		self.Channel4Button.SetEvent(ui.__mem_func__(self.__OnClickChannel4Button))
		if CHANNELAZ == 1:
			self.Channel2Button.Hide()
			self.Channel3Button.Hide()
			self.Channel4Button.Hide()
		elif CHANNELAZ == 2:
			self.Channel3Button.Hide()
			self.Channel4Button.Hide()
		elif CHANNELAZ == 3:
			self.Channel4Button.Hide()			
		self.BGBoard.Hide()
		print "XMAS_SNOW ON"
		background.EnableSnow(1)
			
		self.serverExitButton.SetEvent(ui.__mem_func__(self.__OnClickExitServerButton))
		self.serverExitButton.SetText(locale.UI_CLOSE)

		# RUNUP_MATRIX_AUTH
		if IsRunupMatrixAuth():
			self.matrixQuizBoard.Hide()
		# RUNUP_MATRIX_AUTH_END

		# NEWCIBN_PASSPOD_AUTH
		if IsNEWCIBNPassPodAuth():
			self.passpodBoard.Hide()
		# NEWCIBN_PASSPOD_AUTH_END

		self.serverBoard.SetPosition(self.xServerBoard, wndMgr.GetScreenHeight())
		self.serverBoard.Hide()

		if self.virtualKeyboard:
			self.virtualKeyboard.Show()
			self.AccountBoard.Show()
			self.AccEditBoard.Hide()
			self.__LoadACCNames()

		if app.loggined:
			self.Connect(self.id, self.pwd)
			self.connectBoard.Hide()
			self.loginBoard.Hide()
		elif not self.stream.isAutoLogin:
			self.connectBoard.Show()
			self.loginBoard.Show()

		## if users have the login infomation, then don't initialize.2005.9 haho
		if self.idEditLine == None:
			self.idEditLine.SetText("")
		if self.pwdEditLine == None:
			self.pwdEditLine.SetText("")

		self.idEditLine.SetFocus()

		global SKIP_LOGIN_PHASE
		if SKIP_LOGIN_PHASE:
			if not self.loginInfo:
				self.connectBoard.Hide()

	def __OpenLoginBoard(self):
		self.BGBoard.Hide()
		print "XMAS_SNOW ON"
		background.EnableSnow(1)
			
		self.serverExitButton.SetEvent(ui.__mem_func__(self.__OnClickExitServerButton))
		self.serverExitButton.SetText(locale.UI_CLOSE)

		# RUNUP_MATRIX_AUTH
		if IsRunupMatrixAuth():
			self.matrixQuizBoard.Hide()
		# RUNUP_MATRIX_AUTH_END

		# NEWCIBN_PASSPOD_AUTH
		if IsNEWCIBNPassPodAuth():
			self.passpodBoard.Hide()
		# NEWCIBN_PASSPOD_AUTH_END

		self.serverBoard.SetPosition(self.xServerBoard, wndMgr.GetScreenHeight())
		self.serverBoard.Hide()

		if self.virtualKeyboard:
			self.virtualKeyboard.Show()
			self.AccountBoard.Show()
			self.AccEditBoard.Hide()
			self.__LoadACCNames()

		if app.loggined:
			self.Connect(self.id, self.pwd)
			self.connectBoard.Hide()
			self.loginBoard.Hide()
		elif not self.stream.isAutoLogin:
			self.connectBoard.Show()
			self.loginBoard.Show()

		## if users have the login infomation, then don't initialize.2005.9 haho
		if self.idEditLine == None:
			self.idEditLine.SetText("")
		if self.pwdEditLine == None:
			self.pwdEditLine.SetText("")

		self.idEditLine.SetFocus()

		global SKIP_LOGIN_PHASE
		if SKIP_LOGIN_PHASE:
			if not self.loginInfo:
				self.connectBoard.Hide()

	def __OnSelectRegionGroup(self):
		self.__RefreshServerList()

	def __OnSelectSettlementArea(self):
		# SEVER_LIST_BUG_FIX
		regionID = self.__GetRegionID()
		serverID = self.serverListOnRegionBoard.GetSelectedItem()

		serverIndex = self.__ServerIDToServerIndex(regionID, serverID)
		self.serverList.SelectItem(serverIndex)
		# END_OF_SEVER_LIST_BUG_FIX
		
		self.__OnSelectServer()

	def __RefreshServerList(self):
		regionID = self.__GetRegionID()
		
		if not serverInfo.REGION_DICT.has_key(regionID):
			return

		self.serverList.ClearItem()

		regionDict = serverInfo.REGION_DICT[regionID]

		# SEVER_LIST_BUG_FIX
		visible_index = 1
		for id, regionDataDict in regionDict.items():
			name = regionDataDict.get("name", "noname")
			if locale.IsBRAZIL() or locale.IsCANADA():
				self.serverList.InsertItem(id, "%s" % (name))
			else:
				if locale.IsCIBN10():			
					if name[0] == "#":
						self.serverList.InsertItem(-1, "  %s" % (name[1:]))
					else:
						self.serverList.InsertItem(id, "  %s" % (name))
						visible_index += 1
				else:
					self.serverList.InsertItem(id, "  %02d. %s" % (visible_index, name))
					
					visible_index += 1
		
		# END_OF_SEVER_LIST_BUG_FIX

	def __OnSelectServer(self):
		self.__OnCloseInputDialog()
		self.__RequestServerStateList()
		self.__RefreshServerStateList()

	def __RequestServerStateList(self):
		regionID = self.__GetRegionID()
		serverID = self.__GetServerID()

		try:
			channelDict = serverInfo.REGION_DICT[regionID][serverID]["channel"]
		except:
			print " __RequestServerStateList - serverInfo.REGION_DICT(%d, %d)" % (regionID, serverID)
			return

		for id, channelDataDict in channelDict.items():
			key=channelDataDict["key"]
			ip=channelDataDict["ip"]
			udp_port=channelDataDict["udp_port"]
			ServerStateChecker.Request(key, ip, udp_port)

	def __RefreshServerStateList(self):

		regionID = self.__GetRegionID()
		serverID = self.__GetServerID()
		bakChannelID = self.channelList.GetSelectedItem()

		self.channelList.ClearItem()

		try:
			channelDict = serverInfo.REGION_DICT[regionID][serverID]["channel"]
		except:
			print " __RequestServerStateList - serverInfo.REGION_DICT(%d, %d)" % (regionID, serverID)
			return

		for channelID, channelDataDict in channelDict.items():
			channelName = channelDataDict["name"]
			channelState = channelDataDict["state"]
			self.channelList.InsertItem(channelID, " %s %s" % (channelName, channelState))

		self.channelList.SelectItem(bakChannelID-1)

	def __GetChannelName(self, regionID, selServerID, selChannelID):
		try:
			return serverInfo.REGION_DICT[regionID][selServerID]["channel"][selChannelID]["name"]
		except KeyError:
			if 9==selChannelID:
				return locale.CHANNEL_PVP
			else:
				return locale.CHANNEL_NORMAL % (selChannelID)

	def NotifyChannelState(self, addrKey, state):
		try:
			stateName=serverInfo.STATE_DICT[state]
		except:
			stateName=serverInfo.STATE_NONE

		regionID=int(addrKey/1000)
		serverID=int(addrKey/10) % 100
		channelID=addrKey%10

		try:
			serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["state"] = stateName
			self.__RefreshServerStateList()

		except:
			import exception
			exception.Abort(locale.CHANNEL_NOT_FIND_INFO)

	def __OnClickExitServerButton(self):
		print "exit server"
		self.__OpenLoginBoard()			

		if IsFullBackImage():
			self.GetChild("bg1").Hide()
			self.GetChild("bg2").Show()
			

	def __OnClickSelectRegionButton(self):
		regionID = self.__GetRegionID()
		serverID = self.__GetServerID()

		if (not serverInfo.REGION_DICT.has_key(regionID)):
			self.PopupNotifyMessage(locale.CHANNEL_SELECT_REGION)
			return

		if (not serverInfo.REGION_DICT[regionID].has_key(serverID)):
			self.PopupNotifyMessage(locale.CHANNEL_SELECT_SERVER)
			return		

		self.__SaveChannelInfo()

		self.serverExitButton.SetEvent(ui.__mem_func__(self.__OnClickExitServerButton))
		self.serverExitButton.SetText(locale.UI_CLOSE)

		self.__RefreshServerList()
		self.__OpenServerBoard()

	def __OnClickSelectServerButton(self):
		if IsFullBackImage():
			self.GetChild("bg1").Show()
			self.GetChild("bg2").Hide()

		regionID = self.__GetRegionID()
		serverID = self.__GetServerID()
		channelID = self.__GetChannelID()

		if (not serverInfo.REGION_DICT.has_key(regionID)):
			self.PopupNotifyMessage(locale.CHANNEL_SELECT_REGION)
			return

		if (not serverInfo.REGION_DICT[regionID].has_key(serverID)):
			self.PopupNotifyMessage(locale.CHANNEL_SELECT_SERVER)
			return

		try:
			channelDict = serverInfo.REGION_DICT[regionID][serverID]["channel"]
		except KeyError:
			return

		try:
			state = channelDict[channelID]["state"]
		except KeyError:
			self.PopupNotifyMessage(locale.CHANNEL_SELECT_CHANNEL)
			return

		# »óÅÂ°¡ FULL °ú °°Àžžé ÁøÀÔ ±ÝÁö
		if state == serverInfo.STATE_DICT[3]: 
			self.PopupNotifyMessage(locale.CHANNEL_NOTIFY_FULL)
			return

		self.__SaveChannelInfo()

		try:
			channelName = serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["name"]
			addrKey = serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["key"]
		except:
			print " ERROR __OnClickSelectServerButton(%d, %d, %d)" % (regionID, serverID, channelID)
			channelName = locale.CHANNEL_NORMAL % channelID

		self.__SetServerInfo("%s, %s " % (channelName))

		try:
			ip = serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["ip"]
			tcp_port = serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["tcp_port"]
		except:
			import exception
			exception.Abort("LoginWindow.__OnClickSelectServerButton - Œ­¹ö Œ±ÅÃ œÇÆÐ")

		try:
			account_ip = serverInfo.REGION_AUTH_SERVER_DICT[regionID][serverID]["ip"]
			account_port = serverInfo.REGION_AUTH_SERVER_DICT[regionID][serverID]["port"]
		except:
			account_ip = 0
			account_port = 0

		try:
			markKey = regionID*1000 + serverID*10
			markAddrValue=serverInfo.MARKADDR_DICT[markKey]
			net.SetMarkServer(markAddrValue["ip"], markAddrValue["tcp_port"])
			app.SetGuildMarkPath(markAddrValue["mark"])
			# GUILD_SYMBOL
			app.SetGuildSymbolPath(markAddrValue["symbol_path"])
			# END_OF_GUILD_SYMBOL

		except:
			import exception
			exception.Abort("LoginWindow.__OnClickSelectServerButton - ž¶Å© Á€ºž ŸøÀœ")

		self.stream.SetConnectInfo(ip, tcp_port, account_ip, account_port)

		self.__OpenLoginBoard() 
		
	def __OnClickChannel1Button(self):
		global DEINEIP
		global AUTHPORT
		global CH1PORT
		self.stream.SetConnectInfo(DEINEIP, CH1PORT, DEINEIP, AUTHPORT)
		net.SetServerInfo("Channel 1")
		net.SetMarkServer(DEINEIP, CH1PORT)
		self.serverInfo.SetText("Channel 1")
		app.SetGuildMarkPath("10.tga")
		app.SetGuildSymbolPath("10")
	def __OnClickChannel2Button(self):
		global DEINEIP
		global AUTHPORT
		global CH2PORT	
		self.stream.SetConnectInfo(DEINEIP, CH3PORT, DEINEIP, AUTHPORT)
		net.SetServerInfo("Channel 2")
		net.SetMarkServer(DEINEIP, CH3PORT)
		self.serverInfo.SetText("Channel 2")
		app.SetGuildMarkPath("10.tga")
		app.SetGuildSymbolPath("10")
	def __OnClickChannel3Button(self):
		global DEINEIP
		global AUTHPORT
		global CH3PORT	
		self.stream.SetConnectInfo(DEINEIP, CH3PORT, DEINEIP, AUTHPORT)
		net.SetServerInfo("Channel 3")
		net.SetMarkServer(DEINEIP, CH3PORT)
		self.serverInfo.SetText("Channel 3")
		app.SetGuildMarkPath("10.tga")
		app.SetGuildSymbolPath("10")
	def __OnClickChannel4Button(self):
		global DEINEIP
		global AUTHPORT
		global CH4PORT	
		self.stream.SetConnectInfo(DEINEIP, CH4PORT, DEINEIP, AUTHPORT)
		net.SetServerInfo("Channel 4")
		net.SetMarkServer(DEINEIP, CH4PORT)
		self.serverInfo.SetText("Channel 4")
		app.SetGuildMarkPath("10.tga")
		app.SetGuildSymbolPath("10")		
	
	def __OnClickLoginButton(self):
		id = self.idEditLine.GetText()
		pwd = self.pwdEditLine.GetText()		

		if len(id)==0:
			self.PopupNotifyMessage(locale.LOGIN_INPUT_ID, self.SetIDEditLineFocus)
			return

		if len(pwd)==0:
			self.PopupNotifyMessage(locale.LOGIN_INPUT_PASSWORD, self.SetPasswordEditLineFocus)
			return

		self.Connect(id, pwd)
		
