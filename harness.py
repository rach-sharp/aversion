import aversion


def run(test_cases):
    print("running test cases")

    funcs = aversion.VERSION_REPO
    successes = 0
    failures = 0

    for func_name in test_cases:
        print(f"- {func_name}")
        old_runs = []
        for version in test_cases[func_name]:
            print(f"-- {version}")
            runs = test_cases[func_name][version]
            for run in runs:
                print(f"--- {run}")
                result = funcs[func_name][version](*run.args, **run.kwargs)
                same = result == run.result
                print(f"{result} == {run.result}, {'passed' if same else 'failed'}")
                if same:
                    successes += 1
                else:
                    failures += 1


    print(f"successes : {successes}")
    print(f"failures  : {failures}")

