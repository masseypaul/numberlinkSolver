
game_basic = {
    "hexa": False,
    "game": [
        "6A    ",
        "    6A",
        "34    ",
        "      ",
        "1    4",
        "2 21 3"],
}

game_basic_walls = {
    "game": [
        "#6A    ",
        "#    6A",
        "#34    ",
        "#      ",
        "#1    4",
        "#2 21 3"],
}

game_impossible_because_loops = {
    "game": ["3  32","2    ","1 1  ","4 4  "]
}

game_CR = {
    "game": [
        "###  1#23   ##",
        "##  ### ###  #",
        "#  #### #### #",
        "# ##### ####  ",
        "  ##### ##### ",
        " ###### ####  ",
        " ###### #### #",
        " ###### ###  #",
        " ###### 3   ##",
        "  ##### ##4###",
        "# ##### ##  ##",
        "#  #### ### ##",
        "##  ### ###  #",
        "###  1#2#### 4"        
    ]
}

game_square_hard = {
    "game": [
    "              A",
    "CA            7",
    "               ",
    "             3 ",
    "  D          6 ",
    "         1     ",
    "       9 5    2",
    "               ",
    "      7      4 ",
    "          9    ",
    "            34 ",
    "  D    6 15    ",
    "  C  2       B8",
    "       B       ",
    "8        E    E",
    ]
}
game_with_sol_not_all_filled = {
    "game": [
        "A         N   ",
        "I  I        E ",
        " A     J      ",
        "         JN   ",
        "              ",
        "         K    ",
        "   HG  K      ",
        "      L       ",
        "   GB     MC  ",
        "   H          ",
        "      D       ",
        "  M    C  D   ",
        "L           F ",
        "B         F  E"
    ]
}

game_square_with_bridges = {
    "game": [
    "          ",
    "          ",
    "    M     ",
    "   J  O   ",
    " B  V R IB",
    "VU J      ",
    "   O      ",
    " L  C    I",
    "      M  R",
    " U    L  C"
    ],
    "bridges": [(2,8),(5,5)]
}

game_hexa = {
    "hexa": True,
    "game": ["#A   ##",
            "# B C #",
            "    D #",
            "  D A E",
            "   C  #",
            "# E  B#",
            "#    ##"],
    "shiftFirstLine": True
}