import sqlite3

conn = sqlite3.connect('classroom.db')

cursor = conn.cursor()

# cursor.execute(
#     """
#     DROP TABLE user
#     """
# )

# PLAYER
# cursor.execute(
#     """
#     CREATE TABLE Players (
#       playerId INTEGER PRIMARY KEY AUTOINCREMENT,
#       username TEXT UNIQUE NOT NULL,
#       password TEXT NOT NULL,
#       currency INTEGER DEFAULT 0,
#       roomName TEXT DEFAULT classroom
#     )
#     """
# )

# SHOP ITEM
# cursor.execute(
#     """
#     CREATE TABLE ShopItem (
#         shopItemId INTEGER PRIMARY KEY AUTOINCREMENT,
#         itemName TEXT UNIQUE NOT NULL,
#         itemPrice INTEGER DEFAULT 0
#     )
#     """
# )

# cursor.execute(
#     """
#     INSERT INTO ShopItem(itemName, itemPrice) VALUES ('lectureNote', '10'), ('diary', '5')
#     """
# )



# PLAYER ITEM
# cursor.execute(
#     """
#     CREATE TABLE PlayerItem (
#       playerItemId INTEGER PRIMARY KEY AUTOINCREMENT,
#       playerId INTEGER NOT NULL,
#       shopItemId INTEGER NOT NULL,
#       FOREIGN KEY(playerId) REFERENCES Players(playerId),
#       FOREIGN KEY(shopItemId) REFERENCES ShopItem(shopItemId)
#     )
#     """
# )

# cursor.execute(
#     """
#     INSERT INTO PlayerItem (playerId, shopItemId) VALUES (1, 2)
#     """
# )

conn.commit()

conn.close()