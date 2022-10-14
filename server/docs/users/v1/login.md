# Login

This creates an access token for a user's id

**Method**: `POST`

**URL**: `/rest/v1/user/login`

**Auth Required**: `True`

**Success**:
```json
{
  "success": true,
  "data": {
    "user_id": "ae2713d2-b129-4bf6-b50e-fa58f5ebf744",
    "access_token": "f62ba500d2c38bc6c39b761b9b9fb0bdc242d2eb0d5dd5e4d7017dcf2e8ca243fb2ad370e8dc086569f1e864c38feb2e76f26c493992f9eecbe25207312cd6be"
  }
}
```
