from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import BaseParser

from engines import postgres_engine
from engines.exceptions import QueryError
from engines.shortcuts import db_exists

from chroma.ChromaEngine import ChromaEngine, QueryParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import time

import json

from .docs import (
    get_db_schema_doc, post_db_query_doc,
    put_db_schema_doc
)

@method_decorator(csrf_exempt, name='dispatch')
class ChromaQueryParser(APIView):
    
    def post(self, request):
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'state':
            return self.chroma_state(request)
        else:
            return self.chroma_query(request)
    
    def chroma_query(self, request):
        try:
            data = json.loads(request.body)
            query_text = data.get("code")
            user_id = data.get("user_id")
        except Exception:
            query_text = None

        if not query_text:
            return Response({"error": "Missing query"}, status=400)
        
        print(f"Received query: {query_text}")
        
        try:
            start_time = time.time()
            
            parsed = QueryParser.parse(query_text)
            
            engine = ChromaEngine(user_id)
            
            command = parsed["command"]
            result = {}
            
            if command == "ADD":
                doc_id = parsed.get("doc_id") or f"doc_{int(time.time() * 1000)}"
                engine.add_document(
                    text=parsed["text"],
                    metadata=parsed.get("metadata"),
                    doc_id=doc_id
                )
                result = {"status": "added", "doc_id": doc_id}
            
            elif command == "SEARCH":
                search_results = engine.search(
                    query=parsed["query"],
                    k=parsed["k"],
                    filters=parsed.get("filters")
                )
                result = {"search_results": search_results}
            
            elif command == "GET":
                doc = engine.get_by_id(parsed["doc_id"])
                result = {"document": doc} if doc else {"error": "Document not found"}
            
            elif command == "DELETE":
                doc = engine.get_by_id(parsed["doc_id"])
                if not doc:
                    return Response({"error": "Document not found"})
                else:
                    engine.delete(parsed["doc_id"])
                    result = {"status": "deleted", "doc_id": parsed["doc_id"]}
            
            db_state = engine.get_db_state()
            execution_time = time.time() - start_time
            
            return Response({
                "command": command,
                "result": result,
                "db_state": db_state,
                "execution_time": f"{execution_time:.4f} seconds",
                "documents_count": len(db_state)
            })
        
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def chroma_state(self, request):
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
        except Exception:
            user_id = None
        if not user_id:
            return Response({"error": "Missing user_id"}, status=400)
        
        engine = ChromaEngine(user_id)
        try:
            state = engine.get_db_state()
            return Response({"state": state})
        except Exception as e:
            return Response({"error": "User not found"})
        


class PlainTextParser(BaseParser):
    media_type = 'text/plain'
    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read().decode('utf-8')


class PutView(APIView):
    @put_db_schema_doc
    def put(self, request: Request):
        data = json.loads(request.body)
        db_name = data.get("user_id")

        if db_exists(postgres_engine, db_name):
            postgres_engine.drop_db(db_name)

        dump = """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50),
            email VARCHAR(100)
        );
"""
        postgres_engine.create_db(db_name, dump)

        return Response({"detail": "Database was set up"}, status=214)


class SchemaView(APIView):
    @get_db_schema_doc
    def get(self, request: Request):
        data = json.loads(request.body)
        db_name = data.get("user_id")
        schema = postgres_engine.get_db(db_name)

        return Response(schema.to_json())


class QueryView(APIView):

    parser_classes = [PlainTextParser]

    @post_db_query_doc
    def post(self, request: Request):
        data = json.loads(request.body)
        db_name = data.get("user_id")

        query = request.data
        query = query.strip()
        query = query.replace('\\n', '')
        print("\n\nDATA:", query, "\n\n")
        if not isinstance(query, str):
            return Response({"detail": "Not a plain string query"}, status=400)
        
        try:
            results = postgres_engine.send_query(db_name, query)
        except QueryError as e:
            return Response({"detail": "QueryError: "+str(e)}, status=400)

        schema = postgres_engine.get_db(db_name)

        json_results = [r.to_json() for r in results]
        json_schema = schema.to_json()

        return Response({
            "results": json_results,
            "schema": json_schema
        })
        