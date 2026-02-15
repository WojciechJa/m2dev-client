import uiScriptLocale
import localeInfo
import constInfo

BOARD_WIDTH = 320
BOARD_HEIGHT = 250

IMG_PATH = "d:/ymir work/ui/adminpanel/create_item/"

window = {
    "name": "CreateFakePlayerDialog",
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
            "title": "Create Fake Player",
            "children":
            (
                # Name
                {"name": "label_name", "type": "text", "x": 20, "y": 42, "text": "Name:"},
                {
                    "name": "edit_name_bg", "type": "thinboard_circle",
                    "x": 98, "y": 38, "width": 184, "height": 22,
                    "children": (
                        {"name": "edit_name", "type": "editline", "x": 2, "y": 2, "width": 180, "height": 18, "input_limit": 24},
                    )
                },

                # Race (label only - ComboBox added dynamically)
                {"name": "label_race", "type": "text", "x": 20, "y": 70, "text": "Race:"},

                # Level
                {"name": "label_level", "type": "text", "x": 20, "y": 102, "text": "Level:"},
                {
                    "name": "edit_level_bg", "type": "thinboard_circle",
                    "x": 98, "y": 98, "width": 54, "height": 22,
                    "children": (
                        {"name": "edit_level", "type": "editline", "x": 2, "y": 2, "width": 50, "height": 18, "input_limit": 3, "only_number": 1, "text": "1"},
                    )
                },

                # Empire (label only - ComboBox added dynamically)
                {"name": "label_empire", "type": "text", "x": 20, "y": 130, "text": "Empire:"},

                # Stats row
                {"name": "label_st", "type": "text", "x": 20, "y": 162, "text": "ST:"},
                {
                    "name": "edit_st_bg", "type": "thinboard_circle",
                    "x": 48, "y": 158, "width": 44, "height": 22,
                    "children": (
                        {"name": "edit_st", "type": "editline", "x": 2, "y": 2, "width": 40, "height": 18, "input_limit": 4, "only_number": 1, "text": "10"},
                    )
                },

                {"name": "label_ht", "type": "text", "x": 100, "y": 162, "text": "HT:"},
                {
                    "name": "edit_ht_bg", "type": "thinboard_circle",
                    "x": 128, "y": 158, "width": 44, "height": 22,
                    "children": (
                        {"name": "edit_ht", "type": "editline", "x": 2, "y": 2, "width": 40, "height": 18, "input_limit": 4, "only_number": 1, "text": "10"},
                    )
                },

                {"name": "label_dx", "type": "text", "x": 180, "y": 162, "text": "DX:"},
                {
                    "name": "edit_dx_bg", "type": "thinboard_circle",
                    "x": 208, "y": 158, "width": 44, "height": 22,
                    "children": (
                        {"name": "edit_dx", "type": "editline", "x": 2, "y": 2, "width": 40, "height": 18, "input_limit": 4, "only_number": 1, "text": "10"},
                    )
                },

                {"name": "label_iq", "type": "text", "x": 260, "y": 162, "text": "IQ:"},
                {
                    "name": "edit_iq_bg", "type": "thinboard_circle",
                    "x": 283, "y": 158, "width": 29, "height": 22,
                    "children": (
                        {"name": "edit_iq", "type": "editline", "x": 2, "y": 2, "width": 25, "height": 18, "input_limit": 4, "only_number": 1, "text": "10"},
                    )
                },

                # Language
                {"name": "label_language", "type": "text", "x": 20, "y": 192, "text": "Language:"},
                {
                    "name": "edit_language_bg", "type": "thinboard_circle",
                    "x": 98, "y": 188, "width": 54, "height": 22,
                    "children": (
                        {"name": "edit_language", "type": "editline", "x": 2, "y": 2, "width": 50, "height": 18, "input_limit": 8, "text": "en"},
                    )
                },

                # Buttons
                {
                    "name": "btn_create", "type": "button",
                    "x": 180, "y": 215, "text": "Create", "text_outline": 1,
                    "default_image": IMG_PATH + "button_1_normal.sub",
                    "over_image": IMG_PATH + "button_1_hover.sub",
                    "down_image": IMG_PATH + "button_1_down.sub",
                },
                {
                    "name": "btn_cancel", "type": "button",
                    "x": 20, "y": 215, "text": "Cancel", "text_outline": 1,
                    "default_image": IMG_PATH + "button_1_normal.sub",
                    "over_image": IMG_PATH + "button_1_hover.sub",
                    "down_image": IMG_PATH + "button_1_down.sub",
                },
            )
        },
    ),
}
