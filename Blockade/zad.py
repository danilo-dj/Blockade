from coordinates import GridCoordinates
from copy import deepcopy
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
        'h_walls_x' : walls,
        'h_walls_o' : walls,
        'v_walls_x' : walls,
        'v_walls_o' : walls,
        'h_walls': (),
        'v_walls': ()
    }
    return (state)

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


def getValidMoves(state,pawn): #[X 1] [6 3] [V 4 9] 
    switcher = {
        'X1': state['position_x'][0],
        'X2': state['position_x'][1],
        'O1': state['position_o'][0],
        'O2': state['position_o'][1] 
    }
                                            
    pawn = switcher[pawn]    

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

    #za horizontanlne zidove

    if pawn.top().top() in state['h_walls']: 
        possible_moves-={pawn.top().top()}
        possible_moves.add(pawn.top())  
    if pawn.bottom() in state['h_walls']:
        possible_moves-={pawn.bottom().bottom()}
        possible_moves.add(pawn.bottom())
    if pawn.bottom().left() in state['h_walls']:
        possible_moves-={pawn.bottom().bottom()}
        possible_moves.add(pawn.bottom())
    if pawn.top().top().left()in state['h_walls']:
        possible_moves-={pawn.top().top()}
        possible_moves.add(pawn.top())

    if pawn.top().left() in state['h_walls']:
        possible_moves-={pawn.top().top(), pawn.top(), pawn.top().left()}
    if pawn.top() in state['h_walls']: 
        possible_moves-={ pawn.top(), pawn.top().right(), pawn.top().top()}        
    if pawn in state['h_walls']:
        possible_moves-={pawn.bottom(),pawn.bottom().right(),pawn.bottom().bottom()}   
    if pawn.left() in state['h_walls']:
        possible_moves-={pawn.bottom().bottom(), pawn.bottom().left(), pawn.bottom()}

    #za vertikalne zidove

    if pawn.left().left() in state['v_walls']:
        possible_moves-={pawn.left().left()}
        possible_moves.add(pawn.left())
    if pawn.right() in state['v_walls']:
        possible_moves-={pawn.right().right()}
        possible_moves.add(pawn.right())
    if pawn.top().left().left() in state['v_walls']:
        possible_moves-={pawn.left().left()}
        possible_moves.add(pawn.left())
    if pawn.top().right() in state['v_walls']:
        possible_moves-={pawn.right().right()}
        possible_moves.add(pawn.right())
    
    if pawn.left() in state['v_walls']:
        possible_moves-={pawn.left().left(), pawn.left(), pawn.bottom().left()}
    if pawn in state['v_walls']:
        possible_moves-={pawn.right().right(), pawn.right(), pawn.bottom().right()}    
    if pawn.top().left() in state['v_walls']:
        possible_moves-={pawn.left().left(), pawn.left(), pawn.top().left}
    if pawn.top() in state['v_walls']:
        possible_moves-={pawn.right().right(), pawn.riht(), pawn.top().right()}

    #ako postoji pesak na possible_moves    
    
    for pm in possible_moves.copy():
        if pm in state['position_o'] or pm in state['position_x']:
            p=pm in state['position_o'] or pm in state['position_x']
            if pm not in state['home_x'] and pm not in state['home_o']:
                c=pm not in state['home_x'] and pm not in state['home_o']
                possible_moves.remove(pm)
        
    #u slucaju da su drugi pesaci na krajnjim pozicijama moze da se pomeri za jedan korak   

    if pawn.top().top() in state['position_x'] or pawn.top().top() in state['position_o']:
        possible_moves.add(pawn.top())
    if pawn.left().left() in state['position_x'] or pawn.left().left() in state['position_o']:
        possible_moves.add(pawn.left())
    if pawn.bottom().bottom() in state['position_x'] or pawn.bottom().bottom() in state['position_o']:
        possible_moves.add(pawn.bottom())
    if pawn.right().right() in state['position_x'] or pawn.right().right() in state['position_o']:
        possible_moves.add(pawn.right())

    for a in possible_moves:
        print(a)   
                                                       
    return #possible_moves

#def makeMove(state, pawn, move):



state = initialState()

state['h_walls']+=(GridCoordinates(8,11),GridCoordinates(4,8),GridCoordinates(5,8))
state['v_walls']+=(GridCoordinates(7,2),GridCoordinates(8,4))
state['position_x'][1].set(8,9)
state['position_o'][1].set(6,9)

print(tableString(state)) 
print(getValidMoves(state,'X2'))  
              







#for a in Table['h_walls']:print(a)

#print(len(Table['h_walls'])+len(Table['v_walls']))

#Table['h_walls']+=(GridCoordinates(4,3),)

#for a in Table['h_walls']:print(a)

#print(len(Table['h_walls'])+len(Table['v_walls']))

#print(Table['position_x'])

#Table['position_x'] = GridCoordinates(5,3)

#print(Table['position_x'])

#print(Table['position_x']!=Table['position_o'])