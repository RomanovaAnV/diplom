function clickHandler(){
files=document.getElementById("files").value;
link=document.getElementById("link").value;
upload_data={
  face_files:files,
  album_link:link
}
json=JSON.stringify(upload_data)
  var url = 'https://findmychild.com/new_request'
  var xhr = new XMLHttpRequest()
  xhr.open('POST', url, true)
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
  xhr.send(json)
}