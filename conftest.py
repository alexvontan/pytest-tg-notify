import pytest
import json
from filelock import FileLock
from lib.bot import Bot
from lib.config import Config


@pytest.fixture(scope='session', autouse=True)
def setup(request, session_data):
    """
    fixture for getting configure
    :param session_data: fixture for collecting tests results
    :param request: internal pytest fixture
    """
    request.session.conf = Config()


@pytest.fixture(scope="session")
def session_data(tmp_path_factory, worker_id, request):
    """
    fixture for collecting tests results in multithreading mode (using pytest-xdist)
    :param tmp_path_factory: fixture for accessing the temporary directory and result file for all threads
    :param worker_id: fixture returning thread id
    :param request: internal pytest fixture
    """
    data = {
        "amount": 0,
        "passed": 0,
        "failed": 0,
        "blocked": 0,
        "worker_count": 0
    }
    # waiting for session ending
    yield
    # next code only for multithreading, 'master' worker means that using only one thread
    if worker_id != 'master':
        root_tmp_dir = tmp_path_factory.getbasetemp().parent
        fn = root_tmp_dir / "data.json"
        # use filelock
        with FileLock(str(fn) + ".lock"):
            if fn.is_file():
                with open(fn) as json_file:
                    data = json.load(json_file)
            # updating amount of tests
            data['failed'] += sum(1 for result in request.session.results.values() if result.failed)
            data['passed'] += sum(1 for result in request.session.results.values() if result.passed)
            data['worker_count'] += 1
            fn.write_text(json.dumps(data))
        # check amount of calculated threads is equal to amount of running threads
        if data['worker_count'] == request.config.workerinput["workercount"]:
            # set tests amount and calculate broken tests
            data['amount'] = request.session.testscollected
            data['blocked'] = data['amount'] - data['failed'] - data['passed']
            percent = round((data['passed'] * 100) / data['amount'], 2)
            Bot().send_message(f"Tests amount: {data['amount']}\n"
                               f"Passed: {data['passed']}\n"
                               f"Failed: {data['failed']}\n"
                               f"Blocked: {data['blocked']}\n"
                               f"Result: {percent}%\n")


def pytest_sessionstart(session):
    """
    pytest-xdist hook, used for declare result dict before session start
    """
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest-xdist hook for make report after session end
    """
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        item.session.results[item] = result
