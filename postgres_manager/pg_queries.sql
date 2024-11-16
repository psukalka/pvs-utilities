CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL
);  

-- Inserting data into employees table  
-- INSERT into employees (name, age) values ('pavan', 30);