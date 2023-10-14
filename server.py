from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from api.user_routes import get_user, create_user, update_user, delete_user
from api.product_routes import get_product, create_product, update_product, delete_product
from api.order_routes import get_order, create_order, update_order, delete_order
from api.order_details_routes import get_order_detail, create_order_detail, update_order_detail, delete_order_detail


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_elements = parsed_path.path.split('/')

        try:
            if path_elements[1] == "users":
                user_id = path_elements[2]
                response_content = get_user(user_id)

            elif path_elements[1] == "products":
                product_id = path_elements[2]
                response_content = get_product(product_id)

            elif path_elements[1] == "orders":
                order_id = path_elements[2]
                response_content = get_order(order_id)

            elif path_elements[1] == "orderdetails":
                order_detail_id = path_elements[2]
                response_content = get_order_detail(order_detail_id)

            else:
                response_content = {"message": "Resource not found"}

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_content).encode())

        except Exception as e:
            self.send_error(500, str(e))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        parsed_path = urlparse(self.path)
        path_elements = parsed_path.path.split('/')

        try:
            if path_elements[1] == "users":
                response_content = create_user(data)

            elif path_elements[1] == "products":
                response_content = create_product(data)

            elif path_elements[1] == "orders":
                response_content = create_order(data)

            elif path_elements[1] == "orderdetails":
                response_content = create_order_detail(data)

            else:
                response_content = {"message": "Resource not found"}

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_content).encode())

        except Exception as e:
            self.send_error(500, str(e))

    # Additional methods like do_PUT and do_DELETE can be added similarly...


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    print("Server started at http://localhost:8000")
    httpd.serve_forever()
