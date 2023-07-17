let expand_more = document.querySelector('.expand-more');
let expand_more_items = document.querySelector('.expand-more-items');

expand_more.addEventListener('click',()=>{
    expand_more_items.classList.toggle('active');
})

function hidealert() {
    var alert_div = document.getElementById('alert_div');
    alert_div.style.display = 'none';
  }
  
// -------whats on your mind upload photo js
$('.custom-img-upload').click(function() {
    $('#img-upload').click();
});

// -------------------------------------------------for post ajax submit and display
$(document).ready(function() {
    $('.post_form').submit(function(e) {
      e.preventDefault(); 
      var formData = new FormData(this); 
      var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
      var form = this;

      $.ajax({
        url: 'home',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            'X-CSRFToken': csrftoken 
          },
        success: function(response) {
          form.reset();
          $('.posted_message').html(response);
          $('.posted_message').show();
          setTimeout(function(){
            $('.posted_message').hide();
          },1000);

          fetch("getpost",{
            headers:{
              'Accept': 'application/json',
              'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
          },
          
          })
          .then((res) => res.json())
          .then((post_data) => {
            console.log("data", post_data)
            console.log("fetch hudaixa")

            var default_posts= document.querySelectorAll('.default_posts');
            default_posts.forEach(function(item){
              item.style.display = 'None';
            })

            // debugger;
            // if (jQuery(".updated_posts").css('display') == 'block'){
            //   console.log("block off to on")
            //   var updated_posts= document.querySelector('.updated_posts');
            //   updated_posts.innerHTML += `<h1>Hello this is test</h1>`;
            // }

            var updated_posts= document.querySelector('.updated_posts');
            updated_posts.style.display = 'block';

            
            template = ''
            post_data.forEach(item =>{
              template +=`
              
          <div class=" w-[620px]  mx-auto mb-10 bg-white shadow-2xl shadow-gray-800 rounded-2xl p-4">
          
              <div class="flex justify-between">
              <div class="flex items-start">
                 
                  <img src=${item.profile_avatar} alt="User Avatar" class="w-10 h-10 rounded-full mr-3">
                  
              <div>
                <h4 class="font-semibold">${item.user_firstname} ${item.user_lastname} </h4>
                <p class="text-gray-500 text-sm">${item.created_at}</p>
              </div>
              </div>
              <span class="material-symbols-outlined mr-2">more_horiz</span>
            </div>
            <div class="mt-4 border-b border-gray-300">
              <p>
              ${item.content}
              </p>
              
              ${item.post_img != null ? `<img src="${item.post_img}" alt="Post Image" class="mt-4">`:''}
              
            </div>
            <div class="flex items-center mt-4">
            <a href="handlelike/${item.id}">
              <button class="flex items-center text-gray-500 hover:text-blue-500">
                <span class="material-symbols-outlined text-red-500">favorite</span>
                ${item.num_likes == 0 ? `<span>0</span>`:`<span>${item.num_likes}</span>`}
              </button>
            </a>
              <button id="comment" class="flex items-center text-gray-500 hover:text-blue-500 ml-8">
                <span class="material-symbols-outlined text-green-500">comment</span>
                Comment
              </button>
            </div>
            
           
            <div class="comment_section hidden rounded-2xl w-full mt-2 p-5 shadow-lg  border-t border-gray-300">
                <div class="flex flex-col font-normal text-[15px]">
                ${item.comments.map((comment, index) => `
                  <div class="flex items-center w-full mr-5">
                    <label class=" w-full my-2 p-2 border-b-2 border-gray-300 rounded-l drop-shadow-2xl shadow-lg ">${comment}</label>
                    <img class="w-10 h-10 mx-2 rounded-full shadow-lg shadow-blue-200" src="${item.commented_user[index]}" alt="">
                  </div>
                    
                `).join('')}

                <form method="POST" action="handlecomment" class="comment_submit">
                  <div class="relative border-2 border-gray-300 w-full p-2 outline-none resize-none focus:border-[#0e9741] rounded-lg">
                      <img class="absolute left-0 top-2 w-10 h-10 mx-2 rounded-full" src="${item.loggedin_user_Profile}" alt="">
                      <input name="post_id" hidden value="${item.id}" class=""></input>
                      <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken_var}">
                      <input name="comment" placeholder="Write a comment..." class="ml-10 w-96 p-2 outline-none resize-none focus:border-[#0e9741] rounded-lg"></input>
                      <button type="submit" class="absolute right-3 top-2  bg-[#5185a1] text-white px-3 py-2 rounded-md hover:bg-[#a8d4b8]">Comment</button>
                  </div>
                </form>
                
              </div>
  
            </div>

          </div>
          `

          });
          
          updated_posts.innerHTML = template;
          
          var commentBtn = document.querySelectorAll('#comment')
          let comment_section = document.querySelectorAll('.comment_section');

          for(let item=0; item<comment_section.length; item++){
            btn = commentBtn[item];
            btn.addEventListener("click",()=> {
              comment_section[item].classList.toggle('hidden')
            })
          }


          })
        },
        error: function(xhr, status, error) {
          console.error('Request failed. Error: ' + error);
        }
      });
    });
  });

