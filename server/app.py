import os
from flask import Flask, request, jsonify, make_response
from azure.cosmos import cosmos_client, PartitionKey 


COSMOSDB_ACCOUNT_URI = os.environ.get("COSMOSDB_ACCOUNT_URI")
COSMOSDB_ACCOUNT_KEY = os.environ.get("COSMOSDB_ACCOUNT_KEY")
COSMOSDB_DATABASE_ID = os.environ.get("COSMOSDB_DATABASE_ID")

client = cosmos_client.CosmosClient(COSMOSDB_ACCOUNT_URI, {
                                    'masterKey': COSMOSDB_ACCOUNT_KEY })

app = Flask(__name__)


categories_container_id = "categories"
roms_container_id = "roms"
regions_container_id = "regions"

database = client.create_database_if_not_exists(COSMOSDB_DATABASE_ID)
categories_container = database.create_container_if_not_exists(
    id=categories_container_id,
    partition_key=PartitionKey(path="/category"),
    offer_throughput=400
)

roms_container = database.create_container_if_not_exists(
    id=roms_container_id,
    partition_key=PartitionKey(path="/roms"),
    offer_throughput=400
)

regions_container = database.create_container_if_not_exists(
    id=regions_container_id,
    partition_key=PartitionKey(path="/regions"),
    offer_throughput=200
)

@app.get('/categories')
def list_categories(offset = 0, limit = 100):
    query = "select * from c offset {} limit {}".format(offset, limit)
    categories = categories_container.query_items(query, enable_cross_partition_query=True)
    out = list(categories)
    return jsonify(data=out)


@app.route('/regions')
def list_regions(offset = 0, limit = 100):
    query = "select * from c offset {} limit {}".format(offset, limit)
    regions = regions_container.query_items(query, enable_cross_partition_query=True)
    out = list(regions)
    return jsonify(data=out)


@app.get('/roms')
def search_roms():
    category = request.args.get("category")
    region = request.args.get("region")
    keyword = request.args.get("keyword")
    offset = request.args.get("offset", 0)
    limit = request.args.get("limit", 100)
    
    query = "select * from c"
    query_params = []
    if category is not None:
        query_params.append("c.category = '{}'".format(category))
    if region is not None:
        query_params.append("c.region = '{}'".format(region))
    if keyword is not None:
        query_params.append("contains(c.title, '{}')".format(keyword))
    if len(query_params) > 0:
        query += " where " + " and ".join(query_params)
    query += " offset {} limit {}".format(offset, limit)
    
    roms = roms_container.query_items(query, enable_cross_partition_query=True)
    out = list(roms)
    return jsonify(data=out)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(error="Not found"), 404)


@app.errorhandler(500)
def server_error(error):
    return make_response(jsonify(error="Internal server error"), 500)


app.run(host='0.0.0.0', port=2020, debug=True)