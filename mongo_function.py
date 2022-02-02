def insert_document(collection, data_):
    """INSERT"""
    return collection.insert_one(data_).inserted_id


def find_document(collection, elements, multiple=False):
    """SELECT"""
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)


def update_document(collection, query_elements, new_values):
    """UPDATE"""
    collection.update_one(query_elements, {'$set': new_values})


def delete_document(collection, query, multiple=False):
    """DELETE"""
    if multiple:
        collection.delete_many(query)
    else:
        collection.delete_one(query)


if __name__ == "__main__":
    from bd import next_collection
    data = {'_id': "vk_id_123456", "name": "Nik", "age": 23}
    id_ = insert_document(next_collection, data)
    print(id_)
    print(find_document(next_collection, {'_id': "vk_id_123456"}, multiple=True))
    update_document(next_collection, {'_id': "vk_id_123456"}, {"age": 33})
    print(find_document(next_collection, {'_id': "vk_id_123456"}, multiple=True))
    delete_document(next_collection, {'_id': "vk_id_123456"}, multiple=True)
    print(find_document(next_collection, {'_id': "vk_id_123456"}, multiple=True))
