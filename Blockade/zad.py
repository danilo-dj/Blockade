from coordinates import GridCoordinates
from copy import *
import re 

def initialState(
    table_width=14,
    table_length=11,    
    home_x=(GridCoordinates(4,4),GridCoordinates(8,4)),
    home_o=(GridCoordinates(4,11),GridCoordinates(8,11)),
    walls = 9
):
    state ={
        'table_width': table_width,
        'table_length': table_length,
        'home_x': home_x,
        'home_o': home_o,
        'position_x': deepcopy(home_x),
        'position_o': deepcopy(home_o),
        'h_walls_x' : copy(walls),
        'h_walls_o' : copy(walls),
        'v_walls_x' : copy(walls),
        'v_walls_o' : walls,
        'h_walls': (),
        'v_walls': ()
    }
    return state



def initialString(width, length):   

    gameStr= ' '
    for a in range(1,width+1):
        gameStr +='  ' + hex(a)[2:].upper() +' '

    gameStr+= '\n  '

    for a in range(width):
        gameStr +=' =  '
    gameStr+= '\n'

    for a in range(1,length+2):
        gameStr += hex(a)[2:].upper() +'ǁ'    
        for b in range(width):            
            gameStr += f' ({a},{b+1}) '
            if b==width-1:break
            gameStr +='|'       
        gameStr += 'ǁ'+hex(a)[2:].upper()+'\n'  
        if a == length : break
        gameStr+= '   '    
        for h in range(width):
            gameStr +=f'h{a},{h+1}\u2015   '
        gameStr+= '\n'

    gameStr +='  '
    for a in range(width):
        gameStr +=' =  '

    gameStr+= '\n '
    for a in range(1,width+1):
        gameStr +='  ' + hex(a)[2:].upper() +' '

    return gameStr 

def tableString(state):

    gameStr = initialString(state['table_width'],state['table_length'])

    for x in state['position_x']:
        i =  state['position_x'].index(x) + 1 
        gameStr=re.sub(f'\({x}\) ',f'X{i}{x}',gameStr) 

    for o in state['position_o']:
        i =  state['position_o'].index(o) + 1
        gameStr=re.sub(f'\({o}\) ',f'O{i}{o}',gameStr)

    for hw in state['h_walls']:
        gameStr=re.sub(f'h{hw}\u2015','=',gameStr)
        gameStr=re.sub(f'h{hw.row},{hw.col+1}\u2015','=',gameStr)
   
    for vw in state['v_walls']:
        gameStr=re.sub(f'\({vw}\) \|','  ǁ',gameStr)
        gameStr=re.sub(f'\({vw.row+1},{vw.col}\) \|','  ǁ',gameStr)
        gameStr=re.sub(f'([XO][12]){vw}\|',r'\1ǁ',gameStr)  
        gameStr=re.sub(f'([XO][12]){vw.row+1},{vw.col}\|',r'\1ǁ',gameStr) 
        
    gameStr = re.sub('\([0-9]*,[0-9]*\)', ' ', gameStr)
    gameStr = re.sub('h[0-9]*,[0-9]*', '', gameStr)
    gameStr = re.sub('([0-9])[0-9]*,[0-9]*',r'\1', gameStr)

    return gameStr


