
import os.path

from googleapiclient.errors import HttpError

from quickstart import get_credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]


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
        for file in response.get("files", []):
            try:
                deleted_file = drive_service.files().delete(fileId=file['id']).execute()
                print(f"Deleted: {file['name']}")
            except Exception as e:
                print(f"Failed to delete {file['name']}: {e}")
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()

