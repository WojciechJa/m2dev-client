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
SLOT_03 = "d:/ymir work/ui/public/Parameter_Slot_03.sub"
SLOT_05 = "d:/ymir work/ui/public/Parameter_Slot_05.sub"

window = {
    "name": "GMTab5",
    "x": PAGE_X,
    "y": PAGE_Y,
    "width": PAGE_W,
    "height": PAGE_H,
    "children": (
        {
            "name": "T5_Title",
            "type": "expanded_image",
            "x": 0,
            "y": 2,
            "image": "d:/ymir work/ui/tab_menu_01.tga",
            "children": (
                {"name": "Guild_War_Title", "type": "text", "x": 10, "y": 3, "text": "Guild / War"},
            ),
        },

        {"name": "Guild_GwList", "type": "button", "x": 10, "y": 30, "text": "GW List", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "T5_Id1", "type": "text", "x": 10, "y": 66, "text": "Guild ID1"},
        {
            "name": "Guild_Id1Slot",
            "type": "image",
            "x": 66,
            "y": 64,
            "image": SLOT_03,
            "children": (
                {"name": "Guild_Id1Value", "type": "editline", "x": 3, "y": 3, "width": 84, "height": 18, "input_limit": 10, "only_number": 1},
            ),
        },
        {"name": "T5_Id2", "type": "text", "x": 145, "y": 66, "text": "Guild ID2"},
        {
            "name": "Guild_Id2Slot",
            "type": "image",
            "x": 201,
            "y": 64,
            "image": SLOT_03,
            "children": (
                {"name": "Guild_Id2Value", "type": "editline", "x": 3, "y": 3, "width": 84, "height": 18, "input_limit": 10, "only_number": 1},
            ),
        },
        {"name": "Guild_GwStop", "type": "button", "x": 278, "y": 61, "text": "GW Stop", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Guild_GwCancel", "type": "button", "x": 339, "y": 61, "text": "GW Cancel", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "T5_Name", "type": "text", "x": 10, "y": 98, "text": "Guild name/id"},
        {
            "name": "Guild_NameSlot",
            "type": "image",
            "x": 88,
            "y": 96,
            "image": SLOT_05,
            "children": (
                {"name": "Guild_NameValue", "type": "editline", "x": 3, "y": 3, "width": 124, "height": 18, "input_limit": 32},
            ),
        },
        {"name": "Guild_State", "type": "button", "x": 245, "y": 93, "text": "Guild State", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Guild_Priv", "type": "button", "x": 367, "y": 93, "text": "Priv Guild", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "T5_Info", "type": "text", "x": 10, "y": 130, "text": "gwstop/gwcancel wymagaja ID gildii, nie nazw."},
    ),
}
