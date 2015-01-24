module.exports =

  # Run grunt tasks concurrently
  # https://github.com/sindresorhus/grunt-concurrent

  tests:
    options:
      logConcurrentOutput: true
    tasks: [
      'connect:tests'
      'watch'
      'shell:tdaemon'
    ]
