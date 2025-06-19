from datetime import datetime, timezone
from typing import Optional
from beanie import Document, before_event, Insert


class UserModel(Document):
    id: int
    
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    
    pm_active: bool = True
    
    created_at: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    
    class Settings:
        name = "users"
        use_state_management = True
    
    @before_event(Insert)
    async def set_date(self):
        self.created_at = datetime.now(timezone.utc)
        self.last_seen = datetime.now(timezone.utc)
        