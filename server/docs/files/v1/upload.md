# Upload File

This route stores the file on the server and adds a database entry

**URL**: `/rest/v1/files/upload`

**Method**: `POST`

**Auth Required**: `True`

**Body:**
(multipart/form-data)
```json
{
  "iv": "[bytes]",
  "encrypted_filename": "[bytes]",
  "file": "[file]"
}
```

**Success**:
```json
{
  "success": true,
  "data": {
    "id": "ea543800-7401-495e-a6e6-de244a121a2d",
    "encrypted_filename": null,
    "iv": null,
    "date_added": "2022-09-27T17:23:18.521Z"
  }
}
```
