import pathlib
_filePath = pathlib.Path(__file__).parent.resolve()

# various timeouts
sleepTime = 1
loadTime = 3
timeout = 60

# full path to chromedriver
chromedriver_path = str(_filePath)+"/../../dependencies/chromedriver"

# flag if chrome should be run with or without UI
# This is nifty for debugging
headless_chrome = False
