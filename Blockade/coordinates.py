
class GridCoordinates:
    """
    Coordinates on square grid
    """

    def __init__(self, row, col):
        self.col  = col
        self.row  = row

    def set(self,row,col):
        self.row=row
        self.col=col    

    def left(self):
        """
        Return the coordinates of the square at left, even if it does not exists
        """
        return GridCoordinates(self.row, self.col - 1)    

    def right(self):
        """
        Return the coordinates of the square at right, even if it does not exists
        """
        return GridCoordinates(self.row,self.col + 1 )

    def top(self):
        """
        Return the coordinates of the square at top, even if it does not exists
        """
        return GridCoordinates(self.row - 1,self.col )

    def bottom(self):
        """
        Return the coordinates of the square at bottom, even if it does not exists
        """
        return GridCoordinates(self.row + 1, self.col)

    def clone(self):
        """
        Return identical coordinates 
        """
        return GridCoordinates(self.row, self.col)

    def __eq__(self, other):
        """
        Override the default Equals behavior.        
        """
        if isinstance(other, self.__class__):
            #return self.__dict__ == other.__dict__
            return self.col == other.col and self.row == other.row
        return NotImplemented

    def __ne__(self, other):
        """
        Define a non-equality test.        
        """
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """
        Override the default hash behavior (that returns the id or the object).        
        """
        return hash((self.col, self.row))

    def __str__(self):
        return "%d,%d" % (self.row, self.col)