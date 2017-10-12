import os
import currint
from invoke import task
from six.moves import input


VERSION_FILE = os.path.join(os.path.dirname(currint.__file__), "__init__.py")


def _write_to_version_file(ctx, version):
    with open(VERSION_FILE, 'r') as version_read:
        output = []
        for line in version_read:
            if line.startswith('__version__'):
                output.append('__version__ = %r' % version)
            else:
                output.append(line.strip())

    with open(VERSION_FILE, 'w') as version_write:
        for line in output:
            version_write.write(line + '\n')


def _commit_and_tag(ctx, version):
    """Commit changes to version file and tag the release"""
    ctx.run('git add %s' % VERSION_FILE, hide='out')
    ctx.run('git commit -m "Releasing version %s"' % version, hide='out')
    ctx.run('git tag %s' % version, hide='out')


def _push_release_changes(ctx, version):
    push = input('Push release changes to master? (y/n): ')
    if push == 'y':
        ctx.run('git push origin master')

        # push the release tag
        ctx.run('git push origin %s' % version)

    else:
        print('Not pushing changes to master!')
        print('Make sure you remember to explictily push the tag!')


@task
def release(ctx):
    # Prompt for version
    print("Current version: %s" % currint.__version__)
    release_version = input('Enter a new version (or "exit"): ')
    if not release_version or release_version == 'exit':
        print('Cancelling release!')
        return

    _write_to_version_file(ctx, release_version)
    _commit_and_tag(ctx, release_version)
    _push_release_changes(ctx, release_version)
