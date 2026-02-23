import uiScriptLocale

ROOT_PATH = "d:/ymir work/ui/public/"

TEMPORARY_X = +13
TEXT_TEMPORARY_X = -10
BUTTON_TEMPORARY_X = 5
PVP_X = -10

window = {
    "name": "SystemOptionDialog",
    "style": ("movable", "float",),

    "x": 0,
    "y": 0,

    "width": 305,
    "height": 465,

    "children":
        (
            {
                "name": "board",
                "type": "board",

                "x": 0,
                "y": 0,

                "width": 305,
                "height": 465,

                "children":
                    (
                        ## Title
                        {
                            "name": "titlebar",
                            "type": "titlebar",
                            "style": ("attach",),

                            "x": 8,
                            "y": 8,

                            "width": 284,
                            "color": "gray",

                            "children":
                                (
                                    {
                                        "name": "titlename", "type": "text", "x": 0, "y": 3,
                                        "horizontal_align": "center", "text_horizontal_align": "center",
                                        "text": uiScriptLocale.SYSTEMOPTION_TITLE,
                                    },
                                ),
                        },

                        ## Music
                        {
                            "name": "music_name",
                            "type": "text",

                            "x": 30,
                            "y": 75,

                            "text": uiScriptLocale.OPTION_MUSIC,
                        },

                        {
                            "name": "music_volume_controller",
                            "type": "sliderbar",

                            "x": 110,
                            "y": 75,
                        },

                        {
                            "name": "bgm_button",
                            "type": "button",

                            "x": 20,
                            "y": 100,

                            "text": uiScriptLocale.OPTION_MUSIC_CHANGE,

                            "default_image": ROOT_PATH + "Middle_Button_01.sub",
                            "over_image": ROOT_PATH + "Middle_Button_02.sub",
                            "down_image": ROOT_PATH + "Middle_Button_03.sub",
                        },

                        {
                            "name": "bgm_file",
                            "type": "text",

                            "x": 100,
                            "y": 102,

                            "text": uiScriptLocale.OPTION_MUSIC_DEFAULT_THEMA,
                        },

                        ## Sound
                        {
                            "name": "sound_name",
                            "type": "text",

                            "x": 30,
                            "y": 50,

                            "text": uiScriptLocale.OPTION_SOUND,
                        },

                        {
                            "name": "sound_volume_controller",
                            "type": "sliderbar",

                            "x": 110,
                            "y": 50,
                        },

                        ## 카메라
                        {
                            "name": "camera_mode",
                            "type": "text",

                            "x": 40 + TEXT_TEMPORARY_X,
                            "y": 135 + 2,

                            "text": uiScriptLocale.OPTION_CAMERA_DISTANCE,
                        },

                        {
                            "name": "camera_short",
                            "type": "radio_button",

                            "x": 110,
                            "y": 135,

                            "text": uiScriptLocale.OPTION_CAMERA_DISTANCE_SHORT,

                            "default_image": ROOT_PATH + "Middle_Button_01.sub",
                            "over_image": ROOT_PATH + "Middle_Button_02.sub",
                            "down_image": ROOT_PATH + "Middle_Button_03.sub",
                        },

                        {
                            "name": "camera_long",
                            "type": "radio_button",

                            "x": 110 + 70,
                            "y": 135,

                            "text": uiScriptLocale.OPTION_CAMERA_DISTANCE_LONG,

                            "default_image": ROOT_PATH + "Middle_Button_01.sub",
                            "over_image": ROOT_PATH + "Middle_Button_02.sub",
                            "down_image": ROOT_PATH + "Middle_Button_03.sub",
                        },

                        ## 안개
                        {
                            "name": "fog_mode",
                            "type": "text",

                            "x": 30,
                            "y": 160 + 2,

                            "text": uiScriptLocale.OPTION_FOG,
                        },

                        {
                            "name": "fog_level0",
                            "type": "radio_button",

                            "x": 110,
                            "y": 160,

                            "text": uiScriptLocale.OPTION_FOG_DENSE,

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },

                        {
                            "name": "fog_level1",
                            "type": "radio_button",

                            "x": 110 + 50,
                            "y": 160,

                            "text": uiScriptLocale.OPTION_FOG_MIDDLE,

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },

                        {
                            "name": "fog_level2",
                            "type": "radio_button",

                            "x": 110 + 100,
                            "y": 160,

                            "text": uiScriptLocale.OPTION_FOG_LIGHT,

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },

                        ## 타일 가속
                        {
                            "name": "tiling_mode",
                            "type": "text",

                            "x": 40 + TEXT_TEMPORARY_X,
                            "y": 185 + 2,

                            "text": uiScriptLocale.OPTION_TILING,
                        },

                        {
                            "name": "tiling_cpu",
                            "type": "radio_button",

                            "x": 110,
                            "y": 185,

                            "text": uiScriptLocale.OPTION_TILING_CPU,

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },

                        {
                            "name": "tiling_gpu",
                            "type": "radio_button",

                            "x": 110 + 50,
                            "y": 185,

                            "text": uiScriptLocale.OPTION_TILING_GPU,

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },

                        {
                            "name": "tiling_apply",
                            "type": "button",

                            "x": 110 + 100,
                            "y": 185,

                            "text": uiScriptLocale.OPTION_TILING_APPLY,

                            "default_image": ROOT_PATH + "middle_Button_01.sub",
                            "over_image": ROOT_PATH + "middle_Button_02.sub",
                            "down_image": ROOT_PATH + "middle_Button_03.sub",
                        },

                        {
                            "name": "fps_mode",
                            "type": "text",

                            "x": 30,
                            "y": 210 + 2,

                            "text": "FPS",
                        },
                        {
                            "name": "fps_60",
                            "type": "radio_button",

                            "x": 110,
                            "y": 210,

                            "text": "60",

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },
                        {
                            "name": "fps_90",
                            "type": "radio_button",

                            "x": 150,
                            "y": 210,

                            "text": "90",

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },
                        {
                            "name": "fps_120",
                            "type": "radio_button",

                            "x": 190,
                            "y": 210,

                            "text": "120",

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },
                        {
                            "name": "fps_unlimited",
                            "type": "radio_button",

                            "x": 230,
                            "y": 210,

                            "text": "Unlimited",

                            "default_image": ROOT_PATH + "Middle_Button_01.sub",
                            "over_image": ROOT_PATH + "Middle_Button_02.sub",
                            "down_image": ROOT_PATH + "Middle_Button_03.sub",
                        },
                        {
                            "name": "separator1",
                            "type": "image",
                            "x": 0,
                            "y": 225,
                            "image": "d:/ymir work/ui/center.tga",
                        },
                        {
                            "name": "separator2",
                            "type": "image",
                            "x": 100,
                            "y": 225,
                            "image": "d:/ymir work/ui/center.tga",
                        },
                        {
                            "name": "perf_mode",
                            "type": "text",

                            "x": 30,
                            "y": 263,

                            "text": "Performance",
                        },
                        {
                            "name": "profile_quality",
                            "type": "radio_button",

                            "x": 110,
                            "y": 260,

                            "text": "Quality",

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },
                        {
                            "name": "profile_balanced",
                            "type": "radio_button",

                            "x": 160,
                            "y": 260,

                            "text": "Balanced",

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },
                        {
                            "name": "profile_performance",
                            "type": "radio_button",

                            "x": 210,
                            "y": 260,

                            "text": "Perf",

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },
                        {
                            "name": "fx_adaptive_toggle",
                            "type": "toggle_button",

                            "x": 110,
                            "y": 285,

                            "text": "FX Adaptive",

                            "default_image": ROOT_PATH + "Middle_Button_01.sub",
                            "over_image": ROOT_PATH + "Middle_Button_02.sub",
                            "down_image": ROOT_PATH + "Middle_Button_03.sub",
                        },
                        {
                            "name": "anim_lod_toggle",
                            "type": "toggle_button",

                            "x": 180,
                            "y": 285,

                            "text": "Anim LOD",

                            "default_image": ROOT_PATH + "Middle_Button_01.sub",
                            "over_image": ROOT_PATH + "Middle_Button_02.sub",
                            "down_image": ROOT_PATH + "Middle_Button_03.sub",
                        },
                        {
                            "name": "texttail_opt_toggle",
                            "type": "toggle_button",

                            "x": 110,
                            "y": 310,

                            "text": "TextTail Opt",

                            "default_image": ROOT_PATH + "Middle_Button_01.sub",
                            "over_image": ROOT_PATH + "Middle_Button_02.sub",
                            "down_image": ROOT_PATH + "Middle_Button_03.sub",
                        },
                        {
                            "name": "vsync_toggle",
                            "type": "toggle_button",

                            "x": 180,
                            "y": 310,

                            "text": "VSync",

                            "default_image": ROOT_PATH + "Middle_Button_01.sub",
                            "over_image": ROOT_PATH + "Middle_Button_02.sub",
                            "down_image": ROOT_PATH + "Middle_Button_03.sub",
                        },
                        {
                            "name": "shadow_cadence_mode",
                            "type": "text",

                            "x": 30,
                            "y": 338,

                            "text": "ShadowCadence",
                        },
                        {
                            "name": "shadow_cadence_1",
                            "type": "radio_button",

                            "x": 110,
                            "y": 335,

                            "text": "1",

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },
                        {
                            "name": "shadow_cadence_2",
                            "type": "radio_button",

                            "x": 160,
                            "y": 335,

                            "text": "2",

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },
                        {
                            "name": "shadow_cadence_3",
                            "type": "radio_button",

                            "x": 210,
                            "y": 335,

                            "text": "3",

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },
                        {
                            "name": "texttail_range_title",
                            "type": "text",

                            "x": 30,
                            "y": 363,

                            "text": "TextTail:",
                        },
                        {
                            "name": "texttail_range_controller",
                            "type": "sliderbar",

                            "x": 110,
                            "y": 365,
                        },
                        {
                            "name" : "texttail_range_value",
                            "type" : "text",

                            "x" : 70,
                            "y" : 363,

                            "text" : "3500",
                        },
                        {
                            "name": "fx_stride_bias_mode",
                            "type": "text",

                            "x": 30,
                            "y": 388,

                            "text": "FX Stride",
                        },
                        {
                            "name": "fx_stride_bias_0",
                            "type": "radio_button",

                            "x": 110,
                            "y": 385,

                            "text": "Cons",

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },
                        {
                            "name": "fx_stride_bias_1",
                            "type": "radio_button",

                            "x": 160,
                            "y": 385,

                            "text": "Bal",

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },
                        {
                            "name": "fx_stride_bias_2",
                            "type": "radio_button",

                            "x": 210,
                            "y": 385,

                            "text": "Aggr",

                            "default_image": ROOT_PATH + "small_Button_01.sub",
                            "over_image": ROOT_PATH + "small_Button_02.sub",
                            "down_image": ROOT_PATH + "small_Button_03.sub",
                        },
                        {
                            "name": "shadow_dynamic_boost_toggle",
                            "type": "toggle_button",

                            "x": 110,
                            "y": 410,

                            "text": "Shadow Boost",

                            "default_image": ROOT_PATH + "Middle_Button_01.sub",
                            "over_image": ROOT_PATH + "Middle_Button_02.sub",
                            "down_image": ROOT_PATH + "Middle_Button_03.sub",
                        },
                        {
                            "name": "texttail_grid_opt_toggle",
                            "type": "toggle_button",

                            "x": 190,
                            "y": 410,

                            "text": "TextTail Grid",

                            "default_image": ROOT_PATH + "Middle_Button_01.sub",
                            "over_image": ROOT_PATH + "Middle_Button_02.sub",
                            "down_image": ROOT_PATH + "Middle_Button_03.sub",
                        },

                        ## 그림자
                        #				{
                        #					"name" : "shadow_mode",
                        #					"type" : "text",

                        #					"x" : 30,
                        #					"y" : 210,

                        #					"text" : uiScriptLocale.OPTION_SHADOW,
                        #				},

                        #				{
                        #					"name" : "shadow_bar",
                        #					"type" : "sliderbar",

                        #					"x" : 110,
                        #					"y" : 210,
                        #				},
                    ),
            },
        ),
}
