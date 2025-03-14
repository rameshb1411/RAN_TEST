*** Settings ***
Library    OperatingSystem
Library    Process
Library    BuiltIn

*** Variables ***
${UE_COUNT}            5
${SIMULATOR_COUNT}     2

*** Test Cases ***
Verify MIB Reception
    [Documentation]    Test MIB reception from DUT RAN to UE simulators.
    Start Call Flow
    Log    Verification of MIB reception completed.

*** Keywords ***
Start Call Flow
    [Arguments]    ${CALL_FLOW}=mib
    Log    Starting test for call flow: ${CALL_FLOW}
    Log    Test will exit in 10 seconds.
    ${result}      Run Process    python    run_tests.py    --call_flow    ${CALL_FLOW}    stdout=results/output.log    stderr=results/error.log
    Should Be True    ${result.rc} == 0
    Log Many     ${result.stdout.splitlines()}
    Log Many     ${result.stderr.splitlines()}
    Log    Test execution completed.
    Log    Robot Framework report generated.
    Log    ${result.stdout}
    Log    ${result.stderr}
    Log    Robot Framework report generation completed.