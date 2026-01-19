import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configuració
SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_ID = os.environ['GDRIVE_FOLDER_ID'] # Llegeix del Secret de GitHub
FILE_NAME = 'examen.pdf' # El nom que surt del LaTeX

def authenticate():
    # Carreguem les credencials des del fitxer temporal que crearà el workflow
    creds = service_account.Credentials.from_service_account_file(
        'credentials.json', scopes=SCOPES)
    return creds

def upload_file():
    try:
        creds = authenticate()
        service = build('drive', 'v3', credentials=creds)

        # Afegim data al nom per no tenir duplicats confusos
        data_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        nom_final = f"Examen_{data_actual}.pdf"

        file_metadata = {
            'name': nom_final,
            'parents': [FOLDER_ID]
        }
        
        media = MediaFileUpload(FILE_NAME, mimetype='application/pdf')

        print(f"Pujant {nom_final} a Drive...")
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f'Èxit! Fitxer pujat amb ID: {file.get("id")}')
        
    except Exception as e:
        print(f"Error pujant el fitxer: {e}")
        exit(1)

if __name__ == '__main__':
    upload_file()