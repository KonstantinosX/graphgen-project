# utils.py
# Some utilities used for the Python wrapper `graphpygen` for the GraphGen system.
#
# Author:   Konstantinos Xirogiannopoulos <kostasx@cs.umd.edu>
# Created:  Tue Aug 18 18:37:11 2015
#
# Adapted from : github.com/nltk/nltk/internals.py

import sys
import os
import subprocess


_java_bin = None
_java_options = []

##########################################################################
# Search for files/binaries
##########################################################################

def _decode_stdoutdata(stdoutdata):
    """ Convert data read from stdout/stderr to unicode """
    if not isinstance(stdoutdata, bytes):
        return stdoutdata
    return stdoutdata

def find_file_iter(filename, env_vars=(), searchpath=(),
    file_names=None, url=None, verbose=True, finding_dir=False):
    """
    Search for a file to be used by nltk.
    :param filename: The name or path of the file.
    :param env_vars: A list of environment variable names to check.
    :param file_names: A list of alternative file names to check.
    :param searchpath: List of directories to search.
    :param url: URL presented to user for download help.
    :param verbose: Whether or not to print path when a file is found.
    """
    file_names = [filename] + (file_names or [])
    assert isinstance(filename, str)
    assert not isinstance(file_names, str)
    assert not isinstance(searchpath, str)
    if isinstance(env_vars, str):
        env_vars = env_vars.split()
    yielded = False

    # File exists, no magic
    for alternative in file_names:
        path_to_file = os.path.join(filename, alternative)
        if os.path.isfile(path_to_file):
            if verbose:
                print('[Found %s: %s]' % (filename, path_to_file))
            yielded = True
            yield path_to_file
        # Check the bare alternatives
        if os.path.isfile(alternative):
            if verbose:
                print('[Found %s: %s]' % (filename, alternative))
            yielded = True
            yield alternative
        # Check if the alternative is inside a 'file' directory
        path_to_file = os.path.join(filename, 'file', alternative)
        if os.path.isfile(path_to_file):
            if verbose:
                print('[Found %s: %s]' % (filename, path_to_file))
            yielded = True
            yield path_to_file

    # Check environment variables
    for env_var in env_vars:
        if env_var in os.environ:
            if finding_dir: # This is to file a directory instead of file
                yielded = True
                yield os.environ[env_var]

            for env_dir in os.environ[env_var].split(os.pathsep):
                # Check if the environment variable contains a direct path to the bin
                if os.path.isfile(env_dir):
                    if verbose:
                        print('[Found %s: %s]'%(filename, env_dir))
                    yielded = True
                    yield env_dir
                # Check if the possible bin names exist inside the environment variable directories
                for alternative in file_names:
                    path_to_file = os.path.join(env_dir, alternative)
                    if os.path.isfile(path_to_file):
                        if verbose:
                            print('[Found %s: %s]'%(filename, path_to_file))
                        yielded = True
                        yield path_to_file
                    # Check if the alternative is inside a 'file' directory
                    path_to_file = os.path.join(env_dir, 'file', alternative)
                    if os.path.isfile(path_to_file):
                        if verbose:
                            print('[Found %s: %s]' % (filename, path_to_file))
                        yielded = True
                        yield path_to_file

    # Check the path list.
    for directory in searchpath:
        for alternative in file_names:
            path_to_file = os.path.join(directory, alternative)
            if os.path.isfile(path_to_file):
                yielded = True
                yield path_to_file

    # If we're on a POSIX system, then try using the 'which' command
    # to find the file.
    if os.name == 'posix':
        for alternative in file_names:
            try:
                p = subprocess.Popen(['which', alternative],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = p.communicate()
                path = _decode_stdoutdata(stdout).strip()
                if path.endswith(alternative) and os.path.exists(path):
                    if verbose:
                        print('[Found %s: %s]' % (filename, path))
                    yielded = True
                    yield path
            except (KeyboardInterrupt, SystemExit, OSError):
                raise
            except:
                pass

    if not yielded:
        msg = ("GraphGen was unable to find the %s file!" "\nUse software specific "
               "configuration paramaters" % filename)
        if env_vars: msg += ' or set the %s environment variable' % env_vars[0]
        msg += '.'
        if searchpath:
            msg += '\n\n  Searched in:'
            msg += ''.join('\n    - %s' % d for d in searchpath)
        if url: msg += ('\n\n  For more information on %s, see:\n    <%s>' %
                        (filename, url))
        div = '='*75
        raise LookupError('\n\n%s\n%s\n%s' % (div, msg, div))


def find_binary(name, path_to_bin=None, env_vars=(), searchpath=(),
                binary_names=None, url=None, verbose=True):
    return next(find_binary_iter(name, path_to_bin, env_vars, searchpath, binary_names, url, verbose))

def find_binary_iter(name, path_to_bin=None, env_vars=(), searchpath=(),
                binary_names=None, url=None, verbose=True):
    """
    Search for a file to be used by nltk.
    :param name: The name or path of the file.
    :param path_to_bin: The user-supplied binary location (deprecated)
    :param env_vars: A list of environment variable names to check.
    :param file_names: A list of alternative file names to check.
    :param searchpath: List of directories to search.
    :param url: URL presented to user for download help.
    :param verbose: Whether or not to print path when a file is found.
    """
    for file in  find_file_iter(path_to_bin or name, env_vars, searchpath, binary_names,
                     url, verbose):
        yield file


# [xx] add classpath option to config_java?
def config_java(bin=None, options=None, verbose=True):
    """
    Configure nltk's java interface, by letting nltk know where it can
    find the Java binary, and what extra options (if any) should be
    passed to Java when it is run.
    :param bin: The full path to the Java binary.  If not specified,
        then nltk will search the system for a Java binary; and if
        one is not found, it will raise a ``LookupError`` exception.
    :type bin: str
    :param options: A list of options that should be passed to the
        Java binary when it is called.  A common value is
        ``'-Xmx512m'``, which tells Java binary to increase
        the maximum heap size to 512 megabytes.  If no options are
        specified, then do not modify the options list.
    :type options: list(str)
    """
    global _java_bin, _java_options
    _java_bin = find_binary('java', bin, env_vars=['JAVAHOME', 'JAVA_HOME'], verbose=verbose, binary_names=['java.exe'])

    if options is not None:
        if isinstance(options, str):
            options = options.split()
        _java_options = list(options)

def java(cmd, classpath=None, stdin=None, stdout=None, stderr=None,
         blocking=True):
    """
    Execute the given java command, by opening a subprocess that calls
    Java.  If java has not yet been configured, it will be configured
    by calling ``config_java()`` with no arguments.
    :param cmd: The java command that should be called, formatted as
        a list of strings.  Typically, the first string will be the name
        of the java class; and the remaining strings will be arguments
        for that java class.
    :type cmd: list(str)
    :param classpath: A ``':'`` separated list of directories, JAR
        archives, and ZIP archives to search for class files.
    :type classpath: str
    :param stdin, stdout, stderr: Specify the executed programs'
        standard input, standard output and standard error file
        handles, respectively.  Valid values are ``subprocess.PIPE``,
        an existing file descriptor (a positive integer), an existing
        file object, and None.  ``subprocess.PIPE`` indicates that a
        new pipe to the child should be created.  With None, no
        redirection will occur; the child's file handles will be
        inherited from the parent.  Additionally, stderr can be
        ``subprocess.STDOUT``, which indicates that the stderr data
        from the applications should be captured into the same file
        handle as for stdout.
    :param blocking: If ``false``, then return immediately after
        spawning the subprocess.  In this case, the return value is
        the ``Popen`` object, and not a ``(stdout, stderr)`` tuple.
    :return: If ``blocking=True``, then return a tuple ``(stdout,
        stderr)``, containing the stdout and stderr outputs generated
        by the java command if the ``stdout`` and ``stderr`` parameters
        were set to ``subprocess.PIPE``; or None otherwise.  If
        ``blocking=False``, then return a ``subprocess.Popen`` object.
    :raise OSError: If the java command returns a nonzero return code.
    """
    if stdin == 'pipe': stdin = subprocess.PIPE
    if stdout == 'pipe': stdout = subprocess.PIPE
    if stderr == 'pipe': stderr = subprocess.PIPE
    if isinstance(cmd, str):
        raise TypeError('cmd should be a list of strings')

    # Make sure we know where a java binary is.
    if _java_bin is None:
        # config_java(bin='/usr/bin/java')
        config_java(options=['-Xmx10G'])
        # config_java(options=default_options, verbose=False)

    # Set up the classpath.
    if isinstance(classpath, str):
        classpaths=[classpath]
    else:
        classpaths=list(classpath)
    classpath=os.path.pathsep.join(classpaths)

    # Construct the full command string.
    cmd = list(cmd)
    cmd = ['-cp', classpath] + cmd
    cmd = [_java_bin] + _java_options + cmd

    # Call java via a subprocess
    p = subprocess.Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr)
    if not blocking: return p
    (stdout, stderr) = p.communicate()

    # Check the return code.
    if p.returncode != 0:
        print(_decode_stdoutdata(stderr))
        raise OSError('Java command failed : ' + str(cmd))

    return (stdout, stderr)

# Only export the 'java' method
__all__ = ['java']
