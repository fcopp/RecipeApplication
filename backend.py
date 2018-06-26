import sqlite3

connection = sqlite3.connect("database/database.db")

c = connection.cursor()

c.execute("""DROP TABLE IF EXISTS ingredients""")
c.execute("""DROP TABLE IF EXISTS recipes""")
c.execute("""DROP TABLE IF EXISTS recipeingredients""")


#Create ingredients
c.execute("""CREATE TABLE IF NOT EXISTS ingredients (
	ingredientID INTEGER PRIMARY KEY, 
	name TEXT,
	UNIQUE(name)
)
""")

c.execute("""CREATE TABLE IF NOT EXISTS recipes (
	recipeID INTEGER PRIMARY KEY, 
	name INT ,
	instructions TEXT,
	UNIQUE(name)
)
""")

c.execute("""CREATE TABLE IF NOT EXISTS recipeingredients (
	recipeID INTEGER NOT NULL,
	ingredientID INTEGER NOT NULL,
	quantity TEXT,
	FOREIGN KEY (recipeID) REFERENCES recipes(recipeID),
	FOREIGN KEY (ingredientID) REFERENCES ingredients(ingredientID)
)
""")

c.execute("""INSERT OR IGNORE INTO recipes (name, instructions) VALUES (1,"penis")""")
c.execute("""INSERT OR IGNORE INTO recipes (name, instructions) VALUES (2,"penis")""")
c.execute("""INSERT OR IGNORE INTO recipes (name, instructions) VALUES (3,"penis")""")
c.execute("""INSERT OR IGNORE INTO recipes (name, instructions) VALUES (1,"cock")""")
c.execute("""SELECT recipeID, * FROM recipes""")
print(c.fetchall())


# c.execute("""CREATE TABLE IF NOT EXISTS sections (
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# course_id INTEGER,
# teacher_id INTEGER,
# days_held VARCHAR(64),
# time_block VARCHAR(64),
# UNIQUE (teacher_id)
# )""")

# c.execute("""INSERT INTO sections
# (course_id, teacher_id, days_held, time_block)
# VALUES
# (1,4,"MWF","08:00-10:00"),
# (2,2,"MWF","08:00-10:00"),
# (1,3,"TTH","08:00-10:00")""")

# c.execute("""INSERT INTO sections
# (course_id, teacher_id, days_held, time_block)
# VALUES
# (1,1,"MWF","09:00-10:00")
# """)

connection.commit()
connection.close()