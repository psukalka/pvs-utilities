# Listing all databases
`\l`

# Describe all tables
`\d` 

# Taking backup of database
`pg_dump -U postgres postgres > /pvs/my_db.dump`

# Loading data from a dump
`psql -U postgres -d postgres -f my_db.dump`
