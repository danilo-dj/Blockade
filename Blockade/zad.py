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
        possible_moves-={pawn.right().right(), pawn.right(), pawn.top().right()}

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

def makeAMove(state, move): #[X 1] [6 3] [V 4 9]

    if  not re.match('\[[XO] [12]\] \[[0-9][0-9]* [0-9][0-9]*\] \[[VH] [0-9][0-9]* [0-9][0-9]*\]',move):
        return 'pogresan format poteza'     

    steprow=re.search('\[([0-9][0-9]*) ([0-9][0-9]*)\] \[[VH] ([0-9][0-9]*) ([0-9][0-9]*)\]', move).group(1)
    stepcol=re.search('\[([0-9][0-9]*) ([0-9][0-9]*)\] \[[VH] ([0-9][0-9]*) ([0-9][0-9]*)\]', move).group(2)
    wallrow=re.search('\[([0-9][0-9]*) ([0-9][0-9]*)\] \[[VH] ([0-9][0-9]*) ([0-9][0-9]*)\]', move).group(3)
    wallcol=re.search('\[([0-9][0-9]*) ([0-9][0-9]*)\] \[[VH] ([0-9][0-9]*) ([0-9][0-9]*)\]', move).group(4)
    
    p=re.search('\[([XO]) ([0-9][0-9]*)\]', move).group(1)
    n=re.search('\[([XO]) ([0-9][0-9]*)\]', move).group(2)          

    pawn=p+n
    step=GridCoordinates(int(steprow), int(stepcol))
    wall_kind=re.search('\[([VH]) [0-9][0-9]* [0-9][0-9]*\]', move).group(1)
    wall_coor=GridCoordinates(int(wallrow),int(wallcol))       

    #postavljanje i provera zida

    if checkPositionForWall(state,wall_coor,wall_kind):
        if wall_kind=='H':
            if re.match('X[12]',pawn):
                if state['h_walls_x']>0:
                    state['h_walls']+=(wall_coor,)
                    state['h_walls_x']-=1
                else:
                    return 'Igrac X nema vise H zidova'    
            if re.match('O[12]',pawn):
                if state['h_walls_o']>0:
                    state['h_walls']+=(wall_coor,)
                    state['h_walls_o']-=1
                else:
                    return 'Igrac O nema vise H zidova'
            
        if wall_kind=='V':
            if re.match('X[12]',pawn):
                if state['v_walls_x']>0:
                    state['v_walls']+=(wall_coor,)
                    state['v_walls_x']-=1
                else:
                    return 'Igrac X nema vise V zidova'    
            if re.match('O[12]',pawn):
                if state['v_walls_o']>0:
                    state['v_walls']+=(wall_coor,)
                    state['v_walls_o']-=1
                else:
                    return 'Igrac O nema vise V zidova'
    else:
        return f'Izabrano polje {wall_coor} za zid je zauzeto'


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
        return f'Korak pesaka {pawn} nije validan'

    return 'Izvrsen je potez:'+move

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

def getWallsTouching(state, position, touchingwall_kind):    # vraca set GridCoordinates
    #moguce pozicije dodirnih zidova    
    possibleTouchingWalls = set()
    if position in state['v_walls']:
        if touchingwall_kind == 'H':
            possibleTouchingWalls.update( {
                position.top().left(),
                position.top(),
                position.top().right(),
                position.bottom(),
                position.bottom().left(),
                position.bottom().right(),
                position.left(),
                position.right()
            } )
        if touchingwall_kind == 'V':
            possibleTouchingWalls.update({
                position.top().top(),
                position.bottom().bottom()
            })
    elif position in state['h_walls']:
        if touchingwall_kind=='V':           
            possibleTouchingWalls.update({
                position.top().left(),
                position.top(),
                position.top().right(),
                position.bottom(),
                position.bottom().left(),
                position.bottom().right(),
                position.right(),
                position.left()
            })
        if touchingwall_kind=='H':
            possibleTouchingWalls.update({ 
                position.left().left(),
                position.right().right()
            })

    touchingWalls = set()

    for pos in possibleTouchingWalls:
        if touchingwall_kind=='V':
            if pos in state['v_walls']:
                touchingWalls.add(pos)        
        if touchingwall_kind=='H':
            if pos in state['h_walls']:
                touchingWalls.add(pos)

    return touchingWalls

