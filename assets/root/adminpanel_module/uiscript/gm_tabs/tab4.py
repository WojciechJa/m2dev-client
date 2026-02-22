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
SLOT_02 = "d:/ymir work/ui/public/Parameter_Slot_02.sub"
SLOT_03 = "d:/ymir work/ui/public/Parameter_Slot_03.sub"
SLOT_04 = "d:/ymir work/ui/public/Parameter_Slot_04.sub"
SLOT_05 = "d:/ymir work/ui/public/Parameter_Slot_05.sub"

window = {
    "name": "GMTab4",
    "x": PAGE_X,
    "y": PAGE_Y,
    "width": PAGE_W,
    "height": PAGE_H,
    "children": (
        {
            "name": "T4_Title",
            "type": "expanded_image",
            "x": 0,
            "y": 2,
            "image": "d:/ymir work/ui/tab_menu_01.tga",
            "children": (
                {"name": "Quest_Event_Title", "type": "text", "x": 10, "y": 3, "text": "Quest / Event"},
            ),
        },

        {"name": "T4_EventLabel", "type": "text", "x": 10, "y": 34, "text": "eventflag"},
        {
            "name": "Ev_FlagNameSlot",
            "type": "image",
            "x": 72,
            "y": 32,
            "image": SLOT_05,
            "children": (
                {"name": "Ev_FlagNameValue", "type": "editline", "x": 3, "y": 3, "width": 124, "height": 18, "input_limit": 32},
            ),
        },
        {
            "name": "Ev_FlagValueSlot",
            "type": "image",
            "x": 206,
            "y": 32,
            "image": SLOT_02,
            "children": (
                {"name": "Ev_FlagValueValue", "type": "editline", "x": 3, "y": 3, "width": 55, "height": 18, "input_limit": 8, "only_number": 1},
            ),
        },
        {"name": "Ev_SetEventFlag", "type": "button", "x": 264, "y": 29, "text": "Set Flag", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Ev_GetEventFlag", "type": "button", "x": 325, "y": 29, "text": "Get All", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "T4_QfLabel", "type": "text", "x": 10, "y": 68, "text": "setqf"},
        {
            "name": "Ev_QFlagNameSlot",
            "type": "image",
            "x": 72,
            "y": 66,
            "image": SLOT_05,
            "children": (
                {"name": "Ev_QFlagNameValue", "type": "editline", "x": 3, "y": 3, "width": 124, "height": 18, "input_limit": 48},
            ),
        },
        {
            "name": "Ev_QFlagValueSlot",
            "type": "image",
            "x": 206,
            "y": 66,
            "image": SLOT_02,
            "children": (
                {"name": "Ev_QFlagValueValue", "type": "editline", "x": 3, "y": 3, "width": 55, "height": 18, "input_limit": 10},
            ),
        },
        {
            "name": "Ev_QTargetSlot",
            "type": "image",
            "x": 272,
            "y": 66,
            "image": SLOT_03,
            "children": (
                {"name": "Ev_QTargetValue", "type": "editline", "x": 3, "y": 3, "width": 84, "height": 18, "input_limit": 24},
            ),
        },
        {"name": "Ev_SetQf", "type": "button", "x": 368, "y": 63, "text": "SetQF", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "Ev_GetQf", "type": "button", "x": 72, "y": 92, "text": "GetQF", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Ev_DelQf", "type": "button", "x": 133, "y": 92, "text": "DelQF", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "T4_StateLabel", "type": "text", "x": 10, "y": 124, "text": "set_state"},
        {
            "name": "Ev_StateQuestSlot",
            "type": "image",
            "x": 72,
            "y": 122,
            "image": SLOT_05,
            "children": (
                {"name": "Ev_StateQuestValue", "type": "editline", "x": 3, "y": 3, "width": 124, "height": 18, "input_limit": 32},
            ),
        },
        {
            "name": "Ev_StateNameSlot",
            "type": "image",
            "x": 206,
            "y": 122,
            "image": SLOT_04,
            "children": (
                {"name": "Ev_StateNameValue", "type": "editline", "x": 3, "y": 3, "width": 109, "height": 18, "input_limit": 32},
            ),
        },
        {"name": "Ev_SetState", "type": "button", "x": 324, "y": 119, "text": "SetState", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "T4_ClearLabel", "type": "text", "x": 10, "y": 156, "text": "clear_quest"},
        {
            "name": "Ev_ClearQuestSlot",
            "type": "image",
            "x": 72,
            "y": 154,
            "image": SLOT_05,
            "children": (
                {"name": "Ev_ClearQuestValue", "type": "editline", "x": 3, "y": 3, "width": 124, "height": 18, "input_limit": 48},
            ),
        },
        {"name": "Ev_ClearQuest", "type": "button", "x": 208, "y": 151, "text": "Clear", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "T4_Info", "type": "text", "x": 10, "y": 188, "text": "Target w setqf/getqf/delqf jest opcjonalny."},
    ),
}
