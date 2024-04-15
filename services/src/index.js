import { loadCompiler, doCompilation } from './compilation.js'
import  {analyze} from "@nomicfoundation/solidity-analyzer"
import { compareVersions } from 'compare-versions'
import fs from 'fs'
const sol_file = process.argv[2]

const DEFAULT_SOLC_VERSION = "0.8.24+commit.e11b9ed9"
const sol_versions = JSON.parse(fs.readFileSync('./list.json', 'utf-8'))

const get_latest_compiler_version = ()=>{
    let latest_v = "0.0.0"
    let latest = DEFAULT_SOLC_VERSION
    for (let i=0; i<sol_versions['builds'].length; i++){
        const vsn = sol_versions['builds'][i]['version']
        
        // discard nightly builds
        if(sol_versions['builds'][i]['longVersion'].includes('nightly')){
            continue
        }

        // if vsn is higher than curent latest
        if (compareVersions(vsn, latest_v)) {
            latest_v = vsn
            latest = 'v' + sol_versions['builds'][i]['longVersion']
        }

    }
    return [latest, latest_v]
}

const get_compiler_version = (sol_src) => {
    const res = analyze(sol_src)
    console.log("detected Pragma versions", res.versionPragmas)
    let max_pragma_version = undefined
    let pragma_version = res.versionPragmas[0].split(' ')[0].split('.')
    pragma_version[0] = pragma_version[0][pragma_version[0].length-1]
    pragma_version = pragma_version.join('.')

    if (res.versionPragmas[0].split(' ')[1]){
        max_pragma_version = res.versionPragmas[0].split(' ')[1].split('.')
        max_pragma_version[0] = max_pragma_version[0][max_pragma_version[0].length-1]
        max_pragma_version = max_pragma_version.join('.')
    }

    let sol_version = DEFAULT_SOLC_VERSION
    for (let i=0; i<sol_versions['builds'].length; i++){
        if (sol_versions['builds'][i]['version'] === pragma_version){
            // discard nightly builds
            if(sol_versions['builds'][i]['longVersion'].includes('nightly')){
                continue
            }
            sol_version = 'v' + sol_versions['builds'][i]['longVersion']
            // console.log("detected compiler version:", sol_version)
        }

        if (max_pragma_version){
            if (sol_versions['builds'][i]['version'] === max_pragma_version){
                if(sol_versions['builds'][i]['longVersion'].includes('nightly')){
                    continue
                }
                sol_version = 'v' + sol_versions['builds'][i]['longVersion']
                // console.log("detected max compiler version:", sol_version)
                break
            }
        }
    }

    if (max_pragma_version){
        console.log("INFO: max version is ", max_pragma_version)

        // max pragma is above latest 
        const latest = get_latest_compiler_version()
        if (compareVersions(max_pragma_version, latest[1])){ 
            console.log("INFO: Max version not supported yet, using latest version:", latest[0])
            sol_version = latest[0]
        }
    }
    return sol_version
}

const run = async () => {
    const content_src = fs.readFileSync(sol_file, 'utf-8')
    const source = {
        'token.sol': {
            content: content_src
        }
    }
    const cv = get_latest_compiler_version()[0]
    console.log("INFO: using compiler version:", cv)

    const compilerConfig = {
        currentCompilerUrl: cv,
        evmVersion: null, // default evm version
        optimize: false,
        runs: 200
    }
    const compiler = await loadCompiler(compilerConfig)
    const compilationResult = await doCompilation(source, compiler)
    if(compilationResult.data.errors === undefined){
        console.log("Compilation succeed!") 
    }else{
        console.log("Compilation failed!")
        console.log(compilationResult.data.errors)
    }
  }

run()