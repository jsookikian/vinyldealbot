from bot import *
from daemon import runner
import os
import praw
class VinylDealBot:
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/var/run/vinyldealbot/vinyldealbot.pid'
        self.pidfile_timeout = 5
        self.reddit = praw.Reddit('VinylDealBot')

    def run(self):
        try:
            print(os.path.dirname(os.path.realpath(__file__)))
            conn = sqlite3.connect('alerts.db')
            c = conn.cursor()
            logging.basicConfig(filename="vinylbot.log", level=logging.INFO, format="%(asctime)s - %(message)s")
            logging.info("Launching VinylDealBot...")
            subreddit = self.reddit.subreddit("vinyldeals")

            while True:
                logging.info("Reading posts")
                readPosts(conn, c, self.reddit, subreddit)
                logging.info("Checking alerts")
                alert(conn, c, self.reddit, subreddit)
        except Exception as e:
            logging.info("Error: " + str(e))


vinyldealbot = VinylDealBot()
vinyldealbot.run()
daemon_runner = runner.DaemonRunner(vinyldealbot)
daemon_runner.do_action()
