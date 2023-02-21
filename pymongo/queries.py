import pymongo
import pprint
client = pymongo.MongoClient("-insert MongoDB connection string-")
db = client["movies"]
reviews = db["reviews"]
pipeline1 = [
    {"$match":{"rating":{"$ne":"null"}}},
    {"$group":{"_id":"$reviewer", "avg_rating":{"$avg":{"$toInt":"$rating"}}}},
    {"$limit": 10}
]

pipeline2 = [
    {"$match":{"review_date":"/2005$/"}},
    {"$sort":{"rating":-1}},
    {"$limit": 10}
]

pipeline3 = [
    {"$match":{"review_date":"/2005$/"}},
    {"$sort":{"rating":1}},
    {"$limit": 10}
]

pipeline4 = [
    {"$project":{"_id":"$review_id",
        "controversy":
            {"$divide":
                [{"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 1]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}},
                {"$max":
                    [1,
                    {"$abs":
                        {"$subtract":
                            [{"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 0]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}},
                            {"$subtract":
                                [{"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 1]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}},
                                {"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 0]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}}]}]}}]}]},
        "helpful":{"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 0]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}},
        "total":{"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 1]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}}}},
    {"$sort":{"controversy":-1}},
    {"$limit": 10}
]

pipeline5 = [
    {"$project":{"_id":"$review_id",
        "helpful":{"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 0]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}},
        "unhelpful":{"$subtract":
            [{"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 1]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}},
            {"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 0]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}}]},
        "score":{"$subtract":
            [{"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 0]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}},
            {"$subtract":
                [{"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 1]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}},
                {"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 0]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}}]}]}}},
    {"$sort":{"score":-1}},
    {"$limit": 10}
]

pipeline6 = [
    {"$project":{"_id":"$review_id",
        "helpful":{"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 0]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}},
        "unhelpful":{"$subtract":
            [{"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 1]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}},
            {"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 0]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}}]},
        "score":{"$subtract":
            [{"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 0]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}},
            {"$subtract":
                [{"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 1]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}},
                {"$toInt":{"$reduce":{"input":{"$split":[{"$arrayElemAt":["$helpful", 0]},',']},"initialValue":'',"in":{"$concat":['$$value','$$this']}}}}]}]}}},
    {"$sort":{"score":1}},
    {"$limit": 10}
]

reviewer_avg = list(reviews.aggregate(pipeline1))
highest_rated = reviews.find({"movie":{"$regex":"2005"}}).sort({"rating":1}).limit(10)
lowest_rated = reviews.find({"movie":{"$regex":"2005"}}).sort({"rating":-1}).limit(10)
highest_rated = list(reviews.aggregate(pipeline2))
lowest_rated = list(reviews.aggregate(pipeline3))
most_controversial = list(reviews.aggregate(pipeline4))
most_helpful = list(reviews.aggregate(pipeline5))
least_helpful = list(reviews.aggregate(pipeline6))

pprint.pprint(most_controversial)
pprint.pprint(most_helpful)
pprint.pprint(least_helpful)
