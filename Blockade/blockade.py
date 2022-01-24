from operator import le
from coordinates import GridCoordinates
from copy import *
from random import randint
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
        'v_walls':()
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

    if pawn.row == 2:
        possible_moves.add(pawn.top())
    if pawn.row == state['table_length']-1:
        possible_moves.add(pawn.bottom())
    if pawn.col == 2:
        possible_moves.add(pawn.left())
    if pawn.col == state['table_width']-1:
        possible_moves.add(pawn.right())

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
            minpenemy=pm in state['position_o'] or pm in state['position_x']
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
    if pawn.left() in state['v_walls'] and pawn.top().top().left() in state['v_walls']:
        possible_moves-={pawn.top().left()}
    if pawn.top().left() in state['v_walls'] and pawn.bottom().left() in state['v_walls']:
        possible_moves-={pawn.bottom().left()}
    if pawn.top().top() in state['v_walls'] and pawn in state['v_walls']:
        possible_moves-={pawn.top().right()}
    if pawn.top() in state['v_walls'] and pawn.bottom() in state['v_walls']:
        possible_moves-={pawn.bottom().right()}
    if pawn.top() in state['h_walls'] and pawn.top().left().left() in state['h_walls']:
        possible_moves-={pawn.top().left()}
    if pawn.top().left() in state['h_walls'] and pawn.top().right() in state['h_walls']:
        possible_moves-={pawn.top().right()}
    if pawn.left().left() in state['h_walls'] and pawn in state['h_walls']:
        possible_moves-={pawn.bottom().left()}
    if pawn.left() in state['h_walls'] and pawn.right() in state['h_walls']:
        possible_moves-={pawn.bottom().right()}

    for p in possible_moves.copy():
        if p.row>state['table_length'] or p.row<1:
            possible_moves-={p}
        if p.col>state['table_width'] or p.col<1:
            possible_moves-={p}

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
        if position == hw.left() and wall == 'H':
            return False

    for vw in state['v_walls']:
        if position == vw.bottom()  and wall =='V':
            return False
        if position == vw.top() and wall == 'V':
            return False 

    if position.col == state['table_width'] or position.row == state['table_length']:
        return False 

    return True

def addWall(state,wall_coor,wall_kind,pawn):
    if(wall_coor.row<1 or wall_coor.col<1 or wall_coor.row>state['table_length'] or wall_coor.col>state['table_width']):
        return False
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
        print('pogresan format poteza')
        return False     

    steprow=re.search('\[([0-9][0-9]*) ([0-9][0-9]*)\] \[[VHX] ([0-9][0-9]*) ([0-9][0-9]*)\]', move).group(1)
    stepcol=re.search('\[([0-9][0-9]*) ([0-9][0-9]*)\] \[[VHX] ([0-9][0-9]*) ([0-9][0-9]*)\]', move).group(2)
    wallrow=re.search('\[([0-9][0-9]*) ([0-9][0-9]*)\] \[[VHX] ([0-9][0-9]*) ([0-9][0-9]*)\]', move).group(3)
    wallcol=re.search('\[([0-9][0-9]*) ([0-9][0-9]*)\] \[[VHX] ([0-9][0-9]*) ([0-9][0-9]*)\]', move).group(4)
    
    minpenemy=re.search('\[([XO]) ([0-9][0-9]*)\]', move).group(1)
    n=re.search('\[([XO]) ([0-9][0-9]*)\]', move).group(2)          

    pawn=minpenemy+n
    step=GridCoordinates(int(steprow), int(stepcol))
    wall_kind=re.search('\[([VHX]) [0-9][0-9]* [0-9][0-9]*\]', move).group(1)
    wall_coor=GridCoordinates(int(wallrow),int(wallcol)) 

    #pomeranje pesaka
    switcher = {
        'X1': state['position_x'][0],
        'X2': state['position_x'][1],
        'O1': state['position_o'][0],
        'O2': state['position_o'][1] 
    }
    pawn_pos = switcher[pawn]
    validMoves = getValidMoves(state,pawn_pos)     

    #postavljanje i provera zida

    if addWall(state,wall_coor,wall_kind,pawn):
        if isTouchingTwoWalls(state,wall_coor):
            for px in state['position_x']:
                for ho in state['home_o']:
                    if pathAstar(state,px,ho)==False:
                        removeWall(state,wall_coor,wall_kind,pawn)
                        print('Zid iskljucuje put do kuce')
                        switcher[pawn]=pawn_pos 
                        return False                        
                else:                    
                    continue
                
            for po in state['position_o']:
                for hx in state['home_x']:
                    if pathAstar(state,po,hx)==False:
                        removeWall(state,wall_coor,wall_kind,pawn)
                        print('Zid iskljucuje put do kuce')
                        switcher[pawn]=pawn_pos 
                        return False
                else:
                    continue
                
    else:             
        return False
    
    if step in validMoves:
        switcher[pawn].set(step.row,step.col)
    else:
        print(f'Korak pesaka {pawn} nije validan')
        removeWall(state,wall_coor,wall_kind,pawn)        
        return False
   
    print('Izvrsen je potez:'+move)
    return True

