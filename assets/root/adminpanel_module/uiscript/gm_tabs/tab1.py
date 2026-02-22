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
    "name": "GMTab1",
    "x": PAGE_X,
    "y": PAGE_Y,
    "width": PAGE_W,
    "height": PAGE_H,
    "children":
        (
            {
                "name": "Background",
                "type": "expanded_image",
                "x": 0,
                "y": 2,
                "image": "d:/ymir work/ui/tab_menu_01.tga",
                "children":
                    (
                        { "name" : "PrivEmpire_Title",
                             "type" : "text",
                             "x" : 10, "y" : 3,
                             "text" : "Priv Empire",
                             },

                        {
                            "name" : "Empire_All",
                            "type" : "toggle_button",
                            "x" : 80,
                            "y" : 3,
                            "default_image" : "d:/ymir work/ui/public/battle/empire_all.sub",
                            "over_image" : "d:/ymir work/ui/public/battle/empire_all_over.sub",
                            "down_image" : "d:/ymir work/ui/public/battle/empire_all_down.sub",

                            "tooltip_text" : "Apply to all empires",
                        },
                        {
                            "name" : "Empire_Shinsoo",
                            "type" : "toggle_button",
                            "x" : 120,
                            "y" : 3,
                            "default_image" : "d:/ymir work/ui/public/battle/empire_shinsu.sub",
                            "over_image" : "d:/ymir work/ui/public/battle/empire_shinsu_over.sub",
                            "down_image" : "d:/ymir work/ui/public/battle/empire_shinsu_down.sub",

                            "tooltip_text" : "Apply to Shinsoo empire only",
                        },
                        {
                            "name" : "Empire_Chunjo",
                            "type" : "toggle_button",
                            "x" : 160,
                            "y" : 3,
                            "default_image" : "d:/ymir work/ui/public/battle/empire_chunjo.sub",
                            "over_image" : "d:/ymir work/ui/public/battle/empire_chunjo_over.sub",
                            "down_image" : "d:/ymir work/ui/public/battle/empire_chunjo_down.sub",
                            "tooltip_text" : "Apply to Chunjo empire only",
                        },
                        {
                            "name" : "Empire_Jinno",
                            "type" : "toggle_button",
                            "x" : 200,
                            "y" : 3,
                            "default_image" : "d:/ymir work/ui/public/battle/empire_jinno.sub",
                            "over_image" : "d:/ymir work/ui/public/battle/empire_jinno_over.sub",
                            "down_image" : "d:/ymir work/ui/public/battle/empire_jinno_down.sub",
                            "tooltip_text" : "Apply to Jinno empire only",
                        },
                    ),
            },

            # PrivEmpire Type
            {
                "name" : "Type_Item",
                "type" : "toggle_button",
                "x" : 10,
                "y" : 40,
                "default_image" : "d:/ymir work/ui/event/event_item.sub",
                "over_image" : "d:/ymir work/ui/event/event_item.sub",
                "down_image" : "d:/ymir work/ui/event/event_item_selected.sub",
            },
            {
                "name" : "Type_Gold",
                "type" : "toggle_button",
                "x" : 50,
                "y" : 40,
                "default_image" : "d:/ymir work/ui/event/event_gold.sub",
                "over_image" : "d:/ymir work/ui/event/event_gold.sub",
                "down_image" : "d:/ymir work/ui/event/event_gold_selected.sub",
            },
            {
                "name" : "Type_Gold10",
                "type" : "toggle_button",
                "x" : 90,
                "y" : 40,
                "default_image" : "d:/ymir work/ui/event/event_gold10.sub",
                "over_image" : "d:/ymir work/ui/event/event_gold10.sub",
                "down_image" : "d:/ymir work/ui/event/event_gold10_selected.sub",
            },
            {
                "name" : "Type_Exp",
                "type" : "toggle_button",
                "x" : 130,
                "y" : 40,
                "default_image" : "d:/ymir work/ui/event/event_exp.sub",
                "over_image" : "d:/ymir work/ui/event/event_exp.sub",
                "down_image" : "d:/ymir work/ui/event/event_exp_selected.sub",
            },

            { "name" : "PrivEmpire_ValueLabel", "type" : "text", "x" : 170, "y" : 39, "text" : "(%)", },
            {
                "name" : "PrivEmpire_ValueSlot",
                "type" : "image",
                "x" : 190,
                "y" : 38,
                "image" : SLOT_SMALL,
                "children" :
                    (
                        { "name" : "PrivEmpire_ValueValue", "type" : "editline", "x" : 3, "y" : 3, "width" : 60, "height" : 18, "input_limit" : 4, "only_number" : 1, },
                    ),
            },
            { "name" : "PrivEmpire_DurationLabel", "type" : "text", "x" : 170, "y" : 59, "text" : "(H)", },
            {
                "name" : "PrivEmpire_DurationSlot",
                "type" : "image",
                "x" : 190,
                "y" : 58,
                "image" : SLOT_SMALL,
                "children" :
                    (
                        { "name" : "PrivEmpire_DurationValue", "type" : "editline", "x" : 3, "y" : 3, "width" : 60, "height" : 18, "input_limit" : 5, "only_number" : 1, },
                    ),
            },
            {
                "name" : "PrivEmpire_Apply",
                "type" : "button",
                "x" : 300,
                "y" : 37,
                "text" : "Apply",
                "default_image" : "d:/ymir work/ui/public/big_button_01.sub",
                "over_image" : "d:/ymir work/ui/public/big_button_02.sub",
                "down_image" : "d:/ymir work/ui/public/big_button_03.sub",
            },
        ),
}
