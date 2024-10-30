# Caching Proxy

This is the project link: https://roadmap.sh/projects/caching-server

## Running the Server

- Start the server:

        python caching_proxy.py --port 3000 --origin http://dummyjson.com
- Clear the cache:

        python chching_proxy.py --clear-cache

This script provides a basic caching proxy server with cache clearing functionality. For production-grade performance, further enhancements like using a more advanced cache backend (e.g., Redis) and handling additional HTTP methods might be added.
