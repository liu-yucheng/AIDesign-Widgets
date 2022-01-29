"""Executable that tests the app as a blackbox."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import asyncio
import json
import os
import pathlib
import re
import shutil
import threading
import typing
import unittest

from os import path as ospath

_copytree = shutil.copytree
_create_subprocess_shell = asyncio.create_subprocess_shell
_dump = json.dump
_exists = ospath.exists
_IO = typing.IO
_isdir = ospath.isdir
# _isfile = ospath.isfile
_join = ospath.join
_listdir = os.listdir
_load = json.load
_makedirs = os.makedirs
_Path = pathlib.Path
_PIPE = asyncio.subprocess.PIPE
_remove = os.remove
_re_compile = re.compile
_rmtree = shutil.rmtree
_run = asyncio.run
_TestCase = unittest.TestCase
_Thread = threading.Thread

_timeout = float(30)

_tests_path = str(_Path(__file__).parent)
_repo_path = str(_Path(_tests_path).parent.parent)
_test_data_path = _join(_repo_path, ".aidesign_widgets_test_data")

_default_configs_path = _join(_repo_path, "aidesign_widgets_default_configs")
_default_test_data_path = _join(_default_configs_path, "test_data")

_cmd_configs_path = _join(_repo_path, "aidesign_widgets_command_configs")
_grid_crop_config_loc = _join(_cmd_configs_path, "grid_crop_config.json")
_rand_crop_config_loc = _join(_cmd_configs_path, "rand_crop_config.json")

_default_cmd_configs_path = _join(_default_test_data_path, "command_configs")
_default_grid_crop_config_loc = _join(_default_cmd_configs_path, "grid_crop_config.json")
_default_rand_crop_config_loc = _join(_default_cmd_configs_path, "rand_crop_config.json")

_default_tocrop_path = _join(_default_test_data_path, "to_crop")

_log_loc = _join(_test_data_path, "log.txt")

_tocrop_path = _join(_test_data_path, "to_crop")
_tocrop1_loc = _join(_tocrop_path, "to_crop_1.jpg")

_cropped_path = _join(_test_data_path, "cropped")

_grid_crop_config_backup_loc = _join(_test_data_path, "grid_crop_config_backup.json")
_rand_crop_config_backup_loc = _join(_test_data_path, "rand_crop_config_backup.json")


def _fix_newline_format(instr):
    instr = str(instr)

    result = instr
    result = result.replace("\r\n", "\n")
    result = result.replace("\r", "\n")
    return result


async def _async_run_cmd(cmd, instr=""):
    cmd = str(cmd)
    instr = str(instr)

    subproc = await _create_subprocess_shell(cmd=cmd, stdin=_PIPE, stdout=_PIPE, stderr=_PIPE)
    inbytes = instr.encode("utf-8", "replace")
    out, err = await subproc.communicate(inbytes)
    exit_code = await subproc.wait()

    out = out.decode("utf-8", "replace")
    out = _fix_newline_format(out)
    err = err.decode("utf-8", "replace")
    err = _fix_newline_format(err)
    result = exit_code, out, err
    return result


def _run_cmd(cmd, instr=""):
    cmd = str(cmd)
    instr = str(instr)

    result = _run(_async_run_cmd(cmd, instr))
    return result


class _FuncThread(_Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        """Inits self with the given args.

        Args:
            group: Group.
            target: Target.
            name: Name.
            args: Arguments
            kwargs: Keyword arguments.
            *: Positional-keyword and keyword-only arguments separator.
            daemon: Daemon thread switch.
        """
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._result = None

    def run(self):
        """Runs the thread."""
        # Adopted from CPython standard library threading source code
        # Ref: https://github.com/python/cpython/blob/main/Lib/threading.py
        try:
            if self._target is not None:
                self._result = self._target(*self._args, **self._kwargs)
        finally:
            # Avoid reference cycles
            del self._target
            del self._args
            del self._kwargs

    def join(self, timeout=None):
        """Joins the thread.

        Args:
            timeout: Timeout length in seconds.

        Returns:
            self._result: Result. Return value.
        """
        super().join(timeout=timeout)
        return self._result


def _load_json(from_loc):
    from_loc = str(from_loc)

    file = open(from_loc, "r")
    result = _load(file)
    file.close()

    result = dict(result)
    return result


def _save_json(from_dict, to_loc):
    from_dict = dict(from_dict)
    to_loc = str(to_loc)

    file = open(to_loc, "w+")
    _dump(from_dict, file, indent=4)
    file.close()


class _TestCmd(_TestCase):

    def __init__(self, methodName=""):
        """Inits self with the given args.

        Args:
            methodName: Method name.
        """
        super().__init__(methodName=methodName)
        self._log: _IO = None

    def setUp(self):
        """Sets up before the tests."""
        super().setUp()
        _makedirs(_test_data_path, exist_ok=True)
        self._log = open(_log_loc, "a+")

        start_info = str(
            "\n"
            "- Test case {}\n"
            "\n"
        ).format(type(self).__name__)
        self._log.write(start_info)

    def tearDown(self):
        """Tears down after the tests."""
        super().tearDown()
        end_info = str(
            "\n"
            "- End of test case {}\n"
            "\n"
        ).format(type(self).__name__)
        self._log.write(end_info)

        self._log.flush()
        self._log.close()

    def _logstr(self, str_to_log):
        str_to_log = str(str_to_log)

        if self._log is not None:
            self._log.write(str_to_log)

    def _log_method_start(self, method_name):
        method_name = str(method_name)

        info = "-- Test method {}\n".format(method_name)
        self._logstr(info)

    def _log_method_end(self, method_name):
        method_name = str(method_name)

        info = "-- End of test method {}\n".format(method_name)
        self._logstr(info)

    def _log_cmdout_start(self, cmd, stream_name):
        cmd = str(cmd)
        stream_name = str(stream_name)

        info = "--- \"{}\" {}\n".format(cmd, stream_name)
        self._logstr(info)

    def _log_cmdout_end(self, cmd, stream_name):
        cmd = str(cmd)
        stream_name = str(stream_name)

        info = "--- End of \"{}\" {}\n".format(cmd, stream_name)
        self._logstr(info)

    def _log_cmdout(self, cmd, stream_name, out):
        cmd = str(cmd)
        stream_name = str(stream_name)
        out = str(out)

        self._log_cmdout_start(cmd, stream_name)

        out_info = "{}\n".format(out)
        self._logstr(out_info)

        self._log_cmdout_end(cmd, stream_name)

    def _backup_cmd_configs(self):
        config = _load_json(_grid_crop_config_loc)
        _save_json(config, _grid_crop_config_backup_loc)
        default_config = _load_json(_default_grid_crop_config_loc)
        _save_json(default_config, _grid_crop_config_loc)

        config = _load_json(_rand_crop_config_loc)
        _save_json(config, _rand_crop_config_backup_loc)
        default_config = _load_json(_default_rand_crop_config_loc)
        _save_json(default_config, _rand_crop_config_loc)

    def _restore_cmd_configs(self):
        config_backup = _load_json(_grid_crop_config_backup_loc)
        _save_json(config_backup, _grid_crop_config_loc)

        if _exists(_grid_crop_config_backup_loc):
            _remove(_grid_crop_config_backup_loc)

        config_backup = _load_json(_rand_crop_config_backup_loc)
        _save_json(config_backup, _rand_crop_config_loc)

        if _exists(_rand_crop_config_backup_loc):
            _remove(_rand_crop_config_backup_loc)


class _TestSimpleCmd(_TestCmd):

    def _test_cmd_norm(self, cmd, instr=""):
        cmd = str(cmd)
        instr = str(instr)

        thread = _FuncThread(target=_run_cmd, args=[cmd, instr])
        thread.start()
        exit_code, out, err = thread.join(_timeout)
        timed_out = thread.is_alive()

        self._log_cmdout(cmd, "stdout", out)
        self._log_cmdout(cmd, "stderr", err)

        fail_msg = "Running \"{}\" results in a timeout".format(cmd)
        self.assertTrue(timed_out is False, fail_msg)

        fail_msg = "Running \"{}\" results in an unexpected exit code: {}".format(cmd, exit_code)
        self.assertTrue(exit_code == 0, fail_msg)


class TestWidgets(_TestSimpleCmd):
    """Tests for the "widgets" command."""

    def test_norm(self):
        """Tests the normal use case."""
        method_name = self.test_norm.__name__
        cmd = "widgets"
        instr = ""
        self._log_method_start(method_name)
        self._test_cmd_norm(cmd, instr)
        self._log_method_end(method_name)


class TestWidgetsHelp(_TestSimpleCmd):
    """Tests for the "widgets help" command."""

    def test_norm(self):
        """Tests the normal use case."""
        method_name = self.test_norm.__name__
        cmd = "widgets help"
        instr = ""
        self._log_method_start(method_name)
        self._test_cmd_norm(cmd, instr)
        self._log_method_end(method_name)


class TestWidgetsPathName(_TestSimpleCmd):
    """Tests for the "widgets path-name" command."""

    def test_norm(self):
        """Tests the normal use case."""
        method_name = self.test_norm.__name__
        cmd = f"widgets path-name {_repo_path}"
        instr = ""
        self._log_method_start(method_name)
        self._test_cmd_norm(cmd, instr)
        self._log_method_end(method_name)


class TestWidgetsGridCrop(_TestCmd):
    """Tests for the "widgets grid-crop" command."""

    def setUp(self):
        """Sets up before the tests."""
        super().setUp()
        self._backup_cmd_configs()

        _rmtree(_cropped_path, ignore_errors=True)
        _rmtree(_tocrop_path, ignore_errors=True)
        _makedirs(_cropped_path, exist_ok=True)
        _copytree(_default_tocrop_path, _tocrop_path)

        config = _load_json(_grid_crop_config_loc)
        config["image_location"] = _tocrop1_loc
        config["output_path"] = _cropped_path
        _save_json(config, _grid_crop_config_loc)

    def tearDown(self):
        """Tears down after the tests."""
        super().tearDown()
        self._restore_cmd_configs()

        _rmtree(_cropped_path, ignore_errors=True)
        _rmtree(_tocrop_path, ignore_errors=True)

    def test_norm(self):
        """Tests the normal use case."""
        method_name = self.test_norm.__name__
        self._log_method_start(method_name)

        cmd = "widgets grid-crop"
        instr = "\n"
        thread = _FuncThread(target=_run_cmd, args=[cmd, instr])
        thread.start()
        exit_code, out, err = thread.join(_timeout)
        timed_out = thread.is_alive()

        self._log_cmdout(cmd, "stdout", out)
        self._log_cmdout(cmd, "stderr", err)

        fail_msg = "Running \"{}\" results in a timeout".format(cmd)
        self.assertTrue(timed_out is False, fail_msg)

        fail_msg = "Running \"{}\" results in an unexpected exit code: {}".format(cmd, exit_code)
        self.assertTrue(exit_code == 0, fail_msg)

        format_incorrect_info = "results format incorrect"

        isdir = _isdir(_cropped_path)
        fail_msg = "{} is not a directory; {}".format(_tocrop_path, format_incorrect_info)
        self.assertTrue(isdir, fail_msg)

        regexs_each = [
            _re_compile(r".*-At-.*-Crop-.*(-Resize-.*)?-Time-.*\.jpg"),
        ]

        contents = _listdir(_cropped_path)

        for regex in regexs_each:

            for fname in contents:
                matched = bool(regex.match(fname))
                fail_msg = "File name {} in {} does not match pattern {}; {}".format(
                    fname, _cropped_path, str(regex), format_incorrect_info
                )
                self.assertTrue(matched, fail_msg)
            # end for

        # end for

        self._log_method_end(method_name)


class TestWidgetsRandCrop(_TestCmd):
    """Tests for the "widgets rand-crop" command."""

    def setUp(self):
        """Sets up before the tests."""
        super().setUp()
        self._backup_cmd_configs()

        _rmtree(_cropped_path, ignore_errors=True)
        _rmtree(_tocrop_path, ignore_errors=True)
        _makedirs(_cropped_path, exist_ok=True)
        _copytree(_default_tocrop_path, _tocrop_path)

        config = _load_json(_rand_crop_config_loc)
        config["image_location"] = _tocrop1_loc
        config["output_path"] = _cropped_path
        _save_json(config, _rand_crop_config_loc)

    def tearDown(self):
        """Tears down after the tests."""
        super().tearDown()
        self._restore_cmd_configs()

        _rmtree(_cropped_path, ignore_errors=True)
        _rmtree(_tocrop_path, ignore_errors=True)

    def test_norm(self):
        """Tests the normal use case."""
        method_name = self.test_norm.__name__
        self._log_method_start(method_name)

        cmd = "widgets rand-crop"
        instr = "\n"
        thread = _FuncThread(target=_run_cmd, args=[cmd, instr])
        thread.start()
        exit_code, out, err = thread.join(_timeout)
        timed_out = thread.is_alive()

        self._log_cmdout(cmd, "stdout", out)
        self._log_cmdout(cmd, "stderr", err)

        fail_msg = "Running \"{}\" results in a timeout".format(cmd)
        self.assertTrue(timed_out is False, fail_msg)

        fail_msg = "Running \"{}\" results in an unexpected exit code: {}".format(cmd, exit_code)
        self.assertTrue(exit_code == 0, fail_msg)

        format_incorrect_info = "results format incorrect"

        isdir = _isdir(_cropped_path)
        fail_msg = "{} is not a directory; {}".format(_tocrop_path, format_incorrect_info)
        self.assertTrue(isdir, fail_msg)

        regexs_each = [
            _re_compile(r".*-At-.*-Crop-.*(-Resize-.*)?(-FlippedAround-(X|Y|XY))?-Time-.*\.jpg"),
        ]

        contents = _listdir(_cropped_path)

        for regex in regexs_each:

            for fname in contents:
                matched = bool(regex.match(fname))
                fail_msg = "File name {} in {} does not match pattern {}; {}".format(
                    fname, _cropped_path, str(regex), format_incorrect_info
                )
                self.assertTrue(matched, fail_msg)
            # end for

        # end for

        self._log_method_end(method_name)


def main():
    """Runs this module as an executable."""
    unittest.main(verbosity=1)


if __name__ == "__main__":
    main()
