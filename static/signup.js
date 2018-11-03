$(document).ready(function() {
  $(".ui.form").form({
    fields: {
      username: {
        identifier: "username",
        rules: [
          {
            type: "empty",
            prompt: "Please enter Username"
          }
        ]
      },
      password: {
        identifier: "password"
      },
      name: {
        identifier: "name"
      },
      email: {
        identifier: "email"
      }
    }
  });
});
