for (var i = 0; i < 5; i++) {
db.duplicates.insert(
    db.runCommand({ 
            aggregate: "record",
            pipeline: [
                        { $group: { 
                            _id: { "polnoe-naimenovanie": "$polnoe-naimenovanie", papka: "$papka", "yuridicheskij-adres": "$yuridicheskij-adres", "okved": "$okved" }, 
                            uniqueIds: { $addToSet: "$_id" },
                            count: { $sum: 1 } 
                        }},
                        { $match: { count: { $gt: 1 }} },
                        { $limit : 5000 }
                    ],
            allowDiskUse: true
        }
    )["result"]
);

db.duplicates2.insert(db.duplicates.find({}, {"uniqueIds": 1, "_id": 0}).toArray());
db.duplicates3.insert(db.duplicates2.find({}, {"uniqueIds": { $slice: [ 1, 20 ]}}).toArray());
db.duplicates4.insert(db.duplicates3.distinct("uniqueIds"));

var ids = db.duplicates4.distinct("str");
ids = ids.map(function(id) { return ObjectId(id); });
db.record.remove({_id: {$in: ids}});

db.duplicates.drop();
db.duplicates2.drop();
db.duplicates3.drop();
db.duplicates4.drop();
db.record.count();
}
