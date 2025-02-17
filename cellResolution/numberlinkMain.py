

from numberlinkDisplay import displayHexagonGame, displaySquareGame
from numberlinkSolver import solve_numberlink
from numberlinkHexaSolver import solve_numberlink_hexa
from game_storage import game_basic, game_CR, game_hexa, game_square_hard, game_square_with_bridges, game_impossible_because_loops, game_basic_walls, game_with_sol_not_all_filled
from make_paths import select_node_pairs_hex, select_node_pairs_rec


path = "./numberlink.cnf"


game = game_with_sol_not_all_filled
created_with_grid = True
hexa_grid = False
size = 5

if created_with_grid:
    if hexa_grid:
        x_human = select_node_pairs_hex(size)
        content = {"game":x_human, "size": size}
        print("not yet implemented")
    else:
        x_human = select_node_pairs_rec(size)
        content = {"game":x_human, "size": size}
        bridges = []
        answer, endDict, message, convertor,posBridgeDict, forbidden = solve_numberlink([], path, bridges=bridges, user_initialized=True, content=content)
        displaySquareGame(answer, endDict, convertor,message,bridges, posBridgeDict, forbidden, (size, size))
else:
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

        displaySquareGame(answer, endDict, convertor,message,bridges, posBridgeDict, forbidden, (len(game_schema), len(game_schema[0])))

