# pyppl_lock

Preventing running processes from running again for PyPPL


It uses `SoftFileLock` from `filelock` to create a lock file in process' `<workdir>`. Once the process is done or failed, the lock is released.

If the pipeline is already running by other processes:
```shell
# in PyPPL's example directory
python 100jobs/100jobs.py
```

```shell
[2019-12-27 10:48:23   PYPPL] +------------------------------------------------------------------------------+
[2019-12-27 10:48:23   PYPPL] |                                                                              |
[2019-12-27 10:48:23   PYPPL] |                   ________        ______________________                     |
[2019-12-27 10:48:23   PYPPL] |                   ___  __ \____  ____  __ \__  __ \__  /                     |
[2019-12-27 10:48:23   PYPPL] |                   __  /_/ /_  / / /_  /_/ /_  /_/ /_  /                      |
[2019-12-27 10:48:23   PYPPL] |                   _  ____/_  /_/ /_  ____/_  ____/_  /___                    |
[2019-12-27 10:48:23   PYPPL] |                   /_/     _\__, / /_/     /_/     /_____/                    |
[2019-12-27 10:48:23   PYPPL] |                           /____/                                             |
[2019-12-27 10:48:23   PYPPL] |                                                                              |
[2019-12-27 10:48:23   PYPPL] |                                    v3.0.0                                    |
[2019-12-27 10:48:23   PYPPL] |                                                                              |
[2019-12-27 10:48:23   PYPPL] +------------------------------------------------------------------------------+
[2019-12-27 10:48:23    TIPS] Check documentation at: https://pyppl.readthedocs.io/en/latest/
[2019-12-27 10:48:23  CONFIG] Read from ~/.PyPPL.toml
[2019-12-27 10:48:23  CONFIG] Read from PYPPL.osenv
[2019-12-27 10:48:23  PLUGIN] Loaded plugins:
[2019-12-27 10:48:23  PLUGIN]   export-0.0.2, flowchart-0.1.2, lock-0.0.2, report-0.5.0, echo-0.0.2,
[2019-12-27 10:48:23  PLUGIN]   strict-0.0.2, rich-0.0.2
[2019-12-27 10:48:23  PLUGIN] Loaded runners:
[2019-12-27 10:48:23  PLUGIN]   local-builtin, sge-0.0.2, dry-0.0.2, ssh-0.0.2, slurm-0.0.2
[2019-12-27 10:48:23   PYPPL] ================================================================================
[2019-12-27 10:48:23   PYPPL] >>> PIPELINE: 100jobs
[2019-12-27 10:48:23   PYPPL] ================================================================================
[2019-12-27 10:48:23 PROCESS] --------------------------------------------------------------------------------
[2019-12-27 10:48:23 PROCESS] p100.notag: No description.
[2019-12-27 10:48:23 PROCESS] --------------------------------------------------------------------------------
[2019-12-27 10:48:23 DEPENDS] [START] => p100.notag => [END]
[2019-12-27 10:48:23 WORKDIR] p100: workdir/PyPPL.p100.notag.d2c7118e
[2019-12-27 10:48:23 P_PROPS] p100: forks  => 1
[2019-12-27 10:48:23 P_PROPS] p100: runner => local
[2019-12-27 10:48:23  P_ARGS] p100: a      => 1
[2019-12-27 10:48:26 WARNING] p100: Another instance of this process is running, waiting ...
[2019-12-27 10:48:26 WARNING] p100: If not, remove the process lock file (or hit Ctrl-C) and try again:
[2019-12-27 10:48:26 WARNING] p100: - workdir/PyPPL.p100.notag.d2c7118e/proc.lock
```
