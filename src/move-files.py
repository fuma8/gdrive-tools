
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

def get_files_in_folder(service, folder_id, mime_type='image/jpeg', only_direct_children=True):
    """指定フォルダ直下にある画像ファイルを取得"""
    query = f"'{folder_id}' in parents and mimeType contains '{mime_type}'"
    if only_direct_children:
        query += " and not mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, spaces='drive', fields='nextPageToken, files(id, name)').execute()
    return results.get('files', []), results

def main():
    service = get_credentials()
    source_folder_id = "1--HN68OiTRMqOYe5f1yiidlhlzu-MkTh"
    target_folder_id = "19tIIYAchN21M4-NgO1rnA4PlofhwLooD"
    page_token = None
    while True: 
        mime_type = 'application/x-tar' #image/jpeg 
        files, results = get_files_in_folder(service, source_folder_id, mime_type)
        if not files:
            print("ファイルが見つかりませんでした。")
            return
        for file in files:
            move_file_to_folder(service, file["id"], target_folder_id)
            print(f"{file['name']}を移動させました")
        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break


if __name__ == "__main__":
  main()

