# DBMS : MySQL Server 8.0 / Remote MySQL

# Tables Used In Project IMS for Retailers's
1. users
2. contacts
3. shop

# MySQL Command To Create Table User
```sql
Create table users(
    userid int not null primary key auto_increment,
    username varchar(50) unique not null,
    name varchar(50) not null,
    email varchar(50) not null,
    contact char(10) not null,
    address varchar(150),
    password varchar(20),
    agree varchar(5) #agree for t&c
);

Alter table users add auto_increment=1000;
```
# MySQL Command To Create Table Contacts
```sql
Create table contacts(
    cid int not null primary key auto_increment,
    name varchar(50) not null,
    email varchar(50) not null,
    subject varchar(50) not null,
    messsage varchar(300) not null,
    date datetime not null
);

Alter table contacts add auto_increment=100;
```
# MySQL Command To Create Table Shop
```sql
Create table shop(
    iid int not null primary key auto_increment,
    name varchar(100) not null,
    description varchar(250)  not null,
    price int not null,
    stock int not null,
    total int not null,
)auto_increment=1001;
```

# Inserting Values Into Table

```sql
CREATE TABLE `sql12577529`.`shop` ( `iid` INT NOT NULL ,  `name` VARCHAR(50) NOT NULL ,  `description` VARCHAR(250) NOT NULL ,  `price` DECIMAL NOT NULL ,  `stock` INT NOT NULL ,  `total` DECIMAL NOT NULL ,  `reoder_level` INT NOT NULL ) ENGINE = InnoDB;


INSERT INTO `shop` (`inventory id`, `name`, `description`, `price`, `stock`, `total`, `reoder_level`) VALUES ('1', 'Soap Lux', 'Lux | Golden Rose| 25g pack', '23.00', '20', '460', '5');
```

# Creating a Trigger to maintain consitency of total values
```sql
CREATE TRIGGER shop_total_val
after UPDATE
ON shop
for each row
SET total = price * stock
```
> To drop a tigger use

`DROP TRIGGER shop_total_val`
