import subprocess
from itertools import combinations, product

#%% Outside actions
def write_in_file_cnf(path,res,nb):
    with open(path,"w") as f:
        f.write(f"p cnf {nb} {len(res)}\n")
        for clause in res:
            s=""
            for c in clause:
                s+=str(c)+" "
            s+="0\n"
            f.write(s)
        f.close()
    print("okay pour le file")

def run_command(command,shortEnding = False):
    try:
        resultat = subprocess.run(command, capture_output=True)
        sortie = str(resultat.stdout)
        sortie_split = sortie.split("\\n")
        is_satisfiable = False
        answer = "v"
        for line in sortie_split:
            if len(line) > 0 and line[0] == "s":
                is_satisfiable = "UNSATISFIABLE" not in line
            if  len(line) > 0 and line[0] == "v":
                if shortEnding:
                    answer = line[2:]
                else:
                    answer = line[2:-2]
        return is_satisfiable,answer
                
    except subprocess.CalledProcessError as e:
        print(f"erreur survenue lors de l'execution de la commande {e}")
        return False,False


#%% Utils
def paraToVar(x,y,color,lenGame,width):
    return 1 + lenGame*color + x*width + y
    
def VarToPara(var, lenGame, width):
    pos = (var-1)%lenGame
    color = (var-1)//lenGame
    x=pos//width
    y=pos%width
    return x,y,color

def findNeighbors(x, y, lenGame, width, forbidden, directions=[(-1,0),(0,-1),(0,1),(1,0)]):
    height = lenGame // width
    neighborList = []
    for dx, dy in directions:
        newX, newY = x + dx, y + dy
        if 0 <= newX < height and 0 <= newY < width and (newX,newY) not in forbidden:
            neighborList.append((newX, newY))
    return neighborList

def whatNeighbors(x,y, shiftFirstLine):
    shift = 1 if shiftFirstLine else 0
    a = (x+shift)%2
    return [(-1,-1+a),(-1,a),(0,-1),(0,1),(1,-1+a),(1,a)]
    

def isEnd(x,y,endDict):
    for key in endDict:
        for pos in endDict[key]:
            if pos[0]==x and pos[1]==y:
                return key
    return -1

def createListOfClauses(varList, nbNeg):
    indexList =  list(combinations(list(range(len(varList))), nbNeg))
    allClauses = []
    for indexes in indexList:
        temp = [-1*varList[i] if i in indexes else varList[i] for i in range(len(varList))]
        allClauses.append(temp)
    developpedClauses = list(product(*allClauses))
    finalClause = []
    i=0
    for clause in developpedClauses:
        newClause = list(set(clause))
        okay = True
        for element in newClause:
            if -element in newClause:
                okay = False
        if okay:
            finalClause.append(tuple(newClause))
        i+=1
    return list(set(finalClause))

