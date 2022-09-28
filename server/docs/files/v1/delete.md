# Delete File

This route deletes the file from the server and deletes the database entry

**URL**: `/rest/v1/files/delete`

**Method**: `DELETE`

**Auth Required**: `True`

**Query Parameters:**
`file_id=[string]`

**Success:**
```json
{
  "success": true
}
```

**No File:**
```json
{
    "success": false,
    "error": "No such file exists!"
}
```
