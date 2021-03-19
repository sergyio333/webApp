def sqlExe(query, conn=None, multiple=True):
    """ The method is used to query data from the database

    @param: query (SQLAlchemy query object - [delete, insert, update])
    @param: conn[optional] (Connection object to the database)
    @param: multiple[optional] (If we wan't a single record we call the method with multiple=False)

    @result: either a List<Dict> or a single <Dict>
    """

    if not conn:
        from sqlalchemy import create_engine
        from .config import DB_URI
        conn = create_engine(DB_URI)

    result = list(map(lambda x: dict(x.items()), conn.execute(query)))
    return result if multiple else result[0]

def sqlAction(query, conn=None):
    """The method is used to modify data in the database

    @param: query (SQLAlchemy query object - [delete, insert, update])
    @param: conn[optional] (Connection object to the database)

    @result: void type method
    """

    if not conn:
        from sqlalchemy import create_engine
        from .config import DB_URI
        conn = create_engine(DB_URI)

    result = conn.execute(query)

def validateFields(data_recived, required_fields):
    """The method is used to validate fields recived from the frontend

    @param: data_recived (dictionary object we recived from the frontend)
    @param: required_fields (list of fields which are required)

    @result: boolean [True => fields are valid | False => some fields are missing]
    """

    # data is valid if all fields in required are also in the recived
    return not len(set(required_fields) - set(data_recived.keys()))