#%% Constraints
def add_path_constraint(constraint, lenGame, width, nbColor, endDict, bridges,forbidden, shiftFirstLine):
    print(bridges)
    # constraint on neighbors
    # constraint.append([])
    for x in range(lenGame//width):
        for y in range(width):
            if (x,y) in bridges and False:
                for color in range(nbColor):
                    varList = [[-paraToVar(x,y,color,lenGame,width)]]
                    varList.append([paraToVar(x-1,y,color,lenGame,width),paraToVar(x+1,y,color,lenGame,width)])
                    varList.append([paraToVar(x,y-1,color,lenGame,width),paraToVar(x,y+1,color,lenGame,width)])
                    constraint.extend(list(product(*varList)))
            elif (x,y) not in forbidden:
                color = isEnd(x,y,endDict)
                if color >= 0:
                    directions = whatNeighbors(x,y,shiftFirstLine)
                    neighbors = findNeighbors(x,y,lenGame, width,forbidden, directions=directions)
                    constraint.append([paraToVar(ne[0],ne[1],color,lenGame,width) for ne in neighbors])
                    possible_index = [-paraToVar(ne[0],ne[1],color,lenGame,width) for ne in neighbors]
                    constraint.extend(combinations(possible_index,2))
                else:
                    for color in range(nbColor):
                        directions = whatNeighbors(x,y,shiftFirstLine)
                        neighbors = findNeighbors(x,y,lenGame, width,forbidden, directions=directions)
                        nbNeg = len(neighbors)-2
                        neighbors_var = [paraToVar(ne[0],ne[1],color,lenGame,width) for ne in neighbors]
                        # possible_partial_clause = createListOfClauses(neighbors_var,nbNeg)
                        possible_partial_clause = combinations(neighbors_var,nbNeg+1)
                        clauses_to_add = [list(clause)+[-paraToVar(x,y,color,lenGame,width)] for clause in possible_partial_clause]
                        neighbors_var = [-paraToVar(ne[0],ne[1],color,lenGame,width) for ne in neighbors]
                        possible_partial_clause = combinations(neighbors_var,6-nbNeg+1)
                        clauses_to_add.extend([list(clause)+[-paraToVar(x,y,color,lenGame,width)] for clause in possible_partial_clause])
                        constraint.extend(clauses_to_add)
    return constraint

def add_constraint_state(constraint, lenGame, width, nbColor, bridges, forbidden):
    # one color per cell except for bridges
    for x in range(lenGame//width):
        for y in range(width):
            if (x,y) in bridges:
                possible_index = [paraToVar(x,y,color,lenGame,width) for color in range(nbColor)]
                constraint.extend(combinations(possible_index,nbColor-1))
                possible_index = [-paraToVar(x,y,color,lenGame,width) for color in range(nbColor)]
                constraint.extend(combinations(possible_index,3))
            elif (x,y) not in forbidden:
                constraint.append([paraToVar(x,y,color,lenGame,width) for color in range(nbColor)])
                possible_index = [-paraToVar(x,y,color,lenGame,width) for color in range(nbColor)]
                constraint.extend(combinations(possible_index,2))
            else:
                for color in range(nbColor):
                    constraint.append([-paraToVar(x,y,color,lenGame,width)])
    return constraint

def init_constraint(endDict, lenGame, width, nbColor):
    # color for end position
    constraint = []
    for key in endDict:
        for pos in endDict[key]:
            constraint.append([paraToVar(pos[0],pos[1],key,lenGame, width)])
    return constraint

#%% Pre process
def preprocess(game):
    endDict = dict()
    convertor = []
    lenGame = 0
    forbidden = []
    for i in range(len(game)):
        lenGame += len(game[i])
        for j in range(len(game[i])):
            if game[i][j] == "#":
                forbidden.append((i,j))
            elif game[i][j] != " ":
                if game[i][j] not in convertor:
                    convertor.append(game[i][j])
                key = convertor.index(game[i][j])
                if key not in endDict:
                    endDict[key] = []
                endDict[key].append((i,j))
    nbColor = len(endDict)
    nbVar = lenGame*nbColor
    return endDict, lenGame, len(game[0]), nbColor, nbVar, convertor, forbidden

def check_game(endDict, convertor):
    for key in endDict:
        if len(endDict[key]) != 2:
            return False , f"Bad number of ending for {convertor[key]}"
    return True, ""

def check_bridges(bridges, lenGame, width):
    for pos in bridges:
        if pos[0] == 0 or pos[0] == lenGame//width-1 or pos[1]==0 or pos[1]==width:
            return False, "bridge on the side of the grid"
    return True,""

def convert_position(content):
    size = content["size"]
    nodes = content["game"]
    endDict = dict()
    forbidden = []
    convertor = []
    if size%2==1:
        halfLine = (size-1)//2
        for i in range(size//2):
            nbEnd = i//2+1
            nbStart = (i+1)//2
            for j in range(nbStart):
                forbidden.append((halfLine-i-1, j))
                forbidden.append((halfLine+i+1, j))
            for j in range(nbEnd):
                forbidden.append((halfLine-i-1, size-1-j))
                forbidden.append((halfLine+i+1, size-1-j))
        for i in range(len(nodes)):
            convertor.append(str(i))
            endDict[i] = []
            for node in nodes[i]:
                if node[0] <= halfLine:
                    diff = halfLine-node[0]+1
                    endDict[i].append((node[0],node[1]-diff//2))
                else:
                    diff = node[0]-halfLine
                    endDict[i].append((node[0], node[1]+diff//2))
    else:
        halfLine = size//2
        sizePlusOne=size+1
        for i in range(sizePlusOne//2):
            nbEnd = i//2+2
            nbStart = (i+1)//2
            for j in range(nbStart):
                forbidden.append((halfLine-i-1, j))
                if i < sizePlusOne//2-1:
                    forbidden.append((halfLine+i+1, j))
            for j in range(nbEnd):
                forbidden.append((halfLine-i-1, sizePlusOne-1-j))
                if i < sizePlusOne//2-1:
                    forbidden.append((halfLine+i+1, sizePlusOne-1-j))
        for i in range(len(nodes)):
            convertor.append(str(i))
            endDict[i] = []
            for node in nodes[i]:
                if node[0] <= halfLine:
                    diff = halfLine-node[0]+1
                    endDict[i].append((node[0],node[1]-diff//2))
                else:
                    diff = node[0]-halfLine
                    endDict[i].append((node[0], node[1]+diff//2))
    nbColor = len(endDict)
    width = size
    lenGame = size*size
    nbVar = lenGame*nbColor
    return endDict, lenGame, width, nbColor, nbVar, convertor, forbidden 

#%% Post process
def format_answer(answer, lenGame, width):
    answer_split = answer.split()
    answer_formatted = dict()
    for a in answer_split:
        if a[0] != "-":
            b = int(a)
            x,y,color = VarToPara(b, lenGame, width)
            if color not in answer_formatted:
                answer_formatted[color] = []
            answer_formatted[color].append((x,y))
    return answer_formatted

def hasLoopHexa(answer, lenGame, width, endDict,forbidden,shiftFirstLine):
    for key in answer:
        start = endDict[key][0]
        done = [start]
        stillNew = True
        while stillNew:
            stillNew = False
            pos = done[-1]
            directions = whatNeighbors(pos[0],pos[1],shiftFirstLine)
            neighbors = findNeighbors(pos[0],pos[1],lenGame,width,forbidden,directions=directions)
            for ne in neighbors:
                if ne in answer[key] and ne not in done:
                    done.append(ne)
                    stillNew = True
                    break
        if len(done) != len(answer[key]):
            return True, list(set(answer[key]).difference(set(done))), key
    return False, [], -1

def find_pos_on_bridges(answer_formatted, bridges):
    posBridgeDict = dict()
    for bridge in bridges:
        for key in answer_formatted:
            if bridge in answer_formatted[key]:
                if bridge not in posBridgeDict:
                    posBridgeDict[bridge] = []
                posBridgeDict[bridge].append(key)
    return posBridgeDict

#%% Main
def solve_numberlink_hexa(game, path,shiftFirstLine, user_initialized = False,content={}, bridges=[]):
    if user_initialized:
         endDict, lenGame, width, nbColor, nbVar, convertor, forbidden = convert_position(content)
    else:
        endDict, lenGame, width, nbColor, nbVar, convertor, forbidden = preprocess(game)
    check, message = check_game(endDict,convertor)
    check_b, message_b = check_bridges(bridges,lenGame, width)
    if not check or not check_b:
        print("Game not correct")
        message = message+"   "+message_b
        return {},endDict,message,convertor,{}, forbidden
    constraint = init_constraint(endDict, lenGame, width, nbColor)
    constraint = add_constraint_state(constraint, lenGame, width, nbColor, bridges, forbidden)
    constraint = add_path_constraint(constraint, lenGame, width, nbColor, endDict, bridges, forbidden, shiftFirstLine)
    answer_formatted = {}
    write_in_file_cnf(path, constraint, nbVar)
    
    command = ["gophersat","--verbose",path]
    is_satisfiable, answer = run_command(command)
    posBridgeDict = {}
    
    if is_satisfiable:
        message = "Solution found"
        answer_formatted = format_answer(answer, lenGame, width)
        posBridgeDict = find_pos_on_bridges(answer_formatted,bridges)
        contain_loop, pos_loop, key_loop = hasLoopHexa(answer_formatted,lenGame, width, endDict,forbidden,shiftFirstLine)
        while is_satisfiable and contain_loop:
            for ne in pos_loop:
                constraint.append([-paraToVar(ne[0],ne[1],key_loop,lenGame,width)])
            write_in_file_cnf(path,constraint, nbVar)
            is_satisfiable, answer = run_command(command)
            if is_satisfiable: 
                answer_formatted = format_answer(answer, lenGame, width)
                posBridgeDict = find_pos_on_bridges(answer_formatted,bridges)
            else:
                answer_formatted = {}
                message = "No solutions because of loops"
                print(message)
                
            contain_loop, pos_loop, key_loop = hasLoopHexa(answer_formatted,lenGame, width, endDict,forbidden,shiftFirstLine)

    else:
        message = "no solution even with loops"
        print(message)
    return answer_formatted,endDict, message, convertor, posBridgeDict, forbidden

