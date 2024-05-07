"""
Workaround for _id fields of MongoDB documents to work with pydantic.
"""

def convert_doc(document) -> dict:
	return {
		"id": str(document["_id"]),
        **document
	}

def convert_doc_list(doc_list) -> list:
	return [
        convert_doc(doc) for doc in doc_list
    ]