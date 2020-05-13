import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import toml

with open('./db.toml', 'r') as f:
    database_config = toml.load(f).get('Database')

client = cosmos_client.CosmosClient(database_config.get("ACCOUNT_URI"), {
                            'masterKey': database_config.get("ACCOUNT_KEY")})
database_id = "Roms"
roms_container_id = "roms"
container_path = "dbs/" + database_id + "/colls/" + roms_container_id

client.UpsertItem(container_path, {
    "title": "a"
})