// ------------for comment toggler
var commentBtn = document.querySelectorAll('#comment')
let comment_section = document.querySelectorAll('.comment_section');
for(let item=0; item<comment_section.length; item++){
  btn = commentBtn[item];
  btn.addEventListener("click",()=> {
    comment_section[item].classList.toggle('hidden')

  })
}



// ----------------------------------------------------for comment ajax display
$(document).ready(function(){
  $('.comment_submit').submit(function(e){
    e.preventDefault();

    var formData = new FormData(this);
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    var form = this;

    $.ajax({
      url: 'handlecomment',
      type:'POST',
      data: formData,
      processData: false,
      contentType:false,
      header:{
        'x-CSRFToken': csrftoken_var
    },
    success: function(response){
      form.reset();

      fetch("getpost",{
        headers:{
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
      },
      })
      .then((res) => res.json())
      .then((post_data) => {
        // console.log("data", post_data)
        
        var default_posts= document.querySelectorAll('.default_posts');
        default_posts.forEach(function(item){
          item.style.display = 'None';
        })

        var updated_posts= document.querySelector('.updated_posts');
        updated_posts.style.display = 'block';

      

        template = ''
        post_data.forEach(item =>{
          template +=`
          
            <div class=" w-[620px]  mx-auto mb-10 bg-white shadow-2xl shadow-gray-800 rounded-2xl p-4">
          
              <div class="flex justify-between">
              <div class="flex items-start">
                
                  <img src=${item.profile_avatar} alt="User Avatar" class="w-10 h-10 rounded-full mr-3">
                  
              <div>
                <h4 class="font-semibold">${item.user_firstname} ${item.user_lastname} </h4>
                <p class="text-gray-500 text-sm">${item.created_at}</p>
              </div>
              </div>
              <span class="material-symbols-outlined mr-2">more_horiz</span>
            </div>
            <div class="mt-4 border-b border-gray-300">
              <p>
              ${item.content}
              </p>
              
              ${item.post_img != null ? `<img src="${item.post_img}" alt="Post Image" class="mt-4">`:''}
              
            </div>
            <div class="flex items-center mt-4">
              <button class="flex items-center text-gray-500 hover:text-blue-500">
                <span class="material-symbols-outlined text-red-500">favorite</span>
                Like
              </button>
              <button id="comment"  class="flex items-center text-gray-500 hover:text-blue-500 ml-8">
                <span class="material-symbols-outlined text-green-500">comment</span>
                Comment
              </button>
            </div>
            
          
              <div class="comment_section hidden rounded-2xl w-full mt-2 p-5 shadow-lg  border-t border-gray-300">
                <div class="flex flex-col font-normal text-[15px]">

                ${item.comments.map((comment, index) => `
                  <div class="flex items-center w-full mr-5">
                    <label class=" w-full my-2 p-2 border-b-2 border-gray-300 rounded-l drop-shadow-2xl shadow-lg ">${comment}</label>
                    <img class="w-10 h-10 mx-2 rounded-full shadow-lg shadow-blue-200" src="${item.commented_user[index]}" alt="">
                  </div>
                  `).join('')}

                  <form method="POST" action="handlecomment" class="comment_submit">
                    <div class="relative border-2 border-gray-300 w-full p-2 outline-none resize-none focus:border-[#0e9741] rounded-lg">
                        <img class="absolute left-0 top-2 w-10 h-10 mx-2 rounded-full" src="${item.loggedin_user_Profile}" alt="">
                        <input name="post_id" hidden value="${item.id}" class=""></input>
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken_var}">
                        <input name="comment" placeholder="Write a comment..." class="ml-10 w-96 p-2 outline-none resize-none focus:border-[#0e9741] rounded-lg"></input>
                        <button type="submit" class="absolute right-3 top-2  bg-[#5185a1] text-white px-3 py-2 rounded-md hover:bg-[#a8d4b8]">Comment</button>
                    </div>
                  </form>
                </div>

              </div>

        </div>
        `
        updated_posts.innerHTML = template

        });
        var commentBtn = document.querySelectorAll('#comment')
        let comment_section = document.querySelectorAll('.comment_section');
      
        for(let item=0; item<comment_section.length; item++){
          btn = commentBtn[item];
          btn.addEventListener("click",()=> {
            comment_section[item].classList.toggle('hidden')
          })
        }
          

      })

    },
    error: function(error) {
      console.error('Request failed. Error: ' + error);
    }

    })

  })

})