def makeAMoveInput(state,input):
    if  re.match('\[[XO] [12]\] \[[0-9][0-9]* [0-9][0-9]*\] \[[VH] [0-9][0-9]* [0-9][0-9]*\]',input):
        return makeAMove(state, input)
    elif  re.match('\[[XO] [12]\] \[[0-9][0-9]* [0-9][0-9]*\]' ,input): 
        return makeAMove(state, input + ' [X 0 0]')
    else: 
        print('nevalidan format poteza') 
        return False 

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
    if(makeAMoveInput(pom, move)):
        return pom
    else:
        return None

def possibleStatesOneMove(state, player): # 'X' ili 'O'    
              
    #najkraci putevi    
    lpX=list()
    lpO=list()
    for ho in state['home_o']:
        for i in range(2):            
            path=pathAstar(state,state['position_x'][i],ho)
            if path!=False:
                lpX.append((path, i+1, len(path)))                            
    
    for hx in state['home_x']:
        for i in range(2):
            path=pathAstar(state,state['position_o'][i],hx)
            if path!=False:                
                lpO.append((path, i+1, len(path)))
    if player == 'X':
        minpath = min(lpX, key=lambda x: x[2])
        minpenemy= min(lpO, key=lambda x: x[2]) 
        lpO.remove(minpenemy)              
        hwLeft=state['h_walls_x']
        vwLeft=state['v_walls_x']
    if player == 'O':
        minpath = min(lpO, key=lambda x: x[2])
        minpenemy = min(lpX, key=lambda x: x[2])
        lpX.remove(minpenemy)
        hwLeft=state['h_walls_o']
        vwLeft=state['v_walls_o']

    possibleStates = list()
    if hwLeft==0 and vwLeft==0:
            possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}]"))
    else:
        k=0
        i=1
        if len(minpenemy[0])<=1:
            if player=='X':
                k=1
                minpenemy= max(lpO, key=lambda x: x[2])                    
            if player=='O':
                k=1
                minpenemy= max(lpX, key=lambda x: x[2])  
        j=len(minpenemy[0])-1                
        while( len(possibleStates) < 2 ):

            if hwLeft > 0:
                if minpenemy[0][i-1][0].row < minpenemy[0][i][0].row:
                    if minpenemy[0][i-1][0].col >= minpenemy[0][i][0].col:                               
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [H {minpenemy[0][i-1][0].row} {minpenemy[0][i-1][0].col}]"))
                    if minpenemy[0][i-1][0].col > minpenemy[0][i][0].col:    
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [H {minpenemy[0][i-1][0].right().row} {minpenemy[0][i-1][0].right().col}]"))
                    if minpenemy[0][i-1][0].col <= minpenemy[0][i][0].col:
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [H {minpenemy[0][i-1][0].left().row} {minpenemy[0][i-1][0].left().col}]"))
                    if minpenemy[0][i-1][0].col < minpenemy[0][i][0].col:    
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [H {minpenemy[0][i-1][0].left().left().row} {minpenemy[0][i-1][0].left().left().col}]"))
                if minpenemy[0][i-1][0].row > minpenemy[0][i][0].row:
                    if minpenemy[0][i-1][0].col >= minpenemy[0][i][0].col: 
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [H {minpenemy[0][i-1][0].top().row} {minpenemy[0][i-1][0].top().col}]"))
                    if minpenemy[0][i-1][0].col > minpenemy[0][i][0].col:    
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [H {minpenemy[0][i-1][0].top().right().row} {minpenemy[0][i-1][0].top().right().col}]"))      
                    if minpenemy[0][i-1][0].col <= minpenemy[0][i][0].col:    
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [H {minpenemy[0][i-1][0].top().left().row} {minpenemy[0][i-1][0].top().left().col}]"))
                    if minpenemy[0][i-1][0].col < minpenemy[0][i][0].col:    
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [H {minpenemy[0][i-1][0].top().left().left().row} {minpenemy[0][i-1][0].top().left().left().col}]"))
            if vwLeft > 0:
                if minpenemy[0][i-1][0].col < minpenemy[0][i][0].col:
                    if minpenemy[0][i-1][0].row >= minpenemy[0][i][0].row:
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [V {minpenemy[0][i-1][0].top().row} {minpenemy[0][i-1][0].top().col}]"))
                    if minpenemy[0][i-1][0].row > minpenemy[0][i][0].row:    
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [V {minpenemy[0][i-1][0].top().top().row} {minpenemy[0][i-1][0].top().top().col}]"))
                    if minpenemy[0][i-1][0].row <= minpenemy[0][i][0].row:
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [V {minpenemy[0][i-1][0].row} {minpenemy[0][i-1][0].col}]"))
                    if minpenemy[0][i-1][0].row < minpenemy[0][i][0].row:    
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [V {minpenemy[0][i-1][0].bottom().row} {minpenemy[0][i-1][0].bottom().col}]"))
                if minpenemy[0][i-1][0].col > minpenemy[0][i][0].col:
                    if minpenemy[0][i-1][0].row >= minpenemy[0][i][0].row:
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [V {minpenemy[0][i-1][0].top().left().row} {minpenemy[0][i-1][0].top().left().col}]"))
                    if minpenemy[0][i-1][0].row > minpenemy[0][i][0].row:
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [V {minpenemy[0][i-1][0].top().top().left().row} {minpenemy[0][i-1][0].top().top().left().col}]"))
                    if minpenemy[0][i-1][0].row <= minpenemy[0][i][0].row:
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [V {minpenemy[0][i-1][0].left().row} {minpenemy[0][i-1][0].left().col}]"))
                    if minpenemy[0][i-1][0].row < minpenemy[0][i][0].row:
                        possibleStates.append(newState(state,f"[{player} {minpath[1]}] [{minpath[0][1][0].row} {minpath[0][1][0].col}] [V {minpenemy[0][i-1][0].bottom().left().row} {minpenemy[0][i-1][0].bottom().left().col}]"))

            #zamene mesta
            i,j = j,i
            #naizmenicno blize kuce blize neprijatelju
            if i>j: 
                j+=1 
                continue
            elif i<j: 
                j-=1 
                continue
            elif i==j:
                if player=='X':
                    if(k==1): break
                    minpenemy= max(lpO, key=lambda x: x[2])                    
                if player=='O':
                    if(k==1): break
                    minpenemy= max(lpX, key=lambda x: x[2])                    
                i=1
                j=len(minpenemy[0])-1
                k=1
                continue 
    possibleStates = list(filter(lambda x: x != None,possibleStates))
    return possibleStates

