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
SLOT_02 = "d:/ymir work/ui/public/Parameter_Slot_02.sub"
SLOT_03 = "d:/ymir work/ui/public/Parameter_Slot_03.sub"

window = {
    "name": "GMTab2",
    "x": PAGE_X,
    "y": PAGE_Y,
    "width": PAGE_W,
    "height": PAGE_H,
    "children": (
        {
            "name": "T2_Title",
            "type": "expanded_image",
            "x": 0,
            "y": 2,
            "image": "d:/ymir work/ui/tab_menu_01.tga",
            "children": (
                {"name": "Players_Title", "type": "text", "x": 10, "y": 3, "text": "Players"},
            ),
        },

        {"name": "T2_NameLabel", "type": "text", "x": 10, "y": 30, "text": "Name"},
        {
            "name": "Ply_NameSlot",
            "type": "image",
            "x": 40,
            "y": 29,
            "image": SLOT_03,
            "children": (
                {"name": "Ply_NameValue", "type": "editline", "x": 3, "y": 3, "width": 84, "height": 18, "input_limit": 24},
            ),
        },

        {"name": "Ply_DC", "type": "button", "x": 136, "y": 27, "text": "DC", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Ply_Kill", "type": "button", "x": 197, "y": 27, "text": "Kill", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Ply_Transfer", "type": "button", "x": 258, "y": 27, "text": "Transfer", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Ply_Stun", "type": "button", "x": 319, "y": 27, "text": "Stun", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "Ply_Slow", "type": "button", "x": 136, "y": 55, "text": "Slow", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Ply_ResetSelf", "type": "button", "x": 197, "y": 55, "text": "Reset", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Ply_Cooltime", "type": "button", "x": 258, "y": 55, "text": "Cooltime", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Ply_AllSkill", "type": "button", "x": 319, "y": 55, "text": "AllSkill", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

# ------------------------------------------------------------------------
        {
            "name": "------",
            "type": "image",
            "x": 0,
            "y": 77,
            "image": "d:/ymir work/ui/center2.tga",
        },
# ------------------------------------------------------------------------

        {"name": "T2_LevelLabel", "type": "text", "x": 10, "y": 90, "text": "Level"},
        {
            "name": "Ply_LevelSlot",
            "type": "image",
            "x": 40,
            "y": 88,
            "image": SLOT_03,
            "children": (
                {"name": "Ply_LevelValue", "type": "editline", "x": 3, "y": 3, "width": 84, "height": 18, "input_limit": 3, "only_number": 1},
            ),
        },
        {"name": "Ply_LevelSelf", "type": "button", "x": 136, "y": 86, "text": "Self Level", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
        {"name": "Ply_Advance", "type": "button", "x": 198, "y": 86, "text": "Advance", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "T2_BlockLabel", "type": "text", "x": 10, "y": 122, "text": "Block min"},
        {
            "name": "Ply_BlockMinsSlot",
            "type": "image",
            "x": 68,
            "y": 120,
            "image": SLOT_02,
            "children": (
                {"name": "Ply_BlockMinsValue", "type": "editline", "x": 3, "y": 3, "width": 55, "height": 18, "input_limit": 6, "only_number": 1},
            ),
        },
        {"name": "Ply_BlockChat", "type": "button", "x": 136, "y": 117, "text": "Block Chat", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "T2_SetLabel", "type": "text", "x": 10, "y": 154, "text": "set field/value"},
        {
            "name": "Ply_SetFieldSlot",
            "type": "image",
            "x": 75,
            "y": 152,
            "image": SLOT_02,
            "children": (
                {"name": "Ply_SetFieldValue", "type": "editline", "x": 3, "y": 3, "width": 55, "height": 18, "input_limit": 16},
            ),
        },
        {
            "name": "Ply_SetValueSlot",
            "type": "image",
            "x": 135,
            "y": 152,
            "image": SLOT_02,
            "children": (
                {"name": "Ply_SetValueValue", "type": "editline", "x": 3, "y": 3, "width": 55, "height": 18, "input_limit": 16},
            ),
        },
        {"name": "Ply_SetApply", "type": "button", "x": 198, "y": 149, "text": "Set", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "T2_SkillLabel", "type": "text", "x": 10, "y": 186, "text": "skill/lvl"},
        {
            "name": "Ply_SkillSlot",
            "type": "image",
            "x": 75,
            "y": 184,
            "image": SLOT_02,
            "children": (
                {"name": "Ply_SkillValue", "type": "editline", "x": 3, "y": 3, "width": 55, "height": 18, "input_limit": 24},
            ),
        },
        {
            "name": "Ply_SkillLevelSlot",
            "type": "image",
            "x": 140,
            "y": 184,
            "image": SLOT_01,
            "children": (
                {"name": "Ply_SkillLevelValue", "type": "editline", "x": 3, "y": 3, "width": 46, "height": 18, "input_limit": 2, "only_number": 1},
            ),
        },
        {"name": "Ply_SetSkillOther", "type": "button", "x": 198, "y": 181, "text": "SetSkillOther", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},

        {"name": "Ply_ResetSubskill", "type": "button", "x": 380, "y": 55, "text": "ResetSubskill", "default_image": BTN1, "over_image": BTN2, "down_image": BTN3},
    ),
}
