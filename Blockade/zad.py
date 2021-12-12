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
        if position == vw.bottom() and wall =='V':
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
            return 'Pobedio je igrac X'
    if (state['position_o'][0]==state['home_x'][0] or 
        state['position_o'][1]==state['home_x'][0] or
        state['position_o'][0]==state['home_x'][1] or
        state['position_o'][1]==state['home_x'][1]):
            return 'Pobedio je igrac O' 
    return 'Sledeci potez'   

def game():

    print('Ko je prvi na potezu?[covek,racunar](c\\r)?')
    a=input()
    print(a)

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