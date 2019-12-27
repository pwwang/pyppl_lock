import pytest
import filelock
from time import sleep
from pyppl import Proc
from pyppl_lock import proc_init, proc_prerun, proc_postrun

def test_init(tmp_path):
	pLockInit = Proc(ppldir = tmp_path)
	proc_init(pLockInit)
	assert 'lock_lock' in pLockInit.config

def test_run(tmp_path, caplog):
	pLockPrerun = Proc(ppldir = tmp_path)
	proc_init(pLockPrerun)
	pLockPrerun.__attrs_property_cached__['workdir'] = pLockPrerun.ppldir / 'pLockPrerun'
	pLockPrerun.workdir.mkdir()
	assert not pLockPrerun.workdir.joinpath('proc.lock').is_file()
	proc_prerun(pLockPrerun)
	assert pLockPrerun.workdir.joinpath('proc.lock').is_file()
	assert pLockPrerun.config.lock_lock.is_locked

	proc_postrun(pLockPrerun, 'succeeded')
	assert not pLockPrerun.config.lock_lock.is_locked
	assert not pLockPrerun.workdir.joinpath('proc.lock').is_file()

@pytest.fixture
def locked_proc(tmp_path):
	pLockLocked = Proc(ppldir = tmp_path)
	proc_init(pLockLocked)
	pLockLocked.__attrs_property_cached__['workdir'] = pLockLocked.ppldir / 'pLockLocked'
	pLockLocked.workdir.mkdir()
	proc_prerun(pLockLocked)
	return pLockLocked


def test_locked(locked_proc, tmp_path, caplog):
	# lock in the same session with same object can be acquired multiple times.
	# So we create another process object.
	assert locked_proc.config.lock_lock.is_locked

	pTestLocked = Proc(ppldir = tmp_path)
	pTestLocked.__attrs_property_cached__['workdir'] = locked_proc.workdir
	# mock the acquire function of SoftFileLock
	from filelock import SoftFileLock
	origin_acquire = SoftFileLock.acquire
	def new_acquire(*args, **kwargs):
		if 'timeout' in kwargs:
			# reduce test time
			kwargs['timeout'] = .5
			origin_acquire(*args, **kwargs)
		else:
			pass
	SoftFileLock.acquire = new_acquire

	caplog.clear()
	proc_prerun(pTestLocked)
	assert 'pTestLocked: Another instance of this process is running, waiting' in caplog.text