def getValidMoves(state,pawn): #[X 1] [6 3] [V 4 9] stanje i poziciju pesaka
    
    possible_moves = {
        pawn.top().left(),
        pawn.top().right(),
        pawn.bottom().left(),
        pawn.bottom().right(),
        pawn.top().top(),                                    
        pawn.bottom().bottom(),
        pawn.left().left(),
        pawn.right().right()      
    }

    one_step = {
        pawn.top(),
        pawn.bottom(),
        pawn.left(),
        pawn.right()
    }

    #ako je home na jedan korak

    for pos in one_step:
        if pos in state['home_x'] or pos in state['home_o']:
            possible_moves.add(pos)

    #u slucaju da su drugi pesaci na krajnjim pozicijama moze da se pomeri za jedan korak   

    if pawn.top().top() in state['position_x'] or pawn.top().top() in state['position_o']:
        possible_moves.add(pawn.top())
    if pawn.left().left() in state['position_x'] or pawn.left().left() in state['position_o']:
        possible_moves.add(pawn.left())
    if pawn.bottom().bottom() in state['position_x'] or pawn.bottom().bottom() in state['position_o']:
        possible_moves.add(pawn.bottom())
    if pawn.right().right() in state['position_x'] or pawn.right().right() in state['position_o']:
        possible_moves.add(pawn.right())

    #za horizontanlne zidove add

    if pawn.top().top() in state['h_walls']: 
        possible_moves.add(pawn.top())  
    if pawn.bottom() in state['h_walls']:
        possible_moves.add(pawn.bottom())
    if pawn.bottom().left() in state['h_walls']:
        possible_moves.add(pawn.bottom())
    if pawn.top().top().left()in state['h_walls']:
        possible_moves.add(pawn.top())
    
    #za vertikalne zidove add

    if pawn.left().left() in state['v_walls']:
        possible_moves.add(pawn.left())
    if pawn.right() in state['v_walls']:
        possible_moves.add(pawn.right())
    if pawn.top().left().left() in state['v_walls']:
        possible_moves.add(pawn.left())
    if pawn.top().right() in state['v_walls']:
        possible_moves.add(pawn.right())

    #ako postoji pesak na possible_moves    
    for pm in possible_moves.copy():
        if pm in state['position_o'] or pm in state['position_x']:
            p=pm in state['position_o'] or pm in state['position_x']
            if pm not in state['home_x'] and pm not in state['home_o']:
                c=pm not in state['home_x'] and pm not in state['home_o']
                possible_moves.remove(pm)

    #za horizontanlne zidove remove

    if pawn.top().top() in state['h_walls']: 
        possible_moves-={pawn.top().top()}  
    if pawn.bottom() in state['h_walls']:
        possible_moves-={pawn.bottom().bottom()}
    if pawn.bottom().left() in state['h_walls']:
        possible_moves-={pawn.bottom().bottom()}
    if pawn.top().top().left()in state['h_walls']:
        possible_moves-={pawn.top().top()}

    if pawn.top().left() in state['h_walls']:
        possible_moves-={pawn.top().top(), pawn.top(), pawn.top().left()}
    if pawn.top() in state['h_walls']: 
        possible_moves-={ pawn.top(), pawn.top().right(), pawn.top().top()}        
    if pawn in state['h_walls']:
        possible_moves-={pawn.bottom(),pawn.bottom().right(),pawn.bottom().bottom()}   
    if pawn.left() in state['h_walls']:
        possible_moves-={pawn.bottom().bottom(), pawn.bottom().left(), pawn.bottom()}

    #za vertikalne zidove remove

    if pawn.left().left() in state['v_walls']:
        possible_moves-={pawn.left().left()}
    if pawn.right() in state['v_walls']:
        possible_moves-={pawn.right().right()}
    if pawn.top().left().left() in state['v_walls']:
        possible_moves-={pawn.left().left()}
    if pawn.top().right() in state['v_walls']:
        possible_moves-={pawn.right().right()}
    
    if pawn.left() in state['v_walls']:
        possible_moves-={pawn.left().left(), pawn.left(), pawn.bottom().left()}
    if pawn in state['v_walls']:
        possible_moves-={pawn.right().right(), pawn.right(), pawn.bottom().right()}    
    if pawn.top().left() in state['v_walls']:
        possible_moves-={pawn.left().left(), pawn.left(), pawn.top().left()}
    if pawn.top() in state['v_walls']:
        possible_moves-={pawn.right().right(), pawn.right(), pawn.top().right()}    

    #za kombinaciju zidova
    if pawn.left().left() in state['h_walls'] and pawn.bottom().left() in state['v_walls']:
        possible_moves-={pawn.bottom().left()}
    if pawn.top().top().left() in state['v_walls'] and pawn.top().left().left() in state['h_walls']:
        possible_moves-={pawn.top().left()}
    if pawn.top().top() in state['v_walls'] and pawn.top().right() in state['h_walls']:
        possible_moves-={pawn.top().right()}
    if pawn.right() in state['h_walls'] and pawn.bottom() in state['v_walls']:
        possible_moves-={pawn.right().bottom()}
    if pawn.left() in state['h_walls'] and pawn.top() in state['v_walls']:
        possible_moves-={pawn.bottom().right()}
    if pawn.top().left() in state['h_walls'] and pawn in state['v_walls']:
        possible_moves-={pawn.top().right()}
    if pawn in state['h_walls'] and pawn.top().left() in state['v_walls']:
        possible_moves-={pawn.bottom().left()}
    if pawn.top() in state['h_walls'] and pawn.left() in state['v_walls']:
        possible_moves-={pawn.top().left()}    

    return possible_moves

