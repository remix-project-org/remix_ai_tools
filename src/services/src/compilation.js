import { Compiler as RemixCompiler } from '@remix-project/remix-solidity'
import { RemixURLResolver } from '@remix-project/remix-url-resolver'

export function loadCompiler (compilerConfig) {
    return new Promise(function (resolve, reject) {
        const importsCallback = (url, cb) => {
            try {
                const urlResolver = new RemixURLResolver()
                urlResolver.resolve(url).then((result) => cb(null, result.content)).catch((error) => cb(error.message))
            } catch (e) {
              cb(e.message)
            }
          }
        const compiler = new RemixCompiler(importsCallback)
        if (compilerConfig) {
            const { currentCompilerUrl, evmVersion, optimize, runs } = compilerConfig
            if (evmVersion) compiler.set('evmVersion', evmVersion)
            if (optimize) compiler.set('optimize', optimize)
            if (runs) compiler.set('runs', runs)
            if (currentCompilerUrl) {
                compiler.loadRemoteVersion(currentCompilerUrl)
                compiler.event.register('compilerLoaded', this, function (version, license) {
                    resolve(compiler)
                })
            } else {
                compiler.onInternalCompilerLoaded()
                resolve(compiler)
            }
        } else {
            compiler.onInternalCompilerLoaded()
            resolve(compiler)
        }
    })
  }

export function doCompilation (sources, compiler) {
    return new Promise(function(resolve, reject) {
        // @ts-ignore
        compiler.event.register('compilationFinished', this, (success, data, source, input, version) => {
        resolve({data, input, version})
      })
      compiler.compile(sources)
    })
  }
