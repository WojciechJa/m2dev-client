import uiScriptLocale

BOARD_WIDTH = 456
BOARD_HEIGHT = 370
TAB_HEIGHT = 36
PAGE_X = 10
PAGE_Y = TAB_HEIGHT + 8
PAGE_W = BOARD_WIDTH - 20
PAGE_H = BOARD_HEIGHT - (TAB_HEIGHT + 26)

SLOT_SMALL = "d:/ymir work/ui/public/Parameter_Slot_03.sub"

window = {
	"name" : "GMTab1",
	"x" : PAGE_X,
	"y" : PAGE_Y,
	"width" : PAGE_W,
	"height" : PAGE_H,
	"children" :
	(
{
	"name" : "Background",
	"type" : "expanded_image",
	"x" : 0,
	"y" : 2,
	"image" : "d:/ymir work/ui/tab_menu_01.tga",
    "children" :
	(
		{ 	"name" : "PrivEmpire_Title",
   			"type" : "text",
   			"x" : 10, "y" : 3,
   			"text" : "Priv Empire",
   		},
	),
},
		{ "name" : "PrivEmpire_EmpireLabel", "type" : "text", "x" : 10, "y" : 32, "text" : "Empire", },
		# "d:/ymir work/ui/public/battle/empire_all.sub"
		# "d:/ymir work/ui/public/battle/empire_shinsoo.sub"
		# "d:/ymir work/ui/public/battle/empire_chunjo.sub"
		# "d:/ymir work/ui/public/battle/empire_jinno.sub"
		{
			"name" : "Empire_All",
			"type" : "toggle_button",
			"x" : 10,
			"y" : 50,
			"default_image" : "d:/ymir work/ui/public/battle/empire_all.sub",
			"over_image" : "d:/ymir work/ui/public/battle/empire_all.sub",
			"down_image" : "d:/ymir work/ui/public/battle/empire_all.sub",
		},
		{
			"name" : "Empire_Shinsoo",
			"type" : "toggle_button",
			"x" : 95,
			"y" : 50,
			"default_image" : "d:/ymir work/ui/public/battle/empire_shinsu.sub",
			"over_image" : "d:/ymir work/ui/public/battle/empire_shinsu.sub",
			"down_image" : "d:/ymir work/ui/public/battle/empire_shinsu.sub",
		},
		{
			"name" : "Empire_Chunjo",
			"type" : "toggle_button",
			"x" : 180,
			"y" : 50,
			"default_image" : "d:/ymir work/ui/public/battle/empire_chunjo.sub",
			"over_image" : "d:/ymir work/ui/public/battle/empire_chunjo.sub",
			"down_image" : "d:/ymir work/ui/public/battle/empire_chunjo.sub",
		},
		{
			"name" : "Empire_Jinno",
			"type" : "toggle_button",
			"x" : 265,
			"y" : 50,
			"default_image" : "d:/ymir work/ui/public/battle/empire_jinno.sub",
			"over_image" : "d:/ymir work/ui/public/battle/empire_jinno.sub",
			"down_image" : "d:/ymir work/ui/public/battle/empire_jinno.sub",
		},

		{ "name" : "PrivEmpire_TypeLabel", "type" : "text", "x" : 10, "y" : 85, "text" : "Event Type", },
		# TODO icons:
		# "d:/ymir work/ui/public/battle/event_item.sub"
		# "d:/ymir work/ui/public/battle/event_gold.sub"
		# "d:/ymir work/ui/public/battle/event_gold10.sub"
		# "d:/ymir work/ui/public/battle/event_exp.sub"
		{
			"name" : "Type_Item",
			"type" : "toggle_button",
			"x" : 10,
			"y" : 105,
			"text" : "Item",
			"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
			"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
			"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
		},
		{
			"name" : "Type_Gold",
			"type" : "toggle_button",
			"x" : 95,
			"y" : 105,
			"text" : "Gold",
			"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
			"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
			"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
		},
		{
			"name" : "Type_Gold10",
			"type" : "toggle_button",
			"x" : 180,
			"y" : 105,
			"text" : "Gold10",
			"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
			"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
			"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
		},
		{
			"name" : "Type_Exp",
			"type" : "toggle_button",
			"x" : 265,
			"y" : 105,
			"text" : "EXP",
			"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
			"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
			"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
		},

		{ "name" : "PrivEmpire_ValueLabel", "type" : "text", "x" : 10, "y" : 140, "text" : "Value (%)", },
		{
			"name" : "PrivEmpire_ValueSlot",
			"type" : "image",
			"x" : 120,
			"y" : 135,
			"image" : SLOT_SMALL,
			"children" :
			(
				{ "name" : "PrivEmpire_ValueValue", "type" : "editline", "x" : 3, "y" : 3, "width" : 60, "height" : 18, "input_limit" : 4, "only_number" : 1, },
			),
		},
		{ "name" : "PrivEmpire_DurationLabel", "type" : "text", "x" : 230, "y" : 140, "text" : "Duration (h)", },
		{
			"name" : "PrivEmpire_DurationSlot",
			"type" : "image",
			"x" : 320,
			"y" : 135,
			"image" : SLOT_SMALL,
			"children" :
			(
				{ "name" : "PrivEmpire_DurationValue", "type" : "editline", "x" : 3, "y" : 3, "width" : 60, "height" : 18, "input_limit" : 5, "only_number" : 1, },
			),
		},
		{
			"name" : "PrivEmpire_Apply",
			"type" : "button",
			"x" : 10,
			"y" : 165,
			"text" : "Apply",
			"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
			"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
			"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
		},
		{ "name" : "PrivEmpire_Info", "type" : "text", "x" : 10, "y" : 195, "text" : "Type: 1=item, 2=gold, 3=gold10, 4=exp", },
	),
}
