from utils.traits.trait import Trait

class TraitEntry:
    def __init__(self, trait: Trait, stack: int) -> None:
        self.trait = trait

        if stack <= 0:
            raise ValueError("Tidak boleh negatif atau 0")

        if stack > self.trait.max_stack:
            raise ValueError("Tidak Bisa Lebih Dari Max_Stack")

        self.__stack = stack

    @property
    def stack(self) -> int:
        return self.__stack


    def increase_stack(self, amount: int) -> None: 
        if amount <= 0:
            raise ValueError("Tidak boleh negatif atau 0")
        
        new_stack = self.__stack + amount

        if new_stack > self.trait.max_stack:
            raise ValueError("Tidak Bisa Lebih Dari Max_Stack")

        self.__stack = new_stack

    def decrease_stack(self, amount: int) -> None:
        if amount > self.stack:
            raise ValueError("Melebihi stack trait")

        if amount <= 0:
            raise ValueError("Tidak boleh negatif atau 0")
        
        self.__stack -= amount
        if self.__stack <= 0:
            self.__stack = 0
