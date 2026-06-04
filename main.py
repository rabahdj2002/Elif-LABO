import functions_framework
from src.elif_v0_1.serverless_handler import handle_step_request as engine_handler

@functions_framework.http
def handle_step_request(request):
    """
    HTTP Cloud Function entry point for ELIF Engine.
    Passes the JSON payload to the engine's serverless handler.
    """
    request_json = request.get_json(silent=True)
    if not request_json:
        return {"error": "No JSON payload provided"}, 400
    
    try:
        # The engine_handler expects the dict payload directly
        result = engine_handler(request_json)
        return result
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }, 500
