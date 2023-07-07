var db_name = process.env["MONGO_DB"]

var ugc = db.getSiblingDB(db_name)

sh.enableSharding(db_name)
sh.shardCollection(db_name + "." + "bookmarks", {"user_id": "hashed"})
sh.shardCollection(db_name + "." + "reviews", {"movie_id": "hashed"})
sh.shardCollection(db_name + "." + "ratings", {"user_id": "hashed"})
