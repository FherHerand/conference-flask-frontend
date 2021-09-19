$("#menu-toggle").click(function (e) {
  e.preventDefault();
  $("#wrapper").toggleClass("toggled");
});

Webcam.set({
  width: 320,
  height: 240,
  image_format: 'jpeg',
  jpeg_quality: 90
});
Webcam.attach('#my_camera');

var hasSnapshot = false;
var base64String = "";
var data_uri_global = "";
var indicator = document.getElementById("indicator");

function take_snapshot() {
  Webcam.snap(function (data_uri) {
    data_uri_global = data_uri;
    document.getElementById('results').innerHTML = '<img src="' + data_uri + '"/>';
    base64String = data_uri.split(',')[1];
    hasSnapshot = true;
    indicator.className = "badge badge-success badge-pill";
    indicator.textContent = "✓"
    //console.log("base64:", base64String);
  });
}

var spinnerDiv = document.getElementById("spinner");
var content = document.getElementById("content");
activateSpinner = () => { spinnerDiv.innerHTML = `<div class="spinner-grow blue-gradient" role="status"></div>`; }
desactivateSpinner = () => { spinnerDiv.innerHTML = ``; }
function init() {
  desactivateSpinner();
}

var cognitoUser = null;
register = function () {
  name = document.getElementById("name").value;
  username = document.getElementById("username").value;
  password = document.getElementById("password").value;
  password_confirm = document.getElementById("password_confirm").value;

  if (name.length > 0 && username.length > 0 && password.length > 0 && password_confirm.length > 0) {
    if (password === password_confirm) {
      if (password.length >= 6) {
        let url = `${_config.API_SERVER_URL}/register`;
        data = {
          name: name,
          username: username,
          password: password,
          data_uri: data_uri_global,
        }
        $.ajax({
          type: "POST",
          url: url,
          data: JSON.stringify(data),
          contentType: "application/json",
          dataType: "json",
          success: function (data, status, xhr) {
            desactivateSpinner();
            if (xhr.status === 200) {
              console.log('data', data);
              sessionStorage.setItem("name", data.name);
              sessionStorage.setItem("username", data.username);
              sessionStorage.setItem("profile_image_path", data.profile_image_path);
              location.href = "./index.html"
            } else {
              alert('Error');
              location.href = "./login.html"
            }
          },
          error: function (xhr, status, error) {
            desactivateSpinner();
            console.log(`ajax post error: ${xhr.status} ${xhr.responseText} ${status} ${error}`);
            var err = JSON.parse(xhr.responseText);
            alert(err.message);
          }
        });
      } else {
        alert("La contraseña debe ser de 6 caracteres como mínimo");
      }
    } else {
      alert("Las contraseñas no coinciden");
    }
  } else {
    alert("Llene todos los datos");
  }
}

init();