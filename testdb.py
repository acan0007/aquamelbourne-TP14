from sqlalchemy import create_engine, text

# Replace with your actual database URI
engine = create_engine('postgresql://acan0007:R4skr_123@localhost:5432/aquamelbournedb')

# Create a connection
connection = engine.connect()

# Correct way to execute the query
result = connection.execute(text('SELECT "siteId", "siteName", "date", "value", "qualifier", "level", "key" FROM ecoli'))

# Fetch and print the results
for row in result:
    print(row)

# Close the connection
connection.close()
