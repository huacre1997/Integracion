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


// Get the image and insert it inside the modal - use its "alt" text as a caption
