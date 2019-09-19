#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import click

from ToDonePy.filer import Filer as Filer


@click.group()
@click.option(
    "--file",
    "-f",
    envvar="TODO_FILE",
    default=(Path.home() / "TODO.csv"),
    type=click.Path(exists=False),
    help="Location of TODO.csv",
)
@click.version_option(version="0.5.4")
@click.pass_context
def to(ctx, file: Path) -> None:
    """Base command for managing tasks

    :note: If you use a location other than the default for --file, 
        I'd recommend setting TODO_FILE as an environemtal variable
    """
    ctx.obj = Filer(Path(file), create=True)


@to.command()
@click.argument("task", required=True, help='Task to be added to your list')
@click.argument("rank", required=True, help='Priority to assign this task')
@click.pass_obj
def do(obj, task: str, rank: int) -> None:
    """Add a task to your list

    :note: If your task is more than 1 word long, enclose it in quotes

    """
    obj.append([",".join([str(rank), task])])
    click.echo("Task added")


@to.command()
@click.pass_obj
def doing(obj) -> None:
    """See tasks in your list

    """
    for line in obj.read():
        click.echo(line)


@to.command()
@click.argument("task", required=True, help='Task to be removed from your list')
@click.pass_obj
def done(obj, task: str) -> None:
    """Remove a task to your list

    :note: If multiple tasks match ``task``, they will all be deleted.

    :note: If your task is more than 1 word long, enclose it in quotes

    """
    obj.delete(task)
    click.echo("Task removed")
