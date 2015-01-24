module.exports =

  # Run shell commands
  # https://github.com/sindresorhus/grunt-shell

  django:
    command: 'coverage run $(which django-admin.py) test && coverage combine && coverage report && coverage html; echo &&
              echo "================================ Flake8 Summary ================================" && flake8 <%= name %>;
              echo "================================================================================"'

  tdaemon:
    command: 'python <%= paths.config %>/lib/tdaemon.py <%= name %> -t django-nose-coverage --ignore-dirs=static,templates'
