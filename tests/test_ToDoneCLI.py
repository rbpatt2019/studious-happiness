#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime as dt
from pathlib import Path
from shutil import which

import pytest
from click.testing import CliRunner

from command_line.ToDoneCLI import to
from tests.make_temp import make_file, make_path


def test_to_do_custom_file(tmp_path):
    """Run to do with existing custom file"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        tsv = make_file(
            tmp_path, "ID\tRank\tDate\tTask\n1\t1\t2019-09-20 20:56:00\tOld task\n"
        )
        result = runner.invoke(to, ["--file", f"{tsv}", "do", "1", "New task"])
        date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        assert result.exit_code == 0
        assert result.output == "1 task(s) added!\n"
        assert (
            Path(tsv).read_text()
            == f"ID\tRank\tDate\tTask\n1\t1\t2019-09-20 20:56:00\tOld task\n2\t1\t{date}\tNew task\n"
        )


def test_to_doing_custom_file(tmp_path):
    """Run to doing with existing custom file"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        tsv = make_file(
            tmp_path,
            "ID\tRank\tDate\tTask\n1\t2\t2019-09-20 20:56:00\tOld task\n2\t1\t2019-09-24 12:57:00\tNew task\n3\t1\t2019-09-23 12:57:00\tNew task\n",
        )
        result = runner.invoke(to, ["--file", f"{tsv}", "doing"])
        assert result.exit_code == 0
        assert (
            result.output
            == "ID\tRank\tDate\tTask\n1\t2\t2019-09-20 20:56:00\tOld task\n2\t1\t2019-09-24 12:57:00\tNew task\n3\t1\t2019-09-23 12:57:00\tNew task\nYou do not have 5 tasks!\n"
        )
        assert (
            Path(tsv).read_text()
            == "ID\tRank\tDate\tTask\n1\t2\t2019-09-20 20:56:00\tOld task\n2\t1\t2019-09-24 12:57:00\tNew task\n3\t1\t2019-09-23 12:57:00\tNew task\n"
        )


@pytest.mark.xfail(reason="Vim hangs the test, resulting in non-0 exit code")
def test_to_doing_custom_file_edit_flag(tmp_path):
    """Run to doing with the edit flag"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        tsv = make_file(
            tmp_path,
            "2,Old task,2019-09-20 20:56:00\n1,New task,2019-09-24 12:57:00\n1,New task,2019-09-23 12:57:00\n",
        )
        result = runner.invoke(to, ["--file", f"{tsv}", "doing", "--edit"])
        assert result.exit_code == 0
        assert result.output == ""


def test_to_doing_custom_file_sort_flag(tmp_path):
    """Run to doing with the --sort flag"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        tsv = make_file(
            tmp_path,
            "ID\tRank\tDate\tTask\n1\t2\t2019-09-20 20:56:00\tOld task\n2\t1\t2019-09-24 12:57:00\tNew task\n3\t1\t2019-09-23 12:57:00\tNew task\n",
        )
        result = runner.invoke(to, ["--file", f"{tsv}", "doing", "--sort", "rank"])
        assert result.exit_code == 0
        assert (
            result.output
            == "ID\tRank\tDate\tTask\n1\t1\t2019-09-24 12:57:00\tNew task\n2\t1\t2019-09-23 12:57:00\tNew task\n3\t2\t2019-09-20 20:56:00\tOld task\nYou do not have 5 tasks!\n"
        )
        assert (
            Path(tsv).read_text()
            == "ID\tRank\tDate\tTask\n1\t1\t2019-09-24 12:57:00\tNew task\n2\t1\t2019-09-23 12:57:00\tNew task\n3\t2\t2019-09-20 20:56:00\tOld task\n"
        )


@pytest.mark.skipif(which("notify-send") is None, reason="Requires notify-send")
def test_to_doing_custom_file_graphic_flag(tmp_path):
    """Run to doing with the --graphic flag"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        tsv = make_file(
            tmp_path,
            "2\t2019-09-20 20:56:00\tOld task\n1\t2019-09-24 12:57:00\tNew task\n1\t2019-09-23 12:57:00\tNew task\n",
        )
        result = runner.invoke(to, ["--file", f"{tsv}", "doing", "--graphic"])
        assert result.exit_code == 0
        assert result.output == ""


def test_to_done_custom_file(tmp_path):
    """Run to done with existing custom file"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        tsv = make_file(
            tmp_path,
            "ID\tRank\tDate\tTask\n1\t2\t2019-09-20 20:56:00\tOld task\n2\t1\t2019-09-24 12:57:00\tNew task\n",
        )
        result = runner.invoke(to, ["--file", f"{tsv}", "done", "New task", "Nothing"])
        assert result.exit_code == 0
        assert (
            result.output
            == 'Task "New task" successfully deleted!\nTask "Nothing" not in TODO.tsv...\n'
        )
        assert (
            Path(tsv).read_text()
            == "ID\tRank\tDate\tTask\n1\t2\t2019-09-20 20:56:00\tOld task\n"
        )
