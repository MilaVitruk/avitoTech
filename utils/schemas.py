"""Здесь находятся JSON-схемы для валидации структуры ответов"""
schema_item = {"type": "array",
               "minItems": 1,
               "items": {
                   "type": "object",
                   "required": ["id", "name", "price", "sellerId", "statistics"],
                   "properties": {
                       "id": {"type": "string"},
                       "name": {"type": "string"},
                       "price": {"type": "integer"},
                       "sellerId": {"type": "integer"},
                       "statistics": {"type": "object",
                                      "required": ["contacts", "likes", "viewCount"],
                                      "properties": {"contacts": {"type": "integer"},
                                                     "likes": {"type": "integer"},
                                                     "viewCount": {"type": "integer"}

                                                     }},
                   }
               }}
schema_BAD_get_response = {
    "type": "object",
    "required": ["result", "status"],
    "properties": {
        "result": {"type": "object",
                   "properties": {"message": {"type": "string"},
                                  "messages": {"type": "object", "properties": {}}},
                   "status": {"type": "string"}}},
    "status": {"type": "string"},
}

schemas = {'get_by_id_OK': schema_item,
           'get_by_id_BAD': schema_BAD_get_response,
           'post_OK': {
               "type": "object",
               "required": ["status"],
               "properties": {
                   "status": {"type": "string"}
               }
           },
           'post_statistic': {
               "type": "object",
               "required": ["contacts", "likes", "viewCount"],
               "properties": {
                   "contacts": {"type": "integer", "const": 0},
                   "likes": {"type": "integer", "const": 0},
                   "viewCount": {"type": "integer", "const": 0}
               }
           },
           'post_BAD': {
               "type": "object",
               # "required": ["result", "status"],
               "properties": {
                   "result": {"type": "object",
                              "properties": {
                                  "messages": {"type": "object",
                                               },
                                  "message": {"type": "string"},
                              }},
                   "status": {"type": "string"}
               }

           },
           'get_statistics_by_id_OK': {"type": "array",
                                       "minItems": 1,
                                       "items": {"type": "object",
                                                 "required": ["contacts", "likes", "viewCount"],
                                                 "properties": {"contacts": {"type": "integer"},
                                                                "likes": {"type": "integer"},
                                                                "viewCount": {"type": "integer"}

                                                                }
                                                 }

                                       },
           'get_statistics_by_id_BAD': schema_BAD_get_response,
           'get_items_by_sellers_id_OK': schema_item,
           'get_items_by_sellers_id_BAD': schema_BAD_get_response,
           }
