import uiScriptLocale

BOARD_WIDTH = 456
BOARD_HEIGHT = 370
TAB_HEIGHT = 36
PAGE_Y = TAB_HEIGHT + 8
PAGE_H = BOARD_HEIGHT - (TAB_HEIGHT + 26)

TAB_IMAGE_PATH = "d:/ymir work/ui/adminpanel/"
SLOT_SMALL = "d:/ymir work/ui/public/Parameter_Slot_03.sub"

window = {
	"name" : "AdminpanelGMCommandsWindow",

	"x" : (SCREEN_WIDTH / 2) - (BOARD_WIDTH / 2),
	"y" : (SCREEN_HEIGHT / 2) - (BOARD_HEIGHT / 2),

	"style" : ("movable", "float",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,
			"title" : "GM Commands",

			"children" :
			(
				## Tab Area (top)
				{
					"name" : "TabControl",
					"type" : "window",

					"x" : 2,
					"y" : 0,

					"width" : BOARD_WIDTH,
					"height" : TAB_HEIGHT,

					"children" :
					(
						## Tab backgrounds
						{
							"name" : "Tab_01",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"image" : TAB_IMAGE_PATH + "admin_tab_menu_1.sub",
						},
						{
							"name" : "Tab_02",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"image" : TAB_IMAGE_PATH + "admin_tab_menu_2.sub",
						},
						{
							"name" : "Tab_03",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"image" : TAB_IMAGE_PATH + "admin_tab_menu_3.sub",
						},
						{
							"name" : "Tab_04",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"image" : TAB_IMAGE_PATH + "admin_tab_menu_4.sub",
						},
						{
							"name" : "Tab_05",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"image" : TAB_IMAGE_PATH + "admin_tab_menu_5.sub",
						},
						{
							"name" : "Tab_06",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"image" : TAB_IMAGE_PATH + "admin_tab_menu_6.sub",
						},
						{
							"name" : "Tab_07",
							"type" : "image",

							"x" : 0,
							"y" : 0,

							"image" : TAB_IMAGE_PATH + "admin_tab_menu_7.sub",
						},
						## Radio buttons
						{
							"name" : "Tab_Button_01",
							"type" : "radio_button",

							"x" : 4,
							"y" : 5,

							"width" : 60,
							"height" : 27,
						},
						{
							"name" : "Tab_Button_02",
							"type" : "radio_button",

							"x" : 68,
							"y" : 5,

							"width" : 60,
							"height" : 27,
						},
						{
							"name" : "Tab_Button_03",
							"type" : "radio_button",

							"x" : 132,
							"y" : 5,

							"width" : 60,
							"height" : 27,
						},
						{
							"name" : "Tab_Button_04",
							"type" : "radio_button",

							"x" : 196,
							"y" : 5,

							"width" : 60,
							"height" : 27,
						},
						{
							"name" : "Tab_Button_05",
							"type" : "radio_button",

							"x" : 260,
							"y" : 5,

							"width" : 60,
							"height" : 27,
						},
						{
							"name" : "Tab_Button_06",
							"type" : "radio_button",

							"x" : 324,
							"y" : 5,

							"width" : 60,
							"height" : 27,
						},
						{
							"name" : "Tab_Button_07",
							"type" : "radio_button",

							"x" : 388,
							"y" : 5,

							"width" : 60,
							"height" : 27,
						},
					),
				},

				## Pages
				{
					"name" : "Page_01",
					"type" : "window",
					"x" : 10,
					"y" : PAGE_Y,
					"width" : BOARD_WIDTH - 20,
					"height" : PAGE_H,
					"children" : (),
				},
				{
					"name" : "Page_02",
					"type" : "window",
					"x" : 10,
					"y" : PAGE_Y,
					"width" : BOARD_WIDTH - 20,
					"height" : PAGE_H,
					"children" : (),
				},
				{
					"name" : "Page_03",
					"type" : "window",
					"x" : 10,
					"y" : PAGE_Y,
					"width" : BOARD_WIDTH - 20,
					"height" : PAGE_H,
					"children" : (),
				},
				{
					"name" : "Page_04",
					"type" : "window",
					"x" : 10,
					"y" : PAGE_Y,
					"width" : BOARD_WIDTH - 20,
					"height" : PAGE_H,
					"children" : (),
				},
				{
					"name" : "Page_05",
					"type" : "window",
					"x" : 10,
					"y" : PAGE_Y,
					"width" : BOARD_WIDTH - 20,
					"height" : PAGE_H,
					"children" : (),
				},
				{
					"name" : "Page_06",
					"type" : "window",
					"x" : 10,
					"y" : PAGE_Y,
					"width" : BOARD_WIDTH - 20,
					"height" : PAGE_H,
					"children" : (),
				},
				{
					"name" : "Page_07",
					"type" : "window",
					"x" : 10,
					"y" : PAGE_Y,
					"width" : BOARD_WIDTH - 20,
					"height" : PAGE_H,
					"children" : (),
				},
			),
		},
	),
}
