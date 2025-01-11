import tarfile

from quickstart import get_credentials
from move_files import get_files_in_folder

def main():
    service = get_credentials()
    source_folder_id = '1--HN68OiTRMqOYe5f1yiidlhlzu-MkTh'
    while True:
        mime_type = 'image/jpeg'
        files, results = get_files_in_folder(service, source_folder_id, mime_type)
        if not files:
            print("ファイルが見つかりませんでした。")
            break
        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break
    

if __name__ == "__main__":
    main()