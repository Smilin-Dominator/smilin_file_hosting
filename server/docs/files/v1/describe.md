# Describe File

This returns the id, encrypted filename, iv and the date the file was uploaded

**URL**: `/rest/v1/files/describe`

**Method**: `GET`

**Auth Required**: `True`

**Query Parameters:**
`file_id=[string]`

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
