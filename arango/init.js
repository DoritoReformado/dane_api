db._createDatabase("dane_db");

var users = require("@arangodb/users");

users.save("Dorito", "TUNOMETECABRASARAMAMBICHE123.");

users.grantDatabase("Dorito", "dane_db", "rw");