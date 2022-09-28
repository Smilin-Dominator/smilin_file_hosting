# Update File

This route updates the file on the server and changes the database entry

**URL**: `/rest/v1/files/update`

**Method**: `PUT`

**Auth Required**: `True`

**Query Parameters:**
`file_id=[string]`

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
