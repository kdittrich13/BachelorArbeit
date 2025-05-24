import subprocess
import time

# Executes flashlight with the given parameters
def run_flashlight(maestro_file_name, bundleId, duration, result_file_name, count):
    result = subprocess.run([
        "flashlight", "test",
        "--testCommand", f"maestro test -e appId={bundleId} {maestro_file_name}",
        "--bundleId", f"{bundleId}",
        "--iterationCount", f"{count}",
        "--duration", f"{duration}",
        "--resultsFilePath", f"{result_file_name}"
    ])
    print(result.args)

# Runs a complete benchmark for the given device and frameworks using the given tests 
def run_benchmark(device, tests, frameworks):
    timestamp = time.strftime("%d_%m_%y_%H_%M")

    for test in tests:
        print(f"Executing test : '{test}' with file '{tests[test]}'")
        for framework in frameworks:
            outputPath = f"tests/devices/{device}/{test}/{framework}_{timestamp}_results.json"
            print(f"Executing for framework : '{framework}' with appID: '{frameworks[framework]}'")
            run_flashlight(
                tests[test],            # Which test file to run
                frameworks[framework],  # The application ID to run the test with
                "32000",                # The duration of the measurement interval in milliseconds
                outputPath,             # The path to the report output file
                10                      # How many iterations of the test to run
            )

if __name__ == '__main__':
    # List of devices to test. Only one hardoded value will be used per run.
    devices = [
        'pixel7',
        'op2',
        'pixel6pro'
    ]

    # The names of the tests and the paths to the associated test files
    tests = {
        'list': 'tests/maestro_test_list.yaml',
        'animation': 'tests/maestro_test_animation.yaml'
    }

    # The names of the frameworks to benchmark and the associated application IDs
    frameworks = {
        'native': 'com.nativeandroid.benchmark',
        'flutter': 'com.flutter.benchmark.flutter_benchmark_app',
        'react_native': 'com.anonymous.react_native_benchmark_app',
        'kmp': 'org.kmp.benchmark'
    }

    # The device to test this run
    device = devices[0]

    print(f"Running benchmark for device: {device}")
    run_benchmark(device, tests, frameworks)