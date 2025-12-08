from fastapi import FastAPI, Request, Response
import httpx
import re

app = FastAPI()

# Target: Juice Shop Internal URL
TARGET_SERVICE = "http://target-app:3000"

def scrub_data(content: str) -> str:
    """Scans response body for sensitive info and redacts it"""
    if not content: return content
    
    # 1. Redact Credit Card Numbers (Matches 16 digits)
    content = re.sub(r'\b(?:\d{4}[ -]?){3}\d{4}\b', '[REDACTED_CREDIT_CARD]', content)
    
    # 2. Redact Emails (Simple regex)
    # Only redacted if it looks like a real email to avoid breaking UI assets
    content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED_EMAIL]', content)
    
    # 3. Redact Passwords in JSON (e.g. "password": "123")
    content = re.sub(r'"password"\s*:\s*"[^"]+"', '"password": "[REDACTED_SECRET]"', content)
    
    return content

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def proxy(path: str, request: Request):
    client = httpx.AsyncClient(base_url=TARGET_SERVICE)
    
    url = f"/{path}"
    if request.query_params:
        url += f"?{request.query_params}"

    # Forward headers but remove Host to avoid confusion
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None) # Let httpx recalculate this

    try:
        # 1. Forward Request
        body = await request.body()
        
        rp_req = client.build_request(
            request.method,
            url,
            headers=headers,
            content=body,
            cookies=request.cookies
        )
        
        rp_resp = await client.send(rp_req)
        
        # 2. Intercept & Scrub Response
        content_type = rp_resp.headers.get("content-type", "")
        
        # Only scrub text/json/html
        if "application/json" in content_type or "text/html" in content_type:
            original_text = rp_resp.text
            scrubbed_text = scrub_data(original_text)
            final_content = scrubbed_text.encode("utf-8")
        else:
            final_content = rp_resp.content

        # 3. Return Response
        return Response(
            content=final_content,
            status_code=rp_resp.status_code,
            # Copy headers but filter out hop-by-hop headers
            headers={k: v for k, v in rp_resp.headers.items() 
                     if k.lower() not in ["content-encoding", "content-length", "transfer-encoding"]}
        )

    except Exception as e:
        return Response(content=f"DLP Error: {str(e)}", status_code=500)