# List Files

This returns an array of files belonging to a user

**URL**: `/rest/v1/files/list`

**Method**: `GET`

**Auth Required**: `True`

**Query Parameters:**
  `page_state=[string]`
  `limit=[integer]`

**Success**:
```json
{
  "success": true,
  "data": {
    "page_state": "00120010973904931d984d179cb84d51cfd65f52f07ffffff5f07ffffff5",
    "files": [
      {
        "id": "0c3d52da-48bc-4e50-9987-0f5a1c860bbf",
        "encrypted_filename": null,
        "iv": null,
        "date_added": "2022-09-27T17:20:56.549Z"
      },
      {
        "id": "1cfcdcc6-c898-47b4-9d83-dfa690e9fce1",
        "encrypted_filename": null,
        "iv": null,
        "date_added": "2022-09-27T17:23:18.518Z"
      },
      {
        "id": "2b356d79-db89-4043-90e5-9c804faac035",
        "encrypted_filename": null,
        "iv": null,
        "date_added": "2022-09-27T17:23:18.516Z"
      },
      {
        "id": "30c32268-ee87-4ad6-82c2-53f0b3359854",
        "encrypted_filename": null,
        "iv": null,
        "date_added": "2022-09-27T13:40:07.813Z"
      },
      {
        "id": "341f6161-6eb8-43c1-a7cb-3a86985900f4",
        "encrypted_filename": null,
        "iv": null,
        "date_added": "2022-09-27T17:23:18.519Z"
      },
      {
        "id": "3c7c8daf-ade0-4976-9de5-12c3ab852f54",
        "encrypted_filename": null,
        "iv": null,
        "date_added": "2022-09-27T17:23:18.517Z"
      },
      {
        "id": "426255a3-6d0d-4cc4-addf-ceb1a9ae9632",
        "encrypted_filename": null,
        "iv": null,
        "date_added": "2022-09-27T17:20:12.970Z"
      },
      {
        "id": "5ffaa1ef-c9d2-42dc-8d59-c672c68f416d",
        "encrypted_filename": null,
        "iv": null,
        "date_added": "2022-09-27T13:40:45.327Z"
      },
      {
        "id": "659e98f5-35dc-4c10-aee1-35fa58cbfdd9",
        "encrypted_filename": null,
        "iv": null,
        "date_added": "2022-09-27T17:23:18.515Z"
      },
      {
        "id": "97390493-1d98-4d17-9cb8-4d51cfd65f52",
        "encrypted_filename": null,
        "iv": null,
        "date_added": "2022-09-27T13:40:58.904Z"
      }
    ]
  }
}
```
