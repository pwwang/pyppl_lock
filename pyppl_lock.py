"""Preventing running processes from running again for PyPPL"""
import filelock
from pyppl.plugin import hookimpl
from pyppl.logger import Logger

__version__ = "0.0.5"

logger = Logger(plugin='lock') # pylint: disable=invalid-name

@hookimpl
def proc_init(proc):
    """Add a config for lock"""
    proc.props.lock_lock = None


@hookimpl
def proc_prerun(proc):
    """Try to access the lock"""
    lockfile = proc.workdir / 'proc.lock'
    lock = proc.props.lock_lock = filelock.SoftFileLock(lockfile)
    try:
        lock.acquire(timeout=3)
    except filelock.Timeout:
        logger.warning(
            'Another instance of this process is running, waiting ...',
            proc=proc.id)
        logger.warning('If not, remove the process lock file '
                       '(or hit Ctrl-C) and try again:',
                       proc=proc.id)
        logger.warning('- %s', lockfile, proc=proc.id)
        try:
            lock.acquire()
        except KeyboardInterrupt:  # pragma: no cover
            lockfile.unlink()
            lock.acquire()


def _lock_release(proc):
    """Release the lock"""
    lockfile = proc.workdir / 'proc.lock'
    if (proc.props.lock_lock
            and isinstance(proc.props.lock_lock, filelock.SoftFileLock)
            and proc.props.lock_lock.is_locked):
        proc.props.lock_lock.release()

    if lockfile.is_file():  # pragma: no cover
        lockfile.unlink()


@hookimpl
def job_build(job, status):
    """Job building failure will also cause pipeline halt"""
    if status == 'failed':
        _lock_release(job.proc)


@hookimpl
def proc_postrun(proc, status):  # pylint: disable=unused-argument
    """We should remove the lock file anyway"""
    _lock_release(proc)
