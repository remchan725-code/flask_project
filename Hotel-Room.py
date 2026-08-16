class RoomAlreadyBooked(Exception):
    pass
class Room:
    def __init__(self,room_id,base_price,is_booked):
        self.room_id = room_id
        self.base_price = base_price
        self.__is_booked = False
    def calculate_price(self,nights):
        return nights * self.base_price
    @property
    def is_booked(self):
        return self.__is_booked
    def book(self):
        if self.__is_booked == True:
            raise RoomAlreadyBooked("Phong da duoc dat!")
        else:
            self.__is_booked = True
    def check_out(self):
        self.__is_booked = False
        return self.__is_booked
    def __str__(self):
        status = "Da dat" if self.__is_booked == True else "Trong"
        return f"Room {self.room_id} - Giá: {self.base_price:,.0f} VNĐ - Trạng thái: {status}"
class Standard_Room(Room):
    pass
class VIP_ROOM(Room):
    def __init__(self,room_id,base_price):
        super().__init__(room_id,base_price,is_booked)
    def calculate_price (self,nights):
        base = super.calculate_price(nights)
        service_fee = base * 0.15
        return base + service_fee
class Booking_Manager:
    def __init__(self):
        self.room = []
    def add_room(self,room):
        self.room[Room.room_id] = room
        if Room.room_id == room :
            raise ValueError("So phong da duoc dat")
        self.room[Room.room_id] = room
        print(f"Dat phong {Room.room_id} thanh cong")
    def get_availble_room(self, *room_types):
        