def checkPositionForWall (state, position, wall): # 'V' 'H'

    for hw in state['h_walls']:
        if hw == position:
            return False

    for vw in state['v_walls']:
        if vw == position:
            return False

    for hw in state['h_walls']:
        if position == hw.right() and wall =='H':
            return False

    for vw in state['v_walls']:
        if position == vw.bottom()  and wall =='V':
            return False 

    if position.col == state['table_width'] or position.row== state['table_length']:
        return False 

    return True

def addWall(state,wall_coor,wall_kind,pawn):
    if checkPositionForWall(state,wall_coor,wall_kind):
        if wall_kind=='H':
            if re.match('X[12]',pawn):
                if state['h_walls_x']>0:
                    state['h_walls']+=(wall_coor,)
                    state['h_walls_x']-=1
                    return True
                else:
                    print('Igrac X nema vise H zidova')
                    return False    
            if re.match('O[12]',pawn):
                if state['h_walls_o']>0:
                    state['h_walls']+=(wall_coor,)
                    state['h_walls_o']-=1
                    return True
                else:
                    print('Igrac O nema vise H zidova')
                    return False
            
        if wall_kind=='V':
            if re.match('X[12]',pawn):
                if state['v_walls_x']>0:
                    state['v_walls']+=(wall_coor,)
                    state['v_walls_x']-=1
                    return True
                else:
                    print('Igrac X nema vise V zidova')
                    return False   
            if re.match('O[12]',pawn):
                if state['v_walls_o']>0:
                    state['v_walls']+=(wall_coor,)
                    state['v_walls_o']-=1
                    return True
                else:
                    print('Igrac O nema vise V zidova')
                    return False
        
        if wall_kind=='X':
            if re.match('X[12]',pawn):
                if state['v_walls_x']>0:                
                    print('Igrac X ima jos V zidova')
                if state['h_walls_x']>0:
                    print('Igrac X ima jos H zidova')   
            if re.match('O[12]',pawn):
                if state['v_walls_o']>0:                    
                    print('Igrac O ima jos V zidova')
                if state['h_walls_o']:
                    print('Igrac O ime jos H zidova')
            return False
    else:
        print(f'Izabrano polje {wall_coor} za zid je zauzeto')
        return False

def removeWall(state,wall_coor,wall_kind,pawn):
    if wall_kind=='H':
        if wall_coor in state['h_walls']:
                li=list(state['h_walls'])
                li.remove(wall_coor)
                state['h_walls']=tuple(li)
                if re.match('X[12]',pawn):            
                    state['h_walls_x']+=1                    
                if re.match('O[12]',pawn):
                    state['h_walls_o']+=1
                return True
        else:
            print('Uneti zid za brisanje nije na tabli')
            return False   
            
    if wall_kind=='V':
        if wall_coor in state['v_walls']:
                li = list(state['v_walls'])
                li.remove(wall_coor)
                state['v_walls']=tuple(li)
                if re.match('X[12]',pawn):            
                    state['v_walls_x']+=1                    
                if re.match('O[12]',pawn):
                    state['v_walls_o']+=1
                return True
        else:
            print('Uneti zid za brisanje nije na tabli')
            return False
        
           


