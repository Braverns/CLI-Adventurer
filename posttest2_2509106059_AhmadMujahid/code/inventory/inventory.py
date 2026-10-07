from items.item import Item

class Inventory:
    def __init__(self) -> None:
        self.max_item: int = 10
        self.items: list[Item | None] = [None] * self.max_item

    def check_slot(self) -> bool:
        for slot in self.items:
            if slot is None:
                return True
            
        return False

    def add_item(self, item: Item) -> None:
        if not self.check_slot():
            raise ValueError("Inventory full tidak bisa menambah item")
        
        for i in range(self.max_item):
            if self.items[i] is None:
                self.items[i] = item
                break
                
    
    def remove_item(self, slot: int) -> Item:
        item = self.items[slot]
        if item is not None:
            self.items[slot] = None
            return item 
        else:
            raise IndexError("Tidak ada item pada slot ini")
        
    def move_item(self, from_slot: int, to_slot: int) -> None:
        self.items[from_slot], self.items[to_slot] = self.items[to_slot], self.items[from_slot]

    def get_item(self, slot: int) -> Item:
        item = self.items[slot]
        if item is not None:
            return item 

        raise IndexError("Tidak ada item pada slot ini")
        