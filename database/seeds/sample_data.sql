-- =============================================================================
-- CASS Sample Data
-- =============================================================================
-- Run this after schema.sql to populate with test data
-- psql -U postgres -d cassdb -f seeds/sample_data.sql

-- -----------------------------------------------------------------------------
-- Categories
-- -----------------------------------------------------------------------------
INSERT INTO categories (name, description) VALUES
('Electronics', 'Electronic devices and accessories'),
('Clothing', 'Apparel and fashion items'),
('Books', 'Books and publications'),
('Home & Garden', 'Home improvement and garden supplies'),
('Sports', 'Sports equipment and accessories');

-- -----------------------------------------------------------------------------
-- Products
-- -----------------------------------------------------------------------------
INSERT INTO products (name, category_id, description, price, stock_quantity, sku) VALUES
-- Electronics
('Wireless Bluetooth Headphones', 1, 'Premium noise-cancelling headphones', 149.99, 50, 'ELEC-001'),
('Laptop Stand', 1, 'Ergonomic aluminum laptop stand', 79.99, 100, 'ELEC-002'),
('USB-C Hub', 1, '7-in-1 USB-C adapter', 45.99, 200, 'ELEC-003'),
('Mechanical Keyboard', 1, 'RGB mechanical gaming keyboard', 129.99, 75, 'ELEC-004'),
('Wireless Mouse', 1, 'Ergonomic wireless mouse', 39.99, 150, 'ELEC-005'),

-- Clothing
('Cotton T-Shirt', 2, 'Premium cotton t-shirt', 24.99, 300, 'CLTH-001'),
('Denim Jeans', 2, 'Classic fit denim jeans', 59.99, 150, 'CLTH-002'),
('Running Shoes', 2, 'Lightweight running shoes', 89.99, 100, 'CLTH-003'),
('Winter Jacket', 2, 'Insulated winter jacket', 149.99, 50, 'CLTH-004'),
('Baseball Cap', 2, 'Adjustable baseball cap', 19.99, 200, 'CLTH-005'),

-- Books
('Python Programming', 3, 'Learn Python from scratch', 44.99, 80, 'BOOK-001'),
('Data Science Handbook', 3, 'Complete guide to data science', 54.99, 60, 'BOOK-002'),
('SQL Mastery', 3, 'Advanced SQL techniques', 39.99, 100, 'BOOK-003'),
('Web Development', 3, 'Modern web development guide', 49.99, 70, 'BOOK-004'),
('Machine Learning', 3, 'Introduction to ML algorithms', 59.99, 50, 'BOOK-005'),

-- Home & Garden
('Garden Tool Set', 4, '5-piece garden tool set', 34.99, 80, 'HOME-001'),
('LED Desk Lamp', 4, 'Adjustable LED desk lamp', 29.99, 120, 'HOME-002'),
('Plant Pot Set', 4, 'Ceramic plant pot set of 3', 24.99, 100, 'HOME-003'),
('Storage Bins', 4, 'Stackable storage bins set', 19.99, 200, 'HOME-004'),
('Wall Clock', 4, 'Modern wall clock', 39.99, 60, 'HOME-005'),

-- Sports
('Yoga Mat', 5, 'Non-slip yoga mat', 29.99, 150, 'SPRT-001'),
('Dumbbells Set', 5, 'Adjustable dumbbells 5-25 lbs', 149.99, 40, 'SPRT-002'),
('Basketball', 5, 'Official size basketball', 24.99, 80, 'SPRT-003'),
('Tennis Racket', 5, 'Lightweight tennis racket', 79.99, 50, 'SPRT-004'),
('Water Bottle', 5, 'Insulated water bottle 32oz', 19.99, 250, 'SPRT-005');

