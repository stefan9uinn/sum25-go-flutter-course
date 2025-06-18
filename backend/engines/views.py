from django.http import JsonResponse
from ChromaEngine import ChromaEngine, QueryParser
import time

def handle_query(request):
    user_id = 1
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)
    
    query_text = request.POST.get("code")
    if not query_text:
        return JsonResponse({"error": "Missing query"}, status=400)
    
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
            engine.delete(parsed["doc_id"])
            result = {"status": "deleted", "doc_id": parsed["doc_id"]}
        
        db_state = engine.get_db_state()
        execution_time = time.time() - start_time
        
        return JsonResponse({
            "command": command,
            "result": result,
            "db_state": db_state,
            "execution_time": f"{execution_time:.4f} seconds",
            "documents_count": len(db_state)
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)