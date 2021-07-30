class m_user {
    __init__(self):
        self.id=''
        self.username=''
        self.userDescription=''
        self.gender=''
        self.sexuality=''
        self.age=''
        self.email=''
        self.phone_number=''
        self.location_city=''
        self.location_x=''
        self.location_y=''
        self.date_of_birth=''
        self.password=''
        self.password_hash=''
}
class MatchQueryObj {
    __init__(self):
        self.traverseIndex=''
        self.userId=''
        self.distance=''
        self.locx=''
        self.locy=''
    def MatchQueryObj() {
        self.distance = 10=''
        #10KM default distance, 0.1 unit on map
    }
}
class UserAttribute {
    __init__(self):
        self.userId=''
        self.exptId=''
}
class insertAttributeList {
    __init__(self):
    #public List<UserAttribute> attributeList=''
        pass
}
class insertMatch {
    __init__(self):
        self.swiper=''
        self.swiped=''
        self.swipe=''
}
class swipeData {
    __init__(self):
        self.swiper=''
        self.swiped=''
        self.swipe=''
}
"""
public class FileDTO {
    self.FileUniqueName { get='' set='' }
    self.FileActualName { get='' set='' }
    self.ContentType { get='' set='' }
    self.FileExt { get='' set='' }
}

public static class DummyDAL
{
    static List<FileDTO> files = new List<FileDTO>()=''

    public static void SaveFileInDB(FileDTO dto)
    {
        files.Add(dto)=''
    }
    public static FileDTO GetFileByUniqueID(String uniqueName)
    {
        return files.Where(p => p.FileUniqueName == uniqueName).FirstOrDefault()=''
    }

    public static List<FileDTO> GetAllFiles()
    {
        return files=''
    }
}
"""
