import subprocess
import logging as log
import Logging


def runCmd(command):
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    while True:
        output = process.stdout.readline()
        log.debug(output.strip())
        print(output.strip())
        return_code = process.poll()
        if return_code is not None:
            # print('RETURN CODE', return_code)
            # Process has finished, read rest of output.
            for output in process.stdout.readlines():
                log.debug(output.strip())
                print(output.strip())
            break

    # TODO: Need to split into to functions:
    # 1) Perform command line without return value.
    # 2) Perform command line with return value.
    return output.strip()
