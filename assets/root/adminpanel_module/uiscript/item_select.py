import uiScriptLocale
import localeInfo
import constInfo

BOARD_WIDTH = 450
BOARD_HEIGHT = 420

IMG_PATH = "d:/ymir work/ui/adminpanel/create_item/"

window = {
	"name": "ItemSelectWindow",
	"x": (SCREEN_WIDTH / 2) - (BOARD_WIDTH / 2),
	"y": (SCREEN_HEIGHT / 2) - (BOARD_HEIGHT / 2),
	"style": ("movable", "float",),
	"width": BOARD_WIDTH,
	"height": BOARD_HEIGHT,
	"children":
	(
		{
			"name": "board", "type": "board_with_titlebar",
			"x": 0, "y": 0, "width": BOARD_WIDTH, "height": BOARD_HEIGHT,
			"title": "Add Item",
			"children":
			(
				## Race tabs
				{"name": "tab_all", "type": "radio_button", "x": 20, "y": 35, "text": "All",
				 "default_image": "d:/ymir work/ui/public/large_button_01.sub",
				 "over_image": "d:/ymir work/ui/public/large_button_02.sub",
				 "down_image": "d:/ymir work/ui/public/large_button_03.sub"},
				{"name": "tab_warrior", "type": "radio_button", "x": 100, "y": 35, "text": "Warrior",
				 "default_image": "d:/ymir work/ui/public/large_button_01.sub",
				 "over_image": "d:/ymir work/ui/public/large_button_02.sub",
				 "down_image": "d:/ymir work/ui/public/large_button_03.sub"},
				{"name": "tab_ninja", "type": "radio_button", "x": 180, "y": 35, "text": "Ninja",
				 "default_image": "d:/ymir work/ui/public/large_button_01.sub",
				 "over_image": "d:/ymir work/ui/public/large_button_02.sub",
				 "down_image": "d:/ymir work/ui/public/large_button_03.sub"},
				{"name": "tab_sura", "type": "radio_button", "x": 260, "y": 35, "text": "Sura",
				 "default_image": "d:/ymir work/ui/public/large_button_01.sub",
				 "over_image": "d:/ymir work/ui/public/large_button_02.sub",
				 "down_image": "d:/ymir work/ui/public/large_button_03.sub"},
				{"name": "tab_shaman", "type": "radio_button", "x": 340, "y": 35, "text": "Shaman",
				 "default_image": "d:/ymir work/ui/public/large_button_01.sub",
				 "over_image": "d:/ymir work/ui/public/large_button_02.sub",
				 "down_image": "d:/ymir work/ui/public/large_button_03.sub"},

				## Search
				{
					"name": "search_board", "type": "thinboard_circle",
					"x": 20, "y": 65, "width": 410, "height": 22,
					"children": (
						{"name": "search_label", "type": "text", "x": 5, "y": 4, "text": "Search:"},
						{"name": "search_editline", "type": "editline", "input_limit": 24,
						 "x": 55, "y": 4, "width": 350, "height": 18},
					)
				},

				## Item list
				{
					"name": "itemlist_background", "type": "thinboard_circle",
					"x": 20, "y": 92, "width": 410, "height": 220,
				},

				## Socket fields
				{"name": "label_socket0", "type": "text", "x": 20, "y": 322, "text": "Socket 0:"},
				{
					"name": "edit_socket0_bg", "type": "thinboard_circle",
					"x": 85, "y": 318, "width": 64, "height": 22,
					"children": (
						{"name": "edit_socket0", "type": "editline", "x": 2, "y": 2, "width": 60, "height": 18, "input_limit": 10, "text": "0"},
					)
				},
				{"name": "label_socket1", "type": "text", "x": 160, "y": 322, "text": "Socket 1:"},
				{
					"name": "edit_socket1_bg", "type": "thinboard_circle",
					"x": 225, "y": 318, "width": 64, "height": 22,
					"children": (
						{"name": "edit_socket1", "type": "editline", "x": 2, "y": 2, "width": 60, "height": 18, "input_limit": 10, "text": "0"},
					)
				},
				{"name": "label_socket2", "type": "text", "x": 300, "y": 322, "text": "Socket 2:"},
				{
					"name": "edit_socket2_bg", "type": "thinboard_circle",
					"x": 365, "y": 318, "width": 64, "height": 22,
					"children": (
						{"name": "edit_socket2", "type": "editline", "x": 2, "y": 2, "width": 60, "height": 18, "input_limit": 10, "text": "0"},
					)
				},

				## Selected item (preview)
				{"name": "label_selected", "type": "text", "x": 20, "y": 352, "text": "Selected: None"},

				## Buttons
				{
					"name": "btn_add", "type": "button",
					"x": 120, "y": 375, "text": "Add", "text_outline": 1,
					"default_image": IMG_PATH + "button_1_normal.sub",
					"over_image": IMG_PATH + "button_1_hover.sub",
					"down_image": IMG_PATH + "button_1_down.sub",
				},
				{
					"name": "btn_cancel", "type": "button",
					"x": 250, "y": 375, "text": "Cancel", "text_outline": 1,
					"default_image": IMG_PATH + "button_1_normal.sub",
					"over_image": IMG_PATH + "button_1_hover.sub",
					"down_image": IMG_PATH + "button_1_down.sub",
				},
			)
		},
	),
}
