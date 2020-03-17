import time
import schedule
from urban_dict.status_updater import StatusUpdater


def run(status_updater: StatusUpdater):
    status_updater.make_status()


if __name__ == "__main__":
    su = StatusUpdater()

    schedule.every().day.at("20:00").do(run, su)
    while True:
        schedule.run_pending()
        time.sleep(1)
