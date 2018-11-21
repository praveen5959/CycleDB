import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

def create_table():

    c.execute('create table if not exists customer(user_id varchar(20), password varchar(30), name varchar(50), ph_no number, constraint pk_cus primary key(user_id))')
    c.execute('create table if not exists category(cat_id varchar(10), cat_name varchar(15),constraint pk_cat primary key(cat_id))')
    c.execute('create table if not exists stock(cycle_name varchar(50),cat_id varchar(10),cost_price number, sell_price number, cycle_image varchar(100),quantity number, description text, constraint pk_stock primary key(cycle_name),constraint fk_stock foreign key(cat_id) references category(cat_id) on delete cascade)')
    c.execute('create table if not exists access(user_id varchar(20), cycle_name varchar(50), constraint pk_acc primary key(user_id,cycle_name), constraint fk1_acc foreign key(user_id) references customer(user_id) on delete cascade,constraint fk2_acc foreign key(cycle_name) references stock(cycle_name) on delete cascade)')
    c.execute('create table if not exists enquiry(enq_id varchar(100), user_id varchar(20), cycle_name varchar(50), cat_id varchar(10),enq_date date, constraint pk_enq primary key(enq_id,user_id,cycle_name,cat_id), constraint fk1_enq foreign key(user_id) references customer(user_id) on delete set null,constraint fk2_enq foreign key(cycle_name) references stock(cycle_name) on delete set null,constraint fk3_enq foreign key(cat_id) references category(cat_id) on delete set null)')
    c.execute('create table if not exists suppliers(s_id varchar(20), s_name varchar(50),s_city varchar(30),ph_no number,email varchar(50), constraint pk_sup primary key(s_id))')
    c.execute('create table if not exists supplies(s_id varchar(20), cycle_name varchar(50), constraint pk_s primary key(s_id,cycle_name),constraint fk1_s foreign key(s_id) references suppliers(s_id) on delete cascade,constraint fk2_s foreign key(cycle_name) references stock(cycle_name) on delete cascade)')
    c.execute('create trigger if not exists calculate_sp after insert on stock for each row begin update stock set sell_price = new.cost_price*1.18*1.2 where cycle_name = new.cycle_name; end')

# def insert():
#     # # c.execute("insert into category values ('1','male')")
#     # c.execute("insert into ")

create_table()
# insert()

