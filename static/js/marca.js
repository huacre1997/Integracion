function eliminateMarca(params) {
    let url=`../marca-llanta/${params}/delete/`
    console.log(url);
    Swal.fire({
        title: 'Está seguro?',
        text: "Desea desactivar esta marca?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminarlo!'
      }).then((result) => {
        if (result.isConfirmed) {
            fetch(url,{
                method:"POST",
               
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                  },
            }).then(data=>data.json()).then(response=>{
                if(response.status==200){
                    Swal.fire(
                        'Eliminado!',
                        "La marca fue eliminada",
                        'success'
                      )
                      tablaMarcas.ajax.reload()
                }else{
                    notificacion(1500,"Error","error","Ha ocurrido un error")
                }
            })
         
        }else{
          return false
        }
      })
}

var modal = document.getElementById('myModal');

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementById('myImg');
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
img.onclick = function(){
    modal.style.display = "block";
    modalImg.src = this.src;
    modalImg.alt = this.alt;
    captionText.innerHTML = this.alt;
}


// When the user clicks on <span> (x), close the modal
modal.onclick = function() {
    img01.className += " out";
    setTimeout(function() {
       modal.style.display = "none";
       img01.className = "modal-content-vehiculo";
     }, 400);
    
 }