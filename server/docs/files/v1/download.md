# Download File

This sends the file as an octet stream

**URL**: `/rest/v1/files/download`

**Method**: `GET`

**Auth Required**: `True`

**Query Parameters:**
`file_id=[string]`

**Success**:
`File Response`

**File Doesn't Exist**:
```json
{
  "success": false,
  "error": "No such file exists!"
}
```
