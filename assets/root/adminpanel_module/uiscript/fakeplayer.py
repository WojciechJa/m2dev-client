import uiScriptLocale
import localeInfo
import constInfo
import item

BOARD_WIDTH = 800
BOARD_HEIGHT = 520

COSTUME_START_INDEX = item.COSTUME_SLOT_START

IMG_PATH = "d:/ymir work/ui/adminpanel/create_item/"

window = {
    "name": "FakePlayerWindow",
    "x": (SCREEN_WIDTH / 2) - (BOARD_WIDTH / 2),
    "y": (SCREEN_HEIGHT / 2) - (BOARD_HEIGHT / 2),
    "style": ("float",),
    "width": BOARD_WIDTH,
    "height": BOARD_HEIGHT,
    "children":
        (
            {
                "name": "board", "type": "board_with_titlebar",
                "x": 0, "y": 0, "width": BOARD_WIDTH, "height": BOARD_HEIGHT,
                "title": "Fake Player Manager",
                "children":
                    (
                        ## LEFT COLUMN - Fake Player List
                        {
                            "name": "list_title", "type": "text",
                            "x": 20, "y": 35, "text": "Fake Players",
                        },
                        {
                            "name": "btn_delete_all", "type": "button",
                            "x": 95, "y": 33, "text": "DELETE ALL", "text_outline": 1,
                            "default_image": IMG_PATH + "button_1_normal.sub",
                            "over_image": IMG_PATH + "button_1_hover.sub",
                            "down_image": IMG_PATH + "button_1_down.sub",
                        },
                        {
                            "name": "list_search_board", "type": "thinboard_circle",
                            "x": 15, "y": 55, "width": 200, "height": 22,
                            "children":
                                (
                                    {"name": "list_search_label", "type": "text", "x": 5, "y": 4, "text": "Search:"},
                                    {
                                        "name": "list_search_editline", "type": "editline", "input_limit": 24,
                                        "x": 50, "y": 4, "width": 145, "height": 18,
                                    },
                                )
                        },
                        {
                            "name": "list_background", "type": "thinboard_circle",
                            "x": 15, "y": 80, "width": 200, "height": 340,
                        },
                        {
                            "name": "btn_refresh", "type": "button",
                            "x": 25, "y": 425, "text": "Refresh", "text_outline": 1,
                            "default_image": IMG_PATH + "button_1_normal.sub",
                            "over_image": IMG_PATH + "button_1_hover.sub",
                            "down_image": IMG_PATH + "button_1_down.sub",
                        },
                        {
                            "name": "btn_create_new", "type": "button",
                            "x": 145, "y": 425, "text": "Create New", "text_outline": 1,
                            "default_image": IMG_PATH + "button_1_normal.sub",
                            "over_image": IMG_PATH + "button_1_hover.sub",
                            "down_image": IMG_PATH + "button_1_down.sub",
                        },
                        {
                            "name": "btn_create_new_random_one", "type": "button",
                            "x": 265, "y": 425, "text": "Create Random One", "text_outline": 1,
                            "default_image": IMG_PATH + "button_1_normal.sub",
                            "over_image": IMG_PATH + "button_1_hover.sub",
                            "down_image": IMG_PATH + "button_1_down.sub",
                        },
                        {
                            "name": "btn_create_new_random_multi", "type": "button",
                            "x": 385, "y": 425, "text": "Create Random Multi", "text_outline": 1,
                            "default_image": IMG_PATH + "button_1_normal.sub",
                            "over_image": IMG_PATH + "button_1_hover.sub",
                            "down_image": IMG_PATH + "button_1_down.sub",
                        },
                        {
                            "name": "label_fake_players_number",
                            "type": "text",
                            "x": 555, "y": 427,
                            "text": "<< Fake Players to spawn"
                        },
                        {
                            "name": "edit_fake_players_number_bg", "type": "thinboard_circle",
                            "x": 508, "y": 425, "width": 44, "height": 22,
                            "children": (
                                {"name": "edit_fake_players_number",
                                 "type": "editline",
                                 "input_limit": 3,
                                 "only_number": 1,
                                 "x": 20, "y": 2,
                                 "width": 40, "height": 18,
                                 "text": "1"},
                            )
                        },
                        {
                            "name": "fake_players_naked_checkbox",
                            "type": "checkbox",
                            "x": 685,
                            "y": 429,
                            "text": "Naked",
                            "text_outline": 1,
                        },

                        ## MIDDLE COLUMN - Details/Edit
                        {
                            "name": "details_board", "type": "border_a",
                            "x": 225, "y": 40, "width": 270, "height": 380,
                            "children":
                                (
                                    {"name": "details_title", "type": "text", "x": 10, "y": 8, "text": "Details"},

                                    {"name": "label_name", "type": "text", "x": 10, "y": 32, "text": "Name:"},
                                    {
                                        "name": "edit_name_bg", "type": "thinboard_circle",
                                        "x": 78, "y": 28, "width": 184, "height": 22,
                                        "children": (
                                            {"name": "edit_name", "type": "editline", "input_limit": 24,
                                             "x": 2, "y": 2, "width": 180, "height": 18},
                                        )
                                    },

                                    {"name": "label_race", "type": "text", "x": 10, "y": 57, "text": "Race:"},

                                    {"name": "label_level", "type": "text", "x": 10, "y": 82, "text": "Level:"},
                                    {
                                        "name": "edit_level_bg", "type": "thinboard_circle",
                                        "x": 78, "y": 78, "width": 54, "height": 22,
                                        "children": (
                                            {"name": "edit_level", "type": "editline", "input_limit": 3,
                                             "only_number": 1,
                                             "x": 2, "y": 2, "width": 50, "height": 18},
                                        )
                                    },

                                    {"name": "label_empire", "type": "text", "x": 140, "y": 82, "text": "Empire:"},

                                    {"name": "label_st", "type": "text", "x": 10, "y": 112, "text": "ST:"},
                                    {
                                        "name": "edit_st_bg", "type": "thinboard_circle",
                                        "x": 38, "y": 108, "width": 54, "height": 22,
                                        "children": (
                                            {"name": "edit_st", "type": "editline", "input_limit": 4, "only_number": 1,
                                             "x": 2, "y": 2, "width": 50, "height": 18},
                                        )
                                    },

                                    {"name": "label_ht", "type": "text", "x": 100, "y": 112, "text": "HT:"},
                                    {
                                        "name": "edit_ht_bg", "type": "thinboard_circle",
                                        "x": 128, "y": 108, "width": 54, "height": 22,
                                        "children": (
                                            {"name": "edit_ht", "type": "editline", "input_limit": 4, "only_number": 1,
                                             "x": 2, "y": 2, "width": 50, "height": 18},
                                        )
                                    },

                                    {"name": "label_dx", "type": "text", "x": 10, "y": 137, "text": "DX:"},
                                    {
                                        "name": "edit_dx_bg", "type": "thinboard_circle",
                                        "x": 38, "y": 133, "width": 54, "height": 22,
                                        "children": (
                                            {"name": "edit_dx", "type": "editline", "input_limit": 4, "only_number": 1,
                                             "x": 2, "y": 2, "width": 50, "height": 18},
                                        )
                                    },

                                    {"name": "label_iq", "type": "text", "x": 100, "y": 137, "text": "IQ:"},
                                    {
                                        "name": "edit_iq_bg", "type": "thinboard_circle",
                                        "x": 128, "y": 133, "width": 54, "height": 22,
                                        "children": (
                                            {"name": "edit_iq", "type": "editline", "input_limit": 4, "only_number": 1,
                                             "x": 2, "y": 2, "width": 50, "height": 18},
                                        )
                                    },

                                    {"name": "label_alignment", "type": "text", "x": 10, "y": 167,
                                     "text": "Alignment:"},
                                    {
                                        "name": "edit_alignment_bg", "type": "thinboard_circle",
                                        "x": 78, "y": 163, "width": 84, "height": 22,
                                        "children": (
                                            {"name": "edit_alignment", "type": "editline", "input_limit": 10,
                                             "x": 2, "y": 2, "width": 80, "height": 18},
                                        )
                                    },

                                    {"name": "label_guild_id", "type": "text", "x": 10, "y": 192, "text": "Guild ID:"},
                                    {
                                        "name": "edit_guild_id_bg", "type": "thinboard_circle",
                                        "x": 78, "y": 188, "width": 84, "height": 22,
                                        "children": (
                                            {"name": "edit_guild_id", "type": "editline", "input_limit": 10,
                                             "only_number": 1,
                                             "x": 2, "y": 2, "width": 80, "height": 18},
                                        )
                                    },

                                    {"name": "label_language", "type": "text", "x": 10, "y": 217, "text": "Language:"},
                                    {
                                        "name": "edit_language_bg", "type": "thinboard_circle",
                                        "x": 78, "y": 213, "width": 54, "height": 22,
                                        "children": (
                                            {"name": "edit_language", "type": "editline", "input_limit": 8,
                                             "x": 2, "y": 2, "width": 50, "height": 18},
                                        )
                                    },

                                    {"name": "horizontal_bar", "type": "bar", "x": 10, "y": 245, "width": 250,
                                     "height": 1, "color": 0xFF6d645a},

                                    {
                                        "name": "btn_save", "type": "button",
                                        "x": 10, "y": 255, "text": "Save", "text_outline": 1,
                                        "default_image": IMG_PATH + "button_1_normal.sub",
                                        "over_image": IMG_PATH + "button_1_hover.sub",
                                        "down_image": IMG_PATH + "button_1_down.sub",
                                    },
                                    {
                                        "name": "btn_delete", "type": "button",
                                        "x": 140, "y": 255, "text": "Delete", "text_outline": 1,
                                        "default_image": IMG_PATH + "button_1_normal.sub",
                                        "over_image": IMG_PATH + "button_1_hover.sub",
                                        "down_image": IMG_PATH + "button_1_down.sub",
                                    },

                                    {"name": "horizontal_bar2", "type": "bar", "x": 10, "y": 290, "width": 250,
                                     "height": 1, "color": 0xFF6d645a},

                                    {
                                        "name": "btn_login", "type": "button",
                                        "x": 10, "y": 300, "text": "Login", "text_outline": 1,
                                        "default_image": IMG_PATH + "button_1_normal.sub",
                                        "over_image": IMG_PATH + "button_1_hover.sub",
                                        "down_image": IMG_PATH + "button_1_down.sub",
                                    },
                                    {
                                        "name": "btn_logout", "type": "button",
                                        "x": 140, "y": 300, "text": "Logout", "text_outline": 1,
                                        "default_image": IMG_PATH + "button_1_normal.sub",
                                        "over_image": IMG_PATH + "button_1_hover.sub",
                                        "down_image": IMG_PATH + "button_1_down.sub",
                                    },

                                    {"name": "horizontal_bar3", "type": "bar", "x": 10, "y": 335, "width": 250,
                                     "height": 1, "color": 0xFF6d645a},

                                    {"name": "label_status", "type": "text", "x": 10, "y": 345, "text": "Status: -"},
                                )
                        },

                        ## RIGHT COLUMN - Equipment (like uiinventory)
                        {
                            "name": "equip_board", "type": "border_a",
                            "x": 505, "y": 40, "width": 280, "height": 380,
                            "children":
                                (
                                    {"name": "equip_title", "type": "text", "x": 120, "y": 8, "text": "Equipment"},

                                    ## Equipment Slot - like real inventory
                                    {
                                        "name": "Equipment_Base",
                                        "type": "image",
                                        "x": 65,
                                        "y": 30,
                                        "image": "d:/ymir work/ui/equipment_bg_without_ring.tga",
                                        "children":
                                            (
                                                {
                                                    "name": "EquipmentSlot",
                                                    "type": "slot",
                                                    "x": 3,
                                                    "y": 3,
                                                    "width": 150,
                                                    "height": 182,
                                                    "slot": (
                                                        {"index": 0, "x": 39, "y": 37, "width": 32, "height": 64},
                                                        {"index": 1, "x": 39, "y": 2, "width": 32, "height": 32},
                                                        {"index": 2, "x": 39, "y": 145, "width": 32, "height": 32},
                                                        {"index": 3, "x": 75, "y": 67, "width": 32, "height": 32},
                                                        {"index": 4, "x": 3, "y": 3, "width": 32, "height": 96},
                                                        {"index": 5, "x": 114, "y": 67, "width": 32, "height": 32},
                                                        {"index": 6, "x": 114, "y": 35, "width": 32, "height": 32},
                                                        {"index": 7, "x": 2, "y": 145, "width": 32, "height": 32},
                                                        {"index": 8, "x": 75, "y": 145, "width": 32, "height": 32},
                                                        {"index": 9, "x": 114, "y": 2, "width": 32, "height": 32},
                                                        {"index": 10, "x": 75, "y": 35, "width": 32, "height": 32},
                                                        {"index": 11, "x": 39, "y": 106, "width": 32, "height": 32},
                                                    ),
                                                },
                                            ),
                                    },

                                    ## Costume Slots
                                    {"name": "costume_title", "type": "text", "x": 120, "y": 225, "text": "Costumes"},
                                    {
                                        "name": "Costume_Base",
                                        "type": "image",

                                        "x": 85,
                                        "y": 245,

                                        "image": "d:/ymir work/ui/costume/costume_bg.jpg",

                                        "children":
                                            (

                                                {
                                                    "name": "CostumeSlot",
                                                    "type": "slot",

                                                    "x": 3,
                                                    "y": 3,

                                                    "width": 127,
                                                    "height": 145,

                                                    "slot":
                                                        (
                                                            {"index": COSTUME_START_INDEX + 0, "x": 61, "y": 45,
                                                             "width": 32, "height": 64},
                                                            {"index": COSTUME_START_INDEX + 1, "x": 61, "y": 8,
                                                             "width": 32, "height": 32},
                                                            {"index": COSTUME_START_INDEX + 2, "x": 5, "y": 145,
                                                             "width": 32, "height": 32},
                                                        ),
                                                },
                                            ),
                                    },
                                )
                        },

                        ## BOTTOM BAR - Mass Login Controls
                        {
                            "name": "mass_control_board", "type": "thinboard_circle",
                            "x": 15, "y": 455, "width": 770, "height": 55,
                            "children":
                                (
                                    {
                                        "name": "btn_login_all",
                                        "type": "button",

                                        "x": 10,
                                        "y": 8,

                                        "text": "Login All", "text_outline": 1,

                                        "default_image": IMG_PATH + "button_1_normal.sub",
                                        "over_image": IMG_PATH + "button_1_hover.sub",
                                        "down_image": IMG_PATH + "button_1_down.sub",
                                    },
                                    {
                                        "name": "btn_logout_all",
                                        "type": "button",

                                        "x": 10,
                                        "y": 28,

                                        "text": "Logout All",
                                        "text_outline": 1,

                                        "default_image": IMG_PATH + "button_1_normal.sub",
                                        "over_image": IMG_PATH + "button_1_hover.sub",
                                        "down_image": IMG_PATH + "button_1_down.sub",
                                    },
                                    {
                                        "name": "btn_stop_mass",
                                        "type": "button",

                                        "x": 130,
                                        "y": 8,

                                        "text": "Stop",
                                        "text_outline": 1,

                                        "default_image": IMG_PATH + "button_1_normal.sub",
                                        "over_image": IMG_PATH + "button_1_hover.sub",
                                        "down_image": IMG_PATH + "button_1_down.sub",
                                    },

                                    {
                                        "name": "label_interval",
                                        "type": "text",
                                        "x": 460,
                                        "y": 33,
                                        "text": "Interval (sec):"
                                    },
                                    {
                                        "name": "edit_interval_bg", "type": "thinboard_circle",
                                        "x": 523, "y": 29, "width": 44, "height": 22,
                                        "children": (
                                            {"name": "edit_interval", "type": "editline", "input_limit": 4,
                                             "x": 2, "y": 2, "width": 40, "height": 18, "text": "1.0"},
                                        )
                                    },

                                    {"name": "label_progress", "type": "text", "x": 460, "y": 6, "text": "Progress:"},

                                    {
                                        "name": "progress_gauge", "type": "gauge",
                                        "x": 510, "y": 10, "width": 200, "height": 20,
                                        "color": "green",
                                    },

                                    {"name": "label_progress_text", "type": "text", "x": 600, "y": 33, "text": "0/0"},
                                )
                        },
                    )
            },
        ),
}
