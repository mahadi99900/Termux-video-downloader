import os
import sys
import subprocess
from rich.console import Console
from rich.progress import Progress, BarColumn, DownloadColumn, TextColumn
from rich.panel import Panel
from rich import box

console = Console()
DOWNLOAD_PATH = "/sdcard/Download"

# ──────────────── ASCII Banner ────────────────
def show_banner():
    console.clear()
    banner = """
████████╗███████╗██████╗ ███████╗███╗   ███╗
╚══██╔══╝██╔════╝██╔══██╗██╔════╝████╗ ████║
   ██║   █████╗  ██████╔╝█████╗  ██╔████╔██║
   ██║   ██╔══╝  ██╔═══╝ ██╔══╝  ██║╚██╔╝██║
   ██║   ███████╗██║     ███████╗██║ ╚═╝ ██║
   ╚═╝   ╚══════╝╚═╝     ╚══════╝╚═╝     ╚═╝
    """
    console.print(Panel(banner, title="[bold cyan]Termux Video Downloader[/bold cyan]", box=box.DOUBLE))

# ──────────────── Download Video Function ────────────────
def download_video(url: str):
    # Automatic filename based on video title
    cmd_info = ["yt-dlp", "--get-title", url]
    try:
        title = subprocess.check_output(cmd_info, text=True).strip()
        safe_title = "".join(c if c.isalnum() or c in " _-." else "_" for c in title)
        filename = f"{safe_title}.mp4"
    except Exception:
        filename = "video.mp4"

    file_path = os.path.join(DOWNLOAD_PATH, filename)

    cmd_download = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",
        "-o", file_path,
        url
    ]

    console.print(f"[bold blue]Downloading:[/bold blue] {filename}\n")

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        transient=True
    ) as progress:
        task = progress.add_task("Downloading...", total=100)
        process = subprocess.Popen(cmd_download, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            line = line.strip()
            if "%" in line:
                try:
                    percent_str = line.split("%")[0].split()[-1]
                    percent = float(percent_str)
                    progress.update(task, completed=percent)
                except:
                    pass
        process.wait()

    if os.path.exists(file_path):
        console.print(f"[green]✅ Download Complete! File saved at:[/green] {file_path}")
    else:
        console.print("[red]❌ Download failed. Please check the link or your internet connection.[/red]")

# ──────────────── Main Menu ────────────────
def main():
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)

    show_banner()
    console.print("[bold yellow]Enter video URL to download (type 'exit' to quit):[/bold yellow]")

    while True:
        url = console.input(">> ").strip()
        if url.lower() == "exit":
            console.print("[bold red]Exiting...[/bold red]")
            sys.exit(0)
        if not url:
            continue
        try:
            download_video(url)
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

        console.print("\n[bold cyan]You can enter another URL or type 'exit' to quit.[/bold cyan]")

if __name__ == "__main__":
    main()