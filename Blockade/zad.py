from coordinates import GridCoordinates
import re 

def initialState(
    table_width=14,
    table_length=11,    
    position_x=(GridCoordinates(4,4),GridCoordinates(8,4)),
    position_o=(GridCoordinates(4,11),GridCoordinates(8,11)),
    walls = 9
):

    state ={
        'table_width': table_width,
        'table_length': table_length,
        'home_x': position_x,
        'home_o': position_o,
        'position_x': position_x,
        'position_o': position_o,
        'h_walls_x' : walls,
        'h_walls_o' : walls,
        'v_walls_x' : walls,
        'v_walls_o' : walls,
        'h_walls': (),
        'v_walls': ()
    }
    return (state)

def initialString(width, length):

    x=1
    y=1

    gameStr= ' '
    for a in range(1,width+1):
        gameStr +=' ' + hex(a)[2:].upper()

    gameStr+= '\n  '

    for a in range(width):
        gameStr +='= '
    gameStr+= '\n'

    for a in range(1,length+2):
        gameStr += hex(a)[2:].upper() +'ǁ'    
        for b in range(width):            
            gameStr += f'({a},{b+1})'
            if b==width-1:break
            gameStr +='|'       
        gameStr += 'ǁ'+hex(a)[2:].upper()+'\n'  
        if a == length : break
        gameStr+= '  '    
        for h in range(width):
            gameStr +=f'h{a},{h+1}\u2015 '
        gameStr+= '\n'

    gameStr +='  '
    for a in range(width):
        gameStr +='= '

    gameStr+= '\n '
    for a in range(1,width+1):
        gameStr +=' ' + hex(a)[2:].upper()

    return gameStr 

def tableString(state):

    gameStr = initialString(state['table_width'],state['table_length'])

    for x in state['position_x']:   
        gameStr=re.sub(f'\({x}\)','X',gameStr) 

    for o in state['position_o']:
        gameStr=re.sub(f'\({o}\)','O',gameStr)

    for hw in state['h_walls']:
        gameStr=re.sub(f'h{hw}\u2015','=',gameStr)
        gameStr=re.sub(f'h{hw.col},{hw.row+1}\u2015','=',gameStr)
   
    for vw in state['v_walls']:
        gameStr=re.sub(f'\({vw}\)\|',' ǁ',gameStr)
        gameStr=re.sub(f'\({vw.col+1},{vw.row}\)\|',' ǁ',gameStr)      

        
    gameStr = re.sub('\([0-9]*,[0-9]*\)', ' ', gameStr)
    gameStr = re.sub('h[0-9]*,[0-9]*', '', gameStr)

    return gameStr


state = initialState()

state['h_walls']+=(GridCoordinates(7,6),GridCoordinates(9,8))
state['v_walls']+=(GridCoordinates(7,7),GridCoordinates(9,10))

print(tableString(state))





#for a in Table['h_walls']:print(a)

#print(len(Table['h_walls'])+len(Table['v_walls']))

#Table['h_walls']+=(GridCoordinates(4,3),)

#for a in Table['h_walls']:print(a)

#print(len(Table['h_walls'])+len(Table['v_walls']))

#print(Table['position_x'])

#Table['position_x'] = GridCoordinates(5,3)

#print(Table['position_x'])

#print(Table['position_x']!=Table['position_o'])