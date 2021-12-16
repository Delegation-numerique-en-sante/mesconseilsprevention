# We should retrieve an entry by default.
GET http://127.0.0.1:8001/SanteFr/Articles.json
HTTP/1.1 200
[Asserts]
jsonpath "$.rows" count == 1

# We should retrieve an entry if age is between 11 and 55.
GET http://127.0.0.1:8001/SanteFr/Articles.json
[QueryStringParams]
Age_max__gte: 39
Age_min__lte: 39
HTTP/1.1 200
[Asserts]
jsonpath "$.rows" count == 1

# We should NOT retrieve any entry if age is below 11.
GET http://127.0.0.1:8001/SanteFr/Articles.json
[QueryStringParams]
Age_max__gte: 10
Age_min__lte: 10
HTTP/1.1 200
[Asserts]
jsonpath "$.rows" count == 0

# We should NOT retrieve any entry if age is above 55.
GET http://127.0.0.1:8001/SanteFr/Articles.json
[QueryStringParams]
Age_max__gte: 56
Age_min__lte: 56
HTTP/1.1 200
[Asserts]
jsonpath "$.rows" count == 0