-- -----------------------------------------------------------------------------
-- Customers
-- -----------------------------------------------------------------------------
INSERT INTO customers (first_name, last_name, email, phone, city, state, country) VALUES
('John', 'Smith', 'john.smith@email.com', '555-0101', 'New York', 'NY', 'USA'),
('Sarah', 'Johnson', 'sarah.j@email.com', '555-0102', 'Los Angeles', 'CA', 'USA'),
('Michael', 'Williams', 'mwilliams@email.com', '555-0103', 'Chicago', 'IL', 'USA'),
('Emily', 'Brown', 'emily.brown@email.com', '555-0104', 'Houston', 'TX', 'USA'),
('David', 'Jones', 'david.jones@email.com', '555-0105', 'Phoenix', 'AZ', 'USA'),
('Jennifer', 'Davis', 'jdavis@email.com', '555-0106', 'Philadelphia', 'PA', 'USA'),
('Robert', 'Miller', 'rmiller@email.com', '555-0107', 'San Antonio', 'TX', 'USA'),
('Lisa', 'Wilson', 'lisa.wilson@email.com', '555-0108', 'San Diego', 'CA', 'USA'),
('James', 'Moore', 'james.m@email.com', '555-0109', 'Dallas', 'TX', 'USA'),
('Amanda', 'Taylor', 'ataylor@email.com', '555-0110', 'San Jose', 'CA', 'USA'),
('Christopher', 'Anderson', 'c.anderson@email.com', '555-0111', 'Austin', 'TX', 'USA'),
('Jessica', 'Thomas', 'jthomas@email.com', '555-0112', 'Jacksonville', 'FL', 'USA'),
('Matthew', 'Jackson', 'matt.j@email.com', '555-0113', 'San Francisco', 'CA', 'USA'),
('Ashley', 'White', 'a.white@email.com', '555-0114', 'Columbus', 'OH', 'USA'),
('Daniel', 'Harris', 'dharris@email.com', '555-0115', 'Fort Worth', 'TX', 'USA'),
('Nicole', 'Martin', 'nicole.m@email.com', '555-0116', 'Charlotte', 'NC', 'USA'),
('Andrew', 'Garcia', 'agarcia@email.com', '555-0117', 'Seattle', 'WA', 'USA'),
('Stephanie', 'Martinez', 'smartinez@email.com', '555-0118', 'Denver', 'CO', 'USA'),
('Joshua', 'Robinson', 'j.robinson@email.com', '555-0119', 'Boston', 'MA', 'USA'),
('Megan', 'Clark', 'mclark@email.com', '555-0120', 'Nashville', 'TN', 'USA');

-- -----------------------------------------------------------------------------
-- Orders (Last 6 months of data)
-- -----------------------------------------------------------------------------
INSERT INTO orders (customer_id, order_date, status, total_amount, shipping_address) VALUES
-- January 2026
(1, '2026-01-05 10:30:00', 'delivered', 249.98, '123 Main St, New York, NY'),
(2, '2026-01-07 14:15:00', 'delivered', 89.99, '456 Oak Ave, Los Angeles, CA'),
(3, '2026-01-10 09:00:00', 'delivered', 174.98, '789 Pine Rd, Chicago, IL'),
(5, '2026-01-12 16:45:00', 'delivered', 59.99, '321 Elm St, Phoenix, AZ'),
(8, '2026-01-15 11:20:00', 'delivered', 199.98, '654 Maple Dr, San Diego, CA'),
(10, '2026-01-18 13:30:00', 'shipped', 129.99, '987 Cedar Ln, San Jose, CA'),

-- December 2025
(4, '2025-12-02 10:00:00', 'delivered', 149.99, '147 Oak St, Houston, TX'),
(6, '2025-12-05 15:30:00', 'delivered', 234.97, '258 Pine Ave, Philadelphia, PA'),
(7, '2025-12-10 09:45:00', 'delivered', 79.98, '369 Elm Rd, San Antonio, TX'),
(9, '2025-12-15 14:00:00', 'delivered', 324.97, '741 Maple St, Dallas, TX'),
(11, '2025-12-18 11:15:00', 'delivered', 44.99, '852 Cedar Dr, Austin, TX'),
(12, '2025-12-20 16:30:00', 'delivered', 189.98, '963 Oak Ln, Jacksonville, FL'),
(13, '2025-12-22 10:45:00', 'delivered', 99.98, '159 Pine St, San Francisco, CA'),
(15, '2025-12-28 13:00:00', 'delivered', 269.97, '357 Elm Ave, Fort Worth, TX'),

-- November 2025
(1, '2025-11-05 09:30:00', 'delivered', 175.98, '123 Main St, New York, NY'),
(2, '2025-11-10 14:45:00', 'delivered', 54.99, '456 Oak Ave, Los Angeles, CA'),
(14, '2025-11-15 11:00:00', 'delivered', 129.99, '753 Maple Rd, Columbus, OH'),
(16, '2025-11-20 15:15:00', 'delivered', 209.97, '951 Cedar St, Charlotte, NC'),
(17, '2025-11-25 10:30:00', 'delivered', 79.99, '246 Oak Dr, Seattle, WA'),
(18, '2025-11-28 13:45:00', 'delivered', 149.99, '468 Pine Ln, Denver, CO'),

-- October 2025
(3, '2025-10-03 09:00:00', 'delivered', 94.98, '789 Pine Rd, Chicago, IL'),
(19, '2025-10-08 14:30:00', 'delivered', 179.98, '579 Elm St, Boston, MA'),
(20, '2025-10-12 11:45:00', 'delivered', 69.98, '680 Maple Ave, Nashville, TN'),
(4, '2025-10-18 16:00:00', 'delivered', 249.98, '147 Oak St, Houston, TX'),
(5, '2025-10-22 10:15:00', 'delivered', 39.99, '321 Elm St, Phoenix, AZ'),
(6, '2025-10-28 13:30:00', 'delivered', 184.97, '258 Pine Ave, Philadelphia, PA'),

