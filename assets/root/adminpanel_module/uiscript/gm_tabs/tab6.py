BOARD_WIDTH = 456
BOARD_HEIGHT = 370
TAB_HEIGHT = 36
PAGE_X = 10
PAGE_Y = TAB_HEIGHT + 8
PAGE_W = BOARD_WIDTH - 20
PAGE_H = BOARD_HEIGHT - (TAB_HEIGHT + 26)

BTN1 = "d:/ymir work/ui/public/middle_button_01.sub"
BTN2 = "d:/ymir work/ui/public/middle_button_02.sub"
BTN3 = "d:/ymir work/ui/public/middle_button_03.sub"
SLOT_01 = "d:/ymir work/ui/public/Parameter_Slot_01.sub"
SLOT_03 = "d:/ymir work/ui/public/Parameter_Slot_03.sub"
SLOT_04 = "d:/ymir work/ui/public/Parameter_Slot_04.sub"

window = {
    "name": "GMTab6",
    "x": PAGE_X,
    "y": PAGE_Y,
    "width": PAGE_W,
    "height": PAGE_H,
    "children": (
        {
            "name": "T6_Title",
            "type": "expanded_image",
            "x": 0,
            "y": 2,
            "image": "d:/ymir work/ui/tab_menu_01.tga",
            "children": (
                {"name": "Horse_Event_Title", "type": "text", "x": 10, "y": 3, "text": "Horse / Event"},
            ),
        },

        {"name": "Horse_State", "type": "button", "x": 10, "y": 30, "text": "Horse State", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Horse_Summon", "type": "button", "x": 132, "y": 30, "text": "Horse Summon", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Horse_Unsummon", "type": "button", "x": 254, "y": 30, "text": "Horse Unsummon", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "T6_Name", "type": "text", "x": 10, "y": 64, "text": "Player"},
        {
            "name": "Horse_NameSlot",
            "type": "image",
            "x": 50,
            "y": 62,
            "image": SLOT_04,
            "children": (
                {"name": "Horse_NameValue", "type": "editline", "x": 3, "y": 3, "width": 109, "height": 18, "input_limit": 24},
            ),
        },
        {"name": "T6_Level", "type": "text", "x": 160, "y": 64, "text": "Level"},
        {
            "name": "Horse_LevelSlot",
            "type": "image",
            "x": 195,
            "y": 62,
            "image": SLOT_01,
            "children": (
                {"name": "Horse_LevelValue", "type": "editline", "x": 3, "y": 3, "width": 46, "height": 18, "input_limit": 2, "only_number": 1},
            ),
        },
        {"name": "Horse_LevelApply", "type": "button", "x": 252, "y": 59, "text": "Apply Level", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "T6_HP", "type": "text", "x": 10, "y": 96, "text": "HP"},
        {
            "name": "Horse_HPSlot",
            "type": "image",
            "x": 32,
            "y": 94,
            "image": SLOT_03,
            "children": (
                {"name": "Horse_HPValue", "type": "editline", "x": 3, "y": 3, "width": 84, "height": 18, "input_limit": 7, "only_number": 1},
            ),
        },
        {"name": "T6_Stam", "type": "text", "x": 120, "y": 96, "text": "Stam"},
        {
            "name": "Horse_StamSlot",
            "type": "image",
            "x": 154,
            "y": 94,
            "image": SLOT_03,
            "children": (
                {"name": "Horse_StamValue", "type": "editline", "x": 3, "y": 3, "width": 84, "height": 18, "input_limit": 7, "only_number": 1},
            ),
        },
        {"name": "Horse_SetStat", "type": "button", "x": 240, "y": 91, "text": "Set Horse Stat", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "Misc_XmasSnow", "type": "button", "x": 10, "y": 132, "text": "xmas_snow", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Misc_XmasSanta", "type": "button", "x": 132, "y": 132, "text": "xmas_santa", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Misc_XmasBoom", "type": "button", "x": 254, "y": 132, "text": "xmas_boom", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "Misc_Eclipse", "type": "button", "x": 10, "y": 161, "text": "eclipse", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Misc_Weekly", "type": "button", "x": 132, "y": 161, "text": "weeklyevent", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Misc_EventHelper", "type": "button", "x": 254, "y": 161, "text": "eventhelper", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "Misc_Siege", "type": "button", "x": 10, "y": 190, "text": "siege", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Misc_Temp", "type": "button", "x": 132, "y": 190, "text": "temp", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Misc_Frog", "type": "button", "x": 254, "y": 190, "text": "frog", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
    ),
}
