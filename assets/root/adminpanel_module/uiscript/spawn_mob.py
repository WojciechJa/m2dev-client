import localeInfo

IMG_PATH = "d:/ymir work/ui/adminpanel/create_item/"
SELECT_PATH = "d:/ymir work/ui/select/"
BUTTON_PATH = "d:/ymir work/ui/game/monster_card/button/"
RADIO_BUTTON_TEXT_X = 20   # FIXED: Reduced from 25 to 20 for better text positioning
PRIMARY_COLOR = 0xffd0c2b7

window = {
    "name": "SpawnMobWindow",
    "x": 0, "y": 0,
    "style": ("movable", "float",),
    "width": 490, "height": 475,
    "children":
        (
            {"name": "board",
             "type": "board_with_titlebar",
             "x": 0,
             "y": 0,
             "width": 490,
             "height": 475,
             "title": localeInfo.ADMINPANEL_SPAWN_MOB_TITLE,
             "children":
                 (
                     # Reset and Spawn buttons
                     {
                         "name": "ResetButton",
                         "type": "button",
                         "x": 355, "y": 415,
                         "text_outline": 1,
                         "text": localeInfo.ADMINPANEL_SPAWN_MOB_RESET_BUTTON,
                         "default_image": IMG_PATH + "button_1_normal.sub",
                         "over_image": IMG_PATH + "button_1_hover.sub",
                         "down_image": IMG_PATH + "button_1_down.sub",
                     },
                     {
                         "name": "SpawnButton",
                         "type": "button",
                         "x": 355,
                         "y": 440,
                         "text_outline": 1,
                         "text": localeInfo.ADMINPANEL_SPAWN_MOB_SPAWN_BUTTON,
                         "default_image": IMG_PATH + "button_1_normal.sub",
                         "over_image": IMG_PATH + "button_1_hover.sub",
                         "down_image": IMG_PATH + "button_1_down.sub",
                     },
                     {
                         "name": "coord_select_btn",
                         "type": "button",
                         "x": 225,
                         "y": 422,
                         #"default_image": "icon/button/tp1.png",
                         #"over_image": "icon/button/tp2.png",
                         #"down_image": "icon/button/tp3.png",
                     },

                     # Search box for mobs
                     {
                         "name": "moblist_search",
                         "type": "thinboard_circle",
                         "x": 15, "y": 40,
                         "width": 200, "height": 20,
                         "children":
                             (
                                 {"name": "moblist_searchinfo", "type": "text", "x": 5, "y": 3,
                                  "text": "Szukaj:"},
                                 {
                                     "name": "mobsearch", "type": "editline", "input_limit": 24,
                                     "x": 50, "y": 3, "width": 150, "height": 30,
                                 },
                             )
                     },

                     # Mob list
                     {
                         "name": "moblist_background", "type": "thinboard_circle",
                         "x": 15, "y": 65, "width": 200, "height": 270,
                     },

                     # Pagination
                     {
                         "name": "prev_page_btn",
                         "type": "button",
                         "x": 20, "y": 340,
                         "default_image": SELECT_PATH + "arrowleft.png",
                         "over_image": SELECT_PATH + "arrowleft.png",
                         "down_image": SELECT_PATH + "arrowleft.png",
                     },
                     {
                         "name": "page_info",
                         "type": "text",
                         "x": 115, "y": 346,
                         "text": "1/1",
                         "text_horizontal_align": "center",
                     },
                     {
                         "name": "next_page_btn", "type": "button",
                         "x": 180, "y": 340,
                         "default_image": SELECT_PATH + "arrowright.png",
                         "over_image": SELECT_PATH + "arrowright.png",
                         "down_image": SELECT_PATH + "arrowright.png",
                     },

                     # Field for count
                     {"name": "field_set_count",
                      "type": "image",
                      "x": 15, "y": 375,
                      "image": IMG_PATH + "textfield_1.sub",
                      "children": (
                          {
                            "name": "info_set_count",
                           "type": "text",
                           "x": 43,
                           "y": 9,
                           "text_horizontal_align": "center",
                           "text_vertical_align": "center",
                           "text": localeInfo.ADMINPANEL_SPAWN_MOB_COUNT_LABEL
                           },
                          {
                              "name": "editline_set_count",
                              "type": "editline",
                              "x": 97,
                              "y": 19,
                              "width": 100,
                              "height": 16,
                              "input_limit": 3,
                              "default_text": "1",
                              "only_number": 1,
                              "text_horizontal_align": "center",
                          },
                          {
                              "name": "field_set_count_overlay",
                              "type": "image",
                              "x": 0,
                              "y": 0,
                              "image": IMG_PATH + "textfield_1.sub",
                          }
                      ),
                      },

                     # Field for sort mode - FIXED TO ACCOMMODATE COMBOBOX
                        {
                         "name": "field_sort_mode",
                         "type": "image",
                         "x": 15, "y": 420,
                         "image": IMG_PATH + "textfield_1.sub",
                              "children": (
                        {
                              "name": "info_sort_mode",
                              "type": "text",
                              "x": 43, "y": 9,
                              "text_horizontal_align": "center",
                              "text_vertical_align": "center",
                              "text": "Sortowanie:"  # Added colon for better formatting
                        },
                        {
                              "name": "field_sort_mode_overlay",
                              "type": "image",
                              "x": 0, "y": 0,
                              "image": IMG_PATH + "textfield_1.sub",
                        }
                      ),
                      },

                     # Configuration panel with 3D model and controls
                     {
                         "name": "mob_config_board",
                         "type": "border_a",
                         "x": 225, "y": 40,
                         "width": 250, "height": 310,
                         "children":
                             (
                                 # Mob title bar
                                 {"name": "titlebar_mob_1",
                                  "type": "image",
                                  "x": 3, "y": 2,
                                  "image": IMG_PATH + "titlebar_1.sub", },

                                 # 3D Model preview area background
                                 {
                                     "name": "model_preview_background",
                                     "type": "thinboard_circle",
                                     "x": 5, "y": 5,
                                     "width": 240, "height": 280,
                                 },

                                 # 3D MODEL CONTROL BUTTONS
                                 # Up camera button
                                 {
                                     "name": "mv_up_button", "type": "button",
                                     "x": 5, "y": 288,
                                     "default_image": BUTTON_PATH + "up_camera/up_camera_button_default.sub",
                                     "over_image": BUTTON_PATH + "up_camera/up_camera_button_over.sub",
                                     "down_image": BUTTON_PATH + "up_camera/up_camera_button_down.sub",
                                 },

                                 # Down camera button
                                 {
                                     "name": "mv_down_button", "type": "button",
                                     "x": 23, "y": 288,
                                     "default_image": BUTTON_PATH + "down_camera/down_camera_button_default.sub",
                                     "over_image": BUTTON_PATH + "down_camera/down_camera_button_over.sub",
                                     "down_image": BUTTON_PATH + "down_camera/down_camera_button_down.sub",
                                 },

                                 # Left rotation button
                                 {
                                     "name": "left_rotation_button", "type": "button",
                                     "x": 41, "y": 288,
                                     "default_image": BUTTON_PATH + "left_rotation/left_rotation_button_default.sub",
                                     "over_image": BUTTON_PATH + "left_rotation/left_rotation_button_over.sub",
                                     "down_image": BUTTON_PATH + "left_rotation/left_rotation_button_down.sub",
                                 },

                                 # Right rotation button
                                 {
                                     "name": "right_rotation_button", "type": "button",
                                     "x": 59, "y": 288,
                                     "default_image": BUTTON_PATH + "right_rotation/right_rotation_button_default.sub",
                                     "over_image": BUTTON_PATH + "right_rotation/right_rotation_button_over.sub",
                                     "down_image": BUTTON_PATH + "right_rotation/right_rotation_button_down.sub",
                                 },

                                 # Model view reset button
                                 {
                                     "name": "mv_reset_button", "type": "button",
                                     "x": 77, "y": 288,
                                     "default_image": BUTTON_PATH + "mv_reset/mv_reset_button_default.sub",
                                     "over_image": BUTTON_PATH + "mv_reset/mv_reset_button_over.sub",
                                     "down_image": BUTTON_PATH + "mv_reset/mv_reset_button_down.sub",
                                 },

                                 # Zoom in button
                                 {
                                     "name": "zoomin_button", "type": "button",
                                     "x": 95, "y": 288,
                                     "default_image": BUTTON_PATH + "zoomin/zoomin_rotation_button_default.sub",
                                     "over_image": BUTTON_PATH + "zoomin/zoomin_rotation_button_over.sub",
                                     "down_image": BUTTON_PATH + "zoomin/zoomin_rotation_button_down.sub",
                                 },

                                 # Zoom out button
                                 {
                                     "name": "zoomout_button", "type": "button",
                                     "x": 113, "y": 288,
                                     "default_image": BUTTON_PATH + "zoomout/zoomin_rotation_button_default.sub",
                                     "over_image": BUTTON_PATH + "zoomout/zoomin_rotation_button_over.sub",
                                     "down_image": BUTTON_PATH + "zoomout/zoomin_rotation_button_down.sub",
                                 },

                                 # Motion change button
                                 {
                                     "name": "motion_button", "type": "button",
                                     "x": 160, "y": 288,
                                     "default_image": BUTTON_PATH + "motion/motion_button_default.sub",
                                     "over_image": BUTTON_PATH + "motion/motion_button_over.sub",
                                     "down_image": BUTTON_PATH + "motion/motion_button_down.sub",
                                 },
                             )
                     },

                     # SPAWN MODE RADIO BUTTONS - PROPER TEXT POSITIONING LIKE ADVANCED GAME OPTIONS
                     {
                         "name": "spawn_mode_window",
                         "type": "window",
                         "x": 225, "y": 355,
                         "width": 150, "height": 50,
                         "children": (
                             # Radio buttons without text - like advanced game options
                             {
                                 "name": "spawn_mode_point",
                                 "type": "radio_button",
                                 "x": 0,
                                 "y": 0,
                                 "default_image": "d:/ymir work/ui/game/advanced_game_options/radio_unselected.png",
                                 "over_image": "d:/ymir work/ui/game/advanced_game_options/radio_unselected.png",
                                 "down_image": "d:/ymir work/ui/game/advanced_game_options/radio_selected.png",
                             },
                             {
                                 "name": "spawn_mode_random",
                                 "type": "radio_button",
                                 "x": 0,
                                 "y": 20,
                                 "default_image": "d:/ymir work/ui/game/advanced_game_options/radio_unselected.png",
                                 "over_image": "d:/ymir work/ui/game/advanced_game_options/radio_unselected.png",
                                 "down_image": "d:/ymir work/ui/game/advanced_game_options/radio_selected.png",
                             },
                             {
                                 "name": "spawn_mode_map",
                                 "type": "radio_button",
                                 "x": 0,
                                 "y": 40,
                                 "default_image": "d:/ymir work/ui/game/advanced_game_options/radio_unselected.png",
                                 "over_image": "d:/ymir work/ui/game/advanced_game_options/radio_unselected.png",
                                 "down_image": "d:/ymir work/ui/game/advanced_game_options/radio_selected.png",
                             },
                             # Separate text elements positioned next to radio buttons
                             {
                                 "name": "spawn_mode_point_text",
                                 "type": "text",
                                 "x": RADIO_BUTTON_TEXT_X,
                                 "y": 0,  # Centered with radio button
                                 "text_horizontal_align": "left",
                                 "text": localeInfo.ADMINPANEL_SPAWN_MOB_MODE_POINT,
                                 "color": PRIMARY_COLOR,
                             },
                             {
                                 "name": "spawn_mode_random_text",
                                 "type": "text",
                                 "x": RADIO_BUTTON_TEXT_X,
                                 "y": 20,  # Centered with radio button (20 + 4)
                                 "text_horizontal_align": "left",
                                 "text": localeInfo.ADMINPANEL_SPAWN_MOB_MODE_RANDOM,
                                 "color": PRIMARY_COLOR,
                             },
                             {
                                 "name": "spawn_mode_map_text",
                                 "type": "text",
                                 "x": RADIO_BUTTON_TEXT_X,
                                 "y": 40,  # Centered with radio button (40 + 4)
                                 "text_horizontal_align": "left",
                                 "text": localeInfo.ADMINPANEL_SPAWN_MOB_MODE_MAP,
                                 "color": PRIMARY_COLOR,
                             },
                         ),
                     },
                 )
             },
        ),
}