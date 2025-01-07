
import os.path

from googleapiclient.errors import HttpError

from quickstart import get_credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]

def move_file_to_folder(service, file_id, target_folder_id):
    """ファイルを別のフォルダに移動"""
    file = service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    service.files().update(
        fileId=file_id,
        addParents=target_folder_id,
        removeParents=previous_parents,
        fields='id, parents'
    ).execute()

def main():
  try:
    drive_service = get_credentials()
    page_token = None
    while True:
        query = f"mimeType='image/jpeg'"
        response = drive_service.files().list(
            spaces="drive",
            q=query,
            fields='nextPageToken, files(id, name)',
            pageToken=page_token
        ).execute()
        target_folder_id = "1--HN68OiTRMqOYe5f1yiidlhlzu-MkTh"
        for file in response.get("files", []):
            move_file_to_folder(drive_service, file["id"], target_folder_id)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()