def makeAMove(state, move): #[X 1] [6 3] [V 4 9]

    if  not re.match('\[[XO] [12]\] \[[0-9][0-9]* [0-9][0-9]*\] \[[VHX] [0-9][0-9]* [0-9][0-9]*\]',move):
        return 'pogresan format poteza'     

    steprow=re.search('\[([0-9][0-9]*) ([0-9][0-9]*)\] \[[VH] ([0-9][0-9]*) ([0-9][0-9]*)\]', move).group(1)
    stepcol=re.search('\[([0-9][0-9]*) ([0-9][0-9]*)\] \[[VH] ([0-9][0-9]*) ([0-9][0-9]*)\]', move).group(2)
    wallrow=re.search('\[([0-9][0-9]*) ([0-9][0-9]*)\] \[[VH] ([0-9][0-9]*) ([0-9][0-9]*)\]', move).group(3)
    wallcol=re.search('\[([0-9][0-9]*) ([0-9][0-9]*)\] \[[VH] ([0-9][0-9]*) ([0-9][0-9]*)\]', move).group(4)
    
    p=re.search('\[([XO]) ([0-9][0-9]*)\]', move).group(1)
    n=re.search('\[([XO]) ([0-9][0-9]*)\]', move).group(2)          

    pawn=p+n
    step=GridCoordinates(int(steprow), int(stepcol))
    wall_kind=re.search('\[([VHX]) [0-9][0-9]* [0-9][0-9]*\]', move).group(1)
    if int(wallcol)>0 and int(wallrow)>0:
        wall_coor=GridCoordinates(int(wallrow),int(wallcol))       

    #postavljanje i provera zida

    if addWall(state,wall_coor,wall_kind,pawn):
        if isTouchingTwoWalls(state,wall_coor):
            for px in state['position_x']:
                for ho in state['home_o']:
                    if pathAstar(state,px,ho)==False:
                        removeWall(state,wall_coor,wall_kind,pawn)
                        print('Zid iskljucuje put do kuce')
                        break
                else:                    
                    continue
                break
            for po in state['position_o']:
                for hx in state['home_x']:
                    if pathAstar(state,po,hx)==False:
                        removeWall(state,wall_coor,wall_kind,pawn)
                        print('Zid iskljucuje put do kuce')
                        break
                else:
                    continue
                break
            

    #pomeranje pesaka
    switcher = {
        'X1': state['position_x'][0],
        'X2': state['position_x'][1],
        'O1': state['position_o'][0],
        'O2': state['position_o'][1] 
    }
                                            
    pawn_pos = switcher[pawn]

    validMoves = getValidMoves(state,pawn_pos)

    if step in validMoves:
        switcher[pawn].set(step.row,step.col)
    else:
        print(f'Korak pesaka {pawn} nije validan')

    print('Izvrsen je potez:'+move)

def makeAMoveInput(state,input):
    if  re.match('\[[XO] [12]\] \[[0-9][0-9]* [0-9][0-9]*\] \[[VH] [0-9][0-9]* [0-9][0-9]*\]',input):
        makeAMove(state, input)
    elif  re.match('\[[XO] [12]\] \[[0-9][0-9]* [0-9][0-9]*\]' ,input): 
        makeAMove(state, input + '[X 0 0]')
    else: print('nevalidan format poteza')  

def is_end(state):
    if (state['position_x'][0]==state['home_o'][0] or 
        state['position_x'][1]==state['home_o'][0] or
        state['position_x'][0]==state['home_o'][1] or
        state['position_x'][1]==state['home_o'][1]):
            print('Pobedio je igrac X')
            return True
    if (state['position_o'][0]==state['home_x'][0] or 
        state['position_o'][1]==state['home_x'][0] or
        state['position_o'][0]==state['home_x'][1] or
        state['position_o'][1]==state['home_x'][1]):
            print('Pobedio je igrac O')
            return True
    print('Sledeci potez') 
    return False 

