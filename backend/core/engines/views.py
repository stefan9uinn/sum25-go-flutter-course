import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from engines.ChromaEngine import ChromaEngine, QueryParser
from engines.PostgresEngine import PostgresEngine
import time
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .exceptions import DBNotExists


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
        
class PostgresQueryParser(APIView):
    
    def post(self, request):
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'state':
            return self.postgres_state(request)
        else:
            return self.postgres_query(request)
    
    def postgres_query(self, request):
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            query_text = data.get("code")
        except Exception:
            user_id = None
            query_text = None
        if not user_id:
            return Response({"error": "Missing user_id"}, status=400)
        
        if not query_text:
            return Response({"error": "Missing query"}, status=400)
        
        print(f"Received query: {query_text}")

        try:
            engine = PostgresEngine(
                root_db="",
                host="localhost",
                port=5432,
                user=config("POSTGRES_USER"),
                password=config("POSTGRES_PASSWORD"),
            )
            start_time = time.time()

            try:
                engine.get_db(user_id)
                result = engine.send_query(user_id, query_text)
                stop_time = time.time()
            except DBNotExists as e:
                result = engine.create_db(user_id, query_text)
                stop_time = time.time()
            execution_time = stop_time - start_time
            return Response({
                "user_id": user_id,
                "result": result,
                "execution_time": f"{execution_time:.4f} seconds"
            })
        except Exception as e:
            return Response({"error": str(e)}, status=400)


    def postgres_state(self, request):
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
        except Exception:
            user_id = None
        if not user_id:
            return Response({"error": "Missing user_id"}, status=400)
        engine = PostgresEngine(
            root_db="",
            host="localhost",
            port=5432,
            user=config("POSTGRES_USER"),
            password=config("POSTGRES_PASSWORD"),
        )

        try:
            state = engine.get_db_state(user_id)
            return Response({"state": state})
        except DBNotExists as e:
            return Response({"error": "Empty DB"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)

