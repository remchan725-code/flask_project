-- 1. Tạo bảng Suppliers
create table Suppliers (
    SID int primary key,
    Sname nvarchar(100) not null,
    Address nvarchar(100),
    Phone varchar(15)
);
go

-- 2. Tạo bảng Products
create table Products (
    PID int primary key,
    Pname nvarchar(100) not null
);
go

-- 3. Tạo bảng Orders với khóa chính phức hợp, khóa ngoại và ràng buộc CHECK
create table Orders (
    SID int,
    PID int,
    Price float check (Price > 0),
    Quantity int check (Quantity > 0),
    primary key (SID, PID),
    foreign key (SID) references Suppliers(SID),
    foreign key (PID) references Products(PID),
    CreatedDate datetime default getdate()
);
go


-- 5. Chèn dữ liệu mẫu
insert into Suppliers (SID, Sname, Address, Phone) values
(1, N'Công ty A', N'Hà Nội', '0912345678'),
(2, N'Công ty B', N'TP.HCM', '0987654321'),
(3, N'Công ty C', N'Đà Nẵng', '0905111222');

insert into Products (PID, Pname) values
(101, N'Laptop'),
(102, N'Điện thoại'),
(103, N'Tai nghe');

insert into Orders (SID, PID, Price, Quantity) values
(1, 101, 15000000, 2),
(1, 103, 500000, 5),
(2, 102, 8000000, 3),
(3, 101, 14500000, 1);
go

-- 6. Truy vấn danh sách chi tiết đơn hàng
select 
    s.Sname, 
    p.Pname, 
    o.Quantity, 
    o.Price, 
    (o.Quantity * o.Price) as TotalAmount,
    o.CreatedDate
from Orders o
join Suppliers s on o.SID = s.SID
join Products p on o.PID = p.PID;
go
