from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive'
client_file = 'credentials.json'

def get_service(SCOPES,CLIENT_SECRET_FILE):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service

def get_folders(service):
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    return items

def create_folders(service,folder_names):
    file_metadata = {}
    metadata_list = []
    for folder in folder_names:
        file_metadata = {'name':folder,'mimeType': 'application/vnd.google-apps.folder'}
        
        file = service.files().create(body=file_metadata,
                                        fields='id').execute()
        print ('Folder ID: %s was created' % file.get('id'))

def delete_folders(service, folder_names):
    for folder in folder_names:
        try:
            file_id = folder['id']
            service.files().delete(fileId=file_id).execute()
        except:
            print('no folders to delete')

def retrieve_all_files(service):
    result = []
    page_token = None
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
                files = service.files().list(**param).execute()

                result.extend(files['items'])
                page_token = files.get('nextPageToken')
            if not page_token:
                break

        except errors.HttpError, error:
            print('An error occurred: %s' % error)
            break
    return result

if __name__ == '__main__':

    service = get_service(SCOPES,client_file)
    get_folders(service)
    #create_folders(creds,['Cob'])
    #folder_list = get_folders(creds)    
    #delete_folders(creds,folder_list)
    #print(folder_list)

    
   
    
    