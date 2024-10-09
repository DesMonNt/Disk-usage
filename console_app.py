from pathlib import Path
import asyncio
import asyncclick as click
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
@click.option('--min-time', type=str, default=None, help='Minimal latest changes time. Format: dd.mm.yy')
@click.option('--max-time', type=str, default=None, help='Maximal latest changes time. Format: dd.mm.yy')
@click.option('--level', type=int, default=None, help='Directory depth')
async def filter(root, extension, owner, min_size, max_size, min_time, max_time, level):
    """Analyze disk usage and filter files."""
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
    if min_time or max_time:
        filter = FileFilter(files)
        files = filter.filter_by_time(min_time, max_time)
    if level:
        filter = FileFilter(files)
        files = filter.filter_by_level(level)

    for file in files:
        click.echo(f"{file.path} \tSize: {file.size} bytes \tOwner: {file.owner} \tLast modified: {file.mtime}")


@cli.command()
@click.option('--root', type=click.Path(exists=True, file_okay=False, path_type=Path), default='.',
              help='Root directory for disk usage analysis')
async def disk_usage(root):
    """Show disk usage for the specified directory."""
    analyzer = DiskAnalyzer(root)
    used, total = await analyzer.disk_usage()

    click.echo(f"Disk usage for '{root}': {(100 * used / total):.2f}% used "
               f"({used / (1024 ** 3):.2f} GB of {total / (1024 ** 3):.2f} GB)\n")


@cli.command()
@click.option('--root', type=click.Path(exists=True, file_okay=False, path_type=Path), default='.',
              help='Root directory for disk usage analysis')
@click.option('--by', type=click.Choice(['extension', 'owner', 'level'], case_sensitive=False),
              required=True, help='Group files by extension, owner, or level')
async def group(root, by):
    """Analyze disk usage and group files."""
    files = await _run_analysis(root)
    filter = FileFilter(files)

    if by == 'extension':
        files = filter.group_by_extension()
    elif by == 'owner':
        files = filter.group_by_owner()
    elif by == 'level':
        files = filter.group_by_level()

    for key, group in files:
        click.echo(f"\n{key}:")

        for file in group:
            click.echo(f"\t{file.path}")


async def _run_analysis(root):
    analyzer = DiskAnalyzer(root)
    task = asyncio.create_task(analyzer.analyze())

    click.echo(f"\nAnalyzing directory: '{root}'\n")

    while not task.done():
        progress = analyzer.current_progress
        click.echo(f"\r|{('#' * int(progress / 2)).ljust(50)}| {progress:.2f}% Complete", nl=False)

        await asyncio.sleep(0.1)

    progress = analyzer.current_progress
    click.echo(f"\r|{('#' * int(progress / 2)).ljust(50)}| {progress:.2f}% Complete\n")

    return analyzer.files


if __name__ == "__main__":
    try:
        cli()
    except (PermissionError, FileNotFoundError) as e:
        click.echo(f"Error: {e}")
