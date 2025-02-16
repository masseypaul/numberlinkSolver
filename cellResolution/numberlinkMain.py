

from numberlinkDisplay import displayHexagonGame, displaySquareGame
from numberlinkSolver import solve_numberlink
from numberlinkHexaSolver import solve_numberlink_hexa
from game_storage import game_basic, game_CR, game_hexa, game_square_hard, game_square_with_bridges, game_impossible_because_loops, game_basic_walls, game_with_sol_not_all_filled



path = "./numberlink.cnf"


game = game_with_sol_not_all_filled
if "hexa" in game and game["hexa"]:
    game_schema = game["game"]
    shiftFirstLine = game["shiftFirstLine"]
    bridges=[]
    answer, endDict, message, convertor,posBridgeDict, forbidden = solve_numberlink_hexa(game_schema, path,shiftFirstLine)
    displayHexagonGame(answer, endDict, convertor,message,bridges, posBridgeDict, forbidden,shiftFirstLine, game_schema)
else:
    game_schema = game["game"]
    bridges = game["bridges"] if "bridges" in game else []
    answer, endDict, message, convertor,posBridgeDict, forbidden = solve_numberlink(game_schema, path, bridges)

    displaySquareGame(answer, endDict, convertor,message,bridges, posBridgeDict, forbidden, game_schema)
    
