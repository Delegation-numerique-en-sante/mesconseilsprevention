# We should retrieve 100 entries by default (automatic pagination).
GET http://127.0.0.1:8001/SanteFr/Articles.json
HTTP/1.1 200
[Asserts]
jsonpath "$.rows" count == 100

# We should retrieve entries if age is 39.
GET http://127.0.0.1:8001/SanteFr/Articles.json
[QueryStringParams]
Age_max__gte: 39
Age_min__lte: 39
HTTP/1.1 200
[Asserts]
jsonpath "$.rows" count == 89

# We should retrieve entries if age is 11.
GET http://127.0.0.1:8001/SanteFr/Articles.json
[QueryStringParams]
Age_max__gte: 10
Age_min__lte: 10
HTTP/1.1 200
[Asserts]
jsonpath "$.rows" count == 36

# We should retrieve entries if age is above 65.
GET http://127.0.0.1:8001/SanteFr/Articles.json
[QueryStringParams]
Age_max__gte: 66
Age_min__lte: 66
HTTP/1.1 200
[Asserts]
jsonpath "$.rows" count == 54
