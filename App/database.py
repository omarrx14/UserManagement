from neo4j import GraphDatabase, basic_auth
# from neo4j import GraphDatabase


class Neo4jConnection:
    def __init__(self, uri: str, user: str, password: str):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def query(self, query: str, parameters: dict = None):
        with self._driver.session() as session:
            return session.run(query, parameters)


driver = GraphDatabase.driver(
    "neo4j://54.172.132.64:7687",
    auth=basic_auth("neo4j", "azimuths-bundle-wartime"))

cypher_query = '''
MATCH (a:Airport{iata:$iata})-[r:HAS_ROUTE]->(other)
  RETURN other.iata as destination
'''

with driver.session(database="neo4j") as session:
    results = session.read_transaction(
        lambda tx: tx.run(cypher_query,
                          iata="DEN").data())
    for record in results:
        print(record['destination'])

driver.close()
