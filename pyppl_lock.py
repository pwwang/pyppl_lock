import filelock
from pyppl.plugin import hookimpl
from pyppl.logger import logger

__version__ = "0.0.1"

@hookimpl
def proc_init(proc):
	proc.add_config('lock_lock')

@hookimpl
def proc_prerun(proc):
	lockfile = proc.workdir / 'proc.lock'
	lock = proc.plugin_config.lock_lock = filelock.FileLock(lockfile)
	try:
		lock.acquire(timeout = 3)
	except filelock.Timeout:
		logger.warning('Another instance of this process is running, waiting ...',
			proc = proc.id)
		logger.warning(
			'If not, remove the process lock file (or hit Ctrl-C) and try again:',
			proc = proc.id)
		logger.warning('- %s', lockfile, proc = proc.id)
		try:
			lock.acquire()
		except KeyboardInterrupt:
			lockfile.unlink()
			lock.acquire()

@hookimpl
def proc_postrun(proc, status):
	"""We should remove the lock file anyway"""
	lockfile = proc.workdir / 'proc.lock'
	if isinstance(proc.plugin_config.lock_lock, filelock.FileLock) and \
		proc.plugin_config.lock_lock.is_locked:

		proc.plugin_config.lock_lock.release()

	if lockfile.is_file():
		lockfile.unlink()