def newState(state, move):
    pom = deepcopy(state)
    makeAMove(pom, move)
    return pom

def possibleStatesOneMove(state, player): # 'X' ili 'O'    
    #moguce pozicije horizontalnih i vertikalnih zidova na osnovu trenutnog stanja    
    allCoor = list()
    for i in range(1,state['table_length']+1):
            for j in range(1,state['table_width']+1):
                allCoor.append(GridCoordinates(i,j))
    possibleHwall = list()
    possibleVwall = list()
    for pos in allCoor:
        if checkPositionForWall(state,pos,'H'):
            possibleHwall.append(pos)
        if checkPositionForWall(state,pos,'V'):
            possibleVwall.append(pos)            
    #moguce pozicije pojedinacnog piona i broj ostalih zidova
    validMoves1 = set()
    validMoves2 = set()
    if player == 'X':        
        validMoves1.update(getValidMoves(state,state['position_x'][0]))
        validMoves2.update(getValidMoves(state, state['position_x'][1]))
        hwLeft=state['h_walls_x']
        vwLeft=state['v_walls_x']
    if player == 'O':
        validMoves1.update(getValidMoves(state,state['position_o'][0]))
        validMoves2.update(getValidMoves(state, state['position_o'][1]))
        hwLeft=state['h_walls_o']
        vwLeft=state['v_walls_o']

    possibleStates = list()
    for i in range(1,3):
        if i==1: validMoves=validMoves1
        if i==2: validMoves=validMoves2            
        for validMove in validMoves:
            if hwLeft>0:
                for hpos in possibleHwall:
                    possibleStates.append(newState(state,f"[{player} {i}] [{validMove.row} {validMove.col}] [H {hpos.row} {hpos.col}]"))
            if vwLeft>0:
                for vpos in possibleVwall:
                    possibleStates.append(newState(state,f"[{player} {i}] [{validMove.row} {validMove.col}] [V {vpos.row} {vpos.col}]"))
    
    return possibleStates

def isTouchingTwoWalls(state, position):    # da li wall na pos dodiruje dva zida
    #moguce pozicije dodirnih zidova    
    possibleTouchingWallsH = set()
    possibleTouchingWallsV = set()
    if position in state['v_walls']:        
        possibleTouchingWallsH.update( {
            position.top().left(),
            position.top(),
            position.top().right(),
            position.bottom(),
            position.bottom().left(),
            position.bottom().right(),
            position.left(),
            position.right()
        } )        
        possibleTouchingWallsV.update({
            position.top().top(),
            position.bottom().bottom()
        })
    elif position in state['h_walls']:                  
        possibleTouchingWallsV.update({
            position.top().left(),
            position.top(),
            position.top().right(),
            position.bottom(),
            position.bottom().left(),
            position.bottom().right(),
            position.right(),
            position.left()
        })    
        possibleTouchingWallsH.update({ 
            position.left().left(),
            position.right().right()
        })
    touchingWalls = 0 

    for pos in possibleTouchingWallsV:
        if pos in state['v_walls']:
            touchingWalls+=1
    for pos in possibleTouchingWallsH:
        if pos in state['h_walls']:
            touchingWalls+=1        

    if touchingWalls >= 2:
        return True
    else:
        return False    

def heuristic(path_state, possibleMoves, home):
               
    if path_state[-1] == home:
        return 0    
    
    heu=12-len(possibleMoves)
    for elem in possibleMoves:
        if elem == home:           
            heu -= 2 
    return heu   

def generateGraphElement(path_state,state, home):
    possibleMoves = list()
    validMoves = list(getValidMoves(state, path_state[-1]))
      
    for vM in validMoves:
        if vM in path_state:
            validMoves.remove(vM)
            continue
        cost = 0        
        cost+= abs(home.col-vM.col)+abs(home.row - vM.row)
        possibleMoves.append(((vM,),cost))        

    return (heuristic(path_state,possibleMoves,home), possibleMoves)

