let uploadedFiles = [];  // тут будут храниться файлы
let maximumFilesCount = 3;

document.addEventListener("DOMContentLoaded", function() {
  let face_files_input = document.getElementById('face_file');
  face_files_input.addEventListener("change", handleFilesInput, false);

  let dropbox = document.getElementById("dragndrop_upload");
  dropbox.addEventListener("dragenter", onDragenter, false);
  dropbox.addEventListener("dragover", onDragover, false);
  dropbox.addEventListener("drop", onDrop, false);

  let submit_button = document.getElementById('send_button');
  submit_button.addEventListener('click', function () {
    this.classList.add("is-loading");
    this.disabled = true;
    let album_link = document.getElementById('album_link').value;
    if (!album_link) {
      alert("Не все данные введены");
    } else {
      makeRequest(album_link, uploadedFiles)
    }
  });

  allow_uploading(true);

});

function onDragenter(e) {
  e.stopPropagation();
  e.preventDefault();
}

function onDragover(e) {
  e.stopPropagation();
  e.preventDefault();
}

function onDrop(e) {
  e.stopPropagation();
  e.preventDefault();

  let dt = e.dataTransfer;
  let files = dt.files;

  addToUploads(files);
}


function allow_uploading(allow_status) {
  let fileInput = document.getElementById('add_file_button');
  let dragndropInput = document.getElementById('dragndrop_upload');

  fileInput.disabled = !allow_status;
  allow_status ? dragndropInput.classList.remove("disabled") : dragndropInput.classList.add("disabled")
}

function updateUploadsList() {
  console.log(uploadedFiles);
  let uploading_files_list = document.getElementById('uploading_files_list');
  uploading_files_list.innerHTML = "";

  for (let i=0;i<uploadedFiles.length;i++) {
    console.log(i);
    let newParagraph = document.createElement("p");
    newParagraph.innerHTML = uploadedFiles[i].name;
    uploading_files_list.appendChild(newParagraph);
  }

  uploadedFiles.forEach(file => function() {
    console.log("smth");
    let newParagraph = document.createElement("p");
    newParagraph.innerHTML = file.name;
    uploading_files_list.appendChild(newParagraph);
  });
}

function addToUploads(files) {
  if (!files) {
    console.log("No files to add");
  } else {
    let allowedLen = (uploadedFiles.length+files.length) > maximumFilesCount ?
        maximumFilesCount - uploadedFiles.length : files.length
    for (let i=0;i<allowedLen;i++) {
      uploadedFiles.push(files[i])
    }

    if (uploadedFiles.length >= 3) {
      allow_uploading(false);
    } else {
      allow_uploading(true);
    }

    updateUploadsList();
  }
}

function handleFilesInput() {
  console.log(this.files)
  addToUploads(this.files)
}


function makeRequest(album_link, files) {
  let formData = new FormData();

  for (let i=0;i<files.length;i++) {
    formData.append("face_file", files[i]);
  }
  formData.append("album_link", album_link);

  let response = fetch("/api/new_request", {
    method: "POST",
    body: formData
  });

  response.then(data => {
    console.log("asdasd")
    console.log(data);
    console.log(data.json());
  });
  console.log(response);
}


function getRequestStatus(request_id) {

  let response = fetch("/api/get_status", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "request_id": request_id,
    })
  });

  response.then(data => {
    console.log(data);
    console.log(data.json());
  });
  console.log(response);

}