// -----------------for add-friend-btn-ajax--------------

$(document).ready(function(){
  $('.add_friend_btn').submit(function(e){
    e.preventDefault();
    
    var formData = new FormData(this);
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    var form = this;

    $.ajax({
      url: url,
      type:'POST',
      data: formData,
      processData: false,
      contentType:false,
      header:{
        'x-CSRFToken': csrftoken
    },
    success: function(response){
      form.reset();
      $('.showing_frnd_btn').hide();
      $('.showing_reqst_btn').css('display', 'flex');
      $('.showing_reqst_btn').show();




    },
    error: function(error) {
      console.error('Request failed. Error: ' + error);
    }

    })

  })

})



// ------------for ajax search =====---------------------=-------
const searchField = document.querySelector('#searchField');
const searchResult = document.querySelector('.search-result');
const noResult = document.querySelector('.noResult');
searchResult.style.display = 'None';

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if(searchValue.trim().length > 0){
    // console.log("searchvalue", searchValue );
    fetch("/search", {
      body: JSON.stringify({searchText: searchValue}),
      method: "POST",
    })
    .then((res) => res.json())
    .then((data) =>{
      console.log("data", data)

      searchResult.style.display = 'block';
      searchResult.innerHTML = "";

      if(data.length === 0 ){
        noResult.style.display = 'block';
      }
      
      else{
        noResult.style.display = 'None';
        data.forEach(item => {
          searchResult.innerHTML += `
            <a href="${profileURL.replace('0',item.id)}" class="p-5 border-b-2 mb-2 flex flex-row justify-between item-center cursor pointer">
              <img src="img/${item.avatar}" alt="User 1" class="w-16 h-16 rounded-md shadow-lg shadow-slate-500/50">
              <span class="text-xl ml-10">${item.first_name} ${item.last_name}</span>
            </a>
          `
        });
      }

    })


  }
  else{
    searchResult.style.display = 'none';
    searchResult.innerHTML = "";
    
}
})
