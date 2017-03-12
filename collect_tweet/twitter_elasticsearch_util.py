from elasticsearch import Elasticsearch


def creat_mapping(elastic_host, index='tweet', doc_type='tweet_data'):
    esclient = Elasticsearch([{'host': elastic_host, 'port': 80}])
    esclient.indices.delete(index=index)
    esclient.indices.create(index=index, ignore=400)
    mapping = {
        "properties": {
            "user_name": {
                "type": "string"
            },
            "timestamp": {
                "type": "string"
            },
            "text": {
                "type": "string"
            },
            "location": {
                "type": "geo_point"
            }
        }
    }

    response = esclient.indices.put_mapping(index=index, doc_type=doc_type, body=mapping)
    return response["acknowledged"]


def upload(elastic_host, json_data, index='tweet', doc_type='tweet_data'):
    """
    :param elastic_host: the host name of your Elasticsearch

    :param json_data: the ready-to-upload data

    :param index: the index of your data

    :param doc_type: document type of your data

    :return: True for success
    """

    esclient = Elasticsearch([{'host': elastic_host, 'port': 80}])
    response = esclient.index(index=index,
                              doc_type=doc_type,
                              body=json_data)
    if response["created"] == "True":
        return True
    return False


def search(elastic_host, key_word=None, index='tweet', doc_type='tweet_data'):
    """
    :param elastic_host: the host name of your Elasticsearch

    :param key_word: what feature of ready-to-delete data that contains

    :param index: the index of your data

    :param doc_type: document type of your data

    :return: the search result, presenting in json
    """

    esclient = Elasticsearch([{'host': elastic_host, 'port': 80}])
    response = esclient.search(index=index,
                               doc_type=doc_type,
                               body={"query": {"match": {"text": key_word}}})
    # print("Got %d Hits:" % response['hits']['total'])
    result = []
    for hit in response['hits']['hits']:
        # print("%(location)s \n%(timestamp)s \n%(user_name)s \n%(text)s\n" % hit["_source"])
        result.append(hit["_source"])
    output = {"result": result}

    return output


def clear(elastic_host, key_word=None, index='tweet', doc_type='tweet_data'):
    """
    :param elastic_host: the host name of your Elasticsearch

    :param key_word: what feature of ready-to-delete data that contains

    :param index: the index of your data

    :param doc_type: document type of your data

    :return: the numbers that deleted
    """
    esclient = Elasticsearch([{'host': elastic_host, 'port': 80}])

    if key_word is None:
        query = {"match_all": {}}
    else:
        query = {"match": {"text": key_word}}

    response = esclient.delete_by_query(index=index,
                                        doc_type='tweet_data',
                                        body={"query": query})
    return response["deleted"]


def location_search(elastic_host, location, radius=10, index="tweet", doc_type="tweet_data"):
    esclient = Elasticsearch([{'host': elastic_host, 'port': 80}])
    query = {
        "bool": {
            "filter": {
                "geo_distance": {
                    "distance": (str(radius)+"km"),
                    "location": location
                }
            }
        }
    }
    print(query)
    response = esclient.search(index=index,
                               doc_type=doc_type,
                               body={"query": query})
    print("Got %d Hits:" % response['hits']['total'])
    result = []
    for hit in response['hits']['hits']:
        print("%(location)s \n%(timestamp)s \n%(user_name)s \n%(text)s\n" % hit["_source"])
        result.append(hit["_source"])
    output = {"result": result}

    return output

    # elastic_host = "search-twittmap-wf-tos22nd6jgkyhdhvbptnb4pv7a.us-east-1.es.amazonaws.com"
