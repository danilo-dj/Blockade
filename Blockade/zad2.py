from coordinates import GridCoordinates
import zad

state = zad.initialState()


def is_end(state):
    if (state['position_x'][0]==state['home_o'][0] or 
        state['position_x'][1]==state['home_o'][0] or
        state['position_x'][0]==state['home_o'][1] or
        state['position_x'][1]==state['home_o'][1]):
            print('Pobedio je igrac X')
    if (state['position_o'][0]==state['home_o'][0] or 
        state['position_o'][1]==state['home_o'][0] or
        state['position_o'][0]==state['home_o'][1] or
        state['position_o'][1]==state['home_o'][1]):
            print('Pobedio je igrac O')
    

  
    def check_if_move_is_valid(state, start_location, end_location):
        if end_location[0] > initialState.table_length or end_location[1] > initialState.table_width:
            print('Zeljeni potez je van koordinata table')
            return

        if end_location[0] == start_location[0] + 2 and \
            end_location[1] == start_location[1]:
            if (start_location[0] + 1, start_location[1]) in state.h_walls or \
                (start_location[0] + 1, start_location[1] -1) in state.h_walls or \
                (start_location[0] + 2, start_location[1]) in state.h_walls or \
                (start_location[0] + 2, start_location[1] -1) in state.h_walls:

                print('Postoji zid na putu')
                return 0
            else:  
                print('Potez je validan', end_location)
                return 1
        
        
        if end_location[0] == start_location[0] + 1 and end_location[1] == start_location[1] - 1:
         
            if end_location in state.h_walls or end_location in state.v_walls:
                print('Postoji zid na putu')
                return 0
            else:
                return 1



print(state)

print(is_end(state))







def checkPositionForWall (state, position):
       #res=False
       for hw in state['h_walls'] :
        if position == hw :
               return False
               #break 
               #print ('Mogućnost postavljanja zida ? : ' + str(res))
               #res=False
       for vw in state['v_walls'] :
        if position == vw :
               return False
               #break
               #print ('Mogućnost postavljanja zida ? : ' + str(res))
        
        
        for hw in state['h_walls'] :
            if position == hw.right():
                return False

        for vw in state['v_walls'] :
            if position == vw.bottom():
                return False 

        if position.col == state['table_width'] or position.row== state['table_length']:
            return False 

        return True 


        state['h_walls'][1].col

        for x in state['h_walls']:
            s=len(state['h_walls'])
            for p in range(s) :
             p=state['h_walls'][position[0]]
            if state['h_walls'][p][0]==position[0] and state['h_walls'][p][1]==(position[1]+1) :
             break
             print('Mogućnost postavljanja zida ne postoji')

            if state['v_walls'][p][1]==position[1] and state['v_walls'][p][0]==(position[0]+1) :
             break
             print('Mogućnost postavljanja zida ne postoji')




