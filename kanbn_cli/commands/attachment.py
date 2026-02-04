"""Attachment commands."""

import mimetypes
import os
import typer
import requests

from kanbn_cli.api.client import KanbnClient
from kanbn_cli.config import load_config
from kanbn_cli.utils.display import print_error, print_success, print_info
from kanbn_cli.utils.errors import KanbnError

app = typer.Typer(help="Manage attachments")


@app.command("upload")
def upload_attachment(
    card_id: str = typer.Argument(..., help="Card ID"),
    file_path: str = typer.Argument(..., help="Path to file"),
):
    """Upload an attachment to a card."""
    try:
        if not os.path.exists(file_path):
            print_error(f"File not found: {file_path}")
            raise typer.Exit(1)

        filename = os.path.basename(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "application/octet-stream"

        config = load_config()
        client = KanbnClient(config)

        # 1. Get presigned URL
        print_info(f"Getting upload URL for {filename}...")
        data = {
            "fileName": filename,
            "fileType": mime_type,
            "cardPublicId": card_id
        }
        presigned = client.post("attachments/presigned-url", json=data)
        
        upload_url = presigned.get("url")
        file_key = presigned.get("key")
        attachment_id = presigned.get("publicId")

        if not upload_url:
            print_error("Failed to get upload URL")
            raise typer.Exit(1)

        # 2. Upload file
        print_info("Uploading file...")
        with open(file_path, "rb") as f:
            response = requests.put(
                upload_url, 
                data=f, 
                headers={"Content-Type": mime_type}
            )
            response.raise_for_status()

        # 3. Confirm upload
        print_info("Confirming upload...")
        confirm_data = {
            "key": file_key,
            "fileName": filename,
            "fileType": mime_type,
            "cardPublicId": card_id
        }
        client.post(f"attachments/{attachment_id}/confirm", json=confirm_data)
        
        print_success(f"Attachment uploaded successfully: {filename}")

    except requests.RequestException as e:
        print_error(f"Upload failed: {str(e)}")
        raise typer.Exit(1)
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)


@app.command("delete")
def delete_attachment(
    attachment_id: str = typer.Argument(..., help="Attachment ID"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    """Delete an attachment."""
    try:
        if not confirm:
            confirm = typer.confirm(f"Are you sure you want to delete attachment {attachment_id}?")
            if not confirm:
                raise typer.Abort()

        config = load_config()
        client = KanbnClient(config)

        client.delete(f"attachments/{attachment_id}")
        print_success(f"Deleted attachment {attachment_id}")

    except typer.Abort:
        print_error("Cancelled")
        raise typer.Exit(1)
    except KanbnError as e:
        print_error(str(e))
        raise typer.Exit(1)
