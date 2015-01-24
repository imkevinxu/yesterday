module.exports =

  # Clear files and folders
  # https://github.com/gruntjs/grunt-contrib-clean

  stylesheets: ['<%= paths.css %>/build']

  scripts: [
    '<%= paths.js %>/build'
    '<%= paths.js %>/tests/build'
  ]

  images: ['<%= paths.img %>/compressed']

  tests: [
    '<%= paths.tests %>/*'
    '.coverage'
  ]

  jasmine: ['<%= paths.tests %>/jasmine']

  specRunner: ['_SpecRunner.html']

  logs: [
    'logs/*.log'
    'logs/*.log.*'
  ]