def isTouchingTwoWalls(state, position):    # da li wall na pos dodiruje dva zida
    #moguce pozicije dodirnih zidova    
    possibleTouchingWallsH = set()
    possibleTouchingWallsV = set()
    touchingWalls = 0
    if position in state['v_walls']:
        if position.row == 1:
            touchingWalls+=1
        if position.row == (state['table_length']-1):
            touchingWalls+=1        
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
        if position.col == 1:
            touchingWalls+=1
        if position.col == (state['table_width']-1):
            touchingWalls+=1                  
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
     

    for pos in possibleTouchingWallsV:
        if pos in state['v_walls']:
            if pos.row == 1:
                touchingWalls+=1
            if pos.row == (state['table_length']-1):
                touchingWalls+=1
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

def eval_state(state,max,player):
    goals = state['home_o'] if player == 'X' else  state['home_x'] 
    pawns = state['position_x'] if player == 'X' else state['position_o']
    sumdistance = 0
    for g in goals:
        for p in pawns:
            sumdistance+=abs(p.row-g.row)**2+abs(p.col-g.col)**2
    if(max):        
        if is_end(state):
            return 1000
        else:            
            return 1000-sumdistance            
    else:        
        if is_end(state):
            return -1000
        else:
            return -(1000-sumdistance) 

