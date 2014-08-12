import uiScriptLocale
		
LOCALE_PATH = uiScriptLocale.LOGIN_PATH
SERVER_BOARD_HEIGHT = 220
SERVER_LIST_HEIGHT = 230

window = {
	"name" : "LoginWindow",
	"sytle" : ("movable",),

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(
		## Board
		{
			"name" : "bg1", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1024.0, "y_scale" : float(SCREEN_HEIGHT) / 768.0,
			"image" : "locale/de/ui/serverlist.sub",
		},
		{
			"name" : "bg2", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1024.0, "y_scale" : float(SCREEN_HEIGHT) / 768.0,
			"image" : "locale/de/ui/login.jpg",
		},
		{
			"name" : "bg3", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1024.0, "y_scale" : float(SCREEN_HEIGHT) / 768.0,
			"image" : "locale/de/ui/login1.sub",
		},
		{
			"name" : "bg4", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1024.0, "y_scale" : float(SCREEN_HEIGHT) / 768.0,
			"image" : "locale/de/ui/login2.sub",
		},
		{
			"name" : "bg5", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1024.0, "y_scale" : float(SCREEN_HEIGHT) / 768.0,
			"image" : "locale/de/ui/login3.sub",
		},
		{
			"name" : "bg6", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1024.0, "y_scale" : float(SCREEN_HEIGHT) / 768.0,
			"image" : "locale/de/ui/login4.sub",
		},
		{
			"name" : "bg7", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1024.0, "y_scale" : float(SCREEN_HEIGHT) / 768.0,
			"image" : "locale/de/ui/login5.sub",
		},
		{
			"name" : "bg8", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1024.0, "y_scale" : float(SCREEN_HEIGHT) / 768.0,
			"image" : "locale/de/ui/login6.sub",
		},
		{
			"name" : "logo1", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1024.0, "y_scale" : float(SCREEN_HEIGHT) / 768.0,
			"image" : "locale/de/ui/logo.sub",
		},
		{
			"name" : "BGBoard",
			"type" : "board",

			"x" : (SCREEN_WIDTH - 288) / 2 + 36,
			"y" : SCREEN_HEIGHT - 260 - 180,
			"width" : 208,
			"height" : 310,

			"children" :
			(
				{
					"name" : "BgButton1",
					"type" : "button",

					"x" : 15,
					"y" : - 120,
					"vertical_align" : "center",

					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",

					"text" : "Hintergrund Nr.1",
				},
				{
					"name" : "BgButton2",
					"type" : "button",

					"x" : 15,
					"y" : - 90,
					"vertical_align" : "center",

					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",

					"text" : "Hintergrund Nr.2",
				},
				{
					"name" : "BgButton3",
					"type" : "button",

					"x" : 15,
					"y" : - 60,
					"vertical_align" : "center",

					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",

					"text" : "Hintergrund Nr.3",
				},
				{
					"name" : "BgButton4",
					"type" : "button",

					"x" : 15,
					"y" : - 30,
					"vertical_align" : "center",

					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",

					"text" : "Hintergrund Nr.4",
				},
				{
					"name" : "BgButton5",
					"type" : "button",

					"x" : 15,
					"y" : 0,
					"vertical_align" : "center",

					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",

					"text" : "Hintergrund Nr.5",
				},
				{
					"name" : "BgButton6",
					"type" : "button",

					"x" : 15,
					"y" : 30,
					"vertical_align" : "center",

					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",

					"text" : "Hintergrund Nr.6",
				},
				{
					"name" : "BgButton7",
					"type" : "button",

					"x" : 15,
					"y" : 60,
					"vertical_align" : "center",

					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",

					"text" : "Hintergrund Nr.7",
				},
				{
					"name" : "BgButton8",
					"type" : "button",

					"x" : 15,
					"y" : 90,
					"vertical_align" : "center",

					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",

					"text" : "Hintergrund Nr.8",
				},
				{
					"name" : "BgButton9",
					"type" : "button",

					"x" : 15,
					"y" : 120,
					"vertical_align" : "center",

					"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",

					"text" : "Abbrechen",
				},
			),
		},
		## ConnectBoard
		{
			"name" : "ConnectBoard",
			"type" : "thinboard",

			"x" : (SCREEN_WIDTH - 564) / 2,
			"y" : (SCREEN_HEIGHT - 442 - 35),
			"width" : 564,
			"height" : 30,

			"children" :
			(			
			),
		},

		## LoginBoard
		{
			"name" : "LoginBoard",
			"type" : "image",

			"x" : ((SCREEN_WIDTH - 636) / 2) - 1,
			"y" : (SCREEN_HEIGHT - 514),

			"image" : LOCALE_PATH + "loginwindow.sub",

			"children" :
			(
				{
					"name" : "ID_EditLine",
					"type" : "editline",

					"x" : 240,
					"y" : 105,

					"width" : 120,
					"height" : 18,

					"input_limit" : 16,
					"enable_codepage" : 0,

					"r" : 1.0,
					"g" : 1.0,
					"b" : 1.0,
					"a" : 1.0,
				},
				{
					"name" : "Password_EditLine",
					"type" : "editline",

					"x" : 240,
					"y" : 138,
					"y" : 138,

					"width" : 120,
					"height" : 18,

					"input_limit" : 16,
					"secret_flag" : 1,
					"enable_codepage" : 0,

					"r" : 1.0,
					"g" : 1.0,
					"b" : 1.0,
					"a" : 1.0,
				},
				{
					"name" : "LoginButton",
					"type" : "button",

					"x" : 229,
					"y" : 162,

					"default_image" : "locale/de/ui/joker/channel_01.tga",
					"over_image" : "locale/de/ui/joker/channel_02.tga",
					"down_image" : "locale/de/ui/joker/channel_03.tga",

					"text" : uiScriptLocale.LOGIN_CONNECT,
				},
				{
					"name" : "barfoot",
					"type" : "image",
					
					"x" : SCREEN_HEIGHT,
					"y" : 0,
					
					
					"default_image" : "locale/de/ui/joker/bar-bot.tga"
				},
				{
					"name" : "LoginSaveButton",
					"type" : "button",

					"x" : 80,
					"y" : 162,

					"default_image" : "locale/de/ui/joker/channel_01.tga",
					"over_image" : "locale/de/ui/joker/channel_02.tga",
					"down_image" : "locale/de/ui/joker/channel_03.tga",

					"text" : "Speichern",
				},
				{
					"name" : "ConnectName",
					"type" : "text",

					"x" : 310,
					"y" : 67,

					"text" : uiScriptLocale.LOGIN_DEFAULT_SERVERADDR,
				},
				{
					"name" : "LoginExitButton",
					"type" : "button",

					"x" : 340,
					"y" : 162,

					"default_image" : "locale/de/ui/joker/channel_01.tga",
					"over_image" : "locale/de/ui/joker/channel_02.tga",
					"down_image" : "locale/de/ui/joker/channel_03.tga",

					"text" : "Beenden",
				},	
				{
					"name" : "ACC1__LABEL",
					"type" : "text",

					"x" : 45,
					"y" : 37,
					"text" : "ACC1 - Leer",
				},
				{
					"name" : "ACC2__LABEL",
					"type" : "text",

					"x" : 45,
					"y" : 67,
					"text" : "ACC2 - Leer",
				},
				{
					"name" : "ACC3__LABEL",
					"type" : "text",

					"x" : 45,
					"y" : 97,
					"text" : "ACC3 - Leer",
				},				
				{
					"name" : "Acc1Login",
					"type" : "button",

					"x" : 150,
					"y" : 35,

					"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/small_button_03.sub",

					"text" : "W\E4hlen",
				},
				{
					"name" : "Acc2Login",
					"type" : "button",

					"x" : 150,
					"y" : 65,

					"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/small_button_03.sub",

					"text" : "W\E4hlen",
				},
				{
					"name" : "Acc3Login",
					"type" : "button",

					"x" : 150,
					"y" : 95,

					"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/small_button_03.sub",

					"text" : "W\E4hlen",
				},
				{
					"name" : "ACC1_LABEL",
					"type" : "text",

					"x" : 45,
					"y" : 37,
					"text" : "ACC1 - Leer",
				},
				{
					"name" : "ACC2_LABEL",
					"type" : "text",

					"x" : 45,
					"y" : 67,
					"text" : "ACC2 - Leer",
				},
				{
					"name" : "ACC3_LABEL",
					"type" : "text",

					"x" : 45,
					"y" : 97,
					"text" : "ACC3 - Leer",
				},
				{
					"name" : "Channel1Button",
					"type" : "button",

					"x" : 564 / 2 + 200,
					"y" : 50,

					"default_image" : "locale/de/ui/joker/channel_01.tga",
					"over_image" : "locale/de/ui/joker/channel_02.tga",
					"down_image" : "locale/de/ui/joker/channel_03.tga",

					"text" : "Channel1",
				},
				{
					"name" : "Channel2Button",
					"type" : "button",

					"x" : 564 / 2 + 200,
					"y" : 80,

					"default_image" : "locale/de/ui/joker/channel_01.tga",
					"over_image" : "locale/de/ui/joker/channel_02.tga",
					"down_image" : "locale/de/ui/joker/channel_03.tga",

					"text" : "Channel2",
				},
				{
					"name" : "Channel3Button",
					"type" : "button",

					"x" : 564 / 2 + 200,
					"y" : 110,

					"default_image" : "locale/de/ui/joker/channel_01.tga",
					"over_image" : "locale/de/ui/joker/channel_02.tga",
					"down_image" : "locale/de/ui/joker/channel_03.tga",

					"text" : "Channel3",
				},
				{
					"name" : "Channel4Button",
					"type" : "button",

					"x" : 564 / 2 + 200,
					"y" : 140,

					"default_image" : "locale/de/ui/joker/channel_01.tga",
					"over_image" : "locale/de/ui/joker/channel_02.tga",
					"down_image" : "locale/de/ui/joker/channel_03.tga",

					"text" : "Channel4",
				},
				#Account
				{
					"name" : "Acc1Del",
					"type" : "button",

					"x" : 150,
					"y" : 35,

					"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/small_button_03.sub",

					"text" : "L\F6sch.",
				},
				{
					"name" : "Acc2Del",
					"type" : "button",

					"x" : 150,
					"y" : 65,

					"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/small_button_03.sub",

					"text" : "L\F6sch.",
				},
				{
					"name" : "Acc3Del",
					"type" : "button",

					"x" : 150,
					"y" : 95,

					"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/small_button_03.sub",

					"text" : "L\F6sch.",
				},
			),
		},	
		## ServerBoard
		{
			"name" : "ServerBoard",
			"type" : "thinboard",

			"x" : 0,
			"y" : SCREEN_HEIGHT - SERVER_BOARD_HEIGHT - 150,
			"width" : 375,
			"height" : SERVER_BOARD_HEIGHT,
			"horizontal_align" : "center",

			"children" :
			(

				## Title
				{
					"name" : "Title",
					"type" : "text",

					"x" : 0,
					"y" : 12,
					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"text" : uiScriptLocale.LOGIN_SELECT_TITLE,
				},
				## ListBox
				{
					"name" : "ServerList",
					"type" : "listbox2",

					"x" : 10,
					"y" : 40,
					"width" : 232,
					"height" : SERVER_LIST_HEIGHT,
					"row_count" : 18,
					"item_align" : 0,
				},
				{
					"name" : "ChannelList",
					"type" : "listbox",

					"x" : 255,
					"y" : 40,
					"width" : 109,
					"height" : SERVER_LIST_HEIGHT,

					"item_align" : 0,
				},

				## Buttons
				{
					"name" : "ServerSelectButton",
					"type" : "button",

					"x" : 300,
					"y" : SERVER_LIST_HEIGHT,

					"default_image" : "locale/de/ui/joker/channel_01.tga",
					"over_image" : "locale/de/ui/joker/channel_02.tga",
					"down_image" : "locale/de/ui/joker/channel_03.tga",

					"text" : uiScriptLocale.OK,
				},
				{
					"name" : "ServerExitButton",
					"type" : "button",

					"x" : 267,
					"y" : SERVER_LIST_HEIGHT + 22,

					"default_image" : "locale/de/ui/joker/channel_01.tga",
					"over_image" : "locale/de/ui/joker/channel_02.tga",
					"down_image" : "locale/de/ui/joker/channel_03.tga",

					"text" : uiScriptLocale.LOGIN_SELECT_EXIT,
				},
			),
		},
	),
}
