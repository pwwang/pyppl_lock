import sys
import pytest
import cmdy
from filelock import SoftFileLock
from time import sleep
from diot import Diot
from pyppl import Proc
from pyppl_lock import proc_init, proc_prerun, proc_postrun, job_build

def test_init(tmp_path):
	pLockInit = Proc(ppldir = tmp_path)
	proc_init(pLockInit)
	assert 'lock_lock' in pLockInit.props

def test_run(tmp_path, caplog):
	pLockPrerun = Proc(ppldir = tmp_path)
	proc_init(pLockPrerun)
	pLockPrerun.__attrs_property_cached__['workdir'] = pLockPrerun.ppldir / 'pLockPrerun'
	pLockPrerun.workdir.mkdir()
	assert not pLockPrerun.workdir.joinpath('proc.lock').is_file()
	proc_prerun(pLockPrerun)
	assert pLockPrerun.workdir.joinpath('proc.lock').is_file()
	assert pLockPrerun.props.lock_lock.is_locked

	proc_postrun(pLockPrerun, 'succeeded')
	assert not pLockPrerun.props.lock_lock.is_locked
	assert not pLockPrerun.workdir.joinpath('proc.lock').is_file()

@pytest.fixture
def locked_proc(request, tmp_path):
	pLockLocked = Proc(ppldir = tmp_path, tag = request.node.name)
	proc_init(pLockLocked)
	pLockLocked.__attrs_property_cached__['workdir'] = pLockLocked.ppldir / 'pLockLocked'
	pLockLocked.workdir.mkdir()
	lockfile = pLockLocked.workdir / 'proc.lock'
	# lock in the same session with same object can be acquired multiple times.
	# So we create another process object.
	cmdy.python(c = 'import filelock; filelock.FileLock("%s").acquire()' % lockfile, _exe = sys.executable, _raise = False)
	return pLockLocked


def test_locked(locked_proc, tmp_path, caplog):
	#assert locked_proc.props.lock_lock.is_locked

	pTestLocked = Proc(ppldir = tmp_path)
	pTestLocked.__attrs_property_cached__['workdir'] = locked_proc.workdir
	# mock the acquire function of SoftFileLock
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

def test_job_build(locked_proc, caplog):

	job = Diot(proc = locked_proc)
	job_build(job, "failed")
	assert not (job.proc.workdir / 'proc.lock').is_file()

