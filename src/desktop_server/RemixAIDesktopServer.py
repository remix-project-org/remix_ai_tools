
import sys
from src.inference import app, code_completion, code_insertion, code_generation, error_explaining, run_answering
from src.inference import state, sysinfos, killServer, init_general, init_completion, code_explaining

app.add_url_rule('/code_completion', 'code_completion', code_completion, methods=['POST'])
app.add_url_rule('/code_insertion', 'code_insertion', code_insertion, methods=['POST'])
app.add_url_rule('/code_generation', 'code_generation', code_generation, methods=['POST'])
app.add_url_rule('/state', 'state', state, methods=['GET'])
app.add_url_rule('/sys', 'sysinfos', sysinfos, methods=['GET'])
app.add_url_rule('/kill', 'killServer', killServer, methods=['POST'])
app.add_url_rule('/init_completion', 'init_completion', init_completion, methods=['POST'])
app.add_url_rule('/init_general', 'init_general', init_general, methods=['POST'])
app.add_url_rule('/error_explaining', 'error_explaining', error_explaining, methods=['POST'])
app.add_url_rule('/solidity_answer', 'run_answering', run_answering, methods=['POST'])
app.add_url_rule('/code_explaining', 'code_explaining', code_explaining, methods=['POST'])

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5501
    app.run(host='0.0.0.0', port=port, processes=1, threaded=True)

# TODO: Handle the context exeeding the model size
# TODO: handle harware generation speed in n-tokens/sec
# TODO: use reset to stop generation
# TODO: implement stop generation on user request