def wallSequence(state,wall_pos,seq):
    hTouching = getWallsTouching(state,wall_pos,'H')
    vTouching = getWallsTouching(state,wall_pos,'V')
    if len(seq) != (seq.add(wall_pos) or len(seq)):    
        for hw in hTouching:
            wallSequence(state,hw,seq)
        for vw in vTouching:
            wallSequence(state,vw,seq)    

def checkSeq(state,wall_pos):
    seq=set()
    wallSequence(state,wall_pos,seq)
    homes=state['home_x']+state['home_o']

    ivica=0    
    for wall in seq:
        if (wall in state['v_walls'] and wall.row==1)or(wall in state['v_walls'] and wall.row==state['table_length']):
            ivica+=1 
        if(wall in state['h_walls'] and wall.col==1)or(wall in state['h_walls'] and wall.col==state['table_width']):
            ivica+=1

    start=None
    finish=None 
    for wall in seq:            
        for home in homes:
            if start==None:
                if wall.row==home.row or wall.col==home.col:
                    start=wall
                    break
            elif finish==None:
                if wall.row==home.row or wall.col==home.col:
                    if start.col!=wall.col and start.row!=wall.row:
                        finish = wall
                        break  

    if ivica>=2:
        if isSeqWithinHomes(state, subSeq(seq,start,finish)):
            return False
    if isSeqClosed(seq):
        return False
    return True

def isSeqWithinHomes(state,seq):    
    for wall in seq:
        if wall.row<state['home_x'][0].row or wall.row>state['home_x'][1].row or wall.col<state['home_x'[0]].col or wall.col>state['home_o'][0].col:
            return False
    return True

def subSeq(seq,start,finish):
    subSq=set()
    if start in seq and finish in seq:
        while start!=finish:
            for wall in seq:            
                if abs(wall.col - start.col)<=2 and abs(wall.row-start.row)<=2:
                    subSeq.add(wall)
                    start = wall
                    break
                if abs(wall.col - start.col)==2 and abs(wall.row-start.row)==2:
                    if wall in state['h_walls'] and start in state['h_walls']:
                        subSeq.add(wall)
                        start=wall
                        break
                    if wall in state['v_walls'] and start in state['v_walls']:
                        subSeq.add(wall)
                        start=wall
                        break
    return subSq

def isSeqClosed(seq):
    seqL=list(seq)
    for i in range(len(seqL)-1):
        touch = getWallsTouching(state,seqL[i],'V')
        touch.update(getWallsTouching(state,seqL[i],'H'))        
        if seqL[i+1] in touch: continue        
        for j in range(i,len(seqL)):
            if seqL[j] in touch:
                pom=seqL[i+1]
                seqL[i+1]=seqL[j]
                seqL[j]=pom
                break

    for i in range(len(seqL)-1):        
        if abs(seqL[i].col - seqL[i+1].col)>2 or abs(seqL[i].row-seqL[i+1].row)>2:
            return False
        if abs(seqL[i].col - seqL[i+1].col)==2 or abs(seqL[i].row-seqL[i+1].row)==2:
            if seqL[i] in state['h_walls'] and seqL[i+1] in state['v_walls']:
                return False
    return True


state = initialState()
#state['h_walls_x']=0
#state['v_walls_x']
state['h_walls']+=(GridCoordinates(7,9),GridCoordinates(3,6),GridCoordinates(2,4),GridCoordinates(4,4),GridCoordinates(4,2))
state['v_walls']+=(GridCoordinates(1,5),GridCoordinates(1,8),GridCoordinates(3,5),GridCoordinates(3,1))
#state['position_x']=(GridCoordinates(),GridCoordinates())
print(tableString(state))
checkSeq(state,GridCoordinates(1,5))

    


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

    a=3
    while a>0:
        print('Igrac X je na potezu!')
        print('Unesi potez u formatu \n [igrac brpesaka] [korak] [vrstazid pozyida] \n')
        move=input()
        print(makeAMove(state, move))
        print(is_end(state))
        print(tableString(state))
        print('Igrac O je na potezu!')
        print('Unesi potez u formatu \n [igrac brpesaka] [korak] [vrstazid pozyida] \n')
        move=input()
        print(makeAMove(state, move))
        print(is_end(state))
        print(tableString(state))
        a-=1


game()
'''