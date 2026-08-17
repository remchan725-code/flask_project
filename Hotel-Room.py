class RoomAlreadyBooked(Exception):
    pass
class Room:
    def __init__(self,room_id,base_price):
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
        status = "Already Booked" if self.__is_booked == True else "Empty"
        room_type = type(self).__name__ 
        return f"[{room_type}] | Room {self.room_id} - Giá: {self.base_price:,.0f} VNĐ - Trạng thái: {status}"
class Standard_Room(Room):
    pass
class VIP_ROOM(Room):
    def __init__(self,room_id,base_price):
        super().__init__(room_id,base_price)
    def calculate_price (self,nights):
        base = super().calculate_price(nights) 
        service_fee = base * 0.15
        return base + service_fee
class Booking_Manager:
    def __init__(self):
        self.rooms = {}
    def add_room(self,room):
        if room.room_id in self.rooms:            # kiểm tra TRƯỚC khi thêm
            raise ValueError(f"So phong {room.room_id} da duoc dat")
        self.rooms[room.room_id] = room
        print(f"Dat phong {room.room_id} thanh cong")
    def get_availble_room(self, *room_types):
        return [
            room
            for room in self.rooms.values()
            if not room.is_booked
            and (not room_types or type(room).__name__ in room_types)
        ]
    def __len__(self):
        return len(self.get_availble_room())
r_std = Standard_Room("101", 500000)
r_vip = VIP_ROOM("201", 1000000)
print(r_std)
print(r_vip)

print("Gia phong cho 2 dem",r_std.calculate_price(2))
print("Gia phong cho 2 dem",r_vip.calculate_price(2))

r_std.book()
print(r_std.is_booked)#True

try:
    r_std.book()
except RoomAlreadyBooked as e:
    print("Phong da duoc book")#Phong da duoc book

r_std.check_out()
print(r_std.is_booked)#False