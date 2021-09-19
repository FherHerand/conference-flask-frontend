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

var spinnerDiv = document.getElementById("spinner");
var content = document.getElementById("content");
activateSpinner = () => { spinnerDiv.innerHTML = `<div class="spinner-grow blue-gradient" role="status"></div>`; }
desactivateSpinner = () => { spinnerDiv.innerHTML = ``; }
function init() {
  desactivateSpinner();
  username = sessionStorage.getItem("username");
  if (username) {
    location.href = "./index.html";
  }
}

login_with_credentials = function () {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;

  if (username.length > 0 && password.length > 0) {

    let url = `${_config.API_SERVER_URL}/login`;
    data = {
      username: username,
      password: password,
      type: 'credentials',
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
    alert("Llene todos los campos");
  }
}

login_with_camera = function () {
  Webcam.snap(function (data_uri) {
    document.getElementById('results').innerHTML = '<img src="' + data_uri + '"/>';

    let url = `${_config.API_SERVER_URL}/login`;
    data = {
      data_uri: data_uri,
      type: 'camera'
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
  });
}

signup = function () {
  location.href = "./signup.html"
}

init();