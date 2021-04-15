function upload_data(files,link){
upload={
  face_files:files.push(0,3),
  album_link:link
}
json=JSON.stringify(upload)
alert(json)
};