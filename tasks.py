from invoke import task, run

from os.path import dirname, abspath

# Create scripted tasks to run in command-line here
# http://docs.pyinvoke.org/en/latest/


PROJECT_ROOT = '%s/yesterday' % dirname(abspath(__file__))


@task
def clean():
    """Clean up static, compiled, test, and log files"""

    print("Deleting *.pyc files...")
    run('find . -name *.pyc -delete')

    print("Deleting collected static files...")
    run('rm -rf %s/public' % PROJECT_ROOT)

    print("Deleting compiled stylesheets...")
    run('rm -rf %s/static/css/build' % PROJECT_ROOT)

    print("Deleting compiled scripts...")
    run('rm -rf %s/static/js/build' % PROJECT_ROOT)
    run('rm -rf %s/static/js/tests/build' % PROJECT_ROOT)

    print('Deleting compressed images...')
    run('rm -rf %s/static/img/compressed' % PROJECT_ROOT)

    print('Deleting test files...')
    run('rm -rf tests/*')
    run('rm -rf .coverage')
    run('rm -rf _SpecRunner.html')

    print('Deleting log files...')
    run('rm -rf logs/*')
