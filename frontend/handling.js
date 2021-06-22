// const cmt_btn=document.getElementById('cmt-btn');
// if(cmt_btn){

//     cmt_btn.addEventListener('submit',function(e){
//         e.preventDefault();
//         e.preventDefault();
    
//         const formData=new FormData(this);
    
    
//         fetch('https://shivamjain123.pythonanywhere.com/comment-api/2',{
//             method:'POST',
//             body:formData
//         }).then(function(response){
//              return response.text();
//         }).then(function(text){
//             console.log(text);
//         }).catch(function(error){
//             console.error(error);
//         })
//     });
// }


// // popup handler
const popu=document.getElementById("popup-handler");
console.log("success");
const tag_con=document.getElementById("tag-cont");
popu.onclick= () =>{
    tag_con.classList.toggle("d-none");

}
console.log(popu);




// const options={
//     headers: {
//         'Content-Type': 'application/json'
//       },
//     method:'POST',
//     body: JSON.stringify(data)
// };
// fetch('https://shivamjain123.pythonanywhere.com/comment-api',options);

