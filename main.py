import datetime
import json
import os.path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

hostName = 'localhost'
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """Класс веб-сервер"""

    @staticmethod
    def __get_html_content() -> str:
        """Метод возвращает HTML-страницу с формой обратной связи."""
        path = os.path.join('./templates', 'contacts.html')
        with open(path, 'r', encoding='UTF-8') as file:
            return file.read()

    def do_GET(self):
        """При GET запросе на сервер выводит в терминале данные от пользователя и генерирует HTML-страницу
        с формой обратной связи."""
        query_components = parse_qs(urlparse(self.path).query)
        print(query_components)
        page_content = self.__get_html_content()
        self.send_response(200)
        self.send_header("Content_type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page_content, "UTF-8"))

    def do_POST(self):
        """При POST запросе на сервер выводит в терминале дату запроса."""
        date_now = datetime.datetime.now()
        date = datetime.datetime.strftime(date_now, '%Y-%m-%d %H:%M')
        self.send_response(200)
        self.send_header("Content_type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(date), "UTF-8"))


if __name__ == '__main__':
    server = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server is running ... http://{hostName}:{serverPort}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
