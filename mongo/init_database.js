var db_name = process.env["MONGO_DB"]
var db_user = process.env["MONGO_USERNAME"]
var db_password = process.env["MONGO_PASSWORD"]

var ugc = db.getSiblingDB(db_name)

ugc.createUser(
    {
        "user": db_user,
        "pwd": db_password,
        "roles": [
            { role: "readWrite", db: db_name }
        ]
    }
)

ugc.createCollection("bookmarks", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "Bookmarks collection",
            required: ["_id", "user_id", "movie_id", "created_at"],
            properties: {
                _id: {
                    bsonType: "binData",
                    description: "'_id' must be a UUID and is required"
                },
                user_id: {
                    bsonType: "binData",
                    description: "'user_id' must be a UUID and is required"
                },
                movie_id: {
                    bsonType: "binData",
                    description: "'movie_id' must be a UUID and is required"
                },
                created_at: {
                    bsonType: "date",
                    description: "'created_at' must be a Date and is required"
                }
            },
            additionalProperties: false
        }
    }
})

ugc.createCollection("reviews", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "Reviews collection",
            required: ["_id", "user_id", "movie_id", "text", "likes", "dislikes", "created_at"],
            properties: {
                _id: {
                    bsonType: "binData",
                    description: "'_id' must be a UUID and is required"
                },
                user_id: {
                    bsonType: "binData",
                    description: "'user_id' must be a UUID and is required"
                },
                movie_id: {
                    bsonType: "binData",
                    description: "'movie_id' must be a UUID and is required"
                },
                text: {
                    bsonType: "string",
                    description: "'text' must be a string and is required"
                },
                likes: {
                    bsonType: "array",
                    description: "'likes' must be a array and is required"
                },
                dislikes: {
                    bsonType: "array",
                    description: "'dislikes' must be a array and is required"
                },
                created_at: {
                    bsonType: "date",
                    description: "'created_at' must be a Date and is required"
                }
            },
            additionalProperties: false
        }
    }
})

ugc.createCollection("movies", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "Bookmarks collection",
            required: ["_id", "rate_count", "rate_value"],
            properties: {
                _id: {
                    bsonType: "binData",
                    description: "'_id' must be a UUID and is required"
                },
                rate_count: {
                    bsonType: "int",
                    description: "'rate_count' must be a INT and is required"
                },
                rate_value: {
                    bsonType: "int",
                    description: "'rate_value' must be a INT and is required"
                }
            },
            additionalProperties: false
        }
    }
})

ugc.createCollection("ratings", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "Ratings collection",
            required: ["_id", "user_id", "movie_id", "rating", "created_at"],
            properties: {
                _id: {
                    bsonType: "binData",
                    description: "'_id' must be a UUID and is required"
                },
                user_id: {
                    bsonType: "binData",
                    description: "'user_id' must be a UUID and is required"
                },
                movie_id: {
                    bsonType: "binData",
                    description: "'movie_id' must be a UUID and is required"
                },
                rating: {
                    bsonType: "int",
                    description: "'rating' must be a INT and is required"
                },
                created_at: {
                    bsonType: "date",
                    description: "'created_at' must be a Date and is required"
                }
            },
            additionalProperties: false
        }
    }
})

ugc.bookmarks.createIndex({"user_id": 1, "movie_id": 1}, {"unique": true})
ugc.reviews.createIndex({"movie_id": 1, "user_id": 1}, {"unique": true})
ugc.ratings.createIndex({"user_id": 1, "movie_id": 1}, {"unique": true})