-- September 2025
(7, '2025-09-05 09:45:00', 'delivered', 119.98, '369 Elm Rd, San Antonio, TX'),
(8, '2025-09-10 15:00:00', 'delivered', 74.98, '654 Maple Dr, San Diego, CA'),
(9, '2025-09-15 11:30:00', 'delivered', 159.99, '741 Maple St, Dallas, TX'),
(10, '2025-09-20 14:15:00', 'delivered', 89.99, '987 Cedar Ln, San Jose, CA'),
(11, '2025-09-25 10:00:00', 'delivered', 204.98, '852 Cedar Dr, Austin, TX'),

-- August 2025
(12, '2025-08-02 09:30:00', 'delivered', 134.98, '963 Oak Ln, Jacksonville, FL'),
(13, '2025-08-08 14:45:00', 'delivered', 59.98, '159 Pine St, San Francisco, CA'),
(14, '2025-08-15 11:15:00', 'delivered', 229.97, '753 Maple Rd, Columbus, OH'),
(15, '2025-08-20 15:30:00', 'delivered', 49.98, '357 Elm Ave, Fort Worth, TX'),
(16, '2025-08-28 10:45:00', 'delivered', 169.98, '951 Cedar St, Charlotte, NC');

-- -----------------------------------------------------------------------------
-- Order Items
-- -----------------------------------------------------------------------------
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
-- Order 1
(1, 1, 1, 149.99), (1, 5, 2, 39.99),
-- Order 2
(2, 3, 1, 89.99),
-- Order 3
(3, 4, 1, 129.99), (3, 11, 1, 44.99),
-- Order 4
(4, 7, 1, 59.99),
-- Order 5
(5, 1, 1, 149.99), (5, 14, 1, 49.99),
-- Order 6
(6, 4, 1, 129.99),
-- Order 7
(7, 9, 1, 149.99),
-- Order 8
(8, 2, 1, 79.99), (8, 11, 1, 44.99), (8, 13, 2, 39.99),
-- Order 9
(9, 5, 2, 39.99),
-- Order 10
(10, 1, 1, 149.99), (10, 4, 1, 129.99), (10, 11, 1, 44.99),
-- Order 11
(11, 11, 1, 44.99),
-- Order 12
(12, 3, 1, 89.99), (12, 13, 2, 39.99),
-- Order 13
(13, 6, 2, 24.99), (13, 10, 2, 19.99),
-- Order 14
(14, 1, 1, 149.99), (14, 2, 1, 79.99), (14, 5, 1, 39.99),
-- Order 15
(15, 4, 1, 129.99), (15, 3, 1, 45.99),
-- Order 16
(16, 12, 1, 54.99),
-- Order 17
(17, 4, 1, 129.99),
-- Order 18
(18, 1, 1, 149.99), (18, 6, 2, 24.99),
-- Order 19
(19, 2, 1, 79.99),
-- Order 20
(20, 9, 1, 149.99),
-- Order 21
(21, 13, 2, 39.99), (21, 25, 1, 19.99),
-- Order 22
(22, 4, 1, 129.99), (22, 14, 1, 49.99),
-- Order 23
(23, 21, 1, 29.99), (23, 5, 1, 39.99),
-- Order 24
(24, 1, 1, 149.99), (24, 13, 2, 39.99),
-- Order 25
(25, 5, 1, 39.99),
-- Order 26
(26, 11, 1, 44.99), (26, 12, 1, 54.99), (26, 14, 1, 49.99),
-- Order 27
(27, 2, 1, 79.99), (27, 5, 1, 39.99),
-- Order 28
(28, 6, 3, 24.99),
-- Order 29
(29, 22, 1, 149.99),
-- Order 30
(30, 3, 1, 89.99),
-- Order 31
(31, 1, 1, 149.99), (31, 12, 1, 54.99),
-- Order 32
(32, 11, 1, 44.99), (32, 13, 2, 39.99),
-- Order 33
(33, 6, 2, 24.99),
-- Order 34
(34, 4, 1, 129.99), (34, 12, 1, 54.99), (34, 11, 1, 44.99),
-- Order 35
(35, 10, 2, 19.99),
-- Order 36
(36, 1, 1, 149.99), (36, 25, 1, 19.99);

-- Update customer last_order_at
UPDATE customers c SET last_order_at = (
    SELECT MAX(order_date) FROM orders o WHERE o.customer_id = c.id
);

-- =============================================================================
-- Sample Queries to Test
-- =============================================================================
-- Try these queries with CASS:
-- 1. "Show me the top 5 customers by total spending"
-- 2. "What are the best selling products?"
-- 3. "Show monthly revenue for the last 6 months"
-- 4. "Which cities have the most customers?"
-- 5. "What is the average order value?"
-- =============================================================================
