*** Settings ***
Library    OperatingSystem
Library    Process
Library    BuiltIn

*** Variables ***
${UE_COUNT}            5
${SIMULATOR_COUNT}     2
${SYSTEM_FRAME_NUMBER} '000001'
${SUB_CARRIER_SPACING} 'scs30or120'
${SSB_OFFSET}          1
${DMRS_POSITION}       'pos1'
${PDCCH_CONFIG}        1
${CELL_BARRED}         'barred'
${INTRA_FREQ}          'notAllowed'
${SPARE}               1

*** Test Cases ***
Verify Custom MIB Reception
    [Documentation]    Test custom MIB reception from DUT RAN to UE simulators.
    Start Custom Call Flow
    Log    Verification of MIB reception completed.

*** Keywords ***
Start Custom Call Flow
    Log    Starting custom test for call flow: custom
    Log    Test will exit in 10 seconds.
    ${result}    Run Process    python    run_tests.py    --call_flow    custom    --systemFrameNumber    ${SYSTEM_FRAME_NUMBER}    --subCarrierSpacingCommon    ${SUB_CARRIER_SPACING}    --ssb_SubcarrierOffset    ${SSB_OFFSET}    --dmrs_TypeA_Position    ${DMRS_POSITION}    --pdcch_ConfigSIB1    ${PDCCH_CONFIG}    --cellBarred    ${CELL_BARRED}    --intraFreqReselection    ${INTRA_FREQ}    --spare    ${SPARE}    stdout=results/output.log    stderr=results/error.log
    Should Be True    ${result.rc} == 0
    Log Many     ${result.stdout.splitlines()}
    Log Many     ${result.stderr.splitlines()}
    Log    Test execution completed.
    Log    Robot Framework report generated.
    Log    ${result.stdout}
    Log    ${result.stderr}
    Log    Robot Framework report generation completed.