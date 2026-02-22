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
    "name": "GMTab3",
    "x": PAGE_X,
    "y": PAGE_Y,
    "width": PAGE_W,
    "height": PAGE_H,
    "children": (
        {
            "name": "T3_Title",
            "type": "expanded_image",
            "x": 0,
            "y": 2,
            "image": "d:/ymir work/ui/tab_menu_01.tga",
            "children": (
                {"name": "World_Teleport_Title", "type": "text", "x": 10, "y": 3, "text": "World / Teleport"},
            ),
        },

        {"name": "T3_TargetLabel", "type": "text", "x": 10, "y": 34, "text": "Target"},
        {
            "name": "World_TargetSlot",
            "type": "image",
            "x": 50,
            "y": 32,
            "image": SLOT_05,
            "children": (
                {"name": "World_TargetValue", "type": "editline", "x": 3, "y": 3, "width": 124, "height": 18, "input_limit": 24},
            ),
        },
        {"name": "World_WarpPlayer", "type": "button", "x": 185, "y": 30, "text": "Warp Player", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "World_TransferPlayer", "type": "button", "x": 245, "y": 30, "text": "Transfer", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "World_WeakenNear", "type": "button", "x": 10, "y": 95, "text": "Weaken Near", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "World_WeakenAll", "type": "button", "x": 70, "y": 95, "text": "Weaken All", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
    ),
}
