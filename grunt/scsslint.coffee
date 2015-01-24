module.exports =

  # Lint your SCSS
  # https://github.com/ahmednuaman/grunt-scss-lint

  options:
    colorizeOutput: true
    config: 'node_modules/grunt-scss-lint/.scss-lint.yml'
  stylesheets: ['<%= paths.css %>/scss/*.scss']
