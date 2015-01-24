module.exports =

  # Run tasks whenever watched files change
  # https://github.com/gruntjs/grunt-contrib-watch

  options:
    spawn: false

  config:
    options:
      reload: true
    files: [
      'Gruntfile.coffee'
      'grunt/*.{coffee,yaml}'
    ]

  livereload:
    options:
      livereload: true
    files: [
      '<%= paths.templates %>/**/*.html'
      '<%= paths.css %>/**/*.{scss,css}'
      '<%= paths.js %>/**/*.{coffee,js}'
    ]

  stylesheets:
    files: ['<%= paths.css %>/scss/*.scss']
    tasks: [
      'newer:scsslint'
      'newer:sass'
      'newer:autoprefixer'
      'replace:stylesheets'
    ]

  scripts:
    files: ['<%= paths.js %>/coffee/*.coffee']
    tasks: [
      'newer:coffeelint:scripts'
      'newer:coffee:scripts'
    ]

  images:
    files: ['<%= paths.img %>/**/*.{png,jpg,gif,svg}']
    tasks: ['newer:imagemin']

  jasmine:
    files: ['<%= paths.js %>/tests/coffee/*.coffee']
    tasks: [
      'lint_jasmine'
      'build_jasmine'
      'notify:test'
    ]
