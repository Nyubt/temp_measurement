import json
import socketserver
from quik import FileLoader
from http.server import BaseHTTPRequestHandler
import threading
from datetime import datetime

from experiment import Experiment
from config import DATABASE, EXPERIMENT
from repository import Repository


class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.dbconn = Repository()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == "/temps":
            self.send_temperatures()
        else:
            self.send_html_page()

    def send_html_page(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        loader = FileLoader(".")
        template = loader.load_template("home.html")
        temps = self.dbconn.read_temp_db()
        s = template.render({"temps": json.dumps(temps)}, loader=loader).encode("utf-8")
        self.wfile.write(s)

    def send_temperatures(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        # Add human-readable datetime representation
        temps = [
            list(t) + [datetime.fromtimestamp(t[3]).strftime("%c")]
            for t in self.dbconn.read_temp_db()
        ]
        self.wfile.write(bytes(json.dumps(temps), "utf-8"))

    def do_POST(self):
        # Porneste ciclul de temperatura
        # intr-un thread nou
        # Porneste frigiderul
        # Citeste temperatura pina nu ajunge la nivelul stabilit
        # Opreste frigiderul
        print("Got request")
        content_length = int(self.headers["Content-Length"])
        print(self.headers)
        params = self.rfile.read(content_length).decode("utf-8")

        map = {}
        for keyval in params.split("&"):
            key, val = keyval.split("=")
            map[key] = val
        print(map)

        x = Experiment(EXPERIMENT["1"])
        x.start()

        self.send_response(200)
        self.end_headers()

        with open("home.html") as f:
            self.wfile.write(bytes(f.read(), "utf-8"))