def pathAstar(state, pawn_pos, home):
    found_end = False
    open_set = set()
    closed_set = set()
    g = {}
    prev_nodes = {}    
    g[(pawn_pos,)] = 0
    prev_nodes[(pawn_pos,)] = None
    open_set.add((pawn_pos,))
    while len(open_set) > 0 and len(closed_set) < 140 and (not found_end): 
        node = None
        for next_node in open_set:
            if node is None or g[next_node] + generateGraphElement(next_node,state,home)[0] < g[node] + generateGraphElement(node,state,home)[0]:
                node = next_node
        endHeuristic=generateGraphElement(node,state,home)[0]
        if endHeuristic==0:
            found_end = True
            end=node
            break
        for (m, cost) in generateGraphElement(node,state,home)[1]:
            if m not in open_set and m not in closed_set:
                open_set.add(m)
                prev_nodes[m] = node
                g[m] = g[node] + cost
            else:
                if g[m] > g[node] + cost:
                    g[m] = g[node] + cost
                    prev_nodes[m] = node
                    if m in closed_set:
                        closed_set.remove(m)
                        open_set.add(m)
        open_set.remove(node)
        closed_set.add(node)        
    path = []
    if found_end:
        prev = end
        while prev_nodes[prev] is not None:
            path.append(prev)
            prev = prev_nodes[prev]
        path.append(prev)
        path.reverse()
        return path
    else:
        return False 

'''
state = initialState()
#state['h_walls_x']=0
#state['v_walls_x']
state['h_walls']+=(GridCoordinates(7,9),GridCoordinates(3,6),GridCoordinates(2,4),GridCoordinates(3,10),GridCoordinates(5,10),GridCoordinates(7,11),
                    GridCoordinates(7,13),GridCoordinates(4,5),GridCoordinates(6,7))
state['v_walls']+=(GridCoordinates(1,5),GridCoordinates(1,8),GridCoordinates(4,9),GridCoordinates(4,11),GridCoordinates(8,10),GridCoordinates(6,4),
                    GridCoordinates(8,4),GridCoordinates(9,8),GridCoordinates(7,6))
#state['position_x']=(GridCoordinates(),GridCoordinates())
print(tableString(state))
for coor in pathAstar(state,GridCoordinates(2,5),state['home_o'][0]):
    print(coor[0])
print('===')
for c in getValidMoves(state,GridCoordinates(5,12)):
    print(c)

    


'''
def game():

    #print('Ko je prvi na potezu?[covek,racunar](c\\r)?')
    #a=input()
    #print(a)

    print('Da li zelite da igrate sa podrazumevanom tablom?(y\\n)?')
    a = input()
    if a=='y':
        state = initialState()
    if a=='n':
        print('Unesi sirinu table paran broj do 28')
        table_width = int(input())
        print('Unesi duzinu table neparan broj do 21')
        table_length = int(input())
        print('Unesi pocetne pozicije za X')
        home_x=()
        for i in range(2):
            row=int(input())
            col=int(input())
            home_x+=(GridCoordinates(row,col),)
        print('Unesi pocetne pozicije za O')
        home_o=()
        for i in range(2):
            row=int(input())
            col=int(input())
            home_o+=(GridCoordinates(row,col),)
        print('Unesi broj zidova svakog tipa po igracu max 18')
        walls=int(input())    
        state = initialState(table_width,table_length,home_x,home_o,walls)
    
    print(tableString(state))
    
    i=0
    while is_end(state)==False:
        if i%2==0:
            print('Igrac X je na potezu!')
        else:
            print('Igrac O je na potezu!')
        print('Unesi potez u formatu \n [igrac brpesaka] [korak] [vrstazid poszida] \n')        
        move=input()
        if re.match('\[X [12]\]',move) and i%2==0:
            makeAMoveInput(state, move)
            print(tableString(state))
            i+=1
        elif re.match('\[O [12]\]',move) and i%2!=0:
            makeAMoveInput(state, move)
            print(tableString(state))
            i+=1
        elif re.match('quit',move):
            break
        else:
            print(tableString(state))
            continue      
                


game()
