module.exports =

  # General purpose text replacement for grunt
  # https://github.com/yoniholmes/grunt-text-replace

  stylesheets:
    src: ['<%= paths.css %>/build/*.css.map']
    overwrite: true
    replacements: [
      from: '<%= name %>/static'
      to: '/static'
    ]

  coverage:
    src: ['<%= paths.tests %>/jasmine/coverage.html']
    overwrite: true
    replacements: [
      from: '<div class="header high">'
      to: '<div class="header high">
            <h1>
              <a href="/tests/jasmine" style="color: #000;">
                Click here for Jasmine Tests
              </a>
            </h1>
          '
    ]

  specRunner:
    src: ['<%= paths.tests %>/jasmine/index.html']
    overwrite: true
    replacements: [
      {
        from: '.grunt'
        to: '../../.grunt'
      }
      {
        from: '<%= name %>'
        to: '../../<%= name %>'
      }
      {
        from: '</body>'
        to: '
            <h1 style="font-family: Helvetica Neue; font-weight: 300;">
              <a href="/tests/jasmine/coverage.html" style="color: #007069;">
                Click here for JS Test Coverage
              </a>
            </h1></body>
            '
      }
    ]
