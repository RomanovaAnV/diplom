// let app = new Vue({
//   el: '#app',
//   data: {
//     requestFiles: FileList(),
//   },
//   delimiters: ['[[', ']]'],
//   methods: {
//     handleFileUpload: handleFileUpload(),
//     sendButtonListener: sendButtonListener(),
//   }
// })

let uploadedFiles = [];  // тут будут храниться файлы
let maximumFilesCount = 3;

document.addEventListener("DOMContentLoaded", function() {

  let socket = new WebSocket("ws://localhost:5000");
  socket.onmessage = function(event) {
    alert("Получены данные " + event.data);
  };


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

  // if (uploadedFiles.length < maximumFilesCount) {
  addToUploads(files);
  // }
}


function allow_uploading(allow_status) {
  let fileInput = document.getElementById('add_file_button');
  let dragndropInput = document.getElementById('dragndrop_upload');

  fileInput.disabled = !allow_status;
  // dragndropInput.disabled = !allow_status;
  allow_status ? dragndropInput.classList.remove("disabled") : dragndropInput.classList.add("disabled")

  // if (allow_status) {
  //   fileInput.disabled = true;
  //   dragndropInput.disabled = true;
  //   // fileInput.setAttribute("disabled", "enabled");
  //   // fileInput.setAttribute("visibility", "visible");
  //   // dragndropInput.setAttribute("visibility", "visible");
  //   // fileInput.style.visibility = "visible";
  //   // dragndropInput.style.visibility = "visible";
  //   // fileInput.style.display = "block";
  //   // dragndropInput.style.display = "block";
  // } else {
  //   fileInput.disabled = false;
  //   dragndropInput.disabled = false;
  //   // fileInput.setAttribute("disabled", "disabled");
  //   // fileInput.setAttribute("visibility", "hidden");
  //   // dragndropInput.setAttribute("visibility", "hidden");
  //   // fileInput.style.visibility = "hidden";
  //   // dragndropInput.style.visibility = "hidden";
  //   // fileInput.style.display = "none";
  //   // dragndropInput.style.display = "none";
  //   // alert(allow_status);
  // }
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
    // if (!uploadedFiles) {
    //   uploadedFiles = files;
    // } else {

    let allowedLen = (uploadedFiles.length+files.length) > maximumFilesCount ?
        maximumFilesCount - uploadedFiles.length : files.length
    for (let i=0;i<allowedLen;i++) {
      uploadedFiles.push(files[i])
    }
      // uploadedFiles.push(...files.slice(0, 3-uploadedFiles.length));
    // }
    // let uploadedFilesLen = !uploadedFiles ? 0 : 3-uploadedFiles.length;
    // uploadedFiles.push(...files.slice(0, uploadedFilesLen));

    if (uploadedFiles.length >= 3) {
      allow_uploading(false);
    } else {
      allow_uploading(true);
    }

    updateUploadsList();
  }
}

function handleFilesInput() {
  // const fileList = this.files; /* now you can work with the file list */
  // uploadedFiles.push(...this.files.slice(0, 3-uploadedFiles.length));
  console.log(this.files)
  addToUploads(this.files)
}

function uploadFiles() {

}

// function sendButtonListener() {
//   let files = document.getElementById('face_file').file.files;
//   let formData = new FormData();
//   files.forEach(file => formData.append('face_file', file)); // добавление файлов из формы в запрос
//
// }

// function handleFileUpload() {
//
// }

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

  response.then(data => console.log(data));
  console.log(response);
}