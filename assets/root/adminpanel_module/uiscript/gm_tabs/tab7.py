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
SLOT_06 = "d:/ymir work/ui/public/Parameter_Slot_06.sub"

window = {
    "name": "GMTab7",
    "x": PAGE_X,
    "y": PAGE_Y,
    "width": PAGE_W,
    "height": PAGE_H,
    "children": (
        {
            "name": "T7_Title",
            "type": "expanded_image",
            "x": 0,
            "y": 2,
            "image": "d:/ymir work/ui/tab_menu_01.tga",
            "children": (
                {"name": "Custom_Command_Title", "type": "text", "x": 10, "y": 3, "text": "Custom command sender"},
            ),
        },
        {"name": "T7_Info", "type": "text", "x": 10, "y": 30, "text": "Wpisz komende z argumentami, np: priv_empire 0 1 100 1"},
        {
            "name": "Custom_CmdSlot",
            "type": "image",
            "x": 10,
            "y": 56,
            "image": SLOT_06,
            "children": (
                {"name": "Custom_CmdValue", "type": "editline", "x": 3, "y": 3, "width": 214, "height": 18, "input_limit": 180},
            ),
        },
        {"name": "Custom_Send", "type": "button", "x": 356, "y": 53, "text": "Send", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
    ),
}
