#!/bin/bash

set -e
set -u

# Create database
create_database() {
	psql -v ON_ERROR_STOP=1 -U "$POSTGRES_MASTER" <<-EOSQL
        CREATE USER $APP_POSTGRES_USER WITH PASSWORD '$APP_POSTGRES_PASSWORD';
        ALTER USER $APP_POSTGRES_USER WITH SUPERUSER;
        CREATE DATABASE $APP_POSTGRES_DB;
        ALTER DATABASE $APP_POSTGRES_DB OWNER TO $APP_POSTGRES_USER;
EOSQL
}

grant_permissions() {
	psql -v ON_ERROR_STOP=1 -U "$POSTGRES_MASTER" <<-EOSQL
        GRANT ALL PRIVILEGES ON DATABASE $APP_POSTGRES_DB TO $APP_POSTGRES_USER;
EOSQL
}

create_tables() {
    psql -v ON_ERROR_STOP=1 -U "$APP_POSTGRES_USER" -d "$APP_POSTGRES_DB" <<-EOSQL

        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE TABLE customers (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL,
            username VARCHAR(255),
            hash TEXT NOT NULL,
            disabled BOOLEAN NOT NULL DEFAULT FALSE
        );

        CREATE TABLE products (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR(255) NOT NULL,
            price NUMERIC(10, 2) NOT NULL,
            quantity_in_stock INTEGER NOT NULL
        );

        CREATE TYPE order_status AS ENUM ('PENDING', 'IN_PROGRESS', 'RESOLVED');

        CREATE TABLE orders (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
            product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
            status order_status NOT NULL,
            quantity INTEGER NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
EOSQL
}

populate_customers() {
	psql -v ON_ERROR_STOP=1 -U "$APP_POSTGRES_USER" -d "$APP_POSTGRES_DB" <<-EOSQL
        INSERT INTO customers (name, address, username, hash) VALUES
        ('Alice Johnson', '123 Maple Street', 'alice', '\$2b\$12\$NpQzC.763GZOIte7D0.GCe3wocby3wgIfOMsy/FNUe2flYdbNjEQ2'),
        ('Bob Smith', '456 Oak Avenue', 'bob', '\$2b\$12$/5L.aT4qC5flKDmK6cndsOl0dS98FEW8ptZ0oUKHLVQezstycojhK'),
        ('Carol White', '789 Pine Lane', 'carol', '\$2b\$12\$3ACJZBysi2V1wXrRSe0zHOKe9WhM5dLkppxCz0Jl2aR7e1hTIdBoC'),
        ('David Brown', '101 Cherry Drive', 'david', '\$2b\$12\$Q.4iidCetG04CpvF0xS5zOOFmkAi5wuvOUodtHflpw6N79lgUwBrW'),
        ('John Doe', '123 Fake Street', 'john', '\$2b\$12\$f8X2mV0u91ihs8GcX/R4DOEaJJrtxECQ1GBe4b/b53MLYdiQSE8tu'),
        ('Eve Black', '202 Birch Road', 'eve', '\$2b\$12\$nqErTiDhtbV1WGpPIn19F.Z3Fz43gRSw2zGwojNOXgAbd0l4M33Fe');
EOSQL
}

populate_products() {
    psql -v ON_ERROR_STOP=1 -U "$APP_POSTGRES_USER" -d "$APP_POSTGRES_DB" <<-EOSQL
        INSERT INTO products (name, price, quantity_in_stock) VALUES
            ('Saffron 5kg', 500.00, 25),
            ('Truffle 1kg', 1000.00, 15),
            ('Vanilla Beans 2kg', 400.00, 30),
            ('Caviar 2kg', 1200.00, 10),
            ('Foie Gras 3kg', 300.00, 20),
            ('Kobe Beef 10kg', 2000.00, 5),
            ('Bluefin Tuna 15kg', 3000.00, 8),
            ('Manuka Honey 20kg', 700.00, 40),
            ('Wagyu Beef 5kg', 1500.00, 12),
            ('Matsutake Mushrooms 2kg', 800.00, 18),
            ('Goose Liver 4kg', 250.00, 22),
            ('Saffron 1kg', 150.00, 50),
            ('Alba White Truffle 1kg', 3500.00, 6),
            ('Yubari King Melon 5kg', 600.00, 10),
            ('Jamon Iberico 10kg', 1200.00, 7),
            ('Wild Salmon 10kg', 500.00, 20),
            ('Black Truffle 2kg', 600.00, 14),
            ('Coffea Luwak 5kg', 300.00, 15),
            ('Birds Nest 1kg', 2000.00, 9),
            ('Edible Gold Leaf 50 sheets', 500.00, 30);
EOSQL
}

connect_database() {
	psql -U "$APP_POSTGRES_USER" -d "$APP_POSTGRES_DB"
}

create_database
grant_permissions
create_tables
populate_customers
populate_products
connect_database
