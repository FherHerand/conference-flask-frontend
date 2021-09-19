$("#menu-toggle").click(function (e) {
  e.preventDefault();
  $("#wrapper").toggleClass("toggled");
});

var spinnerDiv = document.getElementById("spinner");
var content = document.getElementById("content");
var usernameTag = document.getElementById("username");
var profileTag = document.getElementById("profile");

activateSpinner = () => { spinnerDiv.innerHTML = `<div class="spinner-grow blue-gradient" role="status"></div>`; }
desactivateSpinner = () => { spinnerDiv.innerHTML = ``; }
function init() {
  desactivateSpinner();
  username = sessionStorage.getItem("username");
  if (username) {
    usernameTag.innerHTML = username;
    profileTag.src = `${sessionStorage.getItem("profile_image_path")}`;
    addStudentView()
  } else {
    logout();
  }
}

logout = function () {
  sessionStorage.clear();
  location.href = "./login.html"
}
init();

function getFormattedDate(timestamp) {
  let current_datetime = new Date(timestamp * 1000);
  let formatted_date =
    current_datetime.getDate()
    + "/" + (current_datetime.getMonth() + 1)
    + "/" + current_datetime.getFullYear()
    + " " + current_datetime.getHours() + ":"
    + current_datetime.getMinutes() + ":"
    + current_datetime.getSeconds();
  return formatted_date;
}

function addStudentView() {
  let html = `
    <h1>Agregar estudiante</h1>
    <form class="text-center border border-light p-5" action="#!">
      <div class="custom-file">
        <input type="file" class="custom-file-input" id="file" lang="es" onchange="onchangeFile()" accept="image/x-png,image/gif,image/jpeg">
        <label class="custom-file-label" for="customFileLang" id="labelFile">Seleccionar Archivo</label>
      </div>  
      <div class="md-form">
        <input type="text" id="name" class="form-control">
        <label for="name" class="active">Nombre de estudiante</label>
      </div>
      <div class="md-form">
        <input type="text" id="code" class="form-control">
        <label for="code" class="active">Código de estudiante</label>
      </div>
      <button type="button" class="btn blue-gradient" onclick="addStudent()">Agregar</button>
    </form>
  `;
  content.innerHTML = html;
}
onchangeFile = function () {
  let inputFile = document.getElementById("file");
  files = inputFile.files;
  inputFilename = document.getElementById("name");
  inputFilename.value = files[0].name.split('.')[0];

  document.getElementById("labelFile").innerHTML = files[0].name;
}
addStudent = function () {
  var file = document.getElementById('file').files[0];
  var name = document.getElementById('name').value;
  var code = document.getElementById('code').value;
  var reader = new FileReader();

  if (code.length > 0 && name.length > 0) {
    if (file) {
      activateSpinner();
      reader.onloadend = function () {
        data_uri = reader.result;

        let url = `${_config.API_SERVER_URL}/student`;
        data = {
          name: name,
          code: code,
          data_uri: data_uri
        };
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
              alert(`Estudiante [${data.code}] ${data.name} registrado`);
            } else {
              alert('Error');
            }
          },
          error: function (xhr, status, error) {
            desactivateSpinner();
            console.log(`ajax post error: ${xhr.status} ${xhr.responseText} ${status} ${error}`);
            var err = JSON.parse(xhr.responseText);
            alert(err.message);
          }
        });
      }
      reader.readAsDataURL(file);
    } else {
      alert("Cargar archivo");
    }
  }
  else {
    alert("Llene todos los campos");
  }
}

function listStudentView() {
  activateSpinner();
  html = `
  <h1>Listado de personas</h1>
  <table id="dtPerson" class="table table-striped table-bordered table-sm" cellspacing="0" width="100%">
    <thead class="thead-light">
      <tr>
        <th class="th-sm">Código</th> 
        <th class="th-sm">Nombre</th>
        <th class="th-sm">Foto</th>
      </tr>
    </thead>
    <tbody>`;

  let url = `${_config.API_SERVER_URL}/student`;
  $.ajax({
    type: "GET",
    url: url,
    contentType: "application/json",
    dataType: "json",
    success: function (data, status, xhr) {
      desactivateSpinner();
      if (xhr.status === 200) {
        console.log('data', data);
        for (i in data.items) {
          item = data.items[i];
          html += `
          <tr>
            <td>${item.code}</td>
            <td>${item.name}</td>
            <td><a href="${item.full_image_path}"><img src="${item.full_image_path}" height="100"></a></td>
          </tr>
          `;
        }
        html += `
          </tbody>
        </table>
        `;
        content.innerHTML = html;
      } else {
        alert('Error');
      }
    },
    error: function (xhr, status, error) {
      desactivateSpinner();
      console.log(`ajax get error: ${xhr.status} ${xhr.responseText} ${status} ${error}`);
      var err = JSON.parse(xhr.responseText);
      alert(err.message);

      html += `
        </tbody>
      </table>
      `;
      content.innerHTML = html;
    }
  });
}

function addAttendaceView() {
  let html = `
    <h1>Agregar asistencia</h1>
    <form class="text-center border border-light p-5" action="#!">
      <div class="custom-file">
        <input type="file" class="custom-file-input" id="file" lang="es" onchange="onchangeFile()" accept="image/x-png,image/gif,image/jpeg">
        <label class="custom-file-label" for="customFileLang" id="labelFile">Seleccionar Archivo</label>
      </div>
      <div class="md-form">
        <input type="text" id="name" class="form-control">
        <label for="name" class="active">Nombre de asistencia</label>
      </div>
      <div class="md-form">
        <input type="number" id="similarity" class="form-control" value="90" min="0" max="100" step="1">
        <label for="similarity" class="active">% Similitud</label>
      </div>
      <button type="button" class="btn blue-gradient" onclick="addAttendance()">Agregar</button>
    </form>
  `;
  content.innerHTML = html;
}
addAttendance = function () {
  var similarity = document.getElementById('similarity').value;
  var file = document.getElementById('file').files[0];
  var name = document.getElementById('name').value;
  var reader = new FileReader();

  if (name.length > 0 && similarity) {
    if (file) {
      activateSpinner();
      reader.onloadend = function () {
        data_uri = reader.result;

        let url = `${_config.API_SERVER_URL}/attendance`;
        data = {
          name: name,
          similarity: similarity,
          data_uri: data_uri
        };
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
              alert(`Asistencia ${data.name} registrada`);
            } else {
              alert('Error');
            }
          },
          error: function (xhr, status, error) {
            desactivateSpinner();
            console.log(`ajax post error: ${xhr.status} ${xhr.responseText} ${status} ${error}`);
            var err = JSON.parse(xhr.responseText);
            alert(err.message);
          }
        });
      }
      reader.readAsDataURL(file);
    } else {
      alert("Cargar archivo");
    }
  } else {
    alert("Llene todos los campos");
  }
}

function listAttendanceView() {
  activateSpinner();
  html = `
  <h1>Listado de asistencias</h1>`;

  let url = `${_config.API_SERVERLESS_URL}/attendance`
  $.ajax({
    type: "GET",
    url: url,
    contentType: "application/json",
    dataType: "json",
    success: function (data, status, xhr) {
      desactivateSpinner();
      if (xhr.status === 200) {
        console.log('data', data);
        data.items.sort(compareTimestamp);
        for (i in data.items) {
          item = data.items[i];
          html += `
          <table id="tdAttendance" class="table table-striped table-bordered table-sm" cellspacing="0" width="100%">
            <thead class="thead-light">
              <tr class="text-center">
                <th colspan="4" class="th-sm">
                  [${getFormattedDate(item.timestamp)}] ${item.name} - ${item.similarity}%    
                  <br/>
                  <a class="btn peach-gradient btn-sm" href="${item.full_image_path}" role="button">Descargar</a>
                </th>
              </tr>
              <tr>
                <th class="th-sm">Estudiante</th>
                <th class="th-sm">Foto</th>
                <th class="th-sm">Asistió</th>
              </tr>
            </thead>
            <tbody>`;
            for (s in item.students) {
              student = item.students[s]
              let assist = student.assist ? "checked" : "";
              html += `
                <tr>
                  <td>[${student.code}] ${student.name}</td>
                  <td><a href="${student.full_image_path}"><img src="${student.full_image_path}" height="100"></a></td>
                  <td>
                    <div class="custom-control custom-checkbox">
                      <input type="checkbox" class="custom-control-input" disabled ${assist}>
                      <label class="custom-control-label"></label>
                    </div>
                  </td>
                </tr>`;
            }
            html += `
              </tbody>
            </table>
            <br/>
            `;
          }
        content.innerHTML = html;
      } else {
        alert('Error');
      }
    },
    error: function (xhr, status, error) {
      desactivateSpinner();
      console.log(`ajax get error: ${xhr.status} ${xhr.responseText} ${status} ${error}`);
      var err = JSON.parse(xhr.responseText);
      alert(err.message);
    }
  });
}

compareTimestamp = function (a, b) {
  if (a.timestamp > b.timestamp) {
    return -1;
  }
  if (a.timestamp < b.timestamp) {
    return 1;
  }
  return 0;
}