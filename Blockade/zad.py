from coordinates import GridCoordinates 

def initialState(
    table_width=11,
    table_length=14,    
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

def stateToString(width, length):

    gameStr= ' '
    for a in range(1,width+2):
        gameStr +=' ' + hex(a)[2:].upper()

    gameStr+= '\n  '

    for a in range(state['table_width+1):
        gameStr +='= '
    gameStr+= '\n'

    for a in range(1,state['table_length']+2):
        gameStr += hex(a)[2:].upper() +'ǁ'    
        for b in range(state['table_width']):
            gameStr += ' ' + '|'        
        gameStr += ' ǁ'+hex(a)[2:].upper()+'\n'  
        if a == state['table_length'] : break
        gameStr+= '  '    
        for a in range(state['table_width']+1):
            gameStr +='\u2015 '
        gameStr+= '\n'

    gameStr +='  '
    for a in range(state['table_width']+1):
        gameStr +='= '

    gameStr+= '\n '
    for a in range(1,state['table_width']+2):
        gameStr +=' ' + hex(a)[2:].upper()

    return gameStr 

def tebleString(width,height):


state = initialState()

print(stateToString(state))





#for a in Table['h_walls']:print(a)

#print(len(Table['h_walls'])+len(Table['v_walls']))

#Table['h_walls']+=(GridCoordinates(4,3),)

#for a in Table['h_walls']:print(a)

#print(len(Table['h_walls'])+len(Table['v_walls']))

#print(Table['position_x'])

#Table['position_x'] = GridCoordinates(5,3)

#print(Table['position_x'])

#print(Table['position_x']!=Table['position_o'])