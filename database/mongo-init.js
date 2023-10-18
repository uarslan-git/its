use('admin')

db.createUser(
    {
      user: "backend_service_user",
      pwd: process.env.DB_SERVICE_PW,
      roles: [ { role: "readWrite", db: "its_db" } ]
    }
  )