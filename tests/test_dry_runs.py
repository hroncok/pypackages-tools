import os
import subprocess


TEST_ROOTS = os.path.join(os.path.dirname(__file__), 'test_roots')
BYTECOMPILE_SCRIPT = 'brp-python-bytecompile.py'
BRP_PYTHON_BYTECOMPILE = os.path.join(os.path.dirname(__file__), '..', BYTECOMPILE_SCRIPT)


def run_bytecompile(directory, rpm_build_root):
    proc = subprocess.Popen([BRP_PYTHON_BYTECOMPILE, '--dry-run', '--config-dir',
        os.path.join(TEST_ROOTS, directory, 'etc', 'pypackages-tools'), 'python', '1'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env={'RPM_BUILD_ROOT': os.path.join(TEST_ROOTS, directory, rpm_build_root)})

    out = proc.communicate()[0].decode('utf-8')
    return proc.returncode, out

def assert_libdirs_not_associated(retcode, output, libdirs, testdir, rpm_build_root):
    """Warning: libdirs must not start with slash!"""
    assert retcode == 11
    assert BYTECOMPILE_SCRIPT + \
        ': Error: there are Python libdirs not associated with any Python runtime:' in output
    full_libdirs = [os.path.join(TEST_ROOTS, testdir, rpm_build_root, l) for l in libdirs]
    for fl in full_libdirs:
        assert BYTECOMPILE_SCRIPT + ': ' + fl in output

def test_no_config_for_libdirs():
    testdir = 'no_configs'
    rpm_build_root = 'some/build/dir/BUILDROOT/foo-1.2.3.fcXY.x86_86/'
    retcode, out = run_bytecompile(testdir, rpm_build_root)
    assert_libdirs_not_associated(retcode, out, ['usr/lib/python2.7', 'usr/lib64/python8.9'],
        testdir, rpm_build_root)
