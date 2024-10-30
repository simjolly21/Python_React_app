import argparse
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, urljoin
import json

# In-memory cache
cache = {}

class CachingProxyHandler(BaseHTTPRequestHandler):
    origin = None  # Will be set to the origin URL

    def do_GET(self):
        # Parse the request path to forward to the origin
        parsed_path = urlparse(self.path)
        full_url = urljoin(self.origin, parsed_path.path)
        
        # Check if response is cached
        if self.path in cache:
            # Cache hit
            response, headers = cache[self.path]
            self.send_response(200)
            self.send_headers(headers, cache_hit=True)
            self.wfile.write(response)
        else:
            # Cache miss - forward request to origin
            origin_response = requests.get(full_url, headers=self.headers)
            
            # Cache the response
            cache[self.path] = (origin_response.content, origin_response.headers)
            
            # Respond to client
            self.send_response(origin_response.status_code)
            self.send_headers(origin_response.headers, cache_hit=False)
            self.wfile.write(origin_response.content)

    def send_headers(self, headers, cache_hit):
        # Copy headers from origin response and add X-Cache header
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header('X-Cache', 'HIT' if cache_hit else 'MISS')
        self.end_headers()

    @staticmethod
    def clear_cache():
        global cache
        cache.clear()

def run_server(port, origin):
    CachingProxyHandler.origin = origin
    server_address = ('', port)
    httpd = HTTPServer(server_address, CachingProxyHandler)
    print(f"Starting caching proxy server on port {port}, forwarding to {origin}")
    httpd.serve_forever()

def main():
    parser = argparse.ArgumentParser(description="Caching Proxy Server")
    parser.add_argument('--port', type=int, help="Port to run the caching proxy server on")
    parser.add_argument('--origin', type=str, help="Origin server URL")
    parser.add_argument('--clear-cache', action='store_true', help="Clear the cache")
    args = parser.parse_args()

    if args.clear_cache:
        CachingProxyHandler.clear_cache()
        print("Cache cleared successfully.")
    else:
        if not args.port or not args.origin:
            print("Error: Please specify both --port and --origin.")
            return
        run_server(args.port, args.origin)

if __name__ == '__main__':
    main()
