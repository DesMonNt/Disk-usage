from datetime import datetime
from pathlib import Path
import asyncio
import click
from disk_usage import DiskAnalyzer, FileFilter


@click.group()
def cli():
    """Disk usage analyzer CLI."""
    pass


@cli.command()
@click.option('--root', type=click.Path(exists=True, file_okay=False, path_type=Path), default='.',
              help='Root directory for analysis')
@click.option('--extension', type=str, default=None, help='Filter by file extension (e.g., .txt)')
@click.option('--owner', type=str, default=None, help='Filter by file owner')
@click.option('--min-size', type=int, default=None, help='Minimum file size in bytes')
@click.option('--max-size', type=int, default=None, help='Maximum file size in bytes')
@click.option('--time', type=datetime, default=None, help='Latest changes time')
@click.option('--level', type=int, default=None, help='Directory depth')
def filter(root, extension, owner, min_size, max_size, time, level):
    """Analyze disk usage and filter files."""
    asyncio.run(_filter(root, extension, owner, min_size, max_size, time, level))


@cli.command()
@click.option('--root', type=click.Path(exists=True, file_okay=False, path_type=Path), default='.',
              help='Root directory for disk usage analysis')
def disk_usage(root):
    """Show disk usage for the specified directory."""
    asyncio.run(_show_disk_usage(root))


@cli.command()
@click.option('--root', type=click.Path(exists=True, file_okay=False, path_type=Path), default='.',
              help='Root directory for disk usage analysis')
@click.option('--by', type=click.Choice(['extension', 'owner', 'level'], case_sensitive=False),
              required=True, help='Group files by extension, owner, or level')
def group(root, by):
    asyncio.run(_group(root, by))


async def _show_disk_usage(root):
    analyzer = DiskAnalyzer(root)
    used, total = await analyzer.disk_usage()

    click.echo(f"Disk usage for '{root}': {(100 * used / total):.2f}% used "
               f"({used / (1024 ** 3):.2f} GB of {total / (1024 ** 3):.2f} GB)\n")


async def _filter(root, extension, owner, min_size, max_size, time, level):
    files = await _run_analysis(root)

    if extension:
        filter = FileFilter(files)
        files = filter.filter_by_extension(extension)
    if owner:
        filter = FileFilter(files)
        files = filter.filter_by_owner(owner)
    if min_size or max_size:
        filter = FileFilter(files)
        files = filter.filter_by_size(min_size, max_size)
    if time:
        filter = FileFilter(files)
        files = filter.filter_by_time(time)
    if level:
        filter = FileFilter(files)
        files = filter.filter_by_level(level)

    for file in files:
        click.echo(f"{file.path} \n\tSize: {file.size} bytes \n\tOwner: {file.owner} \n\tLast modified: {file.mtime}\n")


async def _group(root, group_by):
    files = await _run_analysis(root)
    filter = FileFilter(files)

    if group_by == 'extension':
        files = filter.group_by_extension()
    elif group_by == 'owner':
        files = filter.group_by_owner()
    elif group_by == 'level':
        files = filter.group_by_level()

    for key, group in files:
        click.echo(f"\n{key}:")

        for file in group:
            click.echo(f"\t{file.path}")


async def _run_analysis(root):
    analyzer = DiskAnalyzer(root)
    task = asyncio.create_task(analyzer.analyze())

    click.echo(f"\nAnalyzing directory: '{root}'")

    while not task.done():
        progress = analyzer.current_progress
        click.echo(f"\r|{('#' * int(progress / 2)).ljust(50)}| {progress:.2f}% Complete", nl=False)

        await asyncio.sleep(0.1)

    progress = analyzer.current_progress
    click.echo(f"\r|{('#' * int(progress / 2)).ljust(50)}| {progress:.2f}% Complete")

    return analyzer.files


if __name__ == "__main__":
    try:
        cli()
    except (PermissionError, FileNotFoundError) as e:
        click.echo(f"Error: {e}")
