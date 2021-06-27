class Node:
    def __init__(self , marker : str , data : str) -> None:
        self.marker = marker
        self.data = data

    def __lt__(self, other):
        return len(self.marker) < len(other.marker)
    
    def __gt__(self, other):
        return len(self.marker) > len(other.marker)

    def __eq__(self, other):
        return len(self.marker) == len(other.marker) and self.marker != other.marker

    def __repr__(self) -> str:
        return f"{ self.marker } : {self.data}"

    def __str__(self) -> str:
        return f"{ self.marker } : {self.data}"