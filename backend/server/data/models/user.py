class User:
  def __init__(self, id, username, password=None, googleid=None, email=None, createdat=None,):
    self.id = id
    self.username = username
    self.createdat = createdat
    self.password = password
    self.googleid = googleid
    self.email = email

  @classmethod
  def from_obj(cls, obj):
    return cls(
      id=obj.get('id'),
      username=obj.get('username'),
      createdat=obj.get('createdat'),
      password=obj.get('password'),
      googleid=obj.get('googleid'),
      email=obj.get('email')
    )

  def __str__(self):
    return f"User {self.username} created at {self.createdat}"
  
  def to_dto(self):
    """Return a dictionary representation of user for the forntend"""
    return {
      'username': self.username,
      'email': self.email
    }