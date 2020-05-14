import toml

import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors


with open('./db.toml', 'r') as f:
    database_config = toml.load(f).get('Database')


client = cosmos_client.CosmosClient(database_config.get("ACCOUNT_URI"), {
                                    'masterKey': database_config.get("ACCOUNT_KEY")})


category_container_link = "dbs/Roms/colls/categories"

with open('config.toml', 'r') as f:
    categories = toml.load(f).get("Run").get("categories")

def normalize_cate(cate_id: str) -> str:
    out = cate_id.replace('-', ' ')
    out = out.capitalize()
    return out

names = [normalize_cate(c) for c in categories]

for i in range(len(categories)):
    client.UpsertItem(category_container_link, {
        "id": categories[i],
        "norm": categories[i],
        "title": names[i]
    })