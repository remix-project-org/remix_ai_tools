import json, time
import subprocess
import os, string, random
from src.prompts import SOLIDITY_VERSION_LATEST_SUPPORTED



detectors_json = './src/utils/detectors.json'
with open(detectors_json, 'r') as f:
    detectors = json.load(f)

def _generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def run(generated_contract):
    """Perfoms solidity compilation on LLM generated contracts. Returns `True` if no error occured during the compilation process, `False` otherwise"""
    try:
        st = time.time()
        temp_file = 'temp' + _generate_random_string(10) + '.sol'
        with open(temp_file, 'w+') as fhd:
            fhd.write(generated_contract)
            fhd.close()

        # compile
        process = subprocess.run(['node', 'src/index.js', temp_file], capture_output=True, universal_newlines=True)
        
        compiled = False
        if process.stderr != '':
            print("WARNING: compilation log", process.stderr)
            compiled = False 
        
        for line in process.stdout.splitlines():
            if "Compilation succeed!" in line:
                compiled = True
                print('INFO: the generated contract compiles')
                break

        if not compiled:
            print('WARNING: the generated contract does not compile')
            print("WARNING: compilation out logs:", process.stdout)
            return False
        
        res = slither(generated_contract_file=temp_file)
        print(f'INFO: compilation took {time.time() - st} seconds'.format("%.2f"))
        return res
    except Exception as ex:
        print('exeption when compiling', ex)
        return False
    finally:
        os.remove(temp_file)

def slither(generated_contract_file):
    try:
        sl_result = _slither_sol_file(generated_contract_file)
        print('INFO: Slither codes', sl_result)
        return False if _has_error_or_warning(sl_result) else True

    except:
        return False

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
            return False