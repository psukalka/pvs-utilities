CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL
);  

-- Inserting data into employees table  
-- INSERT into employees (name, age) values ('pavan', 30);

CREATE TABLE employees_partitioned(
    id SERIAL,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    PRIMARY KEY (id, age)
) PARTITION BY RANGE (age);

CREATE TABLE employees_young PARTITION OF employees_partitioned
    FOR VALUES FROM (20) TO (30);

CREATE TABLE employees_middle PARTITION OF employees_partitioned
    FOR VALUES FROM (30) TO (45);

CREATE TABLE employees_senior PARTITION OF employees_partitioned
    FOR VALUES FROM (45) TO (61);

INSERT INTO employees_partitioned 
SELECT * FROM employees; 

SELECT setval(
    'employees_partitioned_id_seq',
    (SELECT MAX(id) FROM employees)
);

SELECT count(*) FROM employees;
SELECT count(*) FROM employees_partitioned;

BEGIN;
    -- Rename old table (backup)
    ALTER TABLE employees 
    RENAME TO employees_old;
    
    -- Rename new partitioned table to original name
    ALTER TABLE employees_partitioned 
    RENAME TO employees;
    
    -- If everything looks good
COMMIT;
