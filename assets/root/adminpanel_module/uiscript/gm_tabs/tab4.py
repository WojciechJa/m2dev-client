BOARD_WIDTH = 456
BOARD_HEIGHT = 370
TAB_HEIGHT = 36
PAGE_X = 10
PAGE_Y = TAB_HEIGHT + 8
PAGE_W = BOARD_WIDTH - 20
PAGE_H = BOARD_HEIGHT - (TAB_HEIGHT + 26)

window = {
	"name" : "GMTab4",
	"x" : PAGE_X,
	"y" : PAGE_Y,
	"width" : PAGE_W,
	"height" : PAGE_H,
	"children" :
	(
		{ "name" : "Page_04_Text", "type" : "text", "x" : 0, "y" : 0, "text" : "Tab 4 (Misc 1)", "all_align" : "center", },
	),
}