def max_value(states, depth, alpha, beta, maxplayer):
    minplayer = 'X' if maxplayer=='O' else 'O'
    if depth == 0 or is_end(states[-1]):
        return (states, eval_state(states[-1], True, maxplayer))
    else:
        for s in possibleStatesOneMove(states[-1],maxplayer):                        
            alpha = max(alpha,
                        min_value(states + [s] ,depth-1, alpha,beta, minplayer),
                        key=lambda x: x[1])
            if alpha[1] >= beta[1]:
                return beta
    return alpha

def min_value(states,depth,alpha, beta, minplayer):
    maxplayer = 'X' if minplayer=='O' else 'O'
    if depth == 0 or is_end(states[-1]):
        return (states, eval_state(states[-1], False,minplayer))
    else:
        for s in possibleStatesOneMove(states[-1],minplayer):                       
            beta = min(beta,
                        max_value(states + [s], depth-1, alpha, beta, maxplayer),
                        key=lambda x: x[1])
            
            if beta[1] <= alpha[1]:
                return alpha
    return beta

def minmax(state, depth, mymove, maxplayer, alpha=(initialState(),-1000000), beta=(initialState(),+1000000)):  #alpha beta su tuplovi (stanje, eval)
    minplayer = 'X' if maxplayer=='O' else 'O'
    if mymove:
        return max_value([state], depth, alpha, beta, maxplayer)
    else:
        return min_value([state], depth, alpha, beta, minplayer)


def game():
    a=None
    while(a != 'n' and a != 'y'):
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
    
    print('Da li zelite da igrate protiv racunanara?(y\\n)?')
    a=input()
    if a=='y':
        print('Ko je [X] prvi na potezu?[covek,racunar](c\\r)?')
        a=input()
        print(tableString(state))
        i=0
        while is_end(state)==False:
            if i%2==0:
                print('Igrac X je na potezu!')
            else:
                print('Igrac O je na potezu!')
            if a=='r' and i%2==0:
                state=minmax(state,3,True,'X')[0][1]
                print(tableString(state))
                i+=1
            if a=='c' and i%2==1:
                state=minmax(state,3,True,'O')[0][1]
                print(tableString(state))
                i+=1
            if (a=='c' and i%2==0) or (a=='r' and i%2==1):
                print('Unesi potez u formatu \n [igrac brpesaka] [korak] [vrstazid poszida] \n')        
                move=input()
                if re.match('\[[X] [12]\] \[[0-9][0-9]* [0-9][0-9]*\]',move) and i%2==0:
                    if makeAMoveInput(state, move):
                        i+=1
                    print(tableString(state))
                elif re.match('\[[O] [12]\] \[[0-9][0-9]* [0-9][0-9]*\]',move) and i%2!=0:
                    if makeAMoveInput(state, move):
                        i+=1
                    print(tableString(state))
                elif re.match('quit',move):
                    break
                else:
                    print(tableString(state))
                    continue

    elif a=='n':
        print(tableString(state))    
        i=0
        while is_end(state)==False:
            if i%2==0:
                print('Igrac X je na potezu!')
            else:
                print('Igrac O je na potezu!')
            print('Unesi potez u formatu \n [igrac brpesaka] [korak] [vrstazid poszida] \n')        
            move=input()
            if re.match('\[[X] [12]\] \[[0-9][0-9]* [0-9][0-9]*\]',move) and i%2==0:
                if makeAMoveInput(state, move):
                    i+=1
                print(tableString(state))
            elif re.match('\[[O] [12]\] \[[0-9][0-9]* [0-9][0-9]*\]',move) and i%2!=0:
                if makeAMoveInput(state, move):
                    i+=1
                print(tableString(state))
            elif re.match('quit',move):
                break
            else:
                print(tableString(state))
                continue     

           
game()



