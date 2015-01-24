module.exports =

  # Parse CSS and add vendor-prefixed CSS properties
  # https://github.com/nDmitry/grunt-autoprefixer

  stylesheets:
    options:
      map: true
    files: [
      expand: true
      cwd: '<%= paths.css %>/build/'
      src: ['*.css']
      dest: '<%= paths.css %>/build'
      ext: '.css'
    ]
