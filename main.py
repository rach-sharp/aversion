import pickle
import sys

import aversion
import harness


if __name__ == "__main__":

    with open("test_runs", "rb") as test_runs_file:
        TEST_RUNS = pickle.load(test_runs_file)

    if sys.argv[1] == "harness":
        harness.run(TEST_RUNS)
    else:
        print(aversion.VERSION_REPO)
        aversion.number_cruncher(2, 3)

        with open("test_runs", "wb") as pickle_file:
            pickle.dump(aversion.TEST_RUNS, pickle_file)
