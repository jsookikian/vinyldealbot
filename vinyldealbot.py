from bot import *
from daemon import runner

class VinylDealBot:
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/var/run/vinyldealbot/vinyldealbot.pid'
        self.pidfile_timeout = 5

    def run(self):
        conn = sqlite3.connect('alerts.db')
        c = conn.cursor()
        logging.basicConfig(filename="vinylbot.log", level=logging.INFO, format="%(asctime)s - %(message)s")
        logging.info("Launching VinylDealBot...")
        reddit = praw.Reddit('VinylDealBot')
        subreddit = reddit.subreddit("vinyldeals")

        while True:
            logging.info("Reading posts")
            readPosts(conn, c, reddit, subreddit)
            logging.info("Checking alerts")
            alert(conn, c, reddit, subreddit)

vinyldealbot = VinylDealBot()
daemon_runner = runner.DaemonRunner(vinyldealbot)
daemon_runner.do_action()
