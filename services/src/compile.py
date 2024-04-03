import json
import subprocess
import solcx
import os, string, random
from src.prompts import SOLIDITY_VERSION_LATEST_SUPPORTED

from slither.slither import Slither

# download set compiler version 
solcx.install_solc(SOLIDITY_VERSION_LATEST_SUPPORTED)
solcx.set_solc_version(SOLIDITY_VERSION_LATEST_SUPPORTED)

detectors_json = './src/utils/detectors.json'
with open(detectors_json, 'r') as f:
    detectors = json.load(f)

def _generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def run(generated_contract):
    """Perfoms solidity compilation on LLM generated contracts. Returns `True` if no error occured during the compilation process, `False` otherwise"""
    try: 
        _ = solcx.compile_source(generated_contract, output_values=["abi", "bin-runtime"], solc_version="0.8.20")
        return slither(generated_contract)
    except Exception as ex:
        _parse_exeption()
        print('exeption when compiling', ex)
        return False


def _parse_exeption():
    pass

def slither(generated_contract):
    temp_file = 'temp' + _generate_random_string(10) + '.sol'
    try:
        with open(temp_file, 'w+') as fhd:
            fhd.write(generated_contract)
            fhd.close()

        sl_result = _slither_sol_file(temp_file)
        print('Slither codes', sl_result)
        return False if _has_error_or_warning(sl_result) else True

    except:
        return False
    finally:
        os.remove(temp_file)


def _slither_sol_file(file_name):
    p = subprocess.run(['slither', file_name, "--exclude-low", "--exclude-informational", "--exclude-dependencies", "--exclude-optimization", "--json", "-"], capture_output=True, universal_newlines=True)
    if p.stdout == '':
        return None
    else:
        output = json.loads(p.stdout)
        return _get_slither_check_from_json(output)

def _get_slither_check_from_json(slither_result):
    if slither_result.get('results').get('detectors') is None:
        return None
    else: 
        return [[detectors.get(d.get('check'))['idx'], detectors.get(d.get('check'))['impact']] for d in slither_result.get('results').get('detectors')]

def _has_error_or_warning(idx_impact_pair):
    if idx_impact_pair is None:
        return False
    
    for idx, level in idx_impact_pair:
        if level == 'High' or level == 'Medium' or level == 'Low' or level == 'Informational' or level == 'Optimization':
            return True
        else:
            raise False