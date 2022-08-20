import json
import socketserver
from quik import FileLoader
from http.server import BaseHTTPRequestHandler
import threading
from datetime import datetime

from experiment import Experiment
from config import DATABASE, EXPERIMENT
from repository import Repository


experiment = None


class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.dbconn = Repository()
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/temps":
            self.send_temperatures()
        elif self.path == "/experiments":
            self.send_experiments()
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

    def send_experiments(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        experiments = self.dbconn.read_test_db()  # Read from database
        self.wfile.write(bytes(json.dumps(experiments), "utf-8"))

    def do_POST(self):
        global experiment

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

        if "start_process" in map:
            if experiment is None:
                # Add experiment to database
                self.dbconn.start_test_db(EXPERIMENT[map["sel1"]].cycles, map["sel1"])
                experiment = Experiment(EXPERIMENT[map["sel1"]])
                experiment.start()
            else:
                print("An experiment is already running")
        elif "stop_process" in map:
            if experiment is not None:
                # Stop experiment in database
                self.dbconn.end_test_db(True)
                experiment.stop()
                experiment = None

        self.send_response(200)
        self.end_headers()

        with open("home.html") as f:
            self.wfile.write(bytes(f.read(), "utf-8